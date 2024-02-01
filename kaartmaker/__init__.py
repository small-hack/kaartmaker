#!python3.12
# https://en.wikipedia.org/wiki/GeoJSON
import geopandas as gpd
# from os import environ, path, uname
from os import path
import matplotlib.pyplot as plt
import matplotlib.patheffects as PathEffects
# from matplotlib.patches import Polygon
# import numpy as np
import pandas as pd
import seaborn as sns


# grabs the default packaged config file from default dot files
PWD = path.dirname(__file__)
EUROPE_JSON = path.join(PWD, 'geojson/europe.geojson')
WORLD_JSON = path.join(PWD, 'geojson/world_subunits.geojson')
CEASEFIRE_CSV= path.join(PWD, 'datasets/world_palestine_votes_minus_unknown.csv')


def process_csv(dataset: str = CEASEFIRE_CSV):
    """
    process csv
    fields: NAME_EN, cease_fire, suspended_unrwa_aid
    """
    df = pd.read_csv(dataset, index_col="NAME_EN")
    return df


def set_limits(ax, data, pad_left=0, pad_right=0, pad_top=0, pad_bottom=0):
    """
    defines borders and sizes of map
    """
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
    figsize: tuple|list = (40, 40)
    ):
    
    assert "color" in maps_to_draw[0].columns, "Missing color column in map dataframe"
    assert "edgecolor" in maps_to_draw[0].columns, "Missing edgecolor column in map dataframe"
    
    fig = plt.figure(figsize=figsize)
    fig.suptitle('europe', fontsize="xx-large", fontweight="bold")
    ax = fig.add_subplot()
    
    for map_index, map_to_draw in enumerate(maps_to_draw):
        map_to_draw.plot(
            ax=ax,
            color=map_to_draw.color,
            edgecolor=map_to_draw.edgecolor,
            hatch="//" if map_index in use_hatch_for_indexes else "",
        )

    # Additional functions below this comment
    set_limits(ax, maps_to_draw[boundry_map_index], **padding)
    
    return ax


def add_label(ax,
              label,
              fontsize=24,
              fontweight="bold", 
              va="center", 
              ha="center"):            
    """
    Add label to each country
    """
    annotation = plt.annotate(
        label["label"], 
        xy=label["xytext"] if "xypin" not in label.keys() else label["xypin"], 
        xytext=None if "xypin" not in label.keys() else label["xytext"], 
        xycoords="data", fontsize=fontsize, va=va, ha=ha,
        linespacing=1.3, color=label["color"], fontweight=fontweight, 
        arrowprops={
            "arrowstyle": "-",
            "linewidth": 2,
        })
    
    annotation.set_path_effects([PathEffects.withStroke(linewidth=6, foreground='w')])


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

    # process country properties to add to the world geojson dataframe
    country_traits = process_csv()

    # parse out just europe
    europe = world[world.CONTINENT == "Europe"].reset_index(drop=True)

    # set europe's outline to be darker
    europe["edgecolor"] = "#000000"
    europe["color"] = "#f0f0f0"

    # update the geojson with cease fire info
    for index, row in country_traits.iterrows():
        cease_fire = row["cease_fire"]

        if cease_fire == "ABSTENTION":
            europe.loc[europe.NAME_EN == index, "color"] = "#FFB000"
        elif cease_fire == "IN FAVOR":
            europe.loc[europe.NAME_EN == index, "color"] = "#648FFF"
        elif cease_fire == "AGAINST":
            europe.loc[europe.NAME_EN == index, "color"] = "#DC267F"

    ax = draw_map(maps_to_draw=[world, europe],
                  boundry_map_index=1,
                  padding={"pad_bottom": -0.03,
                           "pad_top": -0.34,
                           "pad_left": -0.03,
                           "pad_right": -0.3},
                  use_hatch_for_indexes=[2])

    europe.to_file(EUROPE_JSON, driver="GeoJSON")  

    # # hide most standard chart components when drawing maps
    plt.axis("off")
    plt.savefig('europe.png')


if __name__ == '__main__':
    main()
