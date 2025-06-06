import pandas as pd
from API.SUPABASE.data import fetchGenerationData, getDApricesHourly, fetchRESCapacityData
from Asset_Modeling.Energy_Modeling.PPA.ComputeRES_shape import VWA_price, AVG_price
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
def buildResVolumePriceDF():
    generation_history = fetchGenerationData(country='FR')

    generation_history['RES'] = generation_history['SR'] + generation_history['WIND']
    generation_history = generation_history[['SR', 'WIND', 'RES']]
    prices = getDApricesHourly()

    df = pd.concat([generation_history, prices], axis=1)

    df = df.dropna()
    return df

def buildCaptureRateDF(resVolumePriceDF, freq='Y', technos=['WIND', 'SR', 'RES'], year_start = 2016):
    df = resVolumePriceDF.copy()
    df = df[df.index.year >= year_start]
    df['group'] = df.index.to_period(freq)
    dfs_capture = {}

    for techno in technos:
        capture_data = {}
        df_temp = df.copy()
        df_temp['generation'] = df_temp[techno]

        for group_period, group_df in df_temp.groupby('group'):
            avg_price = AVG_price(group_df)
            vwavg_price = VWA_price(group_df)
            capture_rate = (vwavg_price - avg_price) / avg_price * 100

            label = str(group_period)
            capture = {
                'Average Price': avg_price,
                'VWA Price': vwavg_price,
                'Capture rate': capture_rate
            }

            if freq == 'Q':
                capture.update({'year': group_period.year, 'quarter': group_period.quarter})
            elif freq == 'M':
                capture.update({'year': group_period.year, 'month': group_period.month})

            capture_data[label] = capture
        dfs_capture[techno] = pd.DataFrame.from_dict(capture_data, orient='index')
    return dfs_capture

def buildAvgHourlyPriceDF():
    df = getDApricesHourly()
    df = df.copy().dropna().sort_index()
    df['month'] = df.index.month
    df['year'] = df.index.year
    df['day'] = df.index.day
    df['hour'] = df.index.hour
    df['normalized'] = df.groupby('year')['price'].transform(lambda x: x / x.mean())
    df = df.groupby(['year', 'hour'])['normalized'].mean()
    df = df.reset_index()
    df_avg_hourly_price = df.pivot(index=['hour'], columns='year', values=df.columns[-1])
    return df_avg_hourly_price
def plotCaptureRates(dfs_capture, showSeason=False):

    plt.figure(figsize=(14, 6))
    techno_sample = next(iter(dfs_capture))

    res_capacity = fetchRESCapacityData(country='FR')
    min_year = pd.to_datetime(dfs_capture['SR'].index.astype(str)).year.min()
    res_capacity = res_capacity[pd.to_datetime(res_capacity.index.astype(str)).year >= min_year]
    res_capacity['RES'] = res_capacity['SR'] + res_capacity['WIND']
    res_capacity.index = pd.to_datetime(res_capacity.index.astype(str))  # Ensure datetime index

    ax1 = plt.gca()

    for techno, df in dfs_capture.items():
        df_sorted = df.copy()
        df_sorted.index = pd.PeriodIndex(df_sorted.index, freq='M')
        df_sorted = df_sorted.sort_index()
        ax1.plot(df_sorted.index.to_timestamp(), df_sorted['Capture rate'], label=techno)

    if showSeason:
        periods = pd.PeriodIndex(dfs_capture[techno_sample].index, freq='M')
        for p in periods:
            ts = p.to_timestamp()
            if p.month in [6, 7, 8]:  # Summer
                ax1.axvspan(ts, ts + pd.offsets.MonthEnd(1), color='#FFECB3', alpha=0.3)
            elif p.month in [12, 1, 2]:  # Winter
                ax1.axvspan(ts, ts + pd.offsets.MonthEnd(1), color='#BBDEFB', alpha=0.3)

    ax2 = ax1.twinx()
    width = 20

    offset = pd.Timedelta(days=30)
    ax2.bar(res_capacity.index, res_capacity['WIND'], width=width, alpha=0.5, label='WIND Capacity')
    ax2.bar(res_capacity.index - offset, res_capacity['SR'], width=width, alpha=0.5, label='SR Capacity')
    ax2.bar(res_capacity.index + offset, res_capacity['RES'], width=width, alpha=0.5, label='Total RES Capacity')

    # Labels and formatting
    ax1.set_title('Monthly Capture Rate with RES Capacity and Seasonal Highlighting')
    ax1.set_xlabel('Month')
    ax1.set_ylabel('Capture Rate (%)')
    ax2.set_ylabel('RES Capacity (MW)')

    ax1.legend(loc='upper left', title='Technology')
    ax2.legend(loc='upper right', title='Capacity')

    ax1.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
