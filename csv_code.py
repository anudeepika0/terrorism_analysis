import pandas as pd

dataset_name = "globalterrorismdb.xlsx"
selected_columns = [1,2,3,7,8,9,10,11,12,13,14,28,29,34,35,40,41,58,81,82,98,105,106]

df = pd.read_excel(dataset_name, usecols=selected_columns )
df.fillna('', inplace=True)
df.to_csv('global_terror.csv',header=True,index=False)

df_india=df[df['country_txt']=='India']
df_india.to_csv('india_terror.csv',header=True,index=False)