import ee, json, datetime
from ee import batch

ee.Initialize(project='gee-wcma-ndvi')

GEOJSON_PATH = "qg1/WCMA_BB.geojson"
CRS = 'EPSG:28354'
CELL_M = 100
FOLDER = 'WCMA_NDVI_TEST'
START = datetime.date(2019,1,1)
MONTHS = 3

with open(GEOJSON_PATH) as f:
    gj = json.load(f)
aoi = ee.Geometry(gj["features"][0]["geometry"])
rect = aoi.bounds()

coords = rect.coordinates().getInfo()[0]
xs = [p[0] for p in coords]
ys = [p[1] for p in coords]
xmin, xmax = min(xs), max(xs)
ymin, ymax = min(ys), max(ys)
ncols = int(((xmax - xmin) / CELL_M) + 0.9999)
nrows = int(((ymax - ymin) / CELL_M) + 0.9999)

def mask_s2(i):
    scl = i.select('SCL')
    m = scl.neq(3).And(scl.neq(8)).And(scl.neq(9)).And(scl.neq(10)).And(scl.neq(11))
    return i.updateMask(m)

def ndvi_month(tile, s, e):
    col = (ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
           .filterBounds(tile)
           .filterDate(s, e)
           .map(mask_s2))
    med = col.median()
    nd = med.normalizedDifference(['B8','B4']).rename('ndvi')
    return nd.clip(tile)

processed = False
for r in range(nrows):
    y_top = ymax - r * CELL_M
    y_bot = y_top - CELL_M
    for c in range(ncols):
        x_left = xmin + c * CELL_M
        x_right = x_left + CELL_M
        tile = ee.Geometry.Rectangle([x_left, y_bot, x_right, y_top])
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
        processed = True
        break
    if processed:
        break
