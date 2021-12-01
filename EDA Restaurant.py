import pandas as pd
from Restaurants import results_df
from textwrap import wrap
import matplotlib.pyplot as plt
import numpy as np
pd.set_option('display.max_columns', None)

#get distribution of grade by cuisine type
# print(len(results_df))
cuisines = results_df.groupby('cuisine_description').camis.count().reset_index().sort_values(by = 'camis', ascending=False)
cuisines_desc = list(cuisines.head(30)['cuisine_description'])
cuisinegrade = results_df[['cuisine_description', 'grade','score']]

cuisinegrade = cuisinegrade[cuisinegrade['cuisine_description'].isin(cuisines_desc)]
# print(len(cuisinegrade))
cuisinegrade = cuisinegrade[cuisinegrade.grade.isin(['A', 'B', 'C'])]
cuisinegrade = cuisinegrade.reset_index().drop('index', axis=1)
pd.set_option('display.max_colwidth', 50)
cg = pd.crosstab(cuisinegrade['cuisine_description'], cuisinegrade.grade).sort_values(by='A', ascending=False)

#print(cg)
# print(len(cg))
cgdensity = cg.apply(lambda r: r/r.sum(), axis=1)
cgdensity = cgdensity.sort_values(by='A')
cglabels = list(cgdensity.index)
cglabels = [ '\n'.join(wrap(l, 20)) for l in cglabels ]

# cgdensity.plot(kind='barh', stacked='True', mark_right=True, figsize = (10,8), color=['b','g','r'])
# plt.ylabel('')
# plt.xlim(0, 1.15)
# plt.xlabel('Percentage of restaurants')
# plt.title('Grade distribution across top 10 cuisine types')
# plt.show()

##################################################################################
#
cuisinegrade['score']=cuisinegrade['score'].astype(int)
print(cuisinegrade)
average_score=cuisinegrade.groupby('cuisine_description')['score'].mean().sort_values()
print(average_score)
print(cuisinegrade.groupby('cuisine_description')['score'].mean().describe())

cuis_avg=cuisinegrade.groupby('cuisine_description')['score'].mean().values
print(cuis_avg)


mean=[]
median=[]
twenty=cuisinegrade['cuisine_description'].value_counts().head(20).index
for i in range(0,20):
    score=cuisinegrade.loc[cuisinegrade['cuisine_description']==twenty[i]]['score']
    plt.hist(score,label=twenty[i][:15],bins=int(np.max(score.values)/2))
    plt.xlim((0,50))
    plt.axvline(x=np.mean(score),color='r',label=f'Mean = {round(np.mean(score),1)}',)
    plt.axvline(x=np.median(score),color='y',label=f'Median = {round(np.median(score),1)}')
    plt.title(f'Score distribution for {twenty[i][:15]} restaurants')
    plt.legend()
    plt.show()