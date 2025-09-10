import ee, json
ee.Initialize(project='gee-wcma-ndvi')

def get_grid():
    GEOJSON_PATH = "qg1/WCMA_BB.geojson"
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

    return {
        "xmin": xmin,
        "xmax": xmax,
        "ymin": ymin,
        "ymax": ymax,
        "width_m": width,
        "height_m": height,
        "ncols": ncols,
        "nrows": nrows,
        "total": nrows * ncols,
        "CELL_M": CELL_M
    }
