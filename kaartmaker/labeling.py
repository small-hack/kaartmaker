from matplotlib.patches import Polygon
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


def do_legend(ax, continent, map_data):
    legend = pd.concat([map_data[map_data.NAME_EN.isin([
        "France", "Spain", "Germany"
        ])]
    ])

    legend = legend.sort_values("color")

    for i, row in legend.reset_index().iterrows():
        ax = draw_legend_geometry(ax, row, -25, -20 - 3.5*i, 2.5)
        ax.annotate(row.color[3:],
                    (-22, -20 - 3.5*i),
                    fontsize=28,
                    fontweight="bold",
                    va="center")

    fontstyles = {"fontweight": "bold", "ha": "left"}
    plt.annotate("Data source:",
                 xy=(0.05, 0.32),
                 fontsize=24,
                 xycoords="axes fraction",
                 **fontstyles)
    plt.annotate("naturalearthdata.com and gadebate.un.org",
                 xy=(0.133, -0.32),
                 fontsize=24,
                 xycoords="axes fraction",
                 color="#1B998B",
                 **fontstyles)
    plt.title(f"UN votes on Ceasefire in Gaza in {continent}",
              x=0.05,
              y=0.29,
              fontsize=42,
              **fontstyles)


def draw_legend_geometry(ax, row, x_loc, y_loc, height):
    x = np.array(row.geometry.boundary.coords.xy[0])
    y = np.array(row.geometry.boundary.coords.xy[1])
    
    x = x - (row.geometry.centroid.x - x_loc)
    y = y - (row.geometry.centroid.y - y_loc)
    
    ratio = height / (y.max() - y.min())
    x = x * ratio + (x_loc - x_loc * ratio)
    y = y * ratio + (y_loc - y_loc * ratio)
    
    ax.add_artist(Polygon(np.stack([x, y], axis=1),
                          facecolor=row.color,
                          edgecolor=row.edgecolor,
                          hatch=row.hatch))
