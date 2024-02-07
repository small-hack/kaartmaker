from geopandas.geodataframe import GeoDataFrame
from matplotlib.patches import Polygon
from matplotlib import axes
import matplotlib.patheffects as PathEffects
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


legend_area = {
        "asia": {
            "legend": {
                "geometry": [35, 0.09],
                "label": [42, 0.09],
                "size": 3.4,
                "font_size": 28,
                "spacing": 4.5,
            },
            "title": [29, 4],
            "subtitle": [29, 3],
            "subtitle_source": [37, 3],
            "countries": ["Israel", "Russia", "Georgia"]
            },
        "africa": {
            "legend": {
                "geometry": [-23, -22],
                "label": [-20, -22],
                "size": 4.5,
                "font_size": 28,
                "spacing": 5,
            },
            "title": [-25, -17],
            "subtitle": [-25, -18],
            "subtitle_source": [-20, -18],
            "countries": ["Chad", "Togo", "Liberia"]
            },
        "caribbean": {
            "legend": {
                "geometry": [-77.6, 13],
                "label": [-76.6, 13],
                "size": 0.75,
                "font_size": 28,
                "spacing": 1,
            },
            "title": [-78.5, 14],
            "subtitle": [-78.5, 13.75],
            "subtitle_source": [-77, 13.75],
            "countries": ["Jamaica", "Haiti"]
            },
        "central america": {
            "legend": {
                "geometry": [-115, 11],
                "label": [-112, 11],
                "size": 1.5,
                "font_size": 28,
                "spacing": 2.25,
            },
            "title": [-117, 13],
            "subtitle": [-117, 12.5],
            "subtitle_source": [-114, 12.5],
            "countries": ["Guatemala", "Mexico", "Panama"]
            },
        "central asia": {
            "legend": {
                "geometry": [54, 10],
                "label": [57, 10],
                "size": 3.5,
                "font_size": 28,
                "spacing": 4.5,
            },
            "title": [51, 13],
            "subtitle": [51, 12.5],
            "subtitle_source": [56, 12.5],
            "countries": ["India"]
            },
        "eastern asia": {
            "legend": {
                "geometry": [130, 16.8],
                "label": [132, 16.8],
                "size": 2,
                "font_size": 28,
                "spacing": 4.5,
            },
            "title": [128.9, 20],
            "subtitle": [128.9, 19],
            "subtitle_source": [134, 19],
            "countries": ["Vietnam"]
            },
        "europe": {
            "legend": {
                "geometry": [-18.2, 59],
                "label": [-16.5, 59],
                "size": 1.1,
                "spacing": 1.6
            },
            "title": [-19.9, 60.5],
            "subtitle": [-19.9, 60],
            "subtitle_source": [-16, 60],
            "countries": ["Slovenia", "Hungary", "Austria"]
            },
        "oceania": {
            "legend": {
                "geometry": [117, -48.5],
                "label": [120, -48.5],
                "size": 3,
                "font_size": 28,
                "spacing": 4.5,
            },
            "title": [115, -44.5],
            "subtitle": [115, -45.5],
            "subtitle_source": [120.5, -45.5],
            "countries": ["Australia", "Papua New Guinea"]
            },
        "south america": {
            "legend": {
                "geometry": [-90, -30],
                "label": [-87, -30],
                "size": 3.75,
                "font_size": 28,
                "spacing": 4.5,
            },
            "title": [-92, -26],
            "subtitle": [-92, -27],
            "subtitle_source": [-87, -27],
            "countries": ["Brazil", "Paraguay", "Argentina"]
            },
        "western asia": {
            "legend": {
                "geometry": [32.25, 17],
                "label": [33.75, 17],
                "size": 1,
                "spacing": 1.6
            },
            "title": [30.75, 18.5],
            "subtitle": [30.75, 18],
            "subtitle_source": [33.2, 18],
            "countries": ["Israel", "Georgia", "Jordan"]
            },
        "world": {
            "legend": {
                "geometry": [-156, -31],
                "label": [-142, -31],
                "size": 7.5,
                "font_size": 28,
                "spacing": 9.7,
            },
            "title": [-165, -21],
            "title_size": 32,
            "subtitle": [-165, -24],
            "subtitle_source": [-144, -24],
            "subtitle_size": 22,
            "countries": ["Brazil", "United States of America", "Germany"]
            },
        }


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
                          source: str = ""):
    """ 
    draw a legend using countries' shapes as the legend, title, and subtitle
    """
    # legend using specific locations for this region
    countries = legend_area[region]['countries']
    legend_dict = legend_area[region]["legend"]
    legend_xy = legend_dict["geometry"]
    legend_label = legend_dict["label"]
    legend_size = legend_dict["size"]
    legend_spacing = legend_dict["spacing"]
    legend_font = legend_dict.get("font_size", 24)

    legend = pd.concat([map_data[map_data.NAME_EN.isin(countries)]])
    legend = legend.sort_values("color")

    # title and sources annotation
    title = legend_area[region]["title"]
    title_size = legend_area[region].get("title_size", 42)
    subtitle = legend_area[region]["subtitle"]
    subtitle_source = legend_area[region]["subtitle_source"]
    subtitle_size = legend_area[region].get("subtitle_size", 24)


    for i, row in legend.reset_index().iterrows():
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
        sources = sources + " and " + source
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
