
odoo.define('Ks_Map.map', function (require) {
    "use strict";

    var ajax = require('web.ajax');
    ajax.jsonRpc("/ks_get_map_cod", 'call', {}, {
    }).then(function (cod){
        var ks_point = new L.LatLng(parseFloat(cod.lan),parseFloat(cod.lon));
        var ks_mymap = L.map('mapid').setView(ks_point, parseInt(cod.zoom));
        L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoiZGV2dnZ2dnZ2diIsImEiOiJja3Nvb2Z1cHkwNnhxMnNzNmNsNTAxZ2d2In0.2LMgt_oPT8XSFQ6IlEjLkw',
        {
        attribution: 'Map data &#169;<a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        maxZoom: 18,
        id: 'mapbox/streets-v11',
        tileSize: 512,
        zoomOffset: -1,
        accessToken: 'your.mapbox.access.token'
    }).addTo(ks_mymap);
    L.marker(ks_point).addTo(ks_mymap);
    });
});