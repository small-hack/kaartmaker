from importlib.metadata import version as get_version
from json import load
from os import path

# path the script is running from
PWD = path.dirname(__file__)
# version of kaartmaker
VERSION = get_version('kaartmaker')

# world using units
WORLD_UNITS_JSON = path.join(PWD, 'geojson/world.geojson')

# world with sub units
WORLD_SUBUNITS_JSON = path.join(PWD, 'geojson/world_subunits.geojson')

# world disputed areas
DISPUTED_JSON = path.join(PWD, 'geojson/disputed.geojson')

with open(path.join(PWD, 'config/boundaries.json')) as json_data:
    COUNTRY_BOUNDARIES = load(json_data)

with open(path.join(PWD, 'config/legend.json')) as json_data:
    LEGEND = load(json_data)

with open(path.join(PWD, 'config/country_labels.json')) as json_data:
    LABELS = load(json_data)
