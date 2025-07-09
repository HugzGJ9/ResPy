from API.SUPABASE.data import getDApricesDaily, getDApricesHourly
from Model.FowardPowerCurve.DailyProfile import simulate_hourly_profile, extendDailyCurveToHourly
from Model.FowardPowerCurve.SeasonalProfile import simulate_seasonal_profile, getCurve
from PPA_class import PPA
from tqdm import tqdm
da_prices = getDApricesDaily()
da_prices_hourly = getDApricesHourly()

def simuMtM(ppa:PPA):
    forward_prices = list(range(62 - 40, 62 + 40, 10))
    Mtm = []
    for forward_price in tqdm(forward_prices, desc="Simulation MtM"):
        CAL = {'2026': forward_price}
        daily_profile = simulate_seasonal_profile(da_prices, start_date="2026-01-01", end_date="2026-12-31")
        hourly_profile = simulate_hourly_profile(da_prices_hourly)
        CURVE_DAILY = getCurve(daily_profile, CAL)
        CURVE_HOURLY = extendDailyCurveToHourly(CURVE_DAILY, hourly_profile)
        Mtm.append(ppa_wind.MtM(CURVE_HOURLY))
    return forward_prices, Mtm


ppa_wind = PPA(id= 9529244,techno='WIND', capacity=10.0)

St, Mtm = simuMtM(ppa_wind)
