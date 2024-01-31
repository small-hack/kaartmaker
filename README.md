Thank you to https://geojson-maps.ash.ms/ for the free GeoJSON data, however it wasn't complete, so then I went to https://www.naturalearthdata.com/

GDAL docker command to convert shape data to geojson:

```bash
docker run \
         --volume ./ne_10m_admin_0_map_subunits:/maps \
         --volume ./outputs:/outputs ghcr.io/osgeo/gdal:ubuntu-full-latest \
         ogr2ogr \
           -f GeoJSON \
           -s_srs /maps/ne_10m_admin_0_map_subunits.prj \
           -t_srs EPSG:4326 \
           /outputs/subunits.geojson /maps/ne_10m_admin_0_map_subunits.shp
```

Thanks to this article for helping me understand how to do gdal conversions:
https://lvngd.com/blog/using-ogr2ogr-convert-shapefiles-geojson/
