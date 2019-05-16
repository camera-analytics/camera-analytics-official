window.onload = function() {

// helper function
function $(id) {
return document.getElementById(id);
}


// create a heatmap instance
var heatmap = h337.create({
container: document.getElementById("heatmapContainer"),
maxOpacity: 0.5,
radius: 10,
blur: 0.75,
});

// boundaries for data generation
var width = +window.getComputedStyle(document.body).width.replace(/px/, "");
var height = +window.getComputedStyle(document.body).height.replace(/px/, "");

// fetch
let dataService = new DataService()

let RADIUS_SIZE = 30

let IMAGE_WIDTH = 640 // pixels
let IMAGE_HEIGHT = 360

let updatePositions = () => {
var positionData = []
var first_max = 0;
var second_max = 0;
dataService.customerPositions().then(positions => {
  const HEATMAP_HEIGHT = positions.length;
  const HEATMAP_WIDTH = positions[0].length;
  for (i = 0; i < HEATMAP_HEIGHT; i++) {
    for (j = 0; j < HEATMAP_WIDTH; j++) {
      if (positions[i][j] != 0) {
        if (positions[i][j] > first_max) {
          first_max = positions[i][j]
        } else if (positions[i][j] > second_max) {
          second_max = positions[i][j]
        }
        positionData.push({x: Math.floor(IMAGE_WIDTH*j/HEATMAP_WIDTH),
                           y: Math.floor(IMAGE_HEIGHT*i/HEATMAP_HEIGHT),
                           value: positions[i][j],
                           radius: RADIUS_SIZE})
      }
    }
  }
  // for (i=0; i < positionStrings.length; i++) {
  //   split = positionStrings[i].split("  ")
  //   // console.log(p)
  //   positionData.push({x: Math.round(IMAGE_WIDTH*parseFloat(split[0])),
  //                      y: Math.round(IMAGE_HEIGHT*parseFloat(split[1])),
  //                      value: 1,
  //                      radius: RADIUS_SIZE})
  // }
  console.log(positionData)
  heatmap.setData({
    min: 0,
    max: second_max,
    data: positionData
  });
})
}

updatePositions()
setInterval(() => {
updatePositions()
}, 1000) // refreshes every 1 second

};
