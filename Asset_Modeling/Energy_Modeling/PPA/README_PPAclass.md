# ⚡ PPA Class – Renewable Energy Contract Modeling

## 🎯 Purpose

The `PPA` class provides a robust framework for modeling **Power Purchase Agreements (PPAs)** and managing **Renewable Energy Source (RES)** portfolios. It enables:

- Simulation of renewable generation profiles  
- Quantification of production risks (e.g., p50, p90)  
- Evaluation of market capture and revenue potential  
- Valuation of contracts under different pricing structures  

---

## 🏗️ Class Structure

Each `PPA` instance includes the following key attributes:

| Attribute       | Description                                                                 |
|----------------|-----------------------------------------------------------------------------|
| `id`           | Unique identifier for the PPA                                                |
| `site_name`    | Name of the renewable generation site                                        |
| `start_date`   | Contract start date                                                          |
| `end_date`     | Contract end date                                                            |
| `capacity`     | Installed capacity in megawatts (MW)                                         |
| `techno`       | Technology type (`solar`, `wind`, etc.)                                      |
| `pricing_type` | Pricing model (`fixed`, `floating`, etc.)                                    |
| `country`      | Country of operation                                                         |
| `proxy`        | Time series representing simulated or historical past generation             |
| `mark`         | Time series representing simulated future generation                         |
| `p50`          | Expected annual generation at a 50% probability level (MWh)                  |

---

## 🧮 Method: `buildProxy()`

The `buildProxy()` method constructs a **generation proxy** for the asset. It can be built from:

- **Historical data**: Cleaned and time-aligned actual production records  
- **Synthetic data**: Modeled generation using weather inputs and power curves

### 🔍 Why It Matters

> The *timing* of generation is just as important as the *volume*.

A plant producing during peak price hours generates more revenue than one producing during low-price periods. The proxy enables:

- Estimation of expected volumes (e.g., p50)
- Backtesting revenue capture using historical price curves
- Comparison of pricing scheme impacts (e.g., fixed vs floating)

---

<p align="center">
  <img src="https://github.com/user-attachments/assets/13b2298c-675b-4992-aa81-77600e53d896" alt="PROXY WIND" width="400">
  <img src="https://github.com/user-attachments/assets/b660b018-b297-484f-ba4e-a7972f37ce1f" alt="PROXY SOLAR" width="400">
  <br/>
  <em>Figure: Examples of WIND and SOLAR generation proxies</em>
</p>

To construct a proxy, a power curve must first be defined for the asset. The full methodology is documented here:

🔗 [🌞🌬️ Building Solar & Wind Power Curves](./README_ResPowerCurve.md)

Once the power curve is established, it is applied to the **hourly weather history** of the site to simulate a historical generation profile — referred to as the **proxy**.

---

## 👤 Author

**Hugo Lambert** – Energy Forecasting & Market Modeling  
Feel free to reach out hugo.lambert.perso@gmail.com
