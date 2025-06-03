import random

from API.SUPABASE.data import getDApricesDaily, getDApricesHourly
from Model.FowardPowerCurve.CurvePowerFR import getCurveHourly, getCurveDaily
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import matplotlib.ticker as mtick

import plotly.io as pio
pio.renderers.default = "iframe_connected"
from tqdm import tqdm
from API.SUPABASE.client import getDfSupabase, getAccessSupabase, getRowsSupabase
from Asset_Modeling.Energy_Modeling.PPA.ComputeRES_shape import AVG_price, VWA_price
from Asset_Modeling.Energy_Modeling.PPA.stats import buildSyntheticGenerationSR, buildSyntheticGenerationWIND
from Logger.Logger import mylogger
import seaborn as sns

from pytz.exceptions import AmbiguousTimeError, NonExistentTimeError
CURVE_DAILY = getCurveDaily()
def datetime_generation(start_date: str, end_date: str) -> pd.DatetimeIndex:
    full_range = pd.date_range(start=start_date, end=end_date, freq="H", inclusive="left")
    return pd.DatetimeIndex(full_range)

class PPA():
    def __init__(self, site_name="Montlucon", techno="SR", capacity=10.0, pricing_type='fixed_price', start_date='01/01/2026', end_date='01/01/2027', id=None, price=None, shape_intraday_vol=0.5):
        if not id:
            self.id = random.randint(1, 10000000)
            self.site_name = site_name
            self.start_date = start_date
            self.end_date = end_date
            self.capacity = capacity
            self.techno = techno
            self.pricing_type = pricing_type
            self.country = "FR" if self.site_name in ['Montlucon'] else None
            self.proxy = pd.DataFrame()
            self.mark = pd.DataFrame()
            self.p50 = None
            self.price = price
            self.shape_intraday_vol = shape_intraday_vol
        else:

            row = getRowsSupabase('PPA', [id])
            self.id = row.iloc[0]['id']
            self.site_name = row.iloc[0]['site_name']
            self.start_date = row.iloc[0]['start_date']
            self.end_date = row.iloc[0]['end_date']
            self.capacity = row.iloc[0]['capacity']
            self.techno = row.iloc[0]['techno']
            self.pricing_type = row.iloc[0]['pricing_type']
            self.country = row.iloc[0]['country']
            self.proxy = pd.read_json(row.iloc[0]['proxy'])
            self.mark = pd.read_json(row.iloc[0]['mark'])
            self.p50 = row.iloc[0]['p50']
            self.price = row.iloc[0]['price']
            self.shape_intraday_vol = row.iloc[0]['shape_intraday_vol']

    def buildProxy(self):

        if not self.proxy.empty:
            mylogger.logger.warning('Proxy TS already set.')
            return
        else:
            if self.country != "FR":
                raise NotImplementedError("FR only")

            import pandas as pd
            if self.techno == "SR":
                weather = getDfSupabase("WeatherFR")
                weather["id"] = pd.to_datetime(weather["id"], utc=True)
                weather = (weather
                           .set_index("id")
                           .sort_index()
                           .loc[:, ["Solar_Radiation"]])

                commissioning = pd.to_datetime(self.start_date, dayfirst=True, utc=True)
                weather = weather.loc[: commissioning - pd.Timedelta(seconds=1)]

                weather.index = weather.index.tz_convert('Europe/Paris')
                generation = buildSyntheticGenerationSR(weather, capacity=self.capacity)
                generation = generation.drop(columns=['Solar_Radiation'])
                self.proxy = generation
                self.proxy = self.proxy.sort_index()

            elif self.techno == "WIND":
                weather = getDfSupabase("WeatherFR")
                weather["id"] = pd.to_datetime(weather["id"], utc=True)

                weather = (weather
                           .set_index("id")
                           .sort_index()
                           .loc[:, ["Wind_Speed_100m"]])

                commissioning = pd.to_datetime(self.start_date, dayfirst=True, utc=True)
                weather = weather.loc[: commissioning - pd.Timedelta(seconds=1)]

                weather.index = weather.index.tz_convert('Europe/Paris')
                generation = buildSyntheticGenerationWIND(weather, self.capacity)
                generation = generation.drop(columns=['Wind_Speed_100m'])
                self.proxy = generation
                self.proxy = self.proxy.sort_index()
            return
    def saveInstance(self):
        supabase = getAccessSupabase('PPA')
        instance = pd.DataFrame([{
            'id': self.id,
            'site_name': self.site_name,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'capacity': self.capacity,
            'techno': self.techno,
            'pricing_type': self.pricing_type,
            'country': self.country,
            'proxy': self.proxy.to_json(),
            'mark': self.mark.to_json(),
            'p50': self.p50
        }])

        instance.set_index('id')
        for col in instance.columns:
            if pd.api.types.is_datetime64_any_dtype(instance[col]):
                instance[col] = instance[col].dt.strftime('%Y-%m-%dT%H:%M:%SZ')

        instance = instance.replace({np.nan: None, np.inf: None, -np.inf: None})
        instance = instance.where(pd.notnull(instance), None)
        instance = instance.to_dict(orient="records")
        supabase.table('PPA').insert(instance).execute()

    def buildMark(self):
        if not self.proxy.empty:
            index = datetime_generation(self.start_date, self.end_date)

            mark_df = pd.DataFrame(index=index)
            mark_df["month"] = mark_df.index.month
            mark_df["hour"] = mark_df.index.hour

            proxy = self.proxy.copy()
            proxy["month"] = proxy.index.month
            proxy["hour"] = proxy.index.hour

            seasonal_avg = proxy.groupby(["month", "hour"])["generation"].mean().reset_index()

            mark_df = mark_df.reset_index().merge(seasonal_avg, on=["month", "hour"], how="left").set_index(
                "index")

            self.mark = mark_df[["generation"]]
            self.p50 = round(self.mark.sum().values[0], 2)
        else:
            mylogger.logger.warning('No proxy saved. Run buildProxy first.')
        return

    def computeCaptureRateYearly(self):
            df = mergePriceVolume(self.proxy)
            yearly_capture = {}
            for y in sorted(df.index.year.unique()):
                df_temp = df[df.index.year==y]
                avg_price = AVG_price(df_temp)
                vwavg_price = VWA_price(df_temp)
                yearly_capture[str(y)] = {'average price': avg_price, 'VWA price': vwavg_price,
                                             'Capture rate': ((vwavg_price - avg_price) / avg_price * 100)}

            df = pd.DataFrame.from_dict(yearly_capture)
            df =df.transpose()
            return df
    def computeCaptureRateQuarter(self):
        df = mergePriceVolume(self.proxy)
        yearly_capture = {}
        for y in sorted(df.index.year.unique()):
            for q in list(range(1, 5, 1)):
                df_temp = df[(df.index.year==y) & (df.index.quarter==q)]
                if df_temp.empty:
                    pass
                else:
                    avg_price = AVG_price(df_temp)
                    vwavg_price = VWA_price(df_temp)
                    yearly_capture[f'{y}_Q{q}'] = {'average price': avg_price, 'VWA price': vwavg_price,
                                                 'Capture rate': ((vwavg_price - avg_price) / avg_price * 100), 'year':y, 'quarter':q}

        df = pd.DataFrame.from_dict(yearly_capture)
        df =df.transpose()
        return df

    def showPowerCurve(self):
        from Model.ResPowerGeneration.dataProcessing import plot_hexbin_density
        weather = getDfSupabase("WeatherFR")
        weather["id"] = pd.to_datetime(weather["id"], utc=True)
        weather["id"] = weather["id"].dt.tz_convert("Europe/Paris")
        x = "Solar_Radiation" if self.techno == "SR" else "Wind_Speed_100m"
        weather = (weather
                   .set_index("id")
                   .sort_index()
                   .loc[:, [x]])
        if self.proxy.index.tz is None:
            weather.index = weather.index.tz_localize(None)
        weather = weather[~weather.index.duplicated(keep='first')]
        df_merged = pd.concat([self.proxy, weather], axis=1).dropna()
        plot_hexbin_density(df_merged, x_col=x, y_col='generation')
        plt.title(f"Power Curve: {x} vs. Generation", fontsize=14)
        plt.xlabel(f"{x}")
        plt.ylabel("Generation [MW]")
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.tight_layout()
        plt.show()

    def show_pnl(self):
        """
        Computes and displays styled histograms of daily and monthly PPA payoff.
        """
        if self.price is None:
            mylogger.logger.warning('Cannot compute payoff: PPA price is not set.')
            return

        if not hasattr(self, 'shape_intraday_vol') or not hasattr(self, 'mark'):
            mylogger.logger.error('Missing required attributes: shape_intraday_vol or mark.')
            return

        curve = getCurveHourly(Curve_daily=CURVE_DAILY, shape_id_vol=self.shape_intraday_vol)
        price_volume = mergePriceVolume(self.mark, curve)

        price_volume['pnl'] = (price_volume['shaped_price'] - self.price) * price_volume['generation']

        # Daily and Monthly PnL
        daily_pnl = price_volume.resample('D').sum()['pnl']
        plot_pnl_timeseries(daily_pnl, title="Daily PPA Payoff")

        monthly_pnl = price_volume.resample('M').sum()['pnl']
        plot_pnl_hist(monthly_pnl, title="Monthly PPA Payoff")
    def computeIntermitencyValue(self):
        price_volume = mergePriceVolume(self.proxy)
        price_volume['VWA_price'] = price_volume['generation'] * price_volume['price']
        price_volume = price_volume.resample('D').sum()
        price_volume['VWA_price'] = price_volume['VWA_price'] / price_volume['generation']
        price_volume['price'] = price_volume['price'] / 24

        price_volume['PC'] = (price_volume['VWA_price'] - price_volume['price']) / price_volume['price']
        PC = price_volume['PC'].mean()
        return PC
    def computeShape(self):
        price_volume = mergePriceVolume(self.proxy)

        price_volume = price_volume.resample('M').sum()
        price_volume['price'] = price_volume['price'] / (24*30)

        price_volume['VWA_price'] = price_volume['generation'] * price_volume['price']
        price_volume = price_volume.resample('Y').sum()

        price_volume['price'] = price_volume['price'] / 12
        price_volume['VWA_price'] = price_volume['VWA_price'] / price_volume['generation']

        price_volume['shape'] = (price_volume['VWA_price'] - price_volume['price']) / price_volume['price']
        shape = price_volume['shape'].mean()
        return shape
    def MtM(self, Curve=None):
        if Curve is None:
            Curve = getCurveHourly(Curve_daily=CURVE_DAILY, shape_id_vol=self.shape_intraday_vol)

        df = pd.concat([self.mark, Curve], axis=1)
        df = df.dropna()
        revenue = df['generation'] * df['shaped_price']
        revenue = revenue.sum()
        return revenue

    def plot_mtm_vs_forward_price(self, central_price=62, delta=40, step=5, year="2026", plot=True, return_df=False):
        """
        Plots MtM as a function of forward price for a given delivery year.

        Parameters:
        - central_price (float): Reference price around which to simulate
        - delta (float): +/- range around central_price to test
        - step (float): Step size for simulation prices
        - year (str): Delivery year
        - plot (bool): Whether to show the matplotlib plot
        - return_df (bool): If True, returns a pandas DataFrame

        Returns:
        - DataFrame (optional): DataFrame with forward_price and MtM
        """
        forward_prices = list(range(int(central_price - delta), int(central_price + delta + 1), step))
        mtm_values = []

        for forward_price in tqdm(forward_prices, desc="Simulating MtM"):
            CAL = {year: forward_price}
            curve_daily = getCurveDaily(CAL)
            curve_hourly = getCurveHourly(Curve_daily=curve_daily, shape_id_vol=self.shape_intraday_vol)
            mtm = ppa_wind.MtM(curve_hourly)
            mtm_values.append(mtm)

        df = pd.DataFrame({
            "forward_price": forward_prices,
            "mtm": mtm_values
        })

        if plot:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(df["forward_price"], df["mtm"], marker='o', linewidth=2, label="MtM vs Forward Price")

            ax.set_title(f"MtM vs Forward Price – CAL {year}", fontsize=16, weight='bold')
            ax.set_xlabel("Forward Price (€/MWh)", fontsize=12)
            ax.set_ylabel("MtM (€)", fontsize=12)
            ax.axhline(0, color='grey', linestyle='--', linewidth=1)
            ax.grid(True, linestyle='--', alpha=0.6)

            # Ajout de repères visuels utiles
            ax.axvline(central_price, color='black', linestyle=':', linewidth=1, label="Central Price")

            if hasattr(self, "price") and self.price is not None:
                ax.axhline(y=0, color='grey', linestyle='--', linewidth=1)
                ax.scatter(central_price, df[df["forward_price"] == central_price]["mtm"].values[0],
                           color='red', zorder=5, label=f"MtM @ {central_price} €/MWh")

            ax.legend()
            plt.tight_layout()
            plt.show()

        return df if return_df else None

    def plot_hedged_mtm_vs_forward_price(self, central_price=62, delta=40, step=5, year="2026", plot=True,
                                         return_df=False):

        forward_prices = list(range(int(central_price - delta), int(central_price + delta + 1), step))
        capture_rate = (100 - ppa_wind.computeCaptureRateYearly().mean()['Capture rate']) /100  # e.g., 0.87
        if not 0 < capture_rate < 2:
            raise ValueError(f"Invalid capture rate: {capture_rate}")

        hedge_volume = capture_rate * self.p50

        mtm_ppa = []
        mtm_hedge = []

        for forward_price in tqdm(forward_prices, desc="Simulating Hedged MtM"):
            CAL = {year: forward_price}
            curve_daily = getCurveDaily(CAL)
            curve_hourly = getCurveHourly(Curve_daily=curve_daily, shape_id_vol=self.shape_intraday_vol)

            mtm = ppa_wind.MtM(curve_hourly)
            hedge = - forward_price * hedge_volume

            mtm_ppa.append(mtm)
            mtm_hedge.append(hedge)

        df = pd.DataFrame({
            "forward_price": forward_prices,
            "mtm_ppa": mtm_ppa,
            "mtm_hedge": mtm_hedge,
        })
        df["mtm_total"] = df["mtm_ppa"] + df["mtm_hedge"]

        if plot:
            plt.figure(figsize=(12, 6))
            plt.plot(df["forward_price"], df["mtm_ppa"], label="MtM PPA", linewidth=2)
            plt.plot(df["forward_price"], df["mtm_hedge"], label="MtM Hedge", linestyle='--', linewidth=2)
            plt.plot(df["forward_price"], df["mtm_total"], label="MtM Total (PPA + Hedge)", linewidth=2, marker='o')
            plt.axhline(0, color='grey', linestyle='--', linewidth=1)
            plt.title(f"Hedged MtM vs Forward Price – CAL {year}", fontsize=16, weight='bold')
            plt.xlabel("Forward Price (€/MWh)", fontsize=12)
            plt.ylabel("MtM (€)", fontsize=12)
            plt.grid(True, linestyle='--', alpha=0.6)
            plt.legend()
            plt.tight_layout()
            plt.show()

        return df if return_df else None
    def DeltaShapeID(self, shape_intraday_vol=None):
        #Method Finite difference to see effect of change of shape_id_vol (corresponds to the volatily of the shape intraday)
        epsilon = 0.001
        if shape_intraday_vol is None:
            curve_neg = getCurveHourly(Curve_daily = CURVE_DAILY, shape_id_vol=self.shape_intraday_vol - epsilon)
            curve_pos =getCurveHourly(Curve_daily = CURVE_DAILY, shape_id_vol=self.shape_intraday_vol + epsilon)
        else:
            curve_neg = getCurveHourly(Curve_daily = CURVE_DAILY, shape_id_vol=shape_intraday_vol - epsilon)
            curve_pos = getCurveHourly(Curve_daily = CURVE_DAILY, shape_id_vol=shape_intraday_vol + epsilon)
        delta_shape_id = (self.MtM(curve_pos)-self.MtM(curve_neg)) / (2*epsilon)
        return delta_shape_id
    def ShapeIDRisk(self):
        deltas= []
        shape_intraday_vols = [x / 100 for x in range(10, 91, 10)]

        for shape_intraday_vol in tqdm(shape_intraday_vols, desc="Simulation MtM"):
            deltas.append(self.DeltaShapeID(shape_intraday_vol=shape_intraday_vol))
        plt.plot(shape_intraday_vols, deltas, label=f'Shape Intraday Volatility vs Range', color='blue', linestyle='-', linewidth=2)
        plt.title(f'Pnl Impact for change in Shape Intraday Volatility')
        plt.xlabel('Shape Intraday Volatility')
        plt.ylabel(f'Pnl')
        plt.legend()
        plt.grid(True)
        plt.show()
