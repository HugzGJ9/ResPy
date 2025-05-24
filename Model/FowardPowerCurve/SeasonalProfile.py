import pandas as pd
from matplotlib import pyplot as plt
from Asset_Modeling.Energy_Modeling.data.data import getDApricesDaily

def simulate_seasonal_profile(da_prices, start_date="2025-01-01", end_date="2025-12-31", rolling_window=None):
    df = da_prices.copy().dropna().sort_index()
    df['year'] = df.index.year
    df['normalized'] = df.groupby('year')['price'].transform(lambda x: x / x.mean())

    df['month'] = df.index.month
    df['weekday'] = df.index.weekday
    df['week_in_month'] = df.index.day.map(lambda d: (d - 1) // 7 + 1)

    seasonal_avg = df.groupby(['month', 'week_in_month', 'weekday'])['normalized'].mean()

    index = pd.date_range(start_date, end_date, freq="D")
    curve = pd.DataFrame(index=index)
    curve['month'] = curve.index.month
    curve['weekday'] = curve.index.weekday
    curve['week_in_month'] = curve.index.day.map(lambda d: (d - 1) // 7 + 1)

    # Use multi-index join and preserve datetime index
    curve_key = curve.set_index(['month', 'week_in_month', 'weekday'])
    curve['normalized_price'] = seasonal_avg.reindex(curve_key.index).values

    if rolling_window:
        curve['normalized_price'] = curve['normalized_price'].rolling(rolling_window, center=True, min_periods=1).mean()

    return curve[['normalized_price']]


def getCurve(profile_normalized, market_prices:dict):
    curve = profile_normalized.copy()
    for year, price in market_prices.items():
        curve[curve.index.year == int(year)] = curve[curve.index.year == int(year)] * price
    curve.columns = ['prices']
    return curve

# da_prices = getDAprices()
# CAL = {'2026':62.46, '2027':60.18, '2028':63.79}
# profile = simulate_seasonal_profile(da_prices, start_date="2026-01-01", end_date="2028-12-31")
# CURVE = getCurve(profile, CAL)
