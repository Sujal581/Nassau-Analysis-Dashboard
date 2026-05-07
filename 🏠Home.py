import streamlit as st
from data_manager import init_data

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_icon="🍪",
    page_title="Nassau Candy | Wholesale Candy",
    layout="wide",
    initial_sidebar_state="collapsed"   
)

#----Slidebar Style (DARK MODE)----
st.sidebar.title("🍬 Nassau Candy")

#----Title Style (DARK MODE)----
st.markdown("# Nassau Candy | Wholesale Candy", unsafe_allow_html=True)
# ---------------- MAIN CONTENT ----------------
st.markdown("""
#### 🏢 About Nassau Candy

**Nassau Candy** is a leading manufacturer, importer, and distributor of wholesale candy and specialty food.  
For over **80+ years**, we have been serving the industry with premium-quality products.

We offer a wide range of:

- 🍫 Chocolate & Bulk Candy  
- 🍭 Specialty Sweets & Confectionery  
- 🥤 Gourmet Soda & Beverages  
- 🌰 Dried Fruits, Nuts & Natural Foods  
- 🧴 Natural Health, Beauty & Household Care  

---

### 🏭 Our Brands & Products

Our catalog includes **25,000+ products**, featuring global brands such as:

- Jelly Belly®  
- Godiva®  
- Ghirardelli®  
- Lindt®  

We also produce exclusive in-house brands like:
- Clever Candy®  
- Nancy Adams®  

---

### 🎃 Seasonal & Specialty Collections

We are known for rare and nostalgic candy collections, including:

- 🎃 Halloween Candy  
- 🎄 Christmas Candy  
- 💘 Valentine’s Day Candy  
- 🐣 Easter Candy  

---

### 🏭 Manufacturing Excellence

Nassau Candy is also a **candy manufacturer**, with production facilities in Hicksville, NY and global partners.  
This allows us to deliver **handcrafted-quality products at scale**.

---

### 🚚 Nationwide Distribution

With **6 distribution centers across the USA**, we ensure:

✔ Fast delivery  
✔ High availability  
✔ Industry-leading logistics performance  

---

### 📰 Learn More

📌 *Visit The Dish* — our official blog for:
- Candy trends  
- Product launches  
- Flavor forecasts  
- Merchandising tips  
""")

# ---------------- DATA INIT ----------------
init_data()
st.success("✅ Data Loaded")

st.info("Use the sidebar to navigate and apply filters.")