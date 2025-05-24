import pandas as pd
from Asset_Modeling.Energy_Modeling.data.data import getDApricesHourly
from Model.FowardPowerCurve.CurvePowerFR import CURVE


def simulate_hourly_profile(da_prices):
    df = da_prices.copy().dropna().sort_index()
    df['month'] = df.index.month
    df['year'] = df.index.year
    df['day'] = df.index.day
    df['normalized'] = df.groupby(['year', 'month', 'day'])['price'].transform(lambda x: x / x.mean())
    df['hour'] = df.index.hour

    month_hourly = df.groupby(['year', 'month', 'hour'])['normalized'].mean()
    monthly_hourly_avg = month_hourly.groupby(['month', 'hour']).mean()
    return pd.DataFrame(monthly_hourly_avg)

def extendDailyCurveToHourly(curve_daily, hourly_profile):

    start_date = curve_daily.index[0].date().strftime("%Y-%m-%d")
    end_date = curve_daily.index[-1].date().strftime("%Y-%m-%d")
    index = pd.date_range(start=start_date, end=end_date, freq="H")

    curve_hourly = pd.DataFrame(index=index)
    curve_hourly['prices'] = curve_hourly.index.normalize().map(curve_daily['prices'])
    curve_hourly['month'] = curve_hourly.index.month
    curve_hourly['hour'] = curve_hourly.index.hour

    curve_hourly['scaler'] = [
        hourly_profile.loc[(month, hour), 'normalized']
        for hour, month in zip(curve_hourly['hour'], curve_hourly['month'])
    ]
    curve_hourly['shaped_price'] = curve_hourly['prices'] * curve_hourly['scaler']
    curve_hourly = curve_hourly[['shaped_price']]
    return curve_hourly
