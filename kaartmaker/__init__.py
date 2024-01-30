#!python3.12
# https://en.wikipedia.org/wiki/GeoJSON
import numpy as np
import pandas as pd
import seaborn as sns
import geopandas as gpd
from os import environ, path, uname

import matplotlib.pyplot as plt
import matplotlib.patheffects as PathEffects
from matplotlib.patches import Polygon


# grabs the default packaged config file from default dot files
PWD = path.dirname(__file__)
EURO_JSON = path.join(PWD, 'geojson/europe.geo.json')
WORLD_JSON = path.join(PWD, 'geojson/world.geo.json')


def set_limits(ax, data, pad_left=0, pad_right=0, pad_top=0, pad_bottom=0):
    xmin_ = data.bounds.minx.min()
    ymin_ = data.bounds.miny.min()
    xmax_ = data.bounds.maxx.max()
    ymax_ = data.bounds.maxy.max()
    
    xmin = xmin_ - pad_left * (xmax_ - xmin_)
    xmax = xmax_ + pad_right * (xmax_ - xmin_)
    ymin = ymin_ - pad_bottom * (ymax_ - ymin_)
    ymax = ymax_ + pad_top * (ymax_ - ymin_)
    
    ax.set(xlim=(xmin, xmax), ylim=(ymin, ymax))


def draw_map(
    maps_to_draw, 
    boundry_map_index: int = 0,
    use_hatch_for_indexes: list = [],
    padding: dict = {},
    labels: list = [],
    figsize: tuple|list = (40, 40)
    ):
    
    assert "color" in maps_to_draw[0].columns, "Missing color column in map dataframe"
    assert "edgecolor" in maps_to_draw[0].columns, "Missing edgecolor column in map dataframe"
    
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot()
    
    for map_index, map_to_draw in enumerate(maps_to_draw):
        map_to_draw.plot(
            ax=ax, color=map_to_draw.color, edgecolor=map_to_draw.edgecolor,
            hatch="//" if map_index in use_hatch_for_indexes else "",
        )

    # Additional functions below this comment
    set_limits(ax, maps_to_draw[boundry_map_index], **padding)
    
    return ax


def main():
    # seaborn style
    font_family = "sans"
    background_color = "#D4F1F4"
    text_color = "#040303"

    sns.set_style({
        "axes.facecolor": background_color,
        "figure.facecolor": background_color,
        "font.family": font_family,
        "text.color": text_color,
    })

    world = gpd.read_file(WORLD_JSON)
    world["color"] = "#f0f0f0"
    world["edgecolor"] = "#c0c0c0"

    europe = world[world.CONTINENT == "Europe"].reset_index(drop=True)
    europe["edgecolor"] = "#000000"

    ax = draw_map(maps_to_draw=[world, europe],
                  boundry_map_index=1,
                  padding={"pad_bottom": -0.08,
                           "pad_top": 0.07,
                           "pad_left": 0.07,
                           "pad_right": 0.05},
                  use_hatch_for_indexes=[2])

    # hide most standard chart components when drawing maps
    plt.axis("off")
    plt.show()

if __name__ == '__main__':
    main()