def mergePriceVolume(volume_df, df_prices=None):
    if volume_df.empty:
        mylogger.logger.warning('No proxy saved. Run buildProxy first.')
        df = pd.DataFrame()
        return df
    else:
        if df_prices is None:
            df_prices = getDfSupabase('DAPowerPriceFR')
            df_prices['id'] = pd.to_datetime(df_prices['id'], utc=True)
            df_prices['id'] = df_prices['id'].dt.tz_convert('Europe/Paris')

            df_prices.index = df_prices['id']
            df_proxy = volume_df[~volume_df.index.duplicated(keep='first')]
            if df_proxy.index.tz is None:
                df_prices.index = df_prices.index.tz_localize(None)
            df_prices = df_prices[~df_prices.index.duplicated(keep='first')]
            df = pd.concat([df_proxy, df_prices], axis=1)
            df = df[df.index.year > 2015]
            df = df[df.index.year < 2025]
            df = df.dropna(subset=['generation'])
            df = df[['generation', 'price']]
        else:
            volume_df = volume_df[~volume_df.index.duplicated(keep='first')]
            if volume_df.index.tz is None:
                df_prices.index = df_prices.index.tz_localize(None)
            df_prices = df_prices[~df_prices.index.duplicated(keep='first')]
            df = pd.concat([volume_df, df_prices], axis=1)
            df = df.dropna()
        return df


