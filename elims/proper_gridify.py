import ee, json
ee.Initialize(project='gee-wcma-ndvi')

GEOJSON_PATH = "../qg1/WCMA_BB.geojson"
CRS = 'EPSG:3857'
CELL_M = 10000

with open(GEOJSON_PATH) as f:
    gj = json.load(f)
aoi = ee.Geometry(gj["features"][0]["geometry"])
bounds = aoi.bounds().transform(ee.Projection(CRS), 1)
coords = bounds.coordinates().getInfo()[0]
xs = [float(p[0]) for p in coords]
ys = [float(p[1]) for p in coords]
xmin, xmax = min(xs), max(xs)
ymin, ymax = min(ys), max(ys)
width = xmax - xmin
height = ymax - ymin
ncols = int((width / CELL_M) + 0.9999)
nrows = int((height / CELL_M) + 0.9999)

print("xmin", xmin, "xmax", xmax)
print("ymin", ymin, "ymax", ymax)
print("width_m", width, "height_m", height)
print("cols", ncols, "rows", nrows, "total", nrows * ncols)

r, c = 2, 3
x_left = xmin + c * CELL_M
x_right = x_left + CELL_M
y_top = ymax - r * CELL_M
y_bot = y_top - CELL_M

tile = ee.Geometry.Rectangle([x_left, y_bot, x_right, y_top], proj=ee.Projection(CRS), geodesic=False)
area = tile.area(maxError=1).getInfo()
print("tile area (m²)", area, "≈", area/1e6, "km²")

