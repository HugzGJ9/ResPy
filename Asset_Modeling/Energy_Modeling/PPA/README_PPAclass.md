# ⚡ PPA Class – Renewable Energy Contract Modeling

## 🎯 Purpose

The `PPA` class is designed to provide a robust framework for modeling **Power Purchase Agreements (PPAs)** and **Renewable Energy Source (RES)** portfolios. It enables:

- Simulation of renewable asset generation profiles
- Quantification of production risks (e.g., p50, p90)
- Evaluation of market capture and revenue potential
- Estimation of contract valuation under different pricing structures

---

## 🏗️ Class Structure

Each `PPA` instance is defined by the following key attributes:

| Attribute       | Description                                                                 |
|----------------|-----------------------------------------------------------------------------|
| `id`           | Unique identifier of the PPA                                                 |
| `site_name`    | Name of the renewable site                                                  |
| `start_date`   | Contract start date                                                          |
| `end_date`     | Contract end date                                                            |
| `capacity`     | Installed capacity in megawatts (MW)                                         |
| `techno`       | Technology type (`solar`, `wind`, etc.)                                      |
| `pricing_type` | Pricing model (`fix`, `floating`, etc.)                                     |
| `country`      | Country of operation                                                         |
| `proxy`        | Time serie representing simulated or historical past generation                  |
| `mark`         | Time serie representing simulated future generation                                |
| `p50`          | Expected annual generation at 50% probability level (MWh)                    |

---

## 🧮 Method: `buildProxy()`

The `buildProxy()` method constructs a generation proxy for the renewable asset. This can be based on:

- **Historical data**: Cleaned, time-aligned real production records
- **Synthetic data**: Modeled generation based on weather inputs and asset characteristics

### 🔍 Why It Matters

> The *timing* of generation is just as critical as the *volume*.

A solar or wind park that produces during peak price hours will generate significantly more revenue than one producing at off-peak times. The proxy allows analysts to:

- Estimate expected volumes (e.g., p50)
- Backtest value capture under real price curves
- Compare different pricing scheme outcomes (e.g., fixed vs floating)

---

:Warn:
DOCUMENTATION TO BE EDITED.
🔗 [🌞🌬️ Building Solar & Wind Power Curves Documentation](./Asset_Modeling/Energy_Modeling/PPA/README_ResPowerCurve.md)

## 🎲 Realism & Noise Modeling

To enhance realism in synthetic generation:

- Add **normally distributed noise** to simulate measurement errors and operational variability
- This enhances the dataset's suitability for **backtesting and valuation stress-testing**

---

## ✅ Summary

The `PPA` class is a foundational module for simulating, analyzing, and valuing renewable energy contracts. It enables:

- 📊 Production risk analysis (e.g., p50, p90)
- 💰 Revenue and market capture forecasting
- ⚖️ Comparison of PPA pricing structures
- 🔍 Contract valuation under realistic scenarios

---

## 📫 Contact

For further information or collaboration inquiries:  
📧 **hugo.lambert.perso@gmail.com**
