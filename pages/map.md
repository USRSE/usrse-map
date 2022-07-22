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
    top: 50px; 
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
    opacity: 0.5;
    background-size: cover;
    border-radius: 50%;
    cursor: pointer;
  }
  .grp_marker {
    background-color: #FFC107;
    opacity: .9;
    border-radius: 50%;

  }
  .mapboxgl-popup {
    max-width: 200px;
  }

  .mapboxgl-popup-content {
    text-align: center;
    font-family: 'Open Sans', sans-serif;
  }
  /* From https://docs.mapbox.com/help/tutorials/choropleth-studio-gl-pt-2/ */
  .map-overlay {
    position: fixed;
    bottom: 0;
    left: 5%;
    background: #fff;
    margin-right: 20px;
    font-family: Arial, sans-serif;
    overflow: auto;
    border-radius: 3px;
  }
  #legend {
    padding: 10px;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
    line-height: 18px;
    height: 150px;
    margin-bottom: 40px;
    width: 200px;
    height: auto;
    width: auto;
  }

  .legend-key {
    display: inline-block;
    border-radius: 20%;
    width: 10px;
    height: 10px;
    margin-right: 5px;
  }
</style>


<div id="map"></div>
<div class='map-overlay' id='legend'></div>

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

  var groupgeo = {
    type: 'FeatureCollection',
    features: [{% for grp in site.data.group-locations %}{
      type: 'Feature',
      geometry: {
        type: 'Point',
        coordinates: [{{ grp.lng }}, {{ grp.lat }}]
      },
      properties: {
        title: '{{ grp.name }}',
        description: '{{ grp.name }}',
      },
      size: {
        width: 15,
        height: 15,
      },
      data: {
        name: '{{ grp.name }}',
        url: '{{ grp.url }}'
      },
    }{% if forloop.last %} {% else %},{% endif %}{% endfor %}]
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

  groupgeo.features.forEach(function(marker) {
    var el = document.createElement('div');
    el.className = 'grp_marker';
    el.setAttribute('style', 'width: ' + marker.size.width + 'px; height: ' + marker.size.height + 'px;');

    var popup = new mapboxgl.Popup({ offset: 25 })
      .setHTML(
        '<div style="padding-top: 15px; padding-bottom: 5px;">' +
          '<p style="margin: 0; padding: 0;">' +
            '<a href=' + marker.data.url +' target="_blank">' + marker.data.name + ' Regional RSE Group</a>' +
          '</p>' +
        '</div>'
      );
    new mapboxgl.Marker(el)
    .setLngLat(marker.geometry.coordinates)
    .setPopup(popup)
    .addTo(map);
  });

  // create legend: from https://docs.mapbox.com/help/tutorials/choropleth-studio-gl-pt-2/
  const legend = document.getElementById('legend');
  const colors = ['#99266E', '#FFC107']
  const layers = ['US-RSE Members','Local/Regional RSE Groups'];
  layers.forEach((layer, i) => {
    const color = colors[i];
    const item = document.createElement('div');
    const key = document.createElement('span');
    key.className = 'legend-key';
    key.style.backgroundColor = color;

    const value = document.createElement('span');
    value.innerHTML = `${layer}`;
    item.appendChild(key);
    item.appendChild(value);
    legend.appendChild(item);
  });

  // Might help with making full height, doesn't seem to
  map.on('load', function () {
    map.resize();
  });
</script>
