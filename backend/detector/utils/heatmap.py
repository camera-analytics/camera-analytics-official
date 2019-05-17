"""
Helper functions for efficiently storing and updating heatmap coordinates.
"""
import os

class HeatMap:
    """
    NOTE: For ~25x less space and 25x faster file reading time, you can store
          it in a binary file (instead of ASCII text).
          10 digits in 1 byte of ASCII versus 256 digits in 1 byte of binary.
          But then you need to deal with Endianness.
    """
    def __init__(self, width, height):
        self.width = width
        self.height = height

        if not os.path.isfile('../positions-hashed.txt'):
            with open('../positions-hashed.txt', 'w') as positions:
                for i in range(self.height):
                    positions.write(','.join(['00000000']*self.width)+ '\n')

    def _get_index(self, normalized_x_coord, normalized_y_coord):
        """
        Each row is of size (width -1) commas + (width*8) numbers + (1) \n
                            = 9*width
        """
        x_coord = min(int(normalized_x_coord*self.width), self.width-1)
        y_coord = min(int(normalized_y_coord*self.height), self.height-1)
        index = y_coord*9*self.width + 9*x_coord
        # print('n_x ', normalized_x_coord, '  n_y ', normalized_y_coord)
        # print('x ', x_coord, '  y ', y_coord)
        return index

    def update(self, normalized_coordinates):
        with open('../positions-hashed.txt', 'r+') as positions:
            index = self._get_index(normalized_coordinates[0],
                                    normalized_coordinates[1])
            positions.seek(index)

            # increment count by 1
            count = int(positions.read(8)) + 1
            positions.seek(index)
            additional_zeros = (8-len(str(count)))*'0'
            positions.write(additional_zeros + str(count))
