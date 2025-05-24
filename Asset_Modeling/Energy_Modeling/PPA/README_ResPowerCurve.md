# 🌞🌬️ Building Solar & Wind Power Curves

## 🎯 Purpose

To estimate the **expected generation volume of renewable assets**, it is essential to develop robust models that convert input weather data into output power.  
This document outlines the methodology for modeling **solar** and **wind** power generation using two key inputs:

- ☀️ **Solar Radiation**  
- 💨 **Wind Speed**

---

## ☀️ Solar Power Curve

### 🗺️ Location

- **Example Site**: Montluçon, France  
- **Data Source**: [Global Solar Atlas – Montluçon](https://globalsolaratlas.info/detail?c=46.34003,2.607396,11&m=site&s=46.34003,2.607396)

<p align="center">
  <img src="https://github.com/user-attachments/assets/7e19ce3f-4250-46fd-91cd-8afba313d7ed" width="500"/>
  <br/>
  <em>Figure 1 – Solar radiation profile for Montluçon from the Global Solar Atlas.</em>
</p>

Each renewable asset has a **specific power curve**, shaped by factors such as:
- Geographic location
- Panel orientation and tilt
- Technology (e.g., PV type, inverter specs)
- Aging, materials, and degradation

---

### ⚙️ Methodology

The Global Solar Atlas provides **monthly-hourly average capacity factors**.  
To align this with real weather data (solar radiation in Montluçon), we computed:

1. The **monthly average hourly solar radiation** from historical records  
2. A **scatter plot** of load factors vs. radiation

<p align="center">
  <img src="https://github.com/user-attachments/assets/1b1ea9d5-82b8-476a-b7d1-82e969a5760e" width="500"/>
  <br/>
  <em>Figure 2 – Scatter plot of average load factors vs. solar radiation for Montluçon.</em>
</p>

A **polynomial regression** was then fitted to the data to generate the power curve model:

<p align="center">
  <img src="https://github.com/user-attachments/assets/05dac703-13a2-4eb1-9478-15c7580ca299" width="500"/>
  <br/>
  <em>Figure 3 – Polynomial regression curve fitting load factor to solar radiation.</em>
</p>

✅ The final model predicts the expected power output for a given solar radiation input.

---

## 🌬️ Wind Power Curve

### 🌍 Resource Data

- **Data Source**: [Global Wind Atlas](https://globalwindatlas.info/en/)

In this case, the **wind power curve** was directly obtained from the Global Wind Atlas, without the need for transformation:

<p align="center">
  <img src="https://github.com/user-attachments/assets/2a158614-d506-4465-ac72-544bebe11ee7" width="500"/>
  <br/>
  <em>Figure 4 – Wind power curve directly sourced from the Global Wind Atlas.</em>
</p>

---

## ✅ Summary

- 🔧 **Solar Curve**: Modeled using polynomial regression between radiation and load factors.
- 📦 **Wind Curve**: Directly sourced and ready to use.
- 📈 Both models are now applicable to forecast hourly renewable generation using weather input data.

---

## 👤 Author

**Hugo Lambert** – Energy Forecasting & Market Modeling  
Feel free to reach out hugo.lambert.perso@gmail.com
