import ee, json, datetime
from ee import batch

ee.Initialize(project='gee-wcma-ndvi')

GEOJSON_PATH = "qg1/WCMA_BB.geojson"
FOLDER = "WCMA_NDVI_v2"
START = datetime.date(2019,1,1)
MONTHS = 3

with open(GEOJSON_PATH) as f:
    gj = json.load(f)
aoi = ee.Geometry(gj["features"][0]["geometry"]).bounds()

def ndvi_month(s, e):
    col = (ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
           .filterBounds(aoi)
           .filterDate(s, e)
           .select(['B4','B8']))
    img = ee.Image(ee.Algorithms.If(
        col.size().gt(0),
        col.mosaic().normalizedDifference(['B8','B4']).rename('ndvi'),
        ee.Image.constant(-9999).rename('ndvi')
    ))
    return img.clip(aoi)

def run():
    for k in range(MONTHS):
        s = ee.Date(START.strftime('%Y-%m-%d')).advance(k,'month')
        e = s.advance(1,'month')
        tag = s.format('YYYY_MM').getInfo()
        img = ndvi_month(s,e)
        task = batch.Export.image.toDrive(
            image=img,
            description=f'NDVI_{tag}_FULL',
            folder=FOLDER,
            fileNamePrefix=f'NDVI_10m_{tag}_FULL',
            region=aoi.transform('EPSG:4326',1),
            scale=10,
            maxPixels=1e13
        )
        task.start()
        print(f'FULL {tag} started')

if __name__ == "__main__":
    run()
