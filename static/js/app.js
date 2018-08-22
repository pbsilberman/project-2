// Create a map object
var myMap = L.map("map", {
    center: [41.8781, -87.6298],
    zoom: 13
});

// Add a tile layer
L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
maxZoom: 18,
id: "mapbox.streets-basic",
accessToken: API_KEY
}).addTo(myMap);

trips_url = '/trips';

d3.json(trips_url).then(function(data) {
    // Once a response is received, send the data.features object to the createFeatures function
    console.log(data);

    createTrips(data)
});

stations_url = '/stationvolume';

d3.json(stations_url).then(function(data) {
    // Once a response is received, send the data.features object to the createFeatures function
    console.log(data);

    createStations(data)
});

function createStations(stationsData) {
    function circleRadius(x) {
        x = +x;
        if (x > 300) {
            return (x/30)
        } else {
            return 10
        }
    }

    for(var i = 0; i < stationsData.length; i++) {
        L.circle([stationsData[i].from_latitude, stationsData[i].from_longitude], {
            fillOpacity: 0.5,
            color: "black",
            weight: 1,
            fillColor: "pink",
            radius: circleRadius(stationsData[i].trip_count)
            }).bindPopup("<h3>" + stationsData[i].name + "</h3><br><h4>" + stationsData[i].trip_count + " trips</h4>")
            .addTo(myMap);
    }
}

function createTrips(tripsData) {

    // Write a loop to run once for each station-to-station connection in the array.
    for(var i = 0; i < tripsData.length; i++) {
        var line = [
            [tripsData[i].from_latitude , tripsData[i].from_longitude],
            [tripsData[i].to_latitude , tripsData[i].to_longitude]
        ];

        // L.polyline(line, {
        //     color: "black",
        //     weight: 1,
        //     opacity: 0.5
        // }).addTo(myMap);
    }

    // var legend = L.control({position: 'bottomright'});

    // legend.onAdd = function (map) {

    //     var div = L.DomUtil.create('div', 'info legend'),
    //         magniutdes = [0,1,2,3,4,5],
    //         labels = [];

    //     // loop through our density intervals and generate a label with a colored square for each interval
    //     for (var i = 0; i < magniutdes.length; i++) {
    //         div.innerHTML +=
    //             '<i style="background:' + chooseColor(magniutdes[i] + 1) + '"></i> ' +
    //             magniutdes[i] + (magniutdes[i + 1] ? '&ndash;' + magniutdes[i + 1] + '<br>' : '+');
    //     }

    //     return div;
    // };

    // legend.addTo(myMap);
}

