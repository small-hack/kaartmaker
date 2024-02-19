import os
import shutil
from urllib.request import Request, urlopen
import zipfile
import geopandas as gpd
import logging
from fake_useragent import UserAgent

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def generate_random_user_agent():
    ua = UserAgent()
    return ua.random


def download_and_extract(url, destination):
    logging.info(f"Downloading and extracting {url} to {destination}")

    ua = generate_random_user_agent()

    logging.info(f"Fake User-agent {ua}")
    req = Request(url)
    req.add_header('user-agent', ua)

    os.makedirs(destination, exist_ok=True)  # Ensure destination directory exists

    with urlopen(req) as f:
        zip_file = f.read()
        with open(os.path.join(destination, "temp.zip"), "wb") as temp_zip:
            temp_zip.write(zip_file)
    try:
        with zipfile.ZipFile(os.path.join(destination, "temp.zip"), "r") as zip_ref:
            zip_ref.extractall(destination)
    except zipfile.BadZipFile:
        logging.error("Error: The downloaded file is not a valid zip file.")
    finally:
        if os.path.exists(os.path.join(destination, "temp.zip")):
            os.remove(os.path.join(destination, "temp.zip"))
    logging.info(f"Download and extraction completed for {url}")


def convert_to_geojson(input_shp, output_geojson):
    logging.info(f"Converting {input_shp} to GeoJSON: {output_geojson}")
    # Read the shapefile using geopandas
    gdf = gpd.read_file(input_shp)

    # Write the GeoJSON file
    gdf.to_file(output_geojson, driver='GeoJSON')
    logging.info(f"Conversion to GeoJSON completed for {input_shp}")


def main():
    # Define the urls
    sovereignty_url = "https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/10m/cultural/ne_10m_admin_0_sovereignty.zip"
    maps_url = "https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/10m/cultural/ne_10m_admin_0_map_units.zip"
    sub_maps_url = "https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/10m/cultural/ne_10m_admin_0_map_subunits.zip"
    disputed_url = "https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/10m/cultural/ne_10m_admin_0_disputed_areas.zip"

    # Define the directories for storing GeoJSON files
    xdg_data_home = os.environ.get("XDG_DATA_HOME",
                                   os.path.join(os.path.expanduser("~"), ".local", "share", "kaarmaker"))
    geojson_dir = os.path.join(xdg_data_home, "geojson")

    # Create the GeoJSON directory if it doesn't exist
    os.makedirs(geojson_dir, exist_ok=True)

    # Download and convert sovereignty data
    download_and_extract(sovereignty_url, os.path.join(xdg_data_home, "soverignty"))
    convert_to_geojson(os.path.join(xdg_data_home, "soverignty", "ne_10m_admin_0_sovereignty.shp"),
                       os.path.join(geojson_dir, "world_sovereignty.geojson"))

    # Download and convert map unit data
    download_and_extract(maps_url, os.path.join(xdg_data_home, "maps"))
    convert_to_geojson(os.path.join(xdg_data_home, "maps", "ne_10m_admin_0_map_units.shp"),
                       os.path.join(geojson_dir, "world.geojson"))

    # Download and convert subunit map data
    download_and_extract(sub_maps_url, os.path.join(xdg_data_home, "sub_maps"))
    convert_to_geojson(os.path.join(xdg_data_home, "sub_maps", "ne_10m_admin_0_map_subunits.shp"),
                       os.path.join(geojson_dir, "world_subunits.geojson"))

    # Download and convert disputed territories data
    download_and_extract(disputed_url, os.path.join(xdg_data_home, "disputed"))
    convert_to_geojson(os.path.join(xdg_data_home, "disputed", "ne_10m_admin_0_disputed_areas.shp"),
                       os.path.join(geojson_dir, "disputed.geojson"))

    # Clean up temporary directories
    shutil.rmtree(os.path.join(xdg_data_home, "soverignty"))
    shutil.rmtree(os.path.join(xdg_data_home, "maps"))
    shutil.rmtree(os.path.join(xdg_data_home, "sub_maps"))
    shutil.rmtree(os.path.join(xdg_data_home, "disputed"))


if __name__ == "__main__":
    main()
