from Asset_Modeling.Energy_Modeling.data.data import getDAprices
from Logger.Logger import mylogger
from Model.Foward_Power_Curve.SeasonalProfile import simulate_seasonal_profile, getCurve

da_prices = getDAprices()
CAL = {'2026':62.46, '2027':60.18, '2028':63.79}
mylogger.logger.info(CAL)
profile = simulate_seasonal_profile(da_prices, start_date="2026-01-01", end_date="2028-12-31")
CURVE = getCurve(profile, CAL)