def plot_res_market_value(market_values_dict):
    plt.figure(figsize=(12, 6))

    for tec, df in market_values_dict.items():
        plt.plot(df.index, df['market_value'], label=f'{tec} Market Value')

    generation = list(range(0, 20000, 500))
    value = [g * 100 for g in generation]
    plt.plot(generation, value, label='Linear Reference', linestyle='--', color='gray')

    plt.title('RES Market Value Over Generation')
    plt.xlabel('Generation')
    plt.ylabel('Market Value (€/MWh)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(12, 6))

    for tec, df in market_values_dict.items():
        df = df.copy()
        df['market%'] = df['market_value'] / df.index
        plt.plot(df.index, df['market%'], label=f'{tec} Market %')

    plt.title('RES Market Value as % of Generation')
    plt.xlabel('Generation')
    plt.ylabel('Market % (€/MWh per MW)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
def plot_duck_curve(df_avg_hourly_price, start=2016, end=2025):
    years = list(range(start, end))
    num_years = len(years)

    cmap = cm.get_cmap('Paired')
    colors = [cmap(i % cmap.N) for i in range(num_years)]

    plt.figure(figsize=(12, 6))

    for i, y in enumerate(years):
        if y in df_avg_hourly_price.columns:
            plt.plot(
                df_avg_hourly_price.index,
                df_avg_hourly_price[y],
                label=str(y),
                color=colors[i],
                linewidth=2
            )

    plt.title("Normalized Hourly Average Prices")
    plt.xlabel("Hour of the day")
    plt.ylabel("Average Price (€/MWh)")
    plt.xticks(range(0, 24))
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend(title="Years", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()

def plot_duck_value_evolution():
    df_avg_hourly_price = buildAvgHourlyPriceDF()
    duck_values = computeDuckValue(df_avg_hourly_price)
    plt.figure(figsize=(12, 6))
    plt.plot(duck_values, linewidth=2)
    plt.title("Duck Values Evolution in Time")
    plt.xlabel("Years")
    plt.ylabel("Duck Values")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend(title="Years", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()
def compute_res_market_value(resVolumePriceDF, technos=['WIND', 'SR', 'RES']):
    df = resVolumePriceDF.copy()
    market_values = {}

    for tec in technos:
        if tec in df.columns:
            df_tec = df[[tec, 'price']].copy()
            df_tec['generation_mwh'] = (df_tec[tec] / 1000).round() * 1000
            df_tec['market_value'] = df_tec['generation_mwh'] * df_tec['price']
            df_tec = df_tec.reset_index()
            df_tec = df_tec[['generation_mwh', 'market_value']]
            df_tec = df_tec.groupby('generation_mwh').mean()
            market_values[tec] = df_tec
    return market_values
def computeDuckValue(df_avg_hourly_price):
    df = df_avg_hourly_price.copy()
    morning_peak = df[(df.index > 6) & (df.index < 10)].max()
    evening_peak = df[(df.index > 15) & (df.index < 22)].max()
    midday_dip = df[(df.index > 10) & (df.index < 17)].min()

    avg_peak = (morning_peak + evening_peak) / 2
    duck_value = avg_peak - midday_dip
    return duck_value

df_avg_hourly_price = buildAvgHourlyPriceDF()
plot_duck_curve(df_avg_hourly_price, start=2017)
df = buildResVolumePriceDF()
market_values_dict = compute_res_market_value(df)
plot_res_market_value(market_values_dict)

dfs_capture = buildCaptureRateDF(df, freq='Y')
plotCaptureRates(dfs_capture)
dfs_capture = buildCaptureRateDF(df, freq='Q')
plotCaptureRates(dfs_capture)
dfs_capture = buildCaptureRateDF(df, freq='M')
plotCaptureRates(dfs_capture, showSeason=True)
dfs_capture = buildCaptureRateDF(df, freq='M', year_start=2023)
plotCaptureRates(dfs_capture, showSeason=True)