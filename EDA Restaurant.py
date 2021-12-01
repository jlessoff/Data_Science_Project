import pandas as pd
from Restaurants import results_df
from textwrap import wrap
import matplotlib.pyplot as plt


#get distribution of grade by cuisine type
print(len(results_df))
cuisines = results_df.groupby('cuisine_description').camis.count().reset_index().sort_values(by = 'camis', ascending=False)
cuisines_desc = list(cuisines.head(20)['cuisine_description'])
print(cuisines_desc)
cuisinegrade = results_df[['cuisine_description', 'grade']]

cuisinegrade = cuisinegrade[cuisinegrade['cuisine_description'].isin(cuisines_desc)]
print(len(cuisinegrade))
cuisinegrade = cuisinegrade[cuisinegrade.grade.isin(['A', 'B', 'C'])]
cuisinegrade = cuisinegrade.reset_index().drop('index', axis=1)
pd.set_option('display.max_colwidth', 50)
cg = pd.crosstab(cuisinegrade['cuisine_description'], cuisinegrade.grade).sort_values(by='A', ascending=False)

print(cg)
print(len(cg))
cgdensity = cg.apply(lambda r: r/r.sum(), axis=1)
cgdensity = cgdensity.sort_values(by='A')
cglabels = list(cgdensity.index)
cglabels = [ '\n'.join(wrap(l, 20)) for l in cglabels ]

cgdensity.plot(kind='barh', stacked='True', mark_right=True, figsize = (10,8), color=['b','g','r'])
plt.ylabel('')
plt.xlim(0, 1.15)
plt.xlabel('Percentage of restaurants')
plt.title('Grade distribution across top 10 cuisine types')

plt.show()