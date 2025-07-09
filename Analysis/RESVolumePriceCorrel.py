import pandas as pd
from API.SUPABASE.data import fetchGenerationData, fetchWeatherData, getDApricesHourly

generation_history = fetchGenerationData(country='FR')
generation_history = generation_history.drop(columns=['id', 'created_at', 'WOF', 'WON'])
generation_history['total_generation'] = generation_history.sum(axis=1)
generation_history = generation_history[['Nuclear', 'SR', 'WIND', 'total_generation']]
weather = fetchWeatherData(country="FR")
prices = getDApricesHourly()

df_merged = pd.concat([weather, generation_history], axis=1)
df_merged = df_merged[['Solar_Radiation', 'Wind_Speed_100m', 'Nuclear', 'SR', 'WIND', 'total_generation']]
df2 = pd.concat([df_merged, prices], axis=1)
df2 = df2.dropna()

df2['year'] = df2.index.year
df2['normalized_price'] = df2.groupby('year')['price'].transform(lambda x: x / x.mean())
df2['month'] = df2.index.month
df2['weekday'] = df2.index.weekday
df2['is_weekday'] = df2['weekday'].apply(lambda x: 1 if x < 6 else 0)
df2['RES'] = df2['WIND'] + df2['SR']

df2['normalized_price'] = df2.groupby('year')['price'].transform(lambda x: x / x.mean())

features = ['Solar_Radiation', 'Wind_Speed_100m', 'Nuclear', 'SR', 'WIND', 'RES', 'total_generation']
grouped_corr = (
    df2.groupby(['year', 'month', 'is_weekday'])[features + ['normalized_price']]
    .corr()
    .abs()  # <-- valeurs absolues ici
    .loc[:, 'normalized_price']
    .drop('normalized_price', level=-1)
    .rename('correlation')
    .reset_index()
)

# Pivot pour avoir les features en colonnes
grouped_corr_pivot = grouped_corr.pivot_table(
    index=['year', 'month', 'is_weekday'],
    columns='level_3',
    values='correlation'
).reset_index()

grouped_corr_pivot['date'] = pd.to_datetime(
    grouped_corr_pivot['year'].astype(str) + '-' + grouped_corr_pivot['month'].astype(str).str.zfill(2)
)

grouped_corr_pivot = grouped_corr_pivot.set_index('date')
grouped_corr_pivot = grouped_corr_pivot.drop(columns=['year', 'month'])

df_correl = grouped_corr_pivot[grouped_corr_pivot['is_weekday'] == 0]
df_correl_weekend = grouped_corr_pivot[grouped_corr_pivot['is_weekday'] == 1]

