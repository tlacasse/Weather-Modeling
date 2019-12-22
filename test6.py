from weather.dataset import open_data
from weather.usgs import GAGEHEIGHT_TEMPLATE
from weather.visuals import display_loop, Projection, RiverMapper, CloudCell
import weather.source as wsrc
import cv2
import numpy as np


data, length = wsrc.get_full_dataset()
sites = wsrc.get_selected_river_sites()
airports = wsrc.get_airports()

latlong_list = wsrc.get_latlong_list(sites)

proj = Projection(wsrc.get_latlong_list(sites), width=16, padding=0.1)
h, w = proj.get_dim()
rmap = RiverMapper((h, w), 7, 10)

latlong_list = proj.on_points(latlong_list)

def to_input(i):
    results = []
    for k, v in zip([GAGEHEIGHT_TEMPLATE.format(s.key) for s, v in sites], latlong_list):
        results.append((v[0], v[1], data[k][i]))
    return results

def upscale(img, sc):
    return cv2.resize(img, (w*sc, h*sc), interpolation=cv2.INTER_NEAREST)

memory_refresh_rate = 30
memory_keep = 20
scale = 50
history = {}
cells = {}
for i in range(h):
    for j in range(w):
        history[(i, j)] = []
        cells[(i, j)] = CloudCell(i, j, scale, num=5)

def predict(model, sequence):
    return model.predict(sequence)[-1]

def loop_func(t):
    img = rmap.map_to_grid(to_input(t))
    return upscale(img, scale)

display_loop(range(length), loop_func)
