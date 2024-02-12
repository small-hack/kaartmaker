from kaartmaker.constants import LEGEND
from geopandas.geodataframe import GeoDataFrame
from matplotlib.patches import Polygon
from matplotlib import axes
import matplotlib.patheffects as PathEffects
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def add_label(ax,
              label: dict,
              default_font_size: int = 24,
              default_font_weight: str = "bold", 
              default_font_color: str = "#040303",
              va: str = "center", 
              ha: str = "center"):            
    """
    Adds a label to e.g. a country or state at a specific pinpoint
    label dict example:
    {"label": "Togo", "xytext": (1.0, 4.1), "xypin": (1.0, 7.5)}
    optionally, you can also have font_size, font_color, and font_weight keys.
    """
    # if font_size, not set in dict, use default from args
    font_size = label.get("font_size", default_font_size)
    # if font_color, not set in dict, use default from args
    font_color = label.get("font_color", default_font_color)
    # if font_weight, not set in dict, use default from args
    font_weight = label.get("font_weight", default_font_weight)

    annotation = plt.annotate(
        label["label"], 
        xy=label["xytext"] if "xypin" not in label.keys() else label["xypin"], 
        xytext=None if "xypin" not in label.keys() else label["xytext"], 
        xycoords="data",
        fontsize=font_size,
        va=va,
        ha=ha,
        linespacing=1.3,
        color=font_color,
        fontweight=font_weight, 
        arrowprops={
            "arrowstyle": "-",
            "linewidth": 2,
        })
    
    annotation.set_path_effects([PathEffects.withStroke(linewidth=6, foreground='w')])


def draw_legend_and_title(ax: axes,
                          region: str,
                          map_data: GeoDataFrame,
                          legend_title: str = "",
                          source: str = "",
                          legend_countries: list = []):
    """ 
    draw a legend using countries' shapes as the legend, title, and subtitle
    """

    # example countries to use for the map's legend
    if legend_countries:
        # make sure the first letter of every country is capital for matching it
        for index, country in enumerate(legend_countries):
           legend_countries[index] = country.title() 

        countries = legend_countries
    else:
        countries = []
        # get all present kinds of votes: abstention, in favor, absent, yes, no
        all_votes = map_data['vote'].unique()
        # for each kind of vote, grab an example country
        for vote_type in all_votes:
            names = map_data.loc[map_data.vote == vote_type].NAME_EN.reset_index(drop=True)
            if names.any():
                countries.append(names[0])

    # legend using specific locations for this region
    legend_dict = LEGEND[region]["legend"]
    legend_xy = legend_dict["geometry"]
    legend_label = legend_dict["label"]
    legend_size = legend_dict["size"]
    legend_spacing = legend_dict["spacing"]
    legend_font = legend_dict.get("font_size", 24)

    legend = pd.concat([map_data[map_data.NAME_EN.isin(countries)]])
    legend = legend.sort_values("color")

    # title and sources annotation
    title = LEGEND[region]["title"]
    title_size = LEGEND[region].get("title_size", 42)
    subtitle = LEGEND[region]["subtitle"]
    subtitle_source = LEGEND[region]["subtitle_source"]
    subtitle_size = LEGEND[region].get("subtitle_size", 24)

    # print(countries)
    for i, row in legend.reset_index().iterrows():
        # print(row.NAME_EN)
        draw_legend_geometry(ax,
                             row,
                             legend_xy[0],
                             legend_xy[1] - legend_spacing*i,
                             legend_size)
        ax.annotate(row.vote,
                    (legend_label[0],
                     legend_label[1] - legend_spacing*i),
                    fontsize=legend_font,
                    fontweight="bold",
                    va="center")

    fontstyles = {"fontweight": "bold", "ha": "left"}

    if region == "world":
        title_region = ""
    elif region == "south america" or region == "western asia":
        title_region = f"\n({region.title()})" 
    else:
        title_region = f" ({region.title()})" 

    ax.annotate(f"{legend_title}{title_region}",
                (title[0], title[1]),
                fontsize=title_size, **fontstyles)

    # data source subtitle and actual sources
    ax.annotate("Data source:",
                (subtitle[0], subtitle[1]),
                va="center",
                fontsize=subtitle_size, **fontstyles)

    sources = "naturalearthdata.com"
    if source:
        sources = sources + ", " + source
    ax.annotate(sources,
                (subtitle_source[0], subtitle_source[1]),
                va="center",
                color="#785EF0",
                fontsize=subtitle_size, **fontstyles)



def draw_legend_geometry(ax: axes,
                         row: pd.core.series.Series,
                         x_loc: float,
                         y_loc: float,
                         height: float):
    """
    draw the legend geometry
    thank you: https://gis.stackexchange.com/a/378894
    """
    # some countries are a single blob
    if row.geometry.geom_type == "Polygon":
        x = np.array(row.geometry.boundary.coords.xy[0])
        y = np.array(row.geometry.boundary.coords.xy[1])
        
        x = x - (row.geometry.centroid.x - x_loc)
        y = y - (row.geometry.centroid.y - y_loc)
        
        ratio = height / (y.max() - y.min())
        x = x * ratio + (x_loc - x_loc * ratio)
        y = y * ratio + (y_loc - y_loc * ratio)
        
        ax.add_artist(Polygon(np.stack([x, y], axis=1),
                              facecolor=row.color,
                              edgecolor=row.edgecolor))
        # hatch=row.hatch))

    # some countries are multi-polygon because they have islands
    else:
        x = np.array(row.geometry.geoms[0].boundary.coords.xy[0])
        y = np.array(row.geometry.geoms[0].boundary.coords.xy[1])
        
        x = x - (row.geometry.geoms[0].centroid.x - x_loc)
        y = y - (row.geometry.geoms[0].centroid.y - y_loc)
        
        ratio = height / (y.max() - y.min())
        x = x * ratio + (x_loc - x_loc * ratio)
        y = y * ratio + (y_loc - y_loc * ratio)
        
        ax.add_artist(Polygon(np.stack([x, y], axis=1),
                              facecolor=row.color,
                              edgecolor=row.edgecolor))
