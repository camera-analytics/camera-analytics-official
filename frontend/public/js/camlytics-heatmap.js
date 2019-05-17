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

var imageHeight, imageWidth

let getDimensions = () => {
  dataService.imageDimensions().then(dimensions => {
    imageHeight = dimensions.height
    imageWidth = dimensions.width
  }
)}

// const IMAGE_HEIGHT = 720
// const IMAGE_WIDTH = 1280

let updatePositions = () => {
  var positionData = []
  var first_max = 0;
  var second_max = 0;
  dataService.customerPositions().then(positions => {
    if (imageHeight != undefined) { // make sure previous fetch succeeded
      console.log(imageHeight)
      var value
      const HEATMAP_HEIGHT = positions.length;
      const HEATMAP_WIDTH = positions[0].length;
      for (i = 0; i < HEATMAP_HEIGHT; i++) {
        for (j = 0; j < HEATMAP_WIDTH; j++) {
          if (positions[i][j] != 0) {
            // // log value
            // value = Math.round(Math.log(positions[i][j]))
            
            value = positions[i][j]
            if (value > first_max) {
              first_max = value
            } else if (positions[i][j] > second_max) {
              second_max = value
            }
            positionData.push({x: Math.floor(imageWidth*j/HEATMAP_WIDTH),
                               y: Math.floor(imageHeight*i/HEATMAP_HEIGHT),
                               value: value,
                               radius: RADIUS_SIZE})
          }
        }
      }
      console.log(positionData)
      heatmap.setData({
        min: 0,
        max: second_max,
        data: positionData
      });
    }
  })
}
getDimensions()
updatePositions()
setInterval(() => {
  getDimensions()
  updatePositions()
}, 1000) // refreshes every 1 second

};
