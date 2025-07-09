import pandas as pd
from API.SUPABASE.data import fetchGenerationData, fetchWeatherData
import matplotlib.pyplot as plt

def plotHisto(df, title='title', x_axis='x_axis', y_axis='y_axis', legend_title='Legend', color_palette=None):
    ax = df.plot(
        kind='bar',
        figsize=(12, 7),
        width=0.8,
        color=color_palette,
        edgecolor='black'
    )

    ax.set_title(title, fontsize=16, weight='bold')
    ax.set_xlabel(x_axis, fontsize=12)
    ax.set_ylabel(y_axis, fontsize=12)
    ax.tick_params(axis='x', rotation=45)
    ax.legend(title=legend_title, bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
def pivotDf(df):
    df = df.copy()
    df.index = pd.to_datetime(df.index)
    df['Year'] = df.index.year
    df['Month'] = df.index.month
    df_pivot = df.pivot(index='Month', columns='Year', values='Temperature')
    return df_pivot

def convertSummerPeak(df):
    df = df[df.index.month > 5]
    df = df[df.index.month < 9]
    df = df[df.index.hour > 11]
    df = df[df.index.hour < 17]
    return df

def fetchACdata():
    df_generation = fetchGenerationData()
    df_weather = fetchWeatherData()


    df_weather = df_weather[['Temperature_2m']]
    df_weather.columns = ['Temperature']
    df_weather = df_weather.dropna()
    df_weather_summer_peak = convertSummerPeak(df_weather)

    all = ['Biomass', 'Fossil Gas', 'Fossil Hard coal',
           'Fossil Oil', 'Hydro Pumped Storage', 'Hydro Run-of-river and poundage',
           'Hydro Water Reservoir', 'Nuclear', 'SR', 'Waste', 'WOF', 'WON', 'WIND']

    df_generation['total'] = df_generation[all].sum(axis=1)

    df_generation = df_generation[['total']]
    df_generation_summer_peak = convertSummerPeak(df_generation)

    save = pd.concat([df_weather_summer_peak, df_generation_summer_peak], axis=1)
    annual_mean = save['total'].resample('Y').transform('mean')
    save['total'] = save['total'] / annual_mean

    return save

def computeCorr(data):
    correl_total_temp = {}
    for y in data.index.year.unique():
        df = data[data.index.year == y]

        if {'total', 'Temperature'}.issubset(df.columns):
            plt.figure()
            plt.scatter(df['Temperature'], df['total'], alpha=0.6)
            plt.title(f'Total vs Temperature - {y}')
            plt.xlabel('Temperature')
            plt.ylabel('Total')
            plt.grid(True)
            plt.show()

            correl_total_temp[y] = df['total'].corr(df['Temperature'])
    return correl_total_temp
def meanHotHours(data, show=True):
    df = data.resample('M').mean()
    df = df.dropna()
    df = pivotDf(df)
    if show:
        plotHisto(df, title='monthly average temperature evolution', x_axis='month', y_axis='mean temperature')
    return df
def countHotHours(data, temp=25, show=True):
    count = data[data['Temperature'] > temp] \
        .resample('M') \
        .size()
    count = pd.DataFrame(count[count > 0])
    count.columns = ['Temperature']
    df_count = pivotDf(count)
    if show:
        plotHisto(df_count, title=f'Number hours above {temp} degrees', x_axis='Month', y_axis='Number of hours')
    return df_count

data = fetchACdata()
# correl_total_temp = computeCorr(data)
#
# correl_df = pd.DataFrame.from_dict(correl_total_temp, orient='index', columns=['corr_total_vs_temp'])
# correl_df.index.name = 'Year'

meanHotHours(data)
countHotHours(data)

# df = pd.concat([df_generation, df_weather], axis=1)