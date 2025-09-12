var aoi = ee.FeatureCollection(
  {
    "type": "FeatureCollection",
    "crs": {"type": "name", "properties": {"name": "EPSG:4326"}},
    "features": [
      {
        "type": "Feature",
        "geometry": {
          "type": "Polygon",
          "coordinates": [
            [
              [142.0997, -36.8167],
              [142.2997, -36.8167],
              [142.2997, -36.6167],
              [142.0997, -36.6167],
              [142.0997, -36.8167]
            ]
          ]
        },
        "properties": {"row": 0, "col": 0, "serial": 0}
      }
    ]
  }
);

function maskClouds(image) {
  var scl = image.select('SCL');
  var mask = scl.neq(3).and(scl.neq(8)).and(scl.neq(9)).and(scl.neq(10));
  return image.updateMask(mask);
}

var s2 = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
  .filterBounds(aoi)
  .map(maskClouds)
  .map(function(img){
    var ndvi = img.normalizedDifference(['B8','B4']).rename('NDVI');
    return img.addBands(ndvi);
  });

var range = s2.reduceColumns(ee.Reducer.minMax(), ['system:time_start']);
var start = ee.Date(range.get('min'));
var end = ee.Date(range.get('max'));

function showNdvi(input) {
  var d1;
  if (input.start) {
    d1 = ee.Date(input.start());
  } else {
    d1 = ee.Date(input);
  }
  var d2 = d1.advance(30,'day');
  var img = s2.filterDate(d1,d2).mean();
  Map.layers().reset();
  Map.addLayer(img.select('NDVI'), {min:-1, max:1, palette:['brown','white','green']}, 'NDVI');
}

var slider = ui.DateSlider({
  start: start,
  end: end,
  value: start,
  period: 1,
  onChange: showNdvi
});
Map.add(slider);

showNdvi(start);

Map.centerObject(aoi, 12);
