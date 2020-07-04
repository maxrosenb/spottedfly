function random_rgba() {
    const o = Math.round, r = Math.random, s = Math.sqrt(255);
    return 'rgba(' + o(s*r()*s) + ',' + o(s*r()*s) + ',' + o(s*r()*s) + ',' + (.3 + r().toFixed(1) *.5) + ')';
}

var chart_data=[];
var i;
var x = "{{result}}";
const res= "{{ result| safe }}";
var res_obj = eval('(' + res + ')');
for (var i = 0; i < res_obj.length; i++) {
  chart_data.push({
    t: new Date(res_obj[i].t),
    y: res_obj[i].y
  });
}

var dataset = {
  data: {
      datasets: [{
          label: 'Scatter Dataset',
          data: []
              }]
           }
        };
var coordinates = [];
dataset.data.datasets[0].data = coordinates;


for (var i = 0; i < res_obj.length; i++) {
  //document.getElementById('chart_place').innerHTML += '<li>' + 'pl: ' + res_obj[i].y + '</li>';
  coordinates.push({
    t: new Date(res_obj[i].t),
    y: res_obj[i].y
  });
}
	var ctx = document.getElementById("examChart").getContext("2d");

var ctx = document.getElementById("examChart").getContext("2d");
var ctx2 = document.getElementById("examChart2").getContext("2d");
var data=[];
data['labels']=[];
data['datasets']=[];
data['datasets'][0]={
    data: [],
    backgroundColor: [],
    borderColor: "rgba(0,0,0,0)",
    label: '{{playlist_name}}'
};
var m = res_obj.length;
var color = random_rgba();
for (i=0;i<m && i<1000;i++){
    var j = res_obj.length - i - 1;
    pl=res_obj[j];
    data['labels'][i]=pl.t;
    data['datasets'][0].data[i]={t :pl.t, y: pl.y};
    data['datasets'][0].backgroundColor[i]=color;
}
data['labels'].reverse()
data['datasets'][0].data.reverse()
var myNewChart = new Chart(ctx2,{type: 'line',data: data, options: {
        maintainAspectRatio: false,
        scales: {
            yAxes: [{
                scaleLabel: {
                    display: true,
                    labelString: 'Followers'
                  }
            }],
            xAxes: [{
                ticks: {
                    maxTicksLimit: 12
                  }
            }]
        },
        plugins: {
zoom: {
	// Container for pan options
	pan: {
		// Boolean to enable panning
		enabled: true,

		// Panning directions. Remove the appropriate direction to disable
		// Eg. 'y' would only allow panning in the y direction
		// A function that is called as the user is panning and returns the
		// available directions can also be used:
		//   mode: function({ chart }) {
		//     return 'xy';
		//   },
		mode: 'xy',

		rangeMin: {
			// Format of min pan range depends on scale type
			x: null,
			y: null
		},
		rangeMax: {
			// Format of max pan range depends on scale type
			x: null,
			y: null
		},

		// On category scale, factor of pan velocity
		speed: 20,

		// Minimal pan distance required before actually applying pan
		threshold: 10,

		// Function called while the user is panning
		onPan: function({chart}) { console.log(`I'm panning!!!`); },
		// Function called once panning is completed
		onPanComplete: function({chart}) { console.log(`I was panned!!!`); }
	},

	// Container for zoom options
	zoom: {
		// Boolean to enable zooming
		enabled: true,

		// Enable drag-to-zoom behavior
		drag: true,

		// Drag-to-zoom effect can be customized
		// drag: {
		// 	 borderColor: 'rgba(225,225,225,0.3)'
		// 	 borderWidth: 5,
		// 	 backgroundColor: 'rgb(225,225,225)',
		// 	 animationDuration: 0
		// },

		// Zooming directions. Remove the appropriate direction to disable
		// Eg. 'y' would only allow zooming in the y direction
		// A function that is called as the user is zooming and returns the
		// available directions can also be used:
		//   mode: function({ chart }) {
		//     return 'xy';
		//   },
		mode: 'xy',

		rangeMin: {
			// Format of min zoom range depends on scale type
			x: null,
			y: null
		},
		rangeMax: {
			// Format of max zoom range depends on scale type
			x: null,
			y: null
		},

		// Speed of zoom via mouse wheel
		// (percentage of zoom on a wheel event)
		speed: 0.1,

		// Minimal zoom distance required before actually applying zoom
		threshold: 2,

		// On category scale, minimal zoom level before actually applying zoom
		sensitivity: 3,

		// Function called while the user is zooming
		onZoom: function({chart}) { console.log(`I'm zooming!!!`); },
		// Function called once zooming is completed
		onZoomComplete: function({chart}) { console.log(`I was zoomed!!!`); }
	}
}
}
    }});
