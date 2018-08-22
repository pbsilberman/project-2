

 var map = L.map("map", {
    center: [
      41.826, -87.615 
    ],
    zoom: 11,
  });

   L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
    attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
    minZoom:2,
    maxZoom: 18,
    id: "mapbox.scenic",
    accessToken: API_KEY
  }).addTo(map);

function onEachFeature(feature, layer) {
    layer.bindPopup("<h3>" + feature.properties.station +
      "</h3><hr><p>Total Docks " + feature.properties.totaldocks + "</p>");
  }

   L.geoJSON(stations, {
    onEachFeature: onEachFeature
   }).addTo(map);



