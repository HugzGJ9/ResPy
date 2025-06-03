import numpy as np
import pandas as pd
from API.SUPABASE.data import getDApricesDaily, getDApricesHourly
from Logger.Logger import mylogger
from Model.FowardPowerCurve.DailyProfile import simulate_hourly_profile, extendDailyCurveToHourly
from Model.FowardPowerCurve.SeasonalProfile import simulate_seasonal_profile, getCurve
from matplotlib import pyplot as plt

da_prices = getDApricesDaily()
da_prices_hourly = getDApricesHourly()

def getCurveDaily(CAL = {'2026':62.46, '2027':60.18, '2028':63.79}):
    mylogger.logger.info(CAL)
    daily_profile = simulate_seasonal_profile(da_prices, start_date="2026-01-01", end_date="2028-12-31")
    Curve = getCurve(daily_profile, CAL)
    return Curve

def getCurveHourly(Curve_daily=None, CAL = {'2026':62.46, '2027':60.18, '2028':63.79}, shape_id_vol=0.5):
    if Curve_daily is None:
        Curve_daily = getCurveDaily(CAL)
    hourly_profile = simulate_hourly_profile(da_prices_hourly, shape_id_vol)
    Curve_hourly = extendDailyCurveToHourly(Curve_daily, hourly_profile)
    return Curve_hourly

def plotHourlyShape(shape_id_vols=[x/100 for x in range(10, 91, 20)]):
    plt.figure(figsize=(12, 6))

    for shape_id_vol in shape_id_vols:
        hourly_profile = simulate_hourly_profile(da_prices_hourly, shape_id_vol)

        # Flatten the MultiIndex for plotting
        flattened_index = [f'{month:02d}-{hour:02d}' for month, hour in hourly_profile.index]
        values = hourly_profile['ID_profile'].values

        plt.plot(flattened_index, values, label=f'Vol {shape_id_vol:.2f}')

    plt.title('Hourly Profile vs Shape ID Volatility')
    plt.xlabel('Month-Hour')
    plt.ylabel('Normalized Value')
    plt.xticks(rotation=90, fontsize=6)  # Small font for many ticks
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
# CAL = {'2026':62.46, '2027':60.18, '2028':63.79}
# mylogger.logger.info(CAL)
# daily_profile = simulate_seasonal_profile(da_prices, start_date="2026-01-01", end_date="2028-12-31")
# hourly_profile = simulate_hourly_profile(da_prices_hourly)
# CURVE_DAILY = getCurve(daily_profile, CAL)
# CURVE_HOURLY = extendDailyCurveToHourly(CURVE_DAILY, hourly_profile)
# plotHourlyShape(shape_id_vols=[0.7, 0.5])