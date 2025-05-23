# 🌞🌬️ Renewable Power Generation Forecast – Day-Ahead

This project aims to **forecast day-ahead wind and solar power generation** to reconstruct the **global power stack** and support a **fundamental-based price forecast** for electricity markets.

---

## 🧠 Objective

The primary goal is to model and forecast the renewable power output for the next day based on weather forecasts. This includes:

- Forecasting **solar** and **wind** generation using machine learning.
- Combining this with consumption forecasts to estimate the **power stack**.
- Enabling a **fundamental pricing model** for day-ahead markets.

---

## 📦 1. Data Sources

### 🌤️ Weather Data
- **Source**: Open-Meteo API  
- **Storage**: Supabase (access via API)
- **Key features**:
[
'Solar_Radiation', 'Direct_Radiation', 'Diffuse_Radiation',
'Direct_Normal_Irradiance', 'Global_Tilted_Irradiance',
'Cloud_Cover', 'Cloud_Cover_Low', 'Cloud_Cover_Mid', 'Cloud_Cover_High',
'Temperature_2m', 'Relative_Humidity_2m', 'Dew_Point_2m', 'Precipitation',
'Wind_Speed_100m', 'Wind_Direction_100m', 'Wind_Gusts_10m',
'Surface_Pressure', 'SR_capa', 'WIND_capa'
]

### ⚡ Generation Data
- **Source**: ENTSO-E API  
- **Labels**: Historical **solar** and **wind** power generation  
- **Storage**: Supabase (separate table)

---

## 🧹 2. Data Cleaning

### ☀️ Solar Generation

**Challenge**: Solar generation data can include physical inconsistencies (e.g., production at night).

**Hybrid Outlier Detection Strategy**:
1. **Binning by Solar Radiation**:
 - Bins reflect different irradiation regimes: night, dawn/dusk, midday.
2. **Low Radiation (< 5 W/m²)**:
 - Any positive generation is flagged and removed (physically implausible).
3. **Moderate Radiation**:
 - **Interquartile Range (IQR)** filtering used:
   ```
   IQR = Q3 - Q1
   Outlier if x < Q1 - 1.5*IQR or x > Q3 + 1.5*IQR
   ```
4. **High Radiation**:
 - **Median Absolute Deviation (MAD)** method used:
   ```
   z = |x - median| / MAD
   Outlier if z > 4
   ```

SOLAR_Cleaning
---

### 🌬️ Wind Generation

**Challenge**: Affected by curtailment, noise, and inconsistencies.

**Two-Stage Outlier Detection**:
1. **Bin-wise IQR Filtering by Wind Speed**:
 - **Low Speeds (< 7 m/s)**: Any positive generation flagged.
 - **7–16 m/s**: Apply IQR method.
2. **Model-Based Residual Filtering**:
 - Fit a 3rd-degree polynomial regression:
   ```
   Y = a₀ + a₁x + a₂x² + a₃x³
   r = y - Y
   z = |r - median(r)| / MAD
   Outlier if z > 5
   ```
WIND_Cleaning
---

## 🤖 3. Model Training

- **Algorithms Used**: LightGBM / XGBoost  
- **No normalization** required due to tree-based models  
- Data cleaning is applied prior to training

### ✅ Model Pipeline
- Cleaned data is piped into training
- Model and pipeline saved in `.pkl` format for deployment

---

## 📈 4. Model Performance

**Best results after tuning and cleaning:**

| Model                      | Target | MAE    | RMSE   | R²    |
|---------------------------|--------|--------|--------|-------|
| `LGBMR_cleaned_tuned`     | WIND   | 639.42 | 836.27 | 0.875 |
| `LGBMR_cleaned_tuned`     | SOLAR  | 128.53 | 229.83 | 0.997 |

---

## 📊 5. Dashboard

Track daily forecasts against actuals in near-real time:

🔗 **[Forecast vs Realized Power Generation – France](https://hugzgj.grafana.net/public-dashboards/62cfe7d7ef9540aba9d6998bb255de5a)**  
> Compare ResPy's morning forecast, RTE’s evening forecast, and the final realized RES generation.

---

## 🛠️ Future Improvements

- Introduce normalization and feature scaling for advanced models (e.g., neural nets)
- Extend location coverage beyond central France
- Add dynamic capacity estimation from asset metadata or satellite imagery
- Integrate with electricity price forecasting module

---

## 🧾 License

MIT License — feel free to use and adapt the approach with proper attribution.

---

## 👤 Author

**Hugo Lambert** – Energy Forecasting & Market Modeling  
Feel free to reach out hugo.lambert.perso@gmail.com

