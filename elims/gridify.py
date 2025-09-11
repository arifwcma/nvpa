import ee, json, datetime
from ee import batch

ee.Initialize(project='gee-wcma-ndvi')

GEOJSON_PATH = "../qg1/WCMA_BB.geojson"
CRS = 'EPSG:4326'
CELL_DEG = 0.01
FOLDER = 'WCMA_NDVI_TEST2'
START = datetime.date(2019,1,1)
MONTHS = 3

with open(GEOJSON_PATH) as f:
    gj = json.load(f)
aoi = ee.Geometry(gj["features"][0]["geometry"])
bounds = aoi.bounds()
coords = bounds.coordinates().getInfo()[0]
xs = [float(p[0]) for p in coords]
ys = [float(p[1]) for p in coords]
xmin, xmax = min(xs), max(xs)
ymin, ymax = min(ys), max(ys)
width = xmax - xmin
height = ymax - ymin
ncols = int((width / CELL_DEG) + 0.9999)
nrows = int((height / CELL_DEG) + 0.9999)

print(f"rows {nrows}, cols {ncols}, total {nrows*ncols}")