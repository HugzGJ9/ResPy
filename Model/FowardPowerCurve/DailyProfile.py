import numpy as np
import pandas as pd
def simulate_hourly_profile_save(da_prices, quant=0.5):
    df = da_prices.copy().dropna().sort_index()
    if 'price' not in df.columns:
        raise ValueError("DataFrame must contain a 'price' column.")

    df['month'] = df.index.month
    df['year'] = df.index.year
    df['day'] = df.index.day
    df['hour'] = df.index.hour

    df['normalized'] = df.groupby(['year', 'month', 'day'])['price'].transform(lambda x: x / x.mean())

    vol_daily = df.resample('D')['normalized'].std()

    profile_dates = []
    for month_i in range(1, 13):
        serie = vol_daily[vol_daily.index.month == month_i]
        if not serie.empty:
            q = serie.quantile(quant)
            closest_date = (serie - q).abs().idxmin()
            profile_dates.append(closest_date)

    df_dates = df.copy()
    df_dates['date_only'] = df_dates.index.date
    selected_dates = set(date.date() for date in profile_dates)
    profile = df_dates[df_dates['date_only'].isin(selected_dates)]
    profile = profile.groupby(['month', 'hour'])['normalized'].mean()
    profile = profile.to_frame(name='normalized')
    return profile

def simulate_hourly_profile(da_prices, quant=0.5):
    df = da_prices.copy().dropna().sort_index()

    if 'price' not in df.columns:
        raise ValueError("DataFrame must contain a 'price' column.")

    # Time columns
    df['year'] = df.index.year
    df['month'] = df.index.month
    df['day'] = df.index.day
    df['hour'] = df.index.hour
    df['date'] = df.index.date

    df['normalized'] = df.groupby('date')['price'].transform(lambda x: x / x.mean())
    df['normalized_modified'] = np.where(df['normalized'] < 1, 2 - df['normalized'], df['normalized'])
    quantile_vals = df.groupby(['month', 'hour'])['normalized_modified'].quantile(quant)
    df = df.merge(quantile_vals.rename('quantile_target'), on=['month', 'hour'])
    df['distance'] = (df['normalized_modified'] - df['quantile_target']).abs()
    df['rank'] = df.groupby(['month', 'hour'])['distance'].rank(method='first')
    selected = df[df['rank'] <= 5]
    profile = selected.groupby(['month', 'hour'])['normalized'].mean().to_frame(name='ID_profile')

    return profile
def extendDailyCurveToHourly(curve_daily, hourly_profile):

    start_date = curve_daily.index[0].date().strftime("%Y-%m-%d")
    end_date = curve_daily.index[-1].date().strftime("%Y-%m-%d")
    index = pd.date_range(start=start_date, end=end_date, freq="H")

    curve_hourly = pd.DataFrame(index=index)
    curve_hourly['prices'] = curve_hourly.index.normalize().map(curve_daily['prices'])
    curve_hourly['month'] = curve_hourly.index.month
    curve_hourly['hour'] = curve_hourly.index.hour

    curve_hourly['scaler'] = [
        hourly_profile.loc[(month, hour), 'ID_profile']
        for hour, month in zip(curve_hourly['hour'], curve_hourly['month'])
    ]
    curve_hourly['shaped_price'] = curve_hourly['prices'] * curve_hourly['scaler']
    curve_hourly = curve_hourly[['shaped_price']]
    return curve_hourly
