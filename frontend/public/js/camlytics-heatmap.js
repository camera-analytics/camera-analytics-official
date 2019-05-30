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

const RADIUS_SIZE = 30

const IMAGE_WIDTH = 432
const IMAGE_HEIGHT = 9/16 * IMAGE_WIDTH

let updatePositions = () => {
  var positionData = []
  var firstMax = 0;
  var secondMax = 0;
  dataService.customerPositions().then(positions => {
    if (IMAGE_HEIGHT != undefined) { // make sure previous fetch succeeded
      var value
      const HEATMAP_HEIGHT = positions.length;
      const HEATMAP_WIDTH = positions[0].length;
      for (i = 0; i < HEATMAP_HEIGHT; i++) {
        for (j = 0; j < HEATMAP_WIDTH; j++) {
          if (positions[i][j] != 0) {
            // // log value
            // value = Math.round(Math.log(positions[i][j]))
            value = positions[i][j]
            if (value > firstMax) {
              firstMax = value
            } else if (positions[i][j] > secondMax) {
              secondMax = value
            }
            positionData.push({x: Math.floor(IMAGE_WIDTH*j/HEATMAP_WIDTH),
                               y: Math.floor(IMAGE_HEIGHT*i/HEATMAP_HEIGHT),
                               value: value,
                               radius: RADIUS_SIZE})
          }
        }
      }
      // console.log(positionData)
      heatmap.setData({
        min: 0,
        max: secondMax,
        data: positionData
      });
    }
  })
}
var date = new Date().getTime()
$("heatmapContainer").style.background = "url('http://localhost:5000/api/image?date="
                                     + date + "')"
$("heatmapContainer").style.backgroundSize = "432px 243px"

updatePositions()
setInterval(() => {
  updatePositions()
}, 1000) // refreshes every 1 second

};
