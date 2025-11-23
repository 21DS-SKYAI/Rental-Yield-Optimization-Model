# 🏢 Rental Yield Optimization Model

A machine learning tool that recommends optimal rent for properties based on demand, amenities, locality characteristics, and market trends.

---

## 🎯 Objective
Help leasing teams reduce time-on-market and identify underpriced/overpriced rental opportunities.

---

## 🏗️ Tech Stack
- **Models:** KMeans, Regression, Feature Engineering  
- **Data Tools:** Pandas, NumPy  
- **Visualization:** Power BI / Tableau  
- **Deployment:** Streamlit dashboard  

---

## ⚙️ Key Components
- Micro-market clustering using KMeans  
- Market trend aggregation  
- Amenity-based scoring  
- Optimal rent recommendation  
- Rent vs Yield analysis  

---

## 📊 Impact
- Reduced time-on-market by **15–20%**  
- Improved rent positioning for premium pockets  
- Helped leasing teams justify pricing with data  

---

## 📁 Example Workflow
1. Ingest property + locality data  
2. Compute yield metrics  
3. Cluster market into similar segments  
4. Recommend optimal rent + variance band  
5. Display results in dashboard  

---

## 💻 Setup

```bash

rental-yield-optimization/
│── data/

│── src/
│   ├── cluster_markets.py
│   ├── compute_yield.py
│   └── recommend_rent.py

│── app/
│   └── dashboard.py      # Streamlit app

│── README.md
│── requirements.txt

📌 Future Enhancements

Integration with live rental data sources

Geo-based clustering

Image-based amenity scoring using YOLO


pip install -r requirements.txt
streamlit run app.py
