import matplotlib.pyplot as plt
import pandas as pd

def DAauctionplot(df, title='Price Curve and Value Histogram', show=True):
    fig, ax1 = plt.subplots(figsize=(10, 5))

    # Plot price curve (line)
    ax1.plot(df['datetime'], df['price'],
             label='Price',
             linestyle='-',
             linewidth=2,
             color='blue')
    ax1.set_ylabel('Price', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    ax1.set_xlabel('Datetime')

    # Create second axis for value bars
    ax2 = ax1.twinx()

    # Compute dynamic bar width (optional polish)
    if len(df['datetime']) > 1:
        delta = (df['datetime'].iloc[1] - df['datetime'].iloc[0]).total_seconds()
        bar_width = delta / (24 * 60 * 60) * 0.8  # fraction of a day
    else:
        bar_width = 0.03

    # Plot histogram as bar
    ax2.bar(df['datetime'], df['value'],
            alpha=0.4,
            color='orange',
            label='Value',
            width=bar_width)
    ax2.set_ylabel('Value', color='orange')
    ax2.tick_params(axis='y', labelcolor='orange')

    # Grid and layout
    ax1.grid(True, which='major', linestyle='--', alpha=0.6)
    fig.autofmt_xdate()
    plt.title(title)
    fig.tight_layout()

    # Optional legend (blue + orange)
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    if lines_1 or lines_2:
        ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left')

    if show:
        plt.show()
    return fig

def ForecastGenplot(df, title='RES Forecast Generation', show=True):
    fig, ax1 = plt.subplots(figsize=(10, 5))

    # Plot price curve (line)
    ax1.plot(df.index, df['WIND'],
             label='Wind',
             linestyle='-',
             linewidth=2,
             color='green')
    ax1.plot(df.index, df['SR'],
             label='Solar',
             linestyle='-',
             linewidth=2,
             color='orange')
    ax1.set_ylabel('Power Generation in MW')
    ax1.set_xlabel('Datetime')
    ax1.grid(True, which='major', linestyle='--', alpha=0.6)
    fig.autofmt_xdate()
    plt.title(title)
    fig.tight_layout()

    # Optional legend (blue + orange)
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    if lines_1:
        ax1.legend(lines_1, labels_1, loc='upper left')
    if show:
        plt.show()
    return fig
if __name__ == '__main__':
    data = pd.read_excel('h:/Downloads/DApriceES2023.xlsx')

