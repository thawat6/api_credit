var map = L.map('map');

var myLayer = L.tileLayer('http://dev.morange.co.th/mapbox-studio-osm-bright/{z}/{x}/{y}.png', {
	attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

var myControl = L.Routing.control({
	layer: myLayer,
	serviceUrl: 'https://api.morange.co.th/osrm/route/v1',
	language: 'en',
	center: L.latLng(16.4397, 102.830036),
	zoom: 13,
	waypoints: [
		L.latLng(16.4397, 102.830036),
		L.latLng(17.397821, 102.788086),
	],
	geocoder: L.Control.Geocoder.nominatim(),
	routeWhileDragging: false,
	reverseWaypoints: true,
});
myControl.addTo(map);
// L.Routing.errorControl(myControl).addTo(map);


// var control = L.Routing.control({
// 	layer: myLayer,
// 	serviceUrl: 'https://api.morange.co.th/osrm/route/v1',
// 	waypoints: [
// 		L.latLng(16.4397, 102.830036),
// 		L.latLng(17.397821, 102.788086),
// 	],
// 	geocoder: L.Control.Geocoder.nominatim(),
// 	routeWhileDragging: false,
// 	reverseWaypoints: true,
// 	showAlternatives: true,
// 	// altLineOptions: {
// 	// 	styles: [
// 	// 		{color: 'black', opacity: 0.15, weight: 9},
// 	// 		{color: 'white', opacity: 0.8, weight: 6},
// 	// 		{color: 'blue', opacity: 0.5, weight: 2}
// 	// 	]
// 	// },
	
// }).addTo(map);

// L.Routing.errorControl(control).addTo(map);

// // control.hide();
// // control.show();

// setTimeout(function(){
// 	control.remove();
// }, 3000);






