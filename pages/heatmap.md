---
layout: page
title: US-RSE Map GL
subtitle: The US Research Software Engineer Association Map (GL!)
use-site-title: true
permalink: /heatmap/
---

<style>
  a {
    color: #08f;
  }

  #info {
    font-family: Helvetica, Arial, sans-serif;
    position: fixed;
    top: 0;
    left: 0;
    margin: 12px;
  }

  #map {
    position: absolute; 
    top: 20px; 
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
  .mapboxgl-popup {
    max-width: 200px;
  }

  .mapboxgl-popup-content {
    text-align: center;
    font-family: 'Open Sans', sans-serif;
  }
</style>
<div id="map"></div>
<script src='https://api.tiles.mapbox.com/mapbox-gl-js/v0.53.1/mapbox-gl.js'></script>
<script src='https://unpkg.com/deck.gl@7.3.3/dist.min.js'></script>
<script>
const data = [{% for loc in site.data.locations %}[{{ loc.lng }}, {{ loc.lat }}, Math.sqrt({{ loc.count }})*15]{% if forloop.last %}{% else %},{% endif %}{% endfor %}]

new deck.DeckGL({
  container: "map",
  mapboxApiAccessToken: '{{ site.mapbox }}',
  mapStyle: 'mapbox://styles/mapbox/dark-v9',
  longitude: -55,
  latitude: 40,
  zoom: 2,
  maxZoom: 16,
  layers: [
    new deck.HeatmapLayer({
      data,
      id: 'heatmap',
      opacity: 1,
      pickable: true,
      getPosition: d => [d[0], d[1]],
      getWeight:d => d[2],
      radiusPixels:10,
      intensity:1,
      threshold:0.03
    })
  ]
});
</script>

</body>
</html>
