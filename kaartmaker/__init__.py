#!python3.12
from click import option, command
# from collections import deque
import geopandas as gpd
from kaartmaker.constants import (PWD, VERSION, LABELS, COUNTRY_BOUNDARIES,
                                  WORLD_SUBUNITS_JSON)

from kaartmaker.process_dataset import process_csv 
from kaartmaker.labeling import add_label, draw_legend_and_title
from os import path
import matplotlib.pyplot as plt
import seaborn as sns
from kaartmaker.help_text import RichCommand, options_help


HELP = options_help()
HELP_SETTINGS = dict(help_option_names=["-h", "--help"])


def determine_regional_area(world_map_data, region: str):
    """
    determine what the actual name of the region is and which counries should
    be displayed. Returns dataframe with only the selected region
    """
    if region == "Middle East" or region == "West Asia" or region == "Western Asia":
        region = "Western Asia"
        # for the purposes of the "Middle East" we also include Iran and Egypt
        world_map_data.loc[world_map_data.NAME_EN == "Iran", "SUBREGION"] = "Western Asia"
        world_map_data.loc[world_map_data.NAME_EN == "Egypt", "SUBREGION"] = "Western Asia"

    if region == "Central Asia" or region == "Southern Asia":
        region = "Southern Asia"
        # for southern asia we include all of central asia
        world_map_data.loc[world_map_data.NAME_EN == "Baikonur", "SUBREGION"] = "Southern Asia"
        world_map_data.loc[world_map_data.NAME_EN == "Mongolia", "SUBREGION"] = "Southern Asia"
        world_map_data.loc[world_map_data.NAME_EN == "Myanmar", "SUBREGION"] = "Southern Asia"
        world_map_data.loc[world_map_data.NAME_EN == "Russia", "SUBREGION"] = "Southern Asia"
        world_map_data.loc[world_map_data.NAME_EN == "People's Republic of China", "SUBREGION"] = "Southern Asia"
        world_map_data.loc[world_map_data.NAME_EN == "Kazakhstan", "SUBREGION"] = "Southern Asia"
        world_map_data.loc[world_map_data.NAME_EN == "Kyrgyzstan", "SUBREGION"] = "Southern Asia"
        world_map_data.loc[world_map_data.NAME_EN == "Tajikistan", "SUBREGION"] = "Southern Asia"
        world_map_data.loc[world_map_data.NAME_EN == "Turkmenistan", "SUBREGION"] = "Southern Asia"
        world_map_data.loc[world_map_data.NAME_EN == "Uzbekistan", "SUBREGION"] = "Southern Asia"

    if region == "East Asia" or region == "Eastern Asia":
        region = "Eastern Asia"
        # for southern asia we include all of south east asia as well 
        world_map_data.loc[world_map_data.NAME_EN == "Brunei", "SUBREGION"] = "Eastern Asia"
        world_map_data.loc[world_map_data.NAME_EN == "Philippines", "SUBREGION"] = "Eastern Asia"
        world_map_data.loc[world_map_data.NAME_EN == "Vietnam", "SUBREGION"] = "Eastern Asia"
        world_map_data.loc[world_map_data.NAME_EN == "Cambodia", "SUBREGION"] = "Eastern Asia"
        world_map_data.loc[world_map_data.NAME_EN == "Laos", "SUBREGION"] = "Eastern Asia"
        world_map_data.loc[world_map_data.NAME_EN == "Thailand", "SUBREGION"] = "Eastern Asia"
        world_map_data.loc[world_map_data.NAME_EN == "Malaysia", "SUBREGION"] = "Eastern Asia"
        world_map_data.loc[world_map_data.NAME_EN == "Myanmar", "SUBREGION"] = "Eastern Asia"
        world_map_data.loc[world_map_data.NAME_EN == "Russia", "SUBREGION"] = "Eastern Asia"
        world_map_data.loc[world_map_data.NAME_EN == "Singapore", "SUBREGION"] = "Eastern Asia"
        world_map_data.loc[world_map_data.NAME_EN == "Indonesia", "SUBREGION"] = "Eastern Asia"

    # verify if this is a continent or subregion
    if region in ["Central Asia", "Western Asia", "Central America",
                  "Caribbean", "Southern Asia", "Eastern Asia"]:
        map_data = world_map_data[world_map_data.SUBREGION == region].reset_index(drop=True)
    else:
        map_data = world_map_data[world_map_data.CONTINENT == region].reset_index(drop=True)

    # set map_data's outline to be darker
    map_data["edgecolor"] = "#000000"
    map_data["color"] = "#f0f0f0"

    return map_data


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
    boundry_map_index: int = 0,
    use_hatch_for_indexes: list = [],
    padding: dict = {},
    figsize: tuple|list = (40, 40),
    labels: list = []):
    """
    Takes a list of geojson dataframes to use for drawing a map and returns an ax obj
    """
    assert "color" in maps_to_draw[0].columns, "Missing color column in map dataframe"
    assert "edgecolor" in maps_to_draw[0].columns, "Missing edgecolor column in map dataframe"
    
    fig = plt.figure(figsize=figsize, layout="compressed")
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


