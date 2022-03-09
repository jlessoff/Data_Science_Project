from sodapy import Socrata
import pandas as pd
from textwrap import wrap
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from secret import app_token,username,password
import folium
from folium.plugins import HeatMap



#create a function to make grade proxy; this is based on ny grading standards. to capture overall performance of restaurant
def func(a_):
    if a_<=13:
        return 'A_rep'
    elif 13< a_<= 27:
        return 'B_rep'
    elif a_ > 27:
        return 'C_rep'

#read in mapping zip code file
neighborhood=pd.read_csv('nyc-zip-codes.csv')

#connect to API for open data
client = Socrata("data.cityofnewyork.us",
                 app_token=app_token,
                 username=username,
                 password=password)

#query to get all violation data; limit necessary and set to400,000, as data set contains under 400,000 observaitons
results = client.get("43nn-pn8j", select='date_trunc_ymd(inspection_date),dba,zipcode,camis,cuisine_description,violation_code,grade,violation_description,score, critical_flag,inspection_type,latitude,longitude', limit=400000)

# Convert to pandas DataFrame
results_df = pd.DataFrame.from_records(results)
results_df = results_df.rename(columns={'date_trunc_ymd_inspection_date': 'inspection_date'}, index={'ONE': 'Row_1'})
#create date variable
results_df['inspection_date']= pd.to_datetime(results_df['inspection_date'])
#clean data and drop missing values
results_df['zipcode'] = pd.to_numeric(results_df.zipcode.astype(str).str.replace(',',''), errors='coerce').dropna().astype(int)
neighborhood['zip_code'] = neighborhood['zip_code'].astype(int)
neighborhood['zip_code'] = neighborhood['zip_code'].astype(int)
results_df = pd.merge(results_df, neighborhood, how="left", left_on='zipcode',right_on='zip_code')
results_df =results_df[(results_df['zipcode'] > 0 )]
#get violation codes that are not as granular
results_df['violation_code'] = results_df['violation_code'].str[:2]
results_df['violation_code']=results_df['violation_code'].dropna().astype(int)
#make sure that the years are 2019,2020,2021
results_df =results_df[(results_df['inspection_date'].dt.year > 2018  )]
results_df =results_df[(results_df['inspection_date'].dt.year < 2022)]
results_df['score']=results_df['score'].dropna().astype(int)
results_df=results_df.dropna()
#apply function to score to get grade proxy
results_df1=results_df.groupby(['camis','inspection_date']).score.mean().reset_index()
results_df1['c'] = results_df1[['score']].apply(lambda x: func(x[0]), axis=1)
results_df1=results_df1.drop(columns=['score',])
results_df = pd.merge(results_df, results_df1, how="left", on=['camis','inspection_date'])

print(results_df.columns)



#create categories for cuisine description
results_df['cuisine_description'] = results_df['cuisine_description'].replace(
    to_replace=['Middle Eastern', 'Moroccan', 'Tapas', 'Spanish', 'Greek',
                'Armenian', 'Basque', 'Afghan', 'Iranian',
                'Turkish'],
                value='Mediterranean')

results_df['cuisine_description'] = results_df['cuisine_description'].replace(
    to_replace=[ 'Scandinavian', 'Czech', 'English', 'German',
                'Portuguese', 'Russian', 'Polish', 'Continental', 'Irish',
                'French','New French','Eastern European'], value='European')

results_df['cuisine_description'] = results_df['cuisine_description'].replace(
    to_replace=['Pizza/Italian'], value='Pizza')

results_df['cuisine_description'] = results_df['cuisine_description'].replace(
    to_replace=['Chinese', 'Japanese','Chinese/Japanese', 'Filipino', 'Indian',
                'Indonesian', 'Bangladeshi','Thai', 'Korean', 'Chinese/Cuban',
                'Vietnamese/Cambodian/Malaysia','Asian/Asian Fusion','Southeast Asian','Pakistani'], value='Asian')

results_df['cuisine_description'] = results_df['cuisine_description'].replace(
    to_replace=['Bottled beverages, including water, sodas, juices, etc.',
                'Café/Coffee/Tea'], value='Beverages')

results_df['cuisine_description'] = results_df['cuisine_description'].replace(
    to_replace=['Bagels/Pretzels', 'Donuts'], value='BakedGoods')

results_df['cuisine_description'] = results_df['cuisine_description'].replace(
    to_replace=['Chilean','Peruvian', 'Caribbean', 'Brazilian',
                'Latin (Cuban, Dominican, Puerto Rican, South & Central American)','Latin American'],
                value='Latin')

results_df['cuisine_description'] = results_df['cuisine_description'].replace(
    to_replace=['Ice Cream, Gelato, Yogurt, Ices','Seafood', 'Chicken',
                'Nuts/Confectionary', 'Hotdogs/Pretzels', 'Hotdogs',
                'Fruits/Vegetables', 'Vegetarian', 'Salads',
                'Steak', 'Juice, Smoothies, Fruit Salads',
                'Pancakes/Waffles','Vegan',  'Jewish/Kosher'], value='Specialty')

results_df['cuisine_description'] = results_df['cuisine_description'].replace(
    to_replace=['Sandwiches', 'Soups', 'Soup/Sandwiches','Soups/Salads/Sandwiches'],
                value='SoupsSandwiches')

results_df['cuisine_description'] = results_df['cuisine_description'].replace(
    to_replace=['Delicatessen', 'Sandwiches/Salads/Mixed Buffet'],
                value='DeliBuffett')

results_df['cuisine_description'] = results_df['cuisine_description'].replace(
    to_replace=['Soul Food', 'Californian', 'Creole/Cajun', 'Cajun',
                'Creole', 'Barbecue', 'Tex-Mex', 'Southwestern', 'Hamburgers','Hawaiian','New American'],
                value='American')
