# 📊 Capture Rate Evolution – French Market

![Yearly capture rate evolution – France](image.png)

Until 2020, wind and solar assets in France had never shown capture rates below 93.6% and 92.7%, respectively. During that period, wind capacity increased by 60%, from 10.3 GW to 16.5 GW, and solar capacity grew by 54%, from 6.1 GW to 9.4 GW.

Since 2020, renewable energy capacity has continued to grow, reaching 26 GW for wind and 21 GW for solar today, corresponding to additional growth of 58% and 123%, respectively. This sharp increase in RES capacity has clearly impacted capture rates, which have dropped significantly: down to 68% for solar in 2024 and below 90% for wind.

![Monthly capture rate (France) – solar and wind](MonthlyCR.png)

![Monthly capture rate (France) – wind detailed](MonthlyCR2.png)

---

# 💰 RES Market Value

![RES market value decline with penetration](RESMV.png)

An interesting graph illustrates how RES penetration affects its market value and highlights the **cannibalization phenomenon**. Up to around 5 GW of generation, both wind and solar maintain a value close to the linear base generation. Beyond that point, wind value begins to decline gradually, whereas solar value drops much more sharply beyond 10 GW of generation.

There are two key explanations for this difference in France:

- Wind tends to be stronger in winter, when electricity demand and market prices are higher.
- Wind generation is more geographically dispersed than solar, allowing surplus wind power to be exported more easily and at better market prices.

![RES value decline vs installed capacity](RES%20VM2.png)

---

# ⏱️ ID Price Shape

The normalization process consists in dividing each data point by the corresponding yearly average across all hours, so that each curve is centered around a mean value of 1. This approach emphasizes the relative shape of the curves while removing the effect of absolute price levels, which were exceptionally high during the peak of the energy crisis in 2022.

![Normalized hourly price curves – Duck curve effect](Duck%20Curve.png)

Another graph illustrates the effect of renewable power penetration on hourly prices. By observing the normalized hourly average prices per year, the **duck curve effect** becomes evident. 

The **duck curve** refers to the distortion of the intraday electricity price or demand curve caused by high solar power generation during midday hours. As solar production ramps up, net demand (or market prices) drops significantly around noon, leading to a "dip" in the curve. In contrast, demand rises again in the early morning and evening when solar output is low, creating higher prices during these hours.

This pattern creates a curve that resembles the shape of a duck: a **dip in the middle** (belly) and **higher levels on both ends** (head and tail). The duck curve effect becomes more pronounced as solar penetration increases, highlighting the challenges of balancing supply and demand in systems with high shares of variable renewable energy.

![DuckValue – Difference between peak and midday normalized prices](DuckValue.png)

To evaluate the duck curve effect on prices, we define a simple metric called **DuckValue**, which measures the difference between average peak and midday dip normalized prices. The graph shows that this value remained relatively stable between 0.24 and 0.36 until 2022. However, starting in 2023, it surged to 0.50 and then to 0.77 in 2024, representing increases of 39% and 139%, respectively. This sharp rise reflects the growing impact of solar penetration on intraday price patterns.
