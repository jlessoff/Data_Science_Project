import folium
from folium.plugins import HeatMap
from Restaurants import results_df
import branca.colormap as cm



results_df=results_df.dropna()
nyc = [40.742, -73.956]

lat = results_df.latitude.tolist()
lng = results_df.longitude.tolist()

color_dict = {'A_rep': 'green', 'B_rep': 'yellow', 'C_rep': 'red'}




map_NM = folium.Map(location=nyc,
                    zoom_start=11,
                    tiles='openstreetmap',
                    control_scale=True)

for lat, lng, grade in zip(results_df['latitude'],
                            results_df['longitude'],
                            results_df['c'], ):
    label = '{}'.format(grade)
    label = folium.Popup(label, parse_html=True)
    folium.CircleMarker([lat, lng],
                        radius=1,
                        popup=label,
                        color=[color_dict.get(grade)],
                        fill=True,
                        fill_color='#3186cc',
                        fill_opacity=0.7,
                        parse_html=False).add_to(map_NM)

map_NM.save('oee.html')
