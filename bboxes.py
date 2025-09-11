import json, os
from gridify import get_grid

def define_cell(row, col, serial, out_dir="cells"):
    g = get_grid()
    xmin, ymax, cell = g["xmin"], g["ymax"], g["CELL_M"]
    x_left = xmin + col * cell
    x_right = x_left + cell
    y_top = ymax - row * cell
    y_bot = y_top - cell
    coords = [[[x_left,y_bot],[x_right,y_bot],[x_right,y_top],[x_left,y_top],[x_left,y_bot]]]
    fc = {
        "type":"FeatureCollection",
        "crs":{"type":"name","properties":{"name":"EPSG:3857"}},
        "features":[{"type":"Feature","geometry":{"type":"Polygon","coordinates":coords},
                     "properties":{"row":row,"col":col,"serial":serial}}]
    }
    os.makedirs(out_dir, exist_ok=True)
    fn = os.path.join(out_dir, f"cell_{serial}_{row}_{col}.geojson")
    with open(fn,"w") as f: json.dump(fc,f)
    print("saved", fn)

def main():
    g = get_grid()
    serial = 0
    for r in range(g["nrows"]):
        for c in range(g["ncols"]):
            define_cell(r, c, serial)
            serial += 1

if __name__=="__main__":
    main()
