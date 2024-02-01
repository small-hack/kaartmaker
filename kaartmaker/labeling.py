from matplotlib.patches import Polygon
import matplotlib.patheffects as PathEffects
import matplotlib.pyplot as plt
import numpy as np


country_labels = {
        "Europe": [
    {"label": "Albania", "coordinates": (20.16, 40.73), "font_size": 18},
    {"label": "Austria", "coordinates": (14.65, 47.58)},
    {"label": "Czechia", "coordinates": (14.71, 49.84)},
    {"label": "Croatia", "coordinates": (16.76, 45.57), "font_size": 22},
    {"label": "Belarus", "coordinates": (27.53, 53.45), "font_size": 28},
    {"label": "Belgium", "coordinates": (4.27, 50.51), "font_size": 22},
    {"label": "Bosnia\nand\nHertzegovina", "coordinates": (17.64, 44.18), "font_size": 16},
    {"label": "Estonia", "coordinates": (25.58, 58.82)},
    {"label": "Bulgaria", "coordinates": (24.61, 42.58)},
    {"label": "Denmark", "coordinates": (9.16, 56.1)},
    {"label": "Finland", "coordinates": (25.56, 62.38), "font_size": 28},
    {"label": "France", "coordinates": (2.4, 46.8), "font_size": 32},
    {"label": "Greece", "coordinates": (21.83, 39.69), "font_size": 22},
    {"label": "Germany", "coordinates": (9.8, 51.3), "font_size": 28},
    {"label": "Hungary", "coordinates": (19.10, 47.06)},
    {"label": "Iceland", "coordinates": (-18.0, 63.92)},
    {"label": "Ireland", "coordinates": (-8.0, 53.7)},
    {"label": "Italy", "coordinates": (12.3, 42.9), "font_size": 28},
    {"label": "Latvia", "coordinates": (25.26, 56.7)},
    {"label": "Lithuania", "coordinates": (23.91, 55.38)},
    {"label": "Poland", "coordinates": (19.2, 52.2), "font_size": 28},
    {"label": "Portugal", "coordinates": (-8.61, 40.061)},
    {"label": "Moldova", "coordinates": (28.6, 47.17), "font_size": 18},
    {"label": "Montenegro", "coordinates": (19.25, 42.7), "font_size": 18},
    {"label": "Netherlands", "coordinates": (5.45, 52.33), "font_size": 18},
    {"label": "Norway", "coordinates": (9.56, 61.15), "font_size": 28},
    {"label": "North\nMacedonia", "coordinates": (21.61, 41.64), "font_size": 16},
    {"label": "Romania", "coordinates": (24.86, 45.95), "font_size": 28},
    {"label": "Russia", "coordinates": (34.38, 55.0), "font_size": 32},
    {"label": "Serbia", "coordinates": (20.89, 43.61)},
    {"label": "Slovakia", "coordinates": (19.23, 48.74), "font_size": 22},
    {"label": "Slovenia", "coordinates": (14.58, 46.12), "font_size": 18},
    {"label": "Spain", "coordinates": (-3.7, 40.5), "font_size": 32},
    {"label": "Switzerland", "coordinates": (8.06, 46.79), "font_size": 18},
    {"label": "Sweden", "coordinates": (15.184, 59.82), "font_size": 28},
    {"label": "Ukraine", "color": "", "coordinates": (31.06, 49.36), "font_size": 28},
    {"label": "United\nKingdom", "coordinates": (-1.37, 52.83)}
    ]
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
    """
    # if font_size, not set in dict, use default from args
    font_size = label.get("font_size", default_font_size)
    # if font_color, not set in dict, use default from args
    font_color = label.get("font_color", default_font_color)
    # if font_weight, not set in dict, use default from args
    font_weight = label.get("font_weight", default_font_weight)

    annotation = plt.annotate(
        label["label"], 
        xy=label["coordinates"] if "xypin" not in label.keys() else label["xypin"], 
        xytext=None if "xypin" not in label.keys() else label["coordinates"], 
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
