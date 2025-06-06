import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import matplotlib.ticker as mtick
import matplotlib.dates as mdates
from matplotlib import pyplot as plt

sns.set_theme(style="whitegrid")
plt.rcParams.update({
    'axes.titlesize': 16,
    'axes.labelsize': 12,
    'legend.fontsize': 11,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'axes.titleweight': 'bold'
})


def DAauctionplot(df, title='Price Curve and Value Histogram', show=True):
    fig, ax1 = plt.subplots(figsize=(12, 6))

    ax1.plot(df['datetime'], df['price'], label='Price', linestyle='-', linewidth=2, color='blue')
    ax1.set_ylabel('Price (€/MWh)', color='blue')
    ax1.set_xlabel('Datetime')
    ax1.tick_params(axis='y', labelcolor='blue')

    ax2 = ax1.twinx()
    if len(df['datetime']) > 1:
        delta = (df['datetime'].iloc[1] - df['datetime'].iloc[0]).total_seconds()
        bar_width = delta / (24 * 60 * 60) * 0.8
    else:
        bar_width = 0.03

    ax2.bar(df['datetime'], df['value'], alpha=0.4, color='orange', label='Value', width=bar_width)
    ax2.set_ylabel('Value (MW)', color='orange')
    ax2.tick_params(axis='y', labelcolor='orange')

    fig.autofmt_xdate()
    ax1.grid(True, linestyle='--', alpha=0.6)
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    plt.title(title)
    plt.tight_layout()
    if show:
        plt.show()
    return fig


def ForecastGenplot(df, title='RES Forecast Generation', show=True):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df.index, df['WIND'], label='Wind', color='green', linewidth=2)
    ax.plot(df.index, df['SR'], label='Solar', color='orange', linewidth=2)
    ax.set_ylabel('Power Generation (MW)')
    ax.set_xlabel('Datetime')
    ax.grid(True, linestyle='--', alpha=0.6)
    fig.autofmt_xdate()
    ax.legend(loc='upper left')
    plt.title(title)
    plt.tight_layout()
    if show:
        plt.show()
    return fig


def plot_pnl_hist(pnl_series, title="PPA Payoff"):
    fig, ax = plt.subplots(figsize=(12, 6))
    color = "#2ca02c" if pnl_series.sum() >= 0 else "#d62728"
    pnl_series.plot(kind='bar', color=color, ax=ax, width=0.8)
    ax.set_title(title)
    ax.set_xlabel("Date")
    ax.set_ylabel("PnL (€)")
    ax.yaxis.set_major_formatter(mtick.StrMethodFormatter('€{x:,.0f}'))
    ax.tick_params(axis='x', rotation=45)
    ax.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()


def plot_pnl_timeseries(pnl_series, title="PPA Daily Payoff", rolling_days=7):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(pnl_series.index, pnl_series.values, label='Daily PnL', alpha=0.4, linewidth=1.2, color='blue')
    if rolling_days:
        rolling = pnl_series.rolling(rolling_days).mean()
        ax.plot(rolling.index, rolling.values, label=f'{rolling_days}-Day Avg', linewidth=2.5, color='black')
    ax.set_title(title)
    ax.set_ylabel("PnL (€)")
    ax.yaxis.set_major_formatter(mtick.StrMethodFormatter('€{x:,.0f}'))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    ax.tick_params(axis='x', rotation=0)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend()
    plt.tight_layout()
    plt.show()


def plotMtM(central_price, df, year):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df["forward_price"], df["mtm"], marker='o', linewidth=2, label="MtM vs Forward Price", color='blue')
    ax.axvline(central_price, color='black', linestyle=':', linewidth=1, label="Central Price")
    ax.axhline(0, color='grey', linestyle='--', linewidth=1)
    ax.scatter(central_price, df[df["forward_price"] == central_price]["mtm"].values[0],
               color='red', zorder=5, label=f"MtM @ {central_price} €/MWh")
    ax.set_title(f"MtM vs Forward Price – CAL {year}")
    ax.set_xlabel("Forward Price (€/MWh)")
    ax.set_ylabel("MtM (€)")
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend()
    plt.tight_layout()
    plt.show()


def plot_hedge(df, year):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df["forward_price"], df["mtm_ppa"], label="MtM PPA", linewidth=2, color='blue')
    ax.plot(df["forward_price"], df["mtm_hedge"], label="MtM Hedge", linestyle='--', linewidth=2, color='orange')
    ax.plot(df["forward_price"], df["mtm_total"], label="MtM Total", linewidth=2, marker='o', color='green')
    ax.axhline(0, color='grey', linestyle='--', linewidth=1)
    ax.set_title(f"Hedged MtM vs Forward Price – CAL {year}")
    ax.set_xlabel("Forward Price (€/MWh)")
    ax.set_ylabel("MtM (€)")
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend()
    plt.tight_layout()
    plt.show()


def plotShapeIDRisk(deltas, shape_intraday_vols):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(shape_intraday_vols, deltas, label='Shape Volatility vs PnL', color='blue', linewidth=2)
    ax.set_title('Pnl Impact for Change in Shape Intraday Volatility')
    ax.set_xlabel('Shape Intraday Volatility')
    ax.set_ylabel('PnL (€)')
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend()
    plt.tight_layout()
    plt.show()


def plot_PriceVolume(df):
    fig, ax1 = plt.subplots(figsize=(12, 6))
    ax1.bar(df.index, df['generation'], label='Generation', alpha=0.6)
    ax1.set_ylabel('Generation')
    ax1.set_xlabel('Time')
    ax2 = ax1.twinx()
    ax2.plot(df.index, df['price'], color='red', label='Price', linewidth=2)
    ax2.set_ylabel('Price')
    plt.title('Generation (bar) and Price (line) Over Time')
    fig.legend(loc='upper right', bbox_to_anchor=(1, 1), bbox_transform=ax1.transAxes)
    plt.tight_layout()
    plt.show()
