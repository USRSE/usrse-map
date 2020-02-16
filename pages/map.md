---
layout: page
title: US-RSE
subtitle: The US Research Software Engineer Association Map
use-site-title: true
permalink: /
---


<style>
  #map {
    position: absolute; 
    top: 90px; 
    width: 100%;
    min-height:900px;
    bottom:0px;
  }
  body { margin: 0; padding: 0;}
  .container {
    width:100% !important; 
    height:100% !important;
    bottom:0px !important;
    }
  .marker {
    background-color: #99266e;
    background-size: cover;
    border-radius: 50%;
    cursor: pointer;
  }
  .mapboxgl-popup {
    max-width: 200px;
  }

  .mapboxgl-popup-content {
    text-align: center;
    font-family: 'Open Sans', sans-serif;
  }
</style>


<div id="map"></div>

<script src='https://api.tiles.mapbox.com/mapbox-gl-js/v1.3.1/mapbox-gl.js'></script>
<link href='https://api.tiles.mapbox.com/mapbox-gl-js/v1.3.1/mapbox-gl.css' rel='stylesheet' />

<script>
  mapboxgl.accessToken = '{{ site.mapbox }}';

  var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/light-v10',
    center: [-55, 40],
    zoom: 2,
  });

  map.addControl(new mapboxgl.NavigationControl());
  map.addControl(new mapboxgl.FullscreenControl());

  var geojson = {
    type: 'FeatureCollection',
    features: [{% for loc in site.data.locations %}{
  type: 'Feature',
  geometry: {
    type: 'Point',
      coordinates: [{{ loc.lng }}, {{ loc.lat }}]
    },
    properties: {
      title: '{{ loc.name | capitalize }}',
      description: '{{ loc.name }}',
    },
    size: {
      width: Math.sqrt({{ loc.count }})*15,
      height: Math.sqrt({{ loc.count }})*15,
    },
    data: {
       name: '{{ loc.name }}',
       count: {{ loc.count }},
    },
  }{% if forloop.last %}{% else %},{% endif %}{% endfor %}]
  };

  geojson.features.forEach(function(marker) {
    var el = document.createElement('div');
    el.className = 'marker';
    el.setAttribute('style', 'width: ' + marker.size.width + 'px; height: ' + marker.size.height + 'px;');

    var popup = new mapboxgl.Popup({ offset: 25 })
      .setHTML(
        '<div style="padding-top: 15px; padding-bottom: 5px;">' +
          '<p style="margin: 0; padding: 0;">' + marker.data.name +
          '</p>' +
          '<p style="margin: 0; padding: 0;">' +
            'Count: ' + marker.data.count +
          '</p>' +
        '</div>'
      );

    new mapboxgl.Marker(el)
    .setLngLat(marker.geometry.coordinates)
    .setPopup(popup)
    .addTo(map);
  });

  // Might help with making full height, doesn't seem to
  map.on('load', function () {
    map.resize();
  });
</script>
