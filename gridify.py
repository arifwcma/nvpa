import json

def get_grid():
    GEOJSON_PATH = "qg1/WCMA_BB.geojson"
    CELL_M = 10000
    with open(GEOJSON_PATH) as f:
        gj = json.load(f)
    coords = gj["features"][0]["geometry"]["coordinates"][0]
    xs = [float(p[0]) for p in coords]
    ys = [float(p[1]) for p in coords]
    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)
    width = xmax - xmin
    height = ymax - ymin
    ncols = int((width / CELL_M) + 0.9999)
    nrows = int((height / CELL_M) + 0.9999)
    return {
        "xmin": xmin, "xmax": xmax, "ymin": ymin, "ymax": ymax,
        "width_m": width, "height_m": height,
        "ncols": ncols, "nrows": nrows, "total": nrows * ncols,
        "CELL_M": CELL_M, "CRS": "EPSG:3857"
    }

if __name__=="__main__":
    print(get_grid())
