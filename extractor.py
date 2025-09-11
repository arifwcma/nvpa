import ee, datetime
from ee import batch
from gridify import get_grid

ee.Initialize(project='gee-wcma-ndvi')

FOLDER = 'WCMA_NDVI_v1'
START = datetime.date(2019,1,1)
MONTHS = 3

def tile_geom(row, col):
    g = get_grid()
    xmin, ymax, cell = g["xmin"], g["ymax"], g["CELL_M"]
    x_left = xmin + col * cell
    x_right = x_left + cell
    y_top = ymax - row * cell
    y_bot = y_top - cell
    return ee.Geometry.Rectangle([x_left, y_bot, x_right, y_top], proj=ee.Projection('EPSG:3857'), geodesic=False)

def ndvi_month(tile, s, e):
    col = (ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
           .filterBounds(tile)
           .filterDate(s, e)
           .select(['B4','B8']))
    img = ee.Image(ee.Algorithms.If(col.size().gt(0),
                                    col.mosaic().normalizedDifference(['B8','B4']).rename('ndvi'),
                                    ee.Image.constant(-9999).rename('ndvi')))
    return img.clip(tile)

def extract(row, col, months=MONTHS, start=START):
    for k in range(months):
        s = ee.Date(start.strftime('%Y-%m-%d')).advance(k,'month')
        e = s.advance(1,'month')
        tag = s.format('YYYY_MM').getInfo()
        tile = tile_geom(row, col)
        img = ndvi_month(tile, s, e)
        task = batch.Export.image.toDrive(
            image=img,
            description=f'NDVI_{tag}_r{row}_c{col}',
            folder=FOLDER,
            fileNamePrefix=f'NDVI_10m_{tag}_r{row}_c{col}',
            region=tile.transform('EPSG:4326',1),
            scale=10,
            maxPixels=1e13
        )
        task.start()
        print(f'r{row} c{col} {tag} started')

extract(0,0)
