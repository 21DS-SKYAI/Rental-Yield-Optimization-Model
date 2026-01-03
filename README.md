# 🏙️ Rental Market Insight Engine  
**Micro-Market Based Rent Optimization**

A self-serve analytics app that helps landlords, brokers, and analysts  
**set the right rent using data instead of guesswork**.

Upload your property data → get instant insights on:
-  Micro-markets
-  Underpriced & overpriced properties
-  Optimal rent recommendations

---

## 🔍 Problem
Landlords often struggle with pricing:
- Set rent too high → property stays vacant  
- Set rent too low → revenue loss  

Most decisions are based on **locality averages**, which compare
*dissimilar properties* and lead to wrong pricing.

---

## 💡 Solution
This app uses **Machine Learning (K-Means clustering)** to:
- Group similar properties into **micro-markets**
- Compare each property only with its **true peers**
- Recommend an **optimal rent** based on market behavior

No technical knowledge required.

---

## 🧩 How It Works (Simple Flow)

1️⃣ Upload your rental property data (CSV / Excel)  
2️⃣ App creates **micro-markets** using location & property features  
3️⃣ Each property is benchmarked against similar properties  
4️⃣ App flags:
   - 🟢 Underpriced
   - ⚪ Fair
   - 🔴 Overpriced  
5️⃣ Optimal rent is calculated and displayed

---

## 📂 Required Data Format

Your file must contain the following **mandatory columns**:
latitude
longitude
carpet_area_sqft
monthly_rent

### Optional (recommended for better accuracy):
amenities_count
building_age


### Example CSV:
```csv
latitude,longitude,carpet_area_sqft,monthly_rent,amenities_count,building_age
19.02,72.84,750,85000,4,8
19.07,72.89,900,120000,6,3
18.98,72.82,600,65000,3,15

git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>

Install dependencies

pip install -r requirements.txt

 Run Streamlit-streamlit run app.py





