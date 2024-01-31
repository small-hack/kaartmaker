Thank you to https://geojson-maps.ash.ms/ for the free GeoJSON data, however it wasn't complete, so then I went to https://www.naturalearthdata.com/

I downloaded the map subunits from:
https://www.naturalearthdata.com/downloads/10m-cultural-vectors/10m-admin-0-details/

Then, I unzipped the zip file and ran the following GDAL command (via docker) to convert shape data to geojson:

```bash
# uses volumes to use local zip file contents and output to local directory outside of container
docker run \
         --volume ./ne_10m_admin_0_map_subunits:/maps \
         --volume ./outputs:/outputs ghcr.io/osgeo/gdal:ubuntu-full-latest \
         ogr2ogr \
           -f GeoJSON \
           -s_srs /maps/ne_10m_admin_0_map_subunits.prj \
           -t_srs EPSG:4326 \
           /outputs/subunits.geojson /maps/ne_10m_admin_0_map_subunits.shp
```

And then I also grabbed disputed areas here:
https://www.naturalearthdata.com/downloads/10m-cultural-vectors/10m-admin-0-breakaway-disputed-areas/


And again with the docker command:
```bash
docker run --volume ./ne_10m_admin_0_disputed_areas:/maps --volume ./outputs:/outputs ghcr.io/osgeo/gdal:ubuntu-full-latest ogr2ogr -f GeoJSON -s_srs /maps/ne_10m_admin_0_disputed_areas.prj -t_srs EPSG:4326 /outputs/disputed.geojson /maps/ne_10m_admin_0_disputed_areas.shp
```

Thanks to this article for helping me understand how to do gdal conversions:
https://lvngd.com/blog/using-ogr2ogr-convert-shapefiles-geojson/
