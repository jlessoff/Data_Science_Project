import folium
from folium.plugins import HeatMap
from Rodents import rodent



map_osm = folium.Map(location=[40.742, -73.956], zoom_start=11)

HeatMap(data=rodent[['latitude','longitude']].groupby(['latitude','longitude']).count().reset_index().values.tolist(), radius=7, max_zoom=10).add_to(map_osm)

map_osm.save('aee.html')
