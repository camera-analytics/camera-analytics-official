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

let RADIUS_SIZE = 10

let IMAGE_WIDTH = 640 // pixels
let IMAGE_HEIGHT = 360

let updatePositions = () => {
var positionData = []
var split
dataService.customerPositions().then(positionStrings => {
  for (i=0; i < positionStrings.length; i++) {
    split = positionStrings[i].split("  ")
    // console.log(p)
    positionData.push({x: Math.round(IMAGE_WIDTH*parseFloat(split[0])),
                       y: Math.round(IMAGE_HEIGHT*parseFloat(split[1])),
                       value: 1,
                       radius: RADIUS_SIZE})
  }
  console.log(positionData)
  heatmap.setData({
    min: 0,
    max: 1,
    data: positionData
  });
})
}

updatePositions()
setInterval(() => {
updatePositions()
}, 10000) // refreshes every 10 seconds

};
