import ee, json
ee.Initialize(project='gee-wcma-ndvi')

with open("qg1/WCMA_BB.geojson") as f:
    gj = json.load(f)

aoi = ee.Geometry(gj["features"][0]["geometry"])
print(aoi)