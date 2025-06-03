# ⚡ Building a Forward Hourly Power Curve

## 🧠 Objective

The objective of this work is to construct a **forward power price curve with hourly granularity**.  
Previously, I developed a daily forward price curve, focusing on capturing **seasonality and daily patterns**.

To go further, this approach aims to extend that logic by incorporating **intraday (hourly) patterns**, derived from historical data.  
The methodology remains consistent: leverage **normalized historical shapes** to reflect structural behavior.

🔗 [Learn more about the Daily Forward Curve Methodology](./Model/ForwardPowerCurve/README_DailyPowerCurve.md)

Since the daily forward curve already embeds **seasonality** and **weekday effects**, the remaining task is to **capture and apply realistic hourly behavior** to expand the daily structure into an hourly one.

---

## 📅 Price Level Analysis

Let’s examine two structurally identical days — **January 5th** from different years:

<p align="center">
  <img src="https://github.com/user-attachments/assets/c9d92cab-e4b8-4d81-a5ec-a3e6ccdf4109" alt="Power prices January 5th, 2015" width="400">
  <img src="https://github.com/user-attachments/assets/77bff67f-44ad-4801-b9f0-cfc1fbbbb481" alt="Power prices January 5th, 2024" width="400">
</p>
<p align="center"><em>Figure: Intraday power price profiles — same shape, different levels.</em></p>

As shown above, while **absolute price levels vary significantly**, the **intraday shape remains similar**.  
This structural consistency is what we aim to extract and reproduce.

---

## ⚙️ Methodology Overview

### ✅ Step 1: Normalize Hourly Prices by Daily Mean

To isolate the **intraday structure**, each hour's price is divided by the corresponding **daily mean**.  
This removes level bias and highlights the relative shape of price movements.

<p align="center">
  <img src="https://github.com/user-attachments/assets/e2bfb3ec-7041-4c76-82b4-da8e20867783" alt="Normalized Jan 5, 2015" width="400">
  <img src="https://github.com/user-attachments/assets/64ba88fc-42ec-4e7f-9781-7e9a56c62397" alt="Normalized Jan 5, 2024" width="400">
</p>
<p align="center"><em>Figure: Normalized intraday shape — January 5th, 2015 & 2024.</em></p>

---

### 🕰️ OLD VERSION — Step 2: Compute Average Hourly Shape per Month

> ⚠️ **Note**: This was the original method for generating monthly profiles. It simply averages all normalized hourly values per month, without selecting representative days.

We compute the **average normalized price for each hour of the day**, grouped by month.  
This produces a **monthly 24-hour profile**, which reflects the average intraday behavior for each calendar month.

<p align="center">
  <img src="https://github.com/user-attachments/assets/1f6ec805-5181-4486-bc57-6fe08d5ddf41" alt="Monthly Normalized Hourly Profiles" width="600">
</p>
<p align="center"><em>Figure: Normalized hourly profiles by month (old method).</em></p>

---

### ✨ NEW VERSION - Step 2: Quantile-Based Shape Extraction

> ✅ **Improved approach**: Instead of averaging all days, this method selects the **most representative daily profiles** based on a quantile filter and smooths the result by averaging the top 5 closest days per `(month, hour)`.

### ⚙️ Core Idea

Rather than taking a simple average over all days, the function:

- Normalizes each day's hourly prices to remove absolute price level effects  
- Emphasizes low-price periods (dips in the curve) using an asymmetric transformation:

```python
df['normalized_modified'] = np.where(df['normalized'] < 1, 2 - df['normalized'], df['normalized'])
```

- Selects the top 5 days per `(month, hour)` that best match a reference quantile shape  
- Averages the normalized shapes of these selected days to produce a smooth, robust intraday profile

<p align="center">
  <img src="https://github.com/user-attachments/assets/168e4eaf-2152-42c6-a5f5-2d4a6ef818ab" alt="Monthly Normalized Hourly Profiles" width="600">
</p>

<p align="center"><em>Figure: Normalized hourly profiles by month.</em></p>

### 🧪 Quantile Parameter & Volatility Metric

This new method improves robustness by using the 50th percentile (median) by default instead of the mean, which tends to be distorted by extreme spikes.

It also introduces the ability to **backtest different quantile values**, offering a new parameter that can influence the valuation of shaped assets such as wind and solar plants.

This parameter defines the concept of **intraday shape volatility** — a metric that captures the sharpness and variability of hourly price curves.

<p align="center">
  <img src="https://github.com/user-attachments/assets/4432107c-46a0-4389-a76b-415d462a0275" alt="Hourly Profiles vs Shape ID Volatility" width="600">
</p>

<p align="center"><em>Figure: Hourly Profiles vs Shape ID Volatility.</em></p>

### 📊 Use Cases & Benefits

- Captures more **representative daily patterns** by avoiding distortion from outliers  
- Enables **quantile tuning** to adjust shape sensitivity and asset pricing dynamics  
- Supports robust modeling for:
  - Power Purchase Agreements (PPAs)  
  - Renewable asset optimization  
  - Shape hedging and structured product pricing

---

### ✅ Step 3: Expand Daily Curve into Hourly Resolution

With normalized hourly profiles per month established, we apply them to the daily forward curve using the following formula:

```math
\text{Hourly Price}_{d,h} = \text{Normalized Shape}_{m,h} \times \text{Forward Daily Price}_d
```

Where:
- \( d \): the day in the forward curve  
- \( h \): the hour (0–23)  
- \( m \): the month corresponding to day \( d \)

This results in a **high-resolution hourly forward curve** that is:
- Consistent with market price expectations (via daily forwards)
- In line with historical intraday behavior (via normalized monthly profiles)

---

### 🔁 Transformation Overview

#### 📥 Input: Daily Forward Curve  
<p align="center">
  <img src="https://github.com/user-attachments/assets/6c73d62c-913f-4258-ab69-d23f18a09e9c" width="600">
</p>

#### 🔄 Apply Monthly Hourly Shape

#### 📤 Output: Hourly Forward Curve  
<p align="center">
  <img src="https://github.com/user-attachments/assets/774877fd-6a07-4a14-88bb-b6311c60a777" width="600">
</p>

---

## ✅ Summary

This method provides a powerful and flexible way to:

- 📊 Generate **hourly forward price curves** using only daily forward data
- 🧠 Preserve **realistic intraday dynamics** derived from historical behavior
- 🔄 Reflect **seasonal adaptation** through monthly normalization

This framework is well-suited for use cases like **short-term forecasting**, **asset valuation**, **hedging**, and **dispatch optimization**.

---

## 👤 Author

**Hugo Lambert** – Energy Forecasting & Market Modeling  
Feel free to reach out hugo.lambert.perso@gmail.com
