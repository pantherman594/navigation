#!/bin/bash

rm MBTA_GTFS.zip
wget https://cdn.mbta.com/MBTA_GTFS.zip

rm mass.pbf
wget http://download.geofabrik.de/north-america/us/massachusetts-latest.osm.pbf
osmconvert massachusetts-latest.osm.pbf -b=41.76,-72.05,42.81,-70.45 --complete-ways -o=mass.pbf
rm massachusetts-latest.osm.pbf
