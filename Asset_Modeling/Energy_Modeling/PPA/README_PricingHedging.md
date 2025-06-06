# 🌱 PPA Pricing – What Is the Fair Price of a PPA? (ongoing)

A **Power Purchase Agreement (PPA)** is a contract between a renewable energy producer and an energy buyer (**offtaker**), ensuring the purchase of the renewable output at a predetermined price. This arrangement provides multiple benefits for both parties.

> **Producers** gain long-term price certainty.  
> **Offtakers** meet decarbonization goals or hedge future energy costs.

However, it also implies a transfer of operational and market risks to the offtaker.

---

## ⚙️ Typical PPA Structure

We consider the most common structure: a **fixed-price, as-produced PPA**.

- Each MWh is sold at the agreed **fixed price**.
- The **offtaker bears all risks**, including:
  - **Intermittency** (profile risk)
  - **Volume uncertainty** (volume risk)
  - **Mismatch with price patterns** (shape risk)

### 💰 PPA Payoff

The payoff is calculated as:

**PPA_Payoff = Σᵢ Volume_produced(i) × (Price_spot(i) − Price_fixed)**

The offtaker **earns or loses money** depending on spot prices relative to the fixed price.

---

## 📊 Pricing Approaches

There are three main methodologies:

---

### 🔍 1. Expected Payoff (Risk-Neutral / Monte Carlo)

This **probabilistic method** uses stochastic simulations of both price and generation.

**P_PPA = E[ Σₜ P_market(t) × Q(t) × DF(t) ] / E[ Σₜ Q(t) × DF(t) ]**

Where:

- **Q(t)**: stochastic generation at time t  
- **P_market(t)**: market price at time t  
- **DF(t)**: discount factor at time t

✅ Accounts for correlation between price and generation.  
⚠️ Requires heavy modeling infrastructure.

---

### 🧾 2. Forward Curve Weighted Average (Deterministic)

A **simplified method** using expected generation and forward prices.

**P_PPA = Σₜ P_fwd(t) × Q(t) / Σₜ Q(t)**

Where:

- **P_fwd(t)**: forward price at time t  
- **Q(t)**: expected (non-stochastic) generation

✅ Simple and fast.  
⚠️ Doesn’t consider price-production correlation.

---

### 📈 3. Historical Resampling (Capture Rate Approach)

Uses **historical data** to estimate PPA price based on real performance.

#### 📏 Capture Rate

**Capture Rate = (VWAP − Average Market Price) / Average Market Price**

Where:

- **VWAP = Σₜ P_spot(t) × Q(t) / Σₜ Q(t)**  
- **Average Market Price** = arithmetic mean of P_spot(t)

#### 🎯 Fair Price

**P_PPA = P_capture × (1 − Risk Premiums)**

Reflects actual market conditions.  
Allows adjusting for profile, shape, and volume risks.

---

## 🔍 Capture Rate Method – In Depth

This document focuses on this method due to its **transparency** and **practicality**.

### ✅ Why Use It?

- **Data-driven**: Based on real or modeled past performance.
- **Earning potential**: Shows how well an asset captures price peaks.
- **Risk decomposition**: Useful for offtakers to understand and manage risks.

### 📉 Risk Management Insights

| Risk Type     | Mitigation Strategy                      |
|---------------|-------------------------------------------|
| Shape Risk    | Diversify with wind + solar               |
| Volume Risk   | Use battery storage or flexible loads     |
| Price Risk    | Hedge via market access (e.g., intraday)  |

> 💡 By actively managing risks, an offtaker can **lower applied premiums** and offer more competitive pricing.

---

## ✅ Conclusion

The fair price of a PPA is a function of:

- **Expected production and prices**
- **Correlation between them**
- **Risk management capabilities of the offtaker**

### Summary Table

| Method        | Pros                          | Cons                          |
|---------------|-------------------------------|-------------------------------|
| Monte Carlo   | Accurate, captures correlation| Complex, infra-heavy          |
| Forward Curve | Fast, simple                  | Ignores correlation           |
| Capture Rate  | Practical, risk-adjustable    | Depends on good historical data |

> 🎯 The **Capture Rate** approach offers a **balanced**, **customizable**, and **realistic** view for modern PPA pricing.
