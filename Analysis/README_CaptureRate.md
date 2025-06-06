# 📊 Capture Rate Evolution – French Market

<p align="center">
  <img src="https://github.com/user-attachments/assets/868c4f5d-8ad9-4b51-9259-2083302689f2" alt="Yearly Capture Rate" width="800">
</p>
<p align="center"><em>Figure: Yearly Capture Rate Evolution – France</em></p>

Until 2020, wind and solar assets in France consistently achieved capture rates above 93.6% and 92.7%, respectively. During this period, wind capacity grew by 60%, from 10.3 GW to 16.5 GW, while solar capacity expanded by 54%, rising from 6.1 GW to 9.4 GW.

Since 2020, renewable capacity has continued to rise, reaching 26 GW for wind and 21 GW for solar, representing additional growth of 58% and 123%, respectively. This surge has had a significant impact on capture rates, which have declined sharply: solar fell to 68% in 2024, and wind dropped below 90%.

<p align="center">
  <img src="https://github.com/user-attachments/assets/3060ffe0-ab56-469b-83e7-bc26a6ce073e" alt="Monthly Capture Rate 1" width="800">
  <br><br>
  <img src="https://github.com/user-attachments/assets/f27aea44-bcb0-4833-ac36-b98321ba2248" alt="Monthly Capture Rate 2" width="800">
</p>
<p align="center"><em>Figure: Monthly Capture Rate Evolution – France</em></p>

---

# 💰 RES Market Value

<p align="center">
  <img src="https://github.com/user-attachments/assets/77236af0-96fd-45f0-a2f0-27e4adcef7e1" alt="RES Market Value" width="800">
</p>
<p align="center"><em>Figure: RES Market Value over Generation</em></p>

The chart above highlights the impact of RES penetration on market value and illustrates the **cannibalization effect**. Up to ~5 GW of generation, both wind and solar maintain a value close to the linear base generation. Beyond that threshold, wind value declines gradually, while solar value drops steeply past 10 GW.

Two main factors explain this divergence in France:

- **Seasonality**: Wind generation peaks in winter when demand and prices are higher.
- **Geographic dispersion**: Wind assets are more distributed across regions, facilitating exports at favorable prices, unlike solar.

<p align="center">
  <img src="https://github.com/user-attachments/assets/8c7b2a81-dd18-452d-9814-7e3511bfbd08" alt="RES Market Value %" width="800">
</p>
<p align="center"><em>Figure: RES Market Value (as % of Base) vs. Generation</em></p>

---

# ⏱️ Intraday Price Shape

To remove the impact of absolute price levels (e.g. the 2022 crisis), we normalize hourly prices by dividing each data point by the corresponding annual average. This centers each curve around 1.0, allowing a clearer comparison of shape over time.

<p align="center">
  <img src="https://github.com/user-attachments/assets/62591592-20c4-4aea-a523-19db99cb9a01" alt="Normalized Hourly Prices" width="800">
</p>
<p align="center"><em>Figure: Normalized Hourly Average Prices</em></p>

The chart reveals the **duck curve effect**, a distortion of hourly price profiles driven by solar generation. As solar ramps up during midday, prices dip, then rise again in the evening as solar fades and demand peaks. This creates the classic “duck” shape: a low belly (noon) and high head/tail (morning/evening).

<p align="center">
  <img src="https://github.com/user-attachments/assets/e011703c-0b0e-41cb-9932-1d8861623138" alt="Duck Value" width="800">
</p>
<p align="center"><em>Figure: Duck Value Evolution Over Time</em></p>

To quantify this effect, we define the **DuckValue** metric:  
> DuckValue = AVG Morning & Evening Peak – Midday Dip

This indicator was stable between 0.24 and 0.36 until 2022, then jumped to **0.50 in 2023** and **0.77 in 2024**, representing increases of 39% and 139%, respectively. These sharp changes reflect the growing impact of solar on intraday market dynamics.
