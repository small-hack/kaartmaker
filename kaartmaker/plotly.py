# plotly stuff taken from their docs
from urllib.request import urlopen
import json
import pandas as pd
import plotly.express as px


URL = 'https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json'
CSV_URL = "https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv"


def plot_stuff():
    with urlopen(URL) as response:
        counties = json.load(response)

    df = pd.read_csv(CSV_URL, dtype={"fips": str})

    fig = px.choropleth(df,
                        geojson=counties,
                        locations='fips',
                        color='unemp',
                        color_continuous_scale="Viridis",
                        range_color=(0, 12),
                        scope="usa",
                        labels={'unemp':'unemployment rate'}
                        )

    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.show()
