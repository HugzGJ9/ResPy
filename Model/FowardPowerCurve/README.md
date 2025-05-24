# 📈 Future Day-Ahead Power Curve Construction

## 🧠 Objective

To model a realistic **future daily Day-Ahead (DA) power price curve**, we use a **seasonal shaping model** based on **normalized historical price patterns**, scaled by current forward market expectations (e.g., calendar futures).

---

## 🔧 Methodology Overview

Historical DA prices exhibit significant variation due to exceptional events:  
![img.png](img.png)

However, for constructing a **forward curve**, the key objective is to extract **seasonal** and **daily** patterns and apply them to the **current market context**.  
To compare price dynamics across years meaningfully, we must first put all data on a **common scale**.

✅ **Solution: Normalization**

---

### Step 1: Normalize Historical Prices

We start by **normalizing** historical daily DA prices to remove distortions caused by absolute price levels (e.g., 2022 vs. 2020):

- **Normalization method**:  
  Scale each year's prices to a common range (e.g., min-max normalization or dividing by annual average).

- **Why not standardize?**  
  Standardization (`(x - mean) / std`) distorts the **shape** of the price curve.  
  Normalization preserves the relative seasonal and daily structure.

---

**Normalized data example:**  
![img_1.png](img_1.png)

---

### Step 2: Classify Historical Days

To capture **seasonality** and **weekly cycles**, we tag each historical day with:

- **Month** (1–12)  
- **Week-in-month** (1–5)  
- **Weekday** (0 = Monday, …, 6 = Sunday)

This enables alignment of structurally similar days across years — e.g., all **first Mondays of January**.

---

### Step 3: Compute the Average Shape

For each combination of `(month, week_in_month, weekday)`, we compute the **average normalized price**.

This yields a **representative daily shape** that captures:

- 🔁 Seasonal variation (monthly and intra-month)  
- 📆 Weekday vs. weekend effects  
- ✅ Intra-day patterns

The result is a **normalized daily profile** of a synthetic “average year”.

![img_2.png](img_2.png)

---

### Step 4: Scale with Forward Prices

We construct future DA power price curves by **repeating the normalized daily shape** and **scaling** it using calendar year forward prices:

Example:
```python
CAL = {
    '2026': 62.46,
    '2027': 60.18,
    '2028': 63.79
}
```

Each year's profile is scaled to match its respective forward price.

---

## ✅ Final Output

The final result is a **daily forward power price curve** that:

- Reflects **historical seasonality** and **weekday structure**  
- Aligns with **market expectations** from forward prices  
- Can be adapted for any horizon (**year**, **quarter**, **month**)

![img_3.png](img_3.png)

---

## 📫 Contact

For further information or collaboration inquiries:  
📧 **hugo.lambert.perso@gmail.com**
