import ee, json
ee.Initialize(project='gee-wcma-ndvi')

with open("cells/cell_0_0_0.geojson") as f:
    gj = json.load(f)

aoi = ee.Geometry(gj["features"][0]["geometry"])

collection = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED").filterBounds(aoi)

dates = collection.reduceColumns(ee.Reducer.minMax(), ["system:time_start"]).getInfo()

print("Earliest date:", ee.Date(dates["min"]).format().getInfo())
print("Latest date:", ee.Date(dates["max"]).format().getInfo())