@command(cls=RichCommand, context_settings=HELP_SETTINGS)
@option("--region", "-r",
        metavar="REGION",
        type=str,
        default="world",
        help=HELP['region'])
@option("--csv", "-C",
        metavar="CSV_FILE",
        type=str,
        help=HELP['csv'])
@option("--save-geojson", "-g",
        is_flag=True,
        help=HELP['save_geojson'])
@option("--save-png", "-p",
        is_flag=True,
        default=True,
        help=HELP['save_png'])
@option("--title", "-t",
        metavar="TITLE",
        help=HELP['title'],
        type=str)
@option("--source", "-s",
        help=HELP['source'],
        default="gadebate.un.org",
        type=str)
@option("--reverse_colors", "-R",
        help=HELP['reverse_colors'],
        default=False,
        is_flag=True)
@option("--use_sub_units", "-u",
        help=HELP['use_sub_units'],
        default=False,
        is_flag=True)
@option("--legend_countries", "-l",
        metavar="COUNTRIES",
        help=HELP['legend_countries'],
        default="",
        type=str)
@option("--version", "-v",
        is_flag=True,
        help=HELP['version'])
def main(
        region: str = "world",
        csv: str = "",
        save_geojson: bool = False,
        save_png: bool = True,
        title: str = "UNGA",
        source: str = "gadebate.un.org",
        reverse_colors: bool = False,
        use_sub_units: bool = False,
        legend_countries: str = "",
        version: bool = True
        ):
    if version:
        print(VERSION)

    if ',' in legend_countries:
        legend_countries = legend_countries.split(',')

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

    world_map_data = gpd.read_file(WORLD_SUBUNITS_JSON)
    fig_padding = COUNTRY_BOUNDARIES[region.lower()]["sub_units"]["padding"]
    fig_size = COUNTRY_BOUNDARIES[region.lower()]["sub_units"]["size"]

    world_map_data["color"] = "#f0f0f0"

    if region.title() != "World":
        world_map_data["edgecolor"] = "#c0c0c0"
        # process out which countries should be shown on the map per region
        map_data = determine_regional_area(world_map_data, region.title())

        # process country properties to add to the world_map_data geojson dataframe
        map_data = process_csv(map_data, csv, reverse_colors=reverse_colors,
                               sub_units=use_sub_units)

        # get labels for each country if applicable
        labels = LABELS[region.lower()]

        # if region is asia, we'll do a smaller size and leave out world map
        if region == "asia":
            maps = [map_data]
            boundary_index = 0
        else:
            boundary_index = 1
            maps = [world_map_data, map_data]
    else:
        world_map_data["edgecolor"] = "#5c5c5c"
        map_data = process_csv(world_map_data, csv, reverse_colors=reverse_colors,
                               sub_units=use_sub_units)
        maps = [map_data]
        boundary_index = 0
        labels = []

    # this takes care of crimea
    # if region.lower() == "europe" or region.lower() == "world":
    #     crimea = world_map_data[world_map_data.NAME_EN == "Autonomous Republic of Crimea"].reset_index(drop=True)
    #     crimea["color"] = "#f0f0f0"
    #     crimea["edgecolor"] = "#c0c0c0"
    #     maps.append(crimea)

    ax = draw_map(maps_to_draw=maps,
                  boundry_map_index=boundary_index,
                  padding=fig_padding,
                  use_hatch_for_indexes=[2],
                  labels=labels,
                  figsize=fig_size)

    region = region.lower()

    draw_legend_and_title(ax, region, map_data, title, source, legend_countries)

    region = region.replace(" ", "_")
    title = title.replace(" ", "_")

    # we can save the final geojson so the use can use it interactively
    if save_geojson:
        json_file = path.join(PWD, f'geojson/{region}_{title}.geojson')
        map_data.to_file(json_file, driver="GeoJSON")  

    # assumably we want to save this as a png
    if save_png:
        # hide most standard chart components when drawing maps
        plt.axis("off")
        plt.savefig(f'{region}_{title}.png')


if __name__ == '__main__':
    main()