# Apply a clean seaborn style
sns.set_theme(style="whitegrid")

def plot_pnl_hist(pnl_series, title="PPA Payoff"):
    fig, ax = plt.subplots(figsize=(12, 6))

    # Define color based on sign of total PnL
    color = "#2ca02c" if pnl_series.sum() >= 0 else "#d62728"

    # Bar plot for readability
    pnl_series.plot(kind='bar', color=color, ax=ax, width=0.8)

    ax.set_title(title, fontsize=16, weight='bold', pad=15)
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("PnL (€)", fontsize=12)
    ax.yaxis.set_major_formatter(mtick.StrMethodFormatter('€{x:,.0f}'))
    ax.tick_params(axis='x', rotation=45)
    ax.grid(visible=True, linestyle='--', linewidth=0.5, alpha=0.7)
    plt.tight_layout()
    plt.show()

def plot_pnl_timeseries(pnl_series, title="PPA Daily Payoff", rolling_days=7):
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    import matplotlib.ticker as mtick

    fig, ax = plt.subplots(figsize=(14, 6))

    # Plot original series
    ax.plot(pnl_series.index, pnl_series.values, label='Daily PnL', alpha=0.4, linewidth=1.2)

    # Optional rolling average for clarity
    if rolling_days:
        rolling = pnl_series.rolling(rolling_days).mean()
        ax.plot(rolling.index, rolling.values, label=f'{rolling_days}-Day Avg', linewidth=2.5)

    ax.set_title(title, fontsize=16, weight='bold')
    ax.set_ylabel("PnL (€)", fontsize=12)
    ax.yaxis.set_major_formatter(mtick.StrMethodFormatter('€{x:,.0f}'))

    # Format x-axis ticks
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    ax.tick_params(axis='x', rotation=0)

    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend()
    plt.tight_layout()
    plt.show()
if __name__ == '__main__':

    ppa_wind = PPA(id= 9529244,techno='WIND', capacity=10.0)
    mylogger.logger.info(f'SHAPE ID Delta : {ppa_wind.DeltaShapeID()}')
    # ppa_wind.ShapeIDRisk()
    ppa_wind.plot_mtm_vs_forward_price(central_price=62, delta=40, step=5, year="2026", return_df=False)

    ppa_wind.show_pnl()
    ppa_wind.showPowerCurve()
    ppa_solar = PPA(techno="SR", capacity=10.0)
    ppa_solar.buildProxy()
    ppa_solar.buildMark()
    ppa_solar.ShapeIDRisk()
    ppa_solar.showPowerCurve()
    ppa_wind.computeShape()
    ppa_wind.computeIntermitencyValue()
    df_quarter = ppa_wind.computeCaptureRateQuarter()
    df_year = ppa_wind.computeCaptureRateYearly()


    ppas = [ppa_solar, ppa_wind]
    for ppa in ppas:
        mylogger.logger.info(ppa.id)
        ppa.buildProxy()
        ppa.buildMark()
        ppa.showPowerCurve()
        # ppa.saveInstance()
