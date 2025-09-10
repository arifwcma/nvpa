import ee, json, datetime
from ee import batch

ee.Initialize(project='gee-wcma-ndvi')

GEOJSON_PATH = "qg1/WCMA_BB.geojson"
CRS = 'EPSG:28354'
CELL_M = 1000
FOLDER = 'WCMA_NDVI_TEST2'
START = datetime.date(2019,1,1)
MONTHS = 3

with open(GEOJSON_PATH) as f:
    gj = json.load(f)
aoi = ee.Geometry(gj["features"][0]["geometry"])

bounds = aoi.bounds(maxError=1).transform(ee.Projection(CRS), 1)
coords = bounds.coordinates().getInfo()[0]
xs = [float(p[0]) for p in coords]
ys = [float(p[1]) for p in coords]
xmin, xmax = min(xs), max(xs)
ymin, ymax = min(ys), max(ys)
print(xmin)

width = xmax - xmin
height = ymax - ymin
ncols = int((width / CELL_M) + 0.9999)
nrows = int((height / CELL_M) + 0.9999)

print(f"rows {nrows}, cols {ncols}, total {nrows*ncols}")
exit(0)

def mask_s2(i):
    scl = i.select('SCL')
    m = scl.neq(3).And(scl.neq(8)).And(scl.neq(9)).And(scl.neq(10)).And(scl.neq(11))
    return i.updateMask(m)

def ndvi_month(tile, s, e):
    col = (ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
           .filterBounds(tile)
           .filterDate(s, e)
           .map(mask_s2))
    med = col.mosaic()
    return med.normalizedDifference(['B8','B4']).rename('ndvi').clip(tile)

for r in range(nrows):
    y_top = ymax - r * CELL_M
    y_bot = y_top - CELL_M
    for c in range(ncols):
        x_left = xmin + c * CELL_M
        x_right = x_left + CELL_M
        tile = ee.Geometry.Rectangle([x_left, y_bot, x_right, y_top], proj=CRS, geodesic=False)
        for k in range(MONTHS):
            s = ee.Date(START.strftime('%Y-%m-%d')).advance(k, 'month')
            e = s.advance(1, 'month')
            tag = s.format('YYYY_MM').getInfo()
            img = ndvi_month(tile, s, e)
            task = batch.Export.image.toDrive(
                image=img,
                description=f'NDVI_{tag}_r{r}_c{c}',
                folder=FOLDER,
                fileNamePrefix=f'NDVI_10m_{tag}_r{r}_c{c}',
                region=tile.transform('EPSG:4326', 1),
                scale=10,
                maxPixels=1e13
            )
            task.start()
            print(f"Row {r}; Col {c}; Month {k} initiated")
