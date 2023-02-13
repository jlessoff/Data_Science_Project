# Import library
import bnlearn as bn
import pandas as pd
from tabulate import tabulate
from Rodents import resultcount
from Restaurants import results_df

def get_exam_count(results_df):
    examcount = results_df.groupby('camis').inspection_date.nunique().reset_index().sort_values(by='inspection_date', ascending=False)
    examcount = examcount.rename(columns={'inspection_date': 'exam_count'})
    return examcount

def get_average_violations(results_df):
    vcount = results_df.groupby(['camis', 'inspection_date']).violation_code.count().reset_index()
    vcount = round(vcount.groupby(['camis']).violation_code.mean().reset_index())
    vcount['vcount'] = vcount['violation_code']
    vcount = vcount.drop(columns=['violation_code'])
    return vcount

def get_violation_indicator(results_df):
    violation_df = results_df.loc[results_df.groupby(['violation_code', 'camis'])['inspection_date'].idxmax()]
    violation_df = violation_df.groupby(['violation_code', 'camis']).count()
    violation_df = violation_df.pivot_table(index='camis', columns='violation_code', values='violation_description').fillna(0)
    return violation_df

def get_restaurant_info(results_df):
    info = results_df.loc[results_df.groupby(['camis'])['inspection_date'].idxmax()]
    info = info[['camis', 'cuisine_description', 'neighborhood', 'zipcode']]
    return info

def merge_data_sets(examcount, vcount, violation_df, info):
    df = pd.merge(examcount, vcount, how="left", on='camis')
    df['vcount'] = df['vcount'].fillna(0)
    df = pd.merge(df, violation_df, how="left", on='camis')
    df = pd.merge(df, info, how="left", on='camis')
    return df

def get_zip_data():
    zippop = pd.read_csv('zipcode_pop.csv')
    zipsize = pd.read_csv('zip_size.csv')
    neighborhood = pd.read_csv('nyc-zip-codes.csv')
    zip_data = pd.merge(zipsize, zippop, how="left", on='zip_code')
    zip_data = pd.merge(zip_data, neighborhood, how="left", on='zip_code')
    zip_data = zip_data.groupby('neighborhood').sum().reset_index()
    zip_data = pd.merge(zip_data, resultcount, how="left", on='neighborhood')
    zip_data['sq_meters'] = pd.to_numeric(zip_data['sq_km'])
    zip_data['Pop'] = pd.to_numeric(zip_data['Pop'])
    zip_data['pop_dens'] = (zip_data['Pop'])/(zip_data['sq_km'])
    zip_data['rat_dens'] = (zip_data['result'])/(zip_data['sq_km'])
    zip_data = zip_data[['rat_dens', 'pop_dens', 'neighborhood']]
    return zip_data

def merge_zip_data(df, zip_data):
    df = pd.merge(df, zip_data, how="left", on='neighborhood')
    df['pop_dens'] = pd.qcut(df['pop_dens'], q=4)
    df['rat_dens'] = pd.qcut(df['rat_dens'], q=2)
    df = df.drop(columns=['camis', 'zipcode'])
    df.to_csv('df.csv')
    df = pd.read_csv('df.csv')
    return df

results_df = pd.read_csv('results.csv')

examcount = get_exam_count(results_df)
vcount = get_average_violations(results_df)
violation_df = get_violation_indicator(results_df)
info = get_restaurant_info(results_df)

df = merge_data_sets(examcount, vcount, violation_df, info)

zip_data = get_zip_data()
df = merge_zip_data(df, zip_data)

print(df)
df.reset_index()


#create df to just look at relationship between violations
df1=df[['2.0','3.0','4.0','5.0','6.0','7.0','8.0','9.0','10.0','19.0','22.0']]

#build DAG
model = bn.structure_learning.fit(df1,methodtype='cs')
model = bn.independence_test(model, df1, test='chi_square', prune=True)
#print table with chi squared stat and p score
print(tabulate(model['independence_test'], tablefmt="grid", headers="keys"))
#plot DAG
bn.plot(model)


#show DAG with all of the variables from df; redo same steps from before
df2=df
model = bn.structure_learning.fit(df2,methodtype='cs')
model = bn.independence_test(model, df2, test='chi_square', prune=True)
print(tabulate(model['independence_test'], tablefmt="grid", headers="keys"))
bn.plot(model)
