#!python3.12

import geopandas as gpd
from kaartmaker.country_labels import add_label, country_labels
from os import path
import matplotlib.pyplot as plt
# from matplotlib.patches import Polygon
# import numpy as np
import pandas as pd
import seaborn as sns


# grabs the default packaged config file from default dot files
PWD = path.dirname(__file__)
WORLD_JSON = path.join(PWD, 'geojson/world_subunits.geojson')
CEASEFIRE_CSV = path.join(PWD, 'datasets/world_palestine_votes_minus_unknown.csv')


def process_csv(data_frame: pd.DataFrame, dataset_csv_file: str = ""):
    """
    take dataframe and process a process csv into it
    fields: NAME_EN, cease_fire, suspended_unrwa_aid
    """
    if not dataset_csv_file:
        dataset_csv_file = CEASEFIRE_CSV
    df = pd.read_csv(dataset_csv_file, index_col="NAME_EN")

    # update the geojson with cease fire info
    for index, row in df.iterrows():
        cease_fire = row["cease_fire"]

        if cease_fire == "ABSTENTION":
            data_frame.loc[data_frame.NAME_EN == index, "color"] = "#999999"
        elif cease_fire == "IN FAVOR":
            data_frame.loc[data_frame.NAME_EN == index, "color"] = "#648FFF"
        elif cease_fire == "AGAINST":
            data_frame.loc[data_frame.NAME_EN == index, "color"] = "#DC267F"

    return data_frame


def set_limits(ax,
               data,
               pad_left: int = 0,
               pad_right: int = 0,
               pad_top: int = 0,
               pad_bottom: int = 0):
    """
    defines limits of data to display, i.e. how much of the map to display
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
    maps_to_draw: list,
    title: str,
    boundry_map_index: int = 0,
    use_hatch_for_indexes: list = [],
    padding: dict = {},
    figsize: tuple|list = (40, 40),
    labels: list = []
    ):
    """
    Takes a list of geojson dataframes to use for drawing a map and returns an ax obj
    """
    
    assert "color" in maps_to_draw[0].columns, "Missing color column in map dataframe"
    assert "edgecolor" in maps_to_draw[0].columns, "Missing edgecolor column in map dataframe"
    
    fig = plt.figure(figsize=figsize)
    fig.suptitle(title, fontsize=72, fontweight="bold")
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

    # add area labels if any were passed in
    if labels:
        for label in labels:
            add_label(ax, label)
    
    return ax


def main(
        continent: str = "Europe",
        csv: str = "",
        save_geojson: bool = False,
        save_png: bool = True
        ):
    # seaborn style
    font_family = "sans"
    background_color = "#D4F1F4"
    text_color = "#040303"

    sns.set_style({
        "axes.facecolor": text_color,
        "figure.facecolor": background_color,
        "font.family": font_family,
        "text.color": text_color,
    })

    world_map_data = gpd.read_file(WORLD_JSON)
    world_map_data["color"] = "#f0f0f0"
    world_map_data["edgecolor"] = "#c0c0c0"

    # parse out just europe
    map_data = world_map_data[world_map_data.CONTINENT == continent].reset_index(drop=True)

    # set map_data's outline to be darker
    map_data["edgecolor"] = "#000000"
    map_data["color"] = "#f0f0f0"

    # process country properties to add to the world_map_data geojson dataframe
    map_data = process_csv(map_data, csv)

    ax = draw_map(maps_to_draw=[world_map_data, map_data],
                  title=f"Map of Continental {continent} UN votes",
                  boundry_map_index=1,
                  padding={"pad_bottom": -0.03,
                           "pad_top": -0.37,
                           "pad_left": -0.04,
                           "pad_right": -0.3},
                  use_hatch_for_indexes=[2],
                  labels=country_labels[continent])

    # we can save the final geojson so the use can use it interactively
    if save_geojson:
        json_file = path.join(PWD, f'geojson/{continent}.geojson')
        map_data.to_file(json_file, driver="GeoJSON")  

    # assumably we want to save this as a png
    if save_png:
        # hide most standard chart components when drawing maps
        plt.axis("off")
        plt.savefig(f'{continent}.png')


if __name__ == '__main__':
    main()
