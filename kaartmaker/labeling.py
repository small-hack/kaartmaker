from matplotlib.patches import Polygon
from matplotlib import axes
import matplotlib.patheffects as PathEffects
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

legend_area = {
        "europe": {
            "legend_geometry": [-17.2, 40],
            "legend": [-15.5, 40],
            "title": [0.03, -0.05],
            "subtitle": [0.03, -0.06],
            "subtitle_source": [0.1, -0.06],
            "countries": ["Slovenia", "Hungary", "Austria"]
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

def do_legend(ax: axes, continent: str, map_data):
    """ 
    draw a legend and the title and subtitle
    """
    # specific locations for this region
    legend_xy = legend_area[continent]["legend_geometry"]
    legend_title_xy = legend_area[continent]["legend"]
    title = legend_area[continent]["title"]
    subtitle = legend_area[continent]["subtitle"]
    subtitle_source = legend_area[continent]["subtitle_source"]
    countries = legend_area[continent]['countries']

    # use special countries for this area 
    legend = pd.concat([map_data[map_data.NAME_EN.isin(countries)]])
    legend = legend.sort_values("color")

    for i, row in legend.reset_index().iterrows():
        draw_legend_geometry(ax, row, legend_xy[0], legend_xy[1] - 1.6*i, 0.8)
        ax.annotate(row.vote,
                    (legend_title_xy[0], legend_title_xy[1] - 1.6*i),
                    fontsize=24,
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
    plt.title(f"UNGA on Ceasefire in Gaza {continent}",
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
    """
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
