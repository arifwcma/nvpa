import ee, json
ee.Initialize(project='gee-wcma-ndvi')

GEOJSON_PATH = "../qg1/WCMA_BB.geojson"
CRS = 'EPSG:3857'
CELL_M = 1000

with open(GEOJSON_PATH) as f:
    gj = json.load(f)
aoi = ee.Geometry(gj["features"][0]["geometry"])

grid = aoi.coveringGrid(ee.Projection('EPSG:4326'), 0.01)

count = grid.size().getInfo()
print("tiles", count)

first = ee.Feature(grid.first())
print("first cell", first.geometry().coordinates().getInfo())
