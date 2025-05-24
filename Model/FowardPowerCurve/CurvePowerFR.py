from Asset_Modeling.Energy_Modeling.data.data import getDApricesDaily, getDApricesHourly
from Logger.Logger import mylogger
from Model.FowardPowerCurve.DailyProfile import simulate_hourly_profile, extendDailyCurveToHourly
from Model.FowardPowerCurve.SeasonalProfile import simulate_seasonal_profile, getCurve

da_prices = getDApricesDaily()
da_prices_hourly = getDApricesHourly()

CAL = {'2026':62.46, '2027':60.18, '2028':63.79}
mylogger.logger.info(CAL)
daily_profile = simulate_seasonal_profile(da_prices, start_date="2026-01-01", end_date="2028-12-31")
hourly_profile = simulate_hourly_profile(da_prices_hourly)
CURVE_DAILY = getCurve(daily_profile, CAL)
CURVE_HOURLY = extendDailyCurveToHourly(CURVE_DAILY, hourly_profile)