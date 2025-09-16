# Retail Sales Exploratory Data Analysis (EDA)

## 📌 Project Overview
This project performs an **Exploratory Data Analysis (EDA)** on an Online Retail dataset to understand customer behavior and business trends.  
We analyze sales transactions, clean the data, generate descriptive statistics, and create meaningful visualizations.  
Finally, we extract **6 key business insights** to guide decision-making.

---

## 🛠️ Tech Stack
- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Jupyter Notebook

---

## 📂 Dataset
- **Source**: [Kaggle - Online Retail Dataset](https://www.kaggle.com/datasets)  
- **Columns**:
  - `InvoiceNo` → Transaction ID  
  - `StockCode` → Product code  
  - `Description` → Product description  
  - `Quantity` → Units purchased  
  - `InvoiceDate` → Date & time of purchase  
  - `UnitPrice` → Price per item  
  - `CustomerID` → Unique customer identifier  
  - `Country` → Customer’s country  

---

## 🚀 Steps Performed
1. **Load Data** → Using `pandas` from Excel/CSV.  
2. **Data Cleaning** → Handle missing values, drop duplicates, remove negative quantities, convert date fields.  
3. **Feature Engineering** → Added `TotalPrice = Quantity × UnitPrice`.  
4. **Descriptive Statistics** → Mean, median, std. deviation of key fields.  
5. **Visualizations** → 
   - Histogram of sales  
   - Bar chart (Top products & countries)  
   - Line chart (sales over time)  
   - Distribution of order values  
   - Repeat vs one-time customers pie chart  
   - Hourly sales trend  
6. **Insights Extraction** → Automated script to summarize key business insights.  

---

## 📊 Key Business Insights
1. Top revenue comes from **United Kingdom** (~ £9M).  
2. Best-selling product is **DOTCOM POSTAGE** (~ £206K).  
3. Peak sales occurred in **Nov 2011** (~ £1.5M).  
4. Average Order Value (AOV) ≈ **£533**.  
5. ~**65%** of customers are **repeat buyers**.  
6. Peak purchasing time is around **10:00 AM**.  

---

## 📷 Example Visualizations
- Top countries by revenue  
- Top 10 products by revenue  
- Monthly sales trend  
- Distribution of order values  
- Repeat vs one-time customers  

---

## 📌 Expected Outcome
- A clean Jupyter Notebook with:  
  - Data preparation  
  - Visualizations  
  - Business insights  
- Useful for business analysts, data scientists, and retail companies.  

---

## ▶️ How to Run
1. Clone this repo or download files.  
2. Install required libraries:
   ```bash
   pip install pandas numpy matplotlib seaborn
