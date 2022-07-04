import pandas as pd
from Restaurants import results_df
from textwrap import wrap
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
###SCORE
fig, ax = plt.subplots()

sns.kdeplot(results_df["score"], shade=True, ax=ax)
ax.legend()

fig.suptitle("Health Inspection Violations Density")

plt.show()


###CUISINE
pd.set_option('display.max_columns', None)
#

# #

results_df['cuisine_description'] = results_df['cuisine_description'].replace(
    to_replace=['Middle Eastern', 'Moroccan', 'Tapas', 'Spanish', 'Greek',
                'Armenian', 'Basque', 'Afghan', 'Iranian',
                'Turkish'],
                value='Mediterranean')

results_df['cuisine_description'] = results_df['cuisine_description'].replace(
    to_replace=[ 'Scandinavian', 'Czech', 'English', 'German',
                'Portuguese', 'Russian', 'Polish', 'Continental', 'Irish',
                'French','Eastern European'], value='European')

results_df['cuisine_description'] = results_df['cuisine_description'].replace(
    to_replace=['Pizza/Italian'], value='Pizza')

results_df['cuisine_description'] = results_df['cuisine_description'].replace(
    to_replace=['Chinese', 'Japanese','Chinese/Japanese', 'Filipino', 'Indian',
                'Indonesian', 'Bangladeshi','Thai', 'Korean', 'Chinese/Cuban',
                'Vietnamese/Cambodian/Malaysia'], value='Asian')

results_df['cuisine_description'] = results_df['cuisine_description'].replace(
    to_replace=['Bottled beverages, including water, sodas, juices, etc.',
                'Café/Coffee/Tea'], value='Beverages')

results_df['cuisine_description'] = results_df['cuisine_description'].replace(
    to_replace=['Bagels/Pretzels', 'Donuts'], value='Baked Goods')

results_df['cuisine_description'] = results_df['cuisine_description'].replace(
    to_replace=['Chilean','Peruvian', 'Caribbean', 'Brazilian',
                'Latin (Cuban, Dominican, Puerto Rican, South & Central American)'],
                value='Latin/Caribbean')

results_df['cuisine_description'] = results_df['cuisine_description'].replace(
    to_replace=['Ice Cream, Gelato, Yogurt, Ices','Seafood', 'Chicken',
                'Nuts/Confectionary', 'Hotdogs/Pretzels', 'Hotdogs',
                'Fruits/Vegetables', 'Vegetarian', 'Salads',
                'Steak', 'Juice, Smoothies, Fruit Salads',
                'Pancakes/Waffles','Vegan',  'Jewish/Kosher'], value='Specialty')

results_df['cuisine_description'] = results_df['cuisine_description'].replace(
    to_replace=['Sandwiches', 'Soups', 'Soup/Sandwiches'],
                value='Soups & Sandwiches')

results_df['cuisine_description'] = results_df['cuisine_description'].replace(
    to_replace=['Delicatessen', 'Sandwiches/Salads/Mixed Buffet'],
                value='Deli/Buffett')

results_df['cuisine_description'] = results_df['cuisine_description'].replace(
    to_replace=['Soul Food', 'Californian', 'Creole/Cajun', 'Cajun',
                'Creole', 'Barbecue', 'Tex-Mex', 'Southwestern', 'Hamburgers','Hawaiian'],
                value='American')


#get distribution of grade PROXY by cuisine type
cuisines = results_df.groupby('cuisine_description').camis.count().reset_index().sort_values(by = 'camis', ascending=False)
cuisines_desc = list(cuisines.head(30)['cuisine_description'])
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

##get score distribution for individual cuisine type
cuisinegrade['score']=cuisinegrade['score'].astype(int)
mean=[]
median=[]
twenty=cuisinegrade['cuisine_description'].value_counts().index
rows = []
for i in range(0,20):
    score=cuisinegrade.loc[cuisinegrade['cuisine_description']==twenty[i]]['score']
    mean=round(np.mean(score),1)
    median=round(np.median(score),1)
    name=twenty[i][:15]
    rows.append([name, mean, median])
    plt.hist(score,label=name,bins=int(np.max(score.values)/2))
    plt.title(f'Score distribution for {twenty[i][:15]} restaurants')
    plt.axvline(x=median, color='r', label=f'Median = {median}', )
    plt.axvline(x=mean, color='g', label=f'Median = {mean}', )
    plt.savefig(i+'scoredistribution.png')
df = pd.DataFrame(rows, columns=["Name", "Mean", "Median"])

##density
ig, ax = plt.subplots()
sns.kdeplot(results_df["score"], shade=True, ax=ax)
ax.legend()
fig.suptitle("Health Inspection Violations Density")
plt.savefig('healthinspectiondensity.png')




