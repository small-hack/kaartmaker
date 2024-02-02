from matplotlib.patches import Polygon
import matplotlib.patheffects as PathEffects
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


country_labels = {
        "Europe": [
    {"label": "Albania", "xytext": (20.16, 40.73), "font_size": 18},
    {"label": "Austria", "xytext": (14.65, 47.58)},
    {"label": "Czechia", "xytext": (14.71, 49.84)},
    {"label": "Croatia", "xytext": (16.76, 45.57), "font_size": 22},
    {"label": "Belarus", "xytext": (27.53, 53.45), "font_size": 28},
    {"label": "Belgium", "xytext": (4.27, 50.51), "font_size": 22},
    {"label": "Bosnia\nand\nHertzegovina", "xytext": (17.64, 44.18), "font_size": 16},
    {"label": "Estonia", "xytext": (25.58, 58.82)},
    {"label": "Bulgaria", "xytext": (24.61, 42.58)},
    {"label": "Denmark", "xytext": (9.16, 56.1)},
    {"label": "Finland", "xytext": (25.56, 62.38), "font_size": 28},
    {"label": "France", "xytext": (2.4, 46.8), "font_size": 32},
    {"label": "Greece", "xytext": (21.83, 39.69), "font_size": 22},
    {"label": "Germany", "xytext": (9.8, 51.3), "font_size": 28},
    {"label": "Hungary", "xytext": (19.10, 47.06)},
    {"label": "Iceland", "xytext": (-18.0, 63.92)},
    {"label": "Ireland", "xytext": (-8.0, 53.7)},
    {"label": "Italy", "xytext": (12.3, 42.9), "font_size": 28},
    {"label": "Latvia", "xytext": (25.26, 56.7)},
    {"label": "Lithuania", "xytext": (23.91, 55.38)},
    {"label": "Poland", "xytext": (19.2, 52.2), "font_size": 28},
    {"label": "Portugal", "xytext": (-8.61, 40.061)},
    {"label": "Moldova", "xytext": (28.6, 47.17), "font_size": 18},
    {"label": "Montenegro", "xytext": (19.25, 42.7), "font_size": 18},
    {"label": "Netherlands", "xytext": (5.45, 52.33), "font_size": 18},
    {"label": "Norway", "xytext": (9.56, 61.15), "font_size": 28},
    {"label": "North\nMacedonia", "xytext": (21.61, 41.64), "font_size": 16},
    {"label": "Romania", "xytext": (24.86, 45.95), "font_size": 28},
    {"label": "Russia", "xytext": (34.38, 55.0), "font_size": 32},
    {"label": "Serbia", "xytext": (20.89, 43.61)},
    {"label": "Slovakia", "xytext": (19.23, 48.74), "font_size": 22},
    {"label": "Slovenia", "xytext": (14.58, 46.12), "font_size": 18},
    {"label": "Spain", "xytext": (-3.7, 40.5), "font_size": 32},
    {"label": "Switzerland", "xytext": (8.06, 46.79), "font_size": 18},
    {"label": "Sweden", "xytext": (15.184, 59.82), "font_size": 28},
    {"label": "Ukraine", "color": "", "xytext": (31.06, 49.36), "font_size": 28},
    {"label": "United\nKingdom", "xytext": (-1.37, 52.83)}
    ],
        "Africa": [
    {"label": "Algeria", "xytext": (2.0, 27.5)},
    {"label": "Angola", "xytext": (17.7, -13.1)},
    {"label": "Benin", "xytext": (3.2, 5.4), "xypin": (2.3, 7.6)},
    {"label": "Botswana", "xytext": (24.4, -22.3)},
    {"label": "Burkina\nFaso", "xytext": (-1.4, 12.6)},
    {"label": "Burundi", "xytext": (43.3, -4.9), "xypin": (29.8, -3.6)},
    {"label": "Cameroon", "xytext": (12.5, 5.2)},
    {"label": "Cape Verde", "xytext": (-23.7, 19), "xypin": (-23.7, 16)},
    {"label": "Central African\nRepublic", "xytext": (21.1, 6.5)},
    {"label": "Chad", "xytext": (18.5, 16.0)},
    {"label": "Comoros", "xytext": (46.8, -9.6), "xypin": (43.3, -11.7)},
    {"label": "Cote\nd'Ivoire", "xytext": (-5.5, 8.5)},
    {"label": "Democratic\nRepublic of\nthe Congo", "xytext": (23.3, -2.7)},
    {"label": "Djibouti", "xytext": (47.0, 13.4), "xypin": (43.0, 12.2)},
    {"label": "Egypt", "xytext": (29.2, 26.6)},
    {"label": "Equatorial\nGuinea", "xytext": (5.9, -2.5), "xypin": (10.5, 1.6)},
    {"label": "Eritrea", "xytext": (43.0, 16.9), "xypin": (38.5, 16.2)},
    {"label": "Lesotho", "xytext": (35.0, -31.0), "xypin": (28.4, -29.5)},
    {"label": "Ethiopia", "xytext": (39.9, 8.5)},
    {"label": "Gabon", "xytext": (11.8, -0.7)},
    {"label": "Ghana", "xytext": (-1.3, 6.6)},
    {"label": "Guinea", "xytext": (-11.6, 11.0)},
    {"label": "Guinea-\nBissau", "xytext": (-20.3, 10.3), "xypin": (-14.5, 12.2)},
    {"label": "Kenya", "xytext": (37.9, 0.5)},
    {"label": "Eswantini", "xytext": (35.5, -29.3), "xypin": (31.5, -26.8)},
    {"label": "Liberia", "xytext": (-10.6, 3.6), "xypin": (-9.6, 6.7)},
    {"label": "Libya", "xytext": (17.5, 27.5)},
    {"label": "Madagascar", "xytext": (46.7, -19.6)},
    {"label": "Malawi", "xytext": (38.9, -21.3), "xypin": (35.0, -15.6)},
    {"label": "Mali", "xytext": (-1.9, 17.8)},
    {"label": "Mauritania", "xytext": (-11.1, 19.6)},
    {"label": "Morocco", "xytext": (-6.9, 31.3)},
    {"label": "Mozambique", "xytext": (40.8, -15.2)},
    {"label": "Namibia", "xytext": (17.3, -20.7)},
    {"label": "Niger", "xytext": (9.8, 17.5)},
    {"label": "Nigera", "xytext": (7.8, 9.8)},
    {"label": "Republic of\nthe Congo", "xytext": (7.8, -7.2), "xypin": (12.0, -4.1)},
    {"label": "Rwanda", "xytext": (43.8, -3.6), "xypin": (30.1, -2.0)},
    {"label": "São Tomé and\nPríncipe", "xytext": (-0.9, 0.2), "xypin": (6.8, 0.2)},
    {"label": "Senegal", "xytext": (-15.0, 14.7)},
    {"label": "Seychelles", "xytext": (55.6, -2), "xypin": (55.6, -4.5)},
    {"label": "Sierra Leone", "xytext": (-16.4, 6.3), "xypin": (-12.0, 8.5)},
    {"label": "Somalia", "xytext": (45.7, 2.7)},
    {"label": "South\nAfrica", "xytext": (22.4, -31.0)},
    {"label": "South\nSudan", "xytext": (30.2, 7.0)},
    {"label": "Sudan", "xytext": (29.7, 16.0)},
    {"label": "Tanzania", "xytext": (35.0, -6.7)},
    {"label": "The\nGambia", "xytext": (-20.3, 13.6), "xypin": (-15.4, 13.6)},
    {"label": "Togo", "xytext": (1.0, 4.1), "xypin": (1.0, 7.5)},
    {"label": "Tunisia", "xytext": (9.3, 38.9), "xypin": (9.3, 35.7)},
    {"label": "Uganda", "xytext": (32.6, 0.9)},
    {"label": "Zambia", "xytext": (26.1, -14.9)},
    {"label": "Zimbawe", "xytext": (29.7, -19.1)}
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