results_df['cuisine_description'] = results_df['cuisine_description'].replace(
    to_replace=['Coffee/Tea','Bakery Products/Desserts','Bottled Beverages'], value='Coffee Tea Beverages')

results_df['cuisine_description'] = results_df['cuisine_description'].replace(
    to_replace=['Egyptian','African','Ethiopian'], value='African')

results_df['cuisine_description'] = results_df['cuisine_description'].replace(
    to_replace=['Listed/Not Applicable','Not Listed/Not Applicable'], value='Other')


###SCORE distribution generally
fig, ax = plt.subplots()
sns.kdeplot(results_df["score"], shade=True, ax=ax)
ax.legend()
fig.suptitle("Health Inspection Violations Density")
plt.xlim(0, 80)



#get distribution of grade PROXY by cuisine type
cuisines = results_df.groupby('cuisine_description').camis.count().reset_index().sort_values(by = 'camis', ascending=False)
cuisines_desc = list(cuisines.head(15)['cuisine_description'])
cuisinegrade = results_df[['cuisine_description', 'c','score']]
cuisinegrade = cuisinegrade[cuisinegrade['cuisine_description'].isin(cuisines_desc)]
cuisinegrade = cuisinegrade[cuisinegrade.c.isin(['A_rep', 'B_rep', 'C_rep'])]
cuisinegrade = cuisinegrade.reset_index().drop('index', axis=1)
pd.set_option('display.max_colwidth', 50)
cg = pd.crosstab(cuisinegrade['cuisine_description'], cuisinegrade.c).sort_values(by='A_rep', ascending=False)
cgdensity = cg.apply(lambda r: r/r.sum(), axis=1)
cgdensity = cgdensity.sort_values(by='A_rep')
cglabels = list(cgdensity.index)
cglabels = [ '\n'.join(wrap(l, 20)) for l in cglabels ]
cgdensity.plot(kind='barh', stacked='True', mark_right=True, figsize = (10,8), color=['b','g','r'])
plt.ylabel('')
plt.xlim(0, 1.15)

plt.xlabel('Percentage of restaurants')
plt.title('Grade dist')
plt.savefig('gradebycuisine.png')

##get score distribution for individual cuisine type top 20 cuisines
cuisinegrade['score']=cuisinegrade['score'].astype(int)
mean=[]
median=[]
twenty=cuisinegrade['cuisine_description'].value_counts().index
rows = []
for i in range(0,15):
    score=cuisinegrade.loc[cuisinegrade['cuisine_description']==twenty[i]]['score']
    mean=round(np.mean(score),1)
    median=round(np.median(score),1)
    name=twenty[i][:15]
    rows.append([name, mean, median])
    plt.hist(score,label=name,bins=int(np.max(score.values)/2))
    plt.title(f'Score distribution for {twenty[i][:15]} restaurants')
    plt.axvline(x=median, color='r', label=f'Median = {median}', )
    plt.axvline(x=mean, color='g', label=f'Median = {mean}', )
    plt.savefig(twenty[i]+'scoredistribution.png')

    plt.show()


df = pd.DataFrame(rows, columns=["Name", "Mean", "Median"])



#CREATE NYC RESTAURANT MAP
# results_df=results_df.dropna()
# nyc = [40.742, -73.956]
# lat = results_df.latitude.tolist()
# lng = results_df.longitude.tolist()

#COLOR BASED ON GRADE
# color_dict = {'A_rep': 'grey', 'B_rep': 'yellow', 'C_rep': 'red'}
# map_NM = folium.Map(location=nyc,
#                     zoom_start=11,
#                     tiles='openstreetmap',
#                     control_scale=True)
#
# for lat, lng, grade in zip(results_df['latitude'],
#                             results_df['longitude'],
#                             results_df['c'], ):
#     label = '{}'.format(grade)
#     label = folium.Popup(label, parse_html=True)
#     folium.CircleMarker([lat, lng],
#                         radius=1,
#                         popup=label,
#                         color=[color_dict.get(grade)],
#                         fill=True,
#                         fill_color='#3186cc',
#                         fill_opacity=0.7,
#                         parse_html=False).add_to(map_NM)

# map_NM.save('restaurantmap.html')

#heat map of a restaurant
results_df1=results_df[['latitude','longitude','c']]
results_df1 = results_df1.loc[(results_df1.c == "A_rep")]
map_nm = folium.Map(location=[40.742, -73.956], zoom_start=11)
HeatMap(data=results_df1[['latitude','longitude']].groupby(['latitude','longitude']).count().reset_index().values.tolist(), radius=7, max_zoom=10).add_to(map_nm)
map_nm.save('A_heat_map.html')

#heat map of b restaurant

results_df1=results_df[['latitude','longitude','c']]
results_df1 = results_df1.loc[(results_df1.c == "B_rep")]
map_nm = folium.Map(location=[40.742, -73.956], zoom_start=11)
HeatMap(data=results_df1[['latitude','longitude']].groupby(['latitude','longitude']).count().reset_index().values.tolist(), radius=7, max_zoom=10).add_to(map_nm)
map_nm.save('B_heat_map.html')

#heat map of c restaurant

results_df1=results_df[['latitude','longitude','c']]
results_df1 = results_df1.loc[(results_df1.c == "C_rep")]
map_nm = folium.Map(location=[40.742, -73.956], zoom_start=11)
HeatMap(data=results_df1[['latitude','longitude']].groupby(['latitude','longitude']).count().reset_index().values.tolist(), radius=7, max_zoom=10).add_to(map_nm)
map_nm.save('C_heat_map.html')





