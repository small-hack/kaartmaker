#!/bin/bash
# Thanks to this article for helping me understand how to use gdal for shape to geojson conversions:
# https://lvngd.com/blog/using-ogr2ogr-convert-shapefiles-geojson/

# download the map with subunits for countries from naturalearthdata.com
curl -L -o maps.zip https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/10m/cultural/ne_10m_admin_0_map_subunits.zip

# decompress directory
unzip maps.zip -d maps

# run GDAL command (via docker) to convert shape data to geojson
# uses volumes to use local zip file contents and output to local directory outside of container
docker run \
    --volume ./maps:/maps \
    --volume ./geojson:/geojson ghcr.io/osgeo/gdal:ubuntu-full-latest \
    ogr2ogr \
        -f GeoJSON \
        -s_srs /maps/ne_10m_admin_0_map_subunits.prj \
        -t_srs EPSG:4326 \
        /geojson/world_with_countries.geojson \
        /maps/ne_10m_admin_0_map_subunits.shp

# download disputed territories
curl -L -o disputed.zip https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/10m/cultural/ne_10m_admin_0_disputed_areas.zip

# decompress directory
unzip disputed.zip -d disputed

# convert disputed territories map to geojson
docker run \
    --volume ./disputed:/maps \
    --volume ./geojson:/geojson \
    ghcr.io/osgeo/gdal:ubuntu-full-latest \
    ogr2ogr \
        -f GeoJSON \
        -s_srs /maps/ne_10m_admin_0_disputed_areas.prj \
        -t_srs EPSG:4326 \
        /geojson/disputed.geojson \
        /maps/ne_10m_admin_0_disputed_areas.shp

# clean up our mess
rm -rf maps* disputed*
