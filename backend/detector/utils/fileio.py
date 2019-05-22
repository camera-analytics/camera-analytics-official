import os

def clear_files():
    PATH = '../data/'
    if os.path.exists(PATH + 'positions-hashed.txt'):
        os.remove(PATH + 'positions-hashed.txt')
    if os.path.exists(PATH + 'records.txt'):
        os.remove(PATH + 'records.txt')
    if os.path.exists(PATH + 'state.txt'):
        os.remove(PATH + 'state.txt')
