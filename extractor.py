import ee, datetime
from ee import batch
from gridify import get_grid

ee.Initialize(project='gee-wcma-ndvi')

def extract(row, col):
    grid = get_grid()
    xmin, ymax, cell = grid["xmin"], grid["ymax"], grid["CELL_M"]
    x_left = xmin + col * cell
    x_right = x_left + cell
    y_top = ymax - row * cell
    y_bot = y_top - cell
    tile = ee.Geometry.Rectangle([x_left, y_bot, x_right, y_top], proj=ee.Projection('EPSG:3857'), geodesic=False)

    def ndvi_month(s, e):
        col = (ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
               .filterBounds(tile)
               .filterDate(s, e)
               .select(['B4','B8']))
        nd = ee.Image(ee.Algorithms.If(
            col.size().gt(0),
            col.mosaic().normalizedDifference(['B8','B4']).rename('ndvi'),
            ee.Image.constant(-9999).rename('ndvi')
        ))
        return nd.clip(tile)

    start = datetime.date(2019,1,1)
    for k in range(3):
        s = ee.Date(start.strftime('%Y-%m-%d')).advance(k,'month')
        e = s.advance(1,'month')
        tag = s.format('YYYY_MM').getInfo()
        img = ndvi_month(s,e)
        task = batch.Export.image.toDrive(
            image=img,
            description=f'NDVI_{tag}_r{row}_c{col}',
            folder='WCMA_NDVI_TEST2',
            fileNamePrefix=f'NDVI_10m_{tag}_r{row}_c{col}',
            region=tile.transform('EPSG:4326',1),
            scale=10,
            maxPixels=1e13
        )
        task.start()
        print(f"Row {row}; Col {col}; Month {tag} initiated")


extract(0,0)
