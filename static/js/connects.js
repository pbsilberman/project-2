// Create a map object
var myMap = L.map("map", {
    center: [41.8781, -87.6298],
    zoom: 13
});

// Add a tile layer
L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
maxZoom: 18,
id: "mapbox.light",
accessToken: API_KEY
}).addTo(myMap);


var circleGroup = L.featureGroup().addTo(myMap).on("click", groupClick);
var marker, test;


d3.json('/stationvolume').then(function(data) {
    // Once a response is received, send the data.features object to the createStations function
    console.log(data);

    createStations(data)
});

function createStations(stationsData) {
    function chooseColor(d) {
        if (d <= 100) {
            return "#DCEDC8";
        }
        else if (d > 100 && d <= 500) {
            return "#e894c1";
        }
        else if (d > 500 && d <= 1000) {
            return "#F45DAD";
        }
        else if (d > 1000 && d <= 2000){
            return "#DD308D";
        }
        else if (d > 2000 && d <= 3000){
            return "#A54277";
        }
        else if (d > 3000) {
            return "#871552";
        }
        else {
        return "green";
        }
    }

    for(var i = 0; i < stationsData.length; i++) {

        var circle = L.circle([stationsData[i].from_latitude, stationsData[i].from_longitude], {
            fillOpacity: 0.75,
            color: "black",
            weight: 1,
            fillColor: chooseColor(stationsData[i].trip_count),
            radius: 50
            })
            //.bindPopup("<h3>" + stationsData[i].name + "</h3><h4>" + stationsData[i].trip_count + " trips</h4>")
            .addTo(circleGroup);
            
        test = stationsData[i].from_station_id;    
        circle.test = test;
    };

    var legend = L.control({position: 'bottomright'});

    legend.onAdd = function (map) {

        var div = L.DomUtil.create('div', 'info legend'),
            trips = [0,100,500,1000,2000,3000],
            labels = [];

        // loop through our density intervals and generate a label with a colored square for each interval
        for (var i = 0; i < trips.length; i++) {
            div.innerHTML +=
                '<i style="background:' + chooseColor(trips[i] + 1) + '"></i> ' +
                trips[i] + (trips[i + 1] ? '&ndash;' + trips[i + 1] + '<br>' : '+');
        }

        return div;
    };

    legend.addTo(myMap);

};

function groupClick(event) {
    // console.log(event.layer.test)
    lineGroup.clearLayers();
    showTrips(event.layer.test)
}


var lineGroup = L.featureGroup().addTo(myMap);

function showTrips(stationID) {
    d3.json(`/trips/${stationID}`).then(function(data) {
        // Once a response is received, send the data object to the createTrips function
        console.log(data);

        createTrips(data)
    });
};

function createTrips(tripsData) {
    // Write a loop to run once for each station-to-station connection in the array and add them to a group.
    for(var i = 0; i < tripsData.length; i++) {
        var line = [
            [tripsData[i].from_latitude , tripsData[i].from_longitude],
            [tripsData[i].to_latitude , tripsData[i].to_longitude]
        ];

        L.polyline(line, {
            color: "black",
            weight: 1,
            opacity: 0.5
        }).addTo(lineGroup);
    }
}