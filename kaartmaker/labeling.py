from matplotlib.patches import Polygon
from matplotlib import axes
import matplotlib.patheffects as PathEffects
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


legend_area = {
        "africa": {
            "legend": {
                "geometry": [-24.5, -23.55],
                "label": [-22.3, -23.55],
                "size": 3.75,
                "font_size": 28,
                "spacing": 4.5,
            },
            "title": [0.03, -0.05],
            "subtitle": [0.03, -0.06],
            "subtitle_source": [0.1, -0.06],
            "countries": ["Chad", "Togo", "Liberia"]
            },
        "central america": {
            "legend": {
                "geometry": [-115, 13.05],
                "label": [-112, 13.05],
                "size": 2,
                "font_size": 28,
                "spacing": 3,
            },
            "title": [0.02, -0.05],
            "subtitle": [0.02, -0.06],
            "subtitle_source": [0.09, -0.06],
            "countries": ["Guatemala", "Mexico", "Panama"]
            },
        "central asia": {
            "legend": {
                "geometry": [57, 7.75],
                "label": [59.5, 7.75],
                "size": 3.5,
                "font_size": 28,
                "spacing": 4.5,
            },
            "title": [0.01, -0.05],
            "subtitle": [0.01, -0.06],
            "subtitle_source": [0.09, -0.06],
            "countries": ["India"]
            },
        "eastern asia": {
            "legend": {
                "geometry": [97, -9.7],
                "label": [99, -9.7],
                "size": 2,
                "font_size": 28,
                "spacing": 4.5,
            },
            "title": [0.01, -0.05],
            "subtitle": [0.01, -0.06],
            "subtitle_source": [0.09, -0.06],
            "countries": ["Cambodia"]
            },
        "oceania": {
            "legend": {
                "geometry": [117, -48.5],
                "label": [120, -48.5],
                "size": 3,
                "font_size": 28,
                "spacing": 4.5,
            },
            "title": [0.01, -0.05],
            "subtitle": [0.01, -0.06],
            "subtitle_source": [0.09, -0.06],
            "countries": ["Australia", "Papua New Guinea"]
            },
        "south america": {
            "legend": {
                "geometry": [-89, -45],
                "label": [-86, -45],
                "size": 3.75,
                "font_size": 28,
                "spacing": 4.5,
            },
            "title": [0.01, -0.05],
            "subtitle": [0.01, -0.06],
            "subtitle_source": [0.09, -0.06],
            "countries": ["Brazil", "Paraguay", "Argentina"]
            },
        "europe": {
            "legend": {
                "geometry": [-17.2, 40],
                "label": [-15.5, 40],
                "size": 0.8,
                "spacing": 1.6
            },
            "title": [0.03, -0.05],
            "subtitle": [0.03, -0.06],
            "subtitle_source": [0.1, -0.06],
            "countries": ["Slovenia", "Hungary", "Austria"]
            },
        "western asia": {
            "legend": {
                "geometry": [32.25, 17],
                "label": [33.75, 17],
                "size": 1,
                "spacing": 1.6
            },
            "title": [0.007, -0.03],
            "subtitle": [0.007, -0.04],
            "subtitle_source": [0.09, -0.04],
            "countries": ["Israel", "Georgia", "Jordan"]
            }
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


def do_legend(ax: axes, region: str, map_data):
    """ 
    draw a legend and the title and subtitle
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
    subtitle = legend_area[region]["subtitle"]
    subtitle_source = legend_area[region]["subtitle_source"]


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
    plt.annotate("Data source:",
                 xy=(subtitle[0], subtitle[1]),
                 fontsize=24,
                 xycoords="axes fraction", **fontstyles)
    plt.annotate("naturalearthdata.com and gadebate.un.org",
                 xy=(subtitle_source[0], subtitle_source[1]),
                 fontsize=24,
                 xycoords="axes fraction",
                 color="#1B998B", **fontstyles)
    plt.title(f"UNGA on Ceasefire in Gaza ({region.title()})",
              x=title[0], y=title[1],
              fontsize=42,
              **fontstyles)


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
