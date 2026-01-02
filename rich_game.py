import streamlit as st
import pandas as pd
import random

# ==========================================
# 0. 基础配置 (防断裂版)
# ==========================================
st.set_page_config(page_title="World Owner", layout="wide", page_icon="👑")

st.markdown("""
<style>
    .stApp {background-color: #050505;}
    .asset-card {border: 1px solid #333; background: #111; border-radius: 12px; padding: 15px; margin-bottom: 20px;}
    h1,h2,h3 {color: #E5C1CD !important;} 
    div,p,span {color: #b0b0b0;}
    [data-testid="stImage"] img {object-fit: cover; aspect-ratio: 16/9; width: 100%; border-radius: 8px;}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 1. 核心图库 (短链接)
# ==========================================
# 这里的链接都缩短了，防止iPad复制中断
IMG = {
    "g63": "https://images.unsplash.com/photo-1520031441872-265149a9e6e5",
    "sl63": "https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8",
    "maybach": "https://images.unsplash.com/photo-1617788138017-80ad40651399",
    "cullinan": "https://images.unsplash.com/photo-1655132333039-47963d76756d",
    "phantom": "https://images.unsplash.com/photo-1631295868223-63265b40d9e4",
    "ferrari": "https://images.unsplash.com/photo-1592198084033-aade902d1aae",
    "lambo_suv": "https://images.unsplash.com/photo-1621996659490-6213b1859303",
    "lambo_car": "https://images.unsplash.com/photo-1544636331-e26879cd4d9b",
    "porsche": "https://images.unsplash.com/photo-1503376763036-066120622c74",
    "mclaren": "https://images.unsplash.com/photo-1621135802920-133df287f89c",
    "bugatti": "https://images.unsplash.com/photo-1627454820574-fb40e69228d4",
    "bmw": "https://images.unsplash.com/photo-1555215695-3004980adade",
    "audi": "https://images.unsplash.com/photo-1603584173870-7f23fdae1b7a",
    "suv": "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf",
    "gulfstream": "https://images.unsplash.com/photo-1540962351504-03099e0a754b",
    "bbj": "https://images.unsplash.com/photo-1583417319070-4a69db38a482",
    "bombardier": "https://images.unsplash.com/photo-1624623190870-1329dc334b07",
    "yacht_big": "https://images.unsplash.com/photo-1569263979104-865ab7cd8d13",
    "yacht_std": "https://images.unsplash.com/photo-1605281317010-fe5ffe79b9b4",
    "tower": "https://images.unsplash.com/photo-1512917774080-9991f1c4c750",
    "villa": "https://images.unsplash.com/photo-1613490493576-7fde63acd811",
    "watch": "https://images.unsplash.com/photo-1524592094714-0f0654e20314",
    "bag": "https://images.unsplash.com/photo-1584917865442-de89df76afd3"
}

def get_img(k, c):
    k = k.lower()
    # Cars
    if "g 63" in k or "g800" in k: return IMG["g63"]
    if "sl" in k or "roadster" in k: return IMG["sl63"]
    if "maybach" in k or "s 680" in k: return IMG["maybach"]
    if "cullinan" in k or "dbx" in k: return IMG["cullinan"]
    if "rolls" in k or "phantom" in k: return IMG["phantom"]
    if "ferrari" in k: return IMG["ferrari"]
    if "urus" in k: return IMG["lambo_suv"]
    if "lambo" in k: return IMG["lambo_car"]
    if "porsche" in k: return IMG["porsche"]
    if "bugatti" in k: return IMG["bugatti"]
    if "mclaren" in k: return IMG["mclaren"]
    if "bmw" in k: return IMG["bmw"]
    if "audi" in k: return IMG["audi"]
    if "nav" in k or "rover" in k: return IMG["suv"]
    # Jets
    if "bbj" in k or "787" in k: return IMG["bbj"]
    if "bombardier" in k or "global" in k: return IMG["bombardier"]
    if "gulfstream" in k or "falcon" in k: return IMG["gulfstream"]
    # Yachts
    if "azzam" in k or "eclipse" in k: return IMG["yacht_big"]
    if "yacht" in k or "fox" in k: return IMG["yacht_std"]
    # Estate
    if "tower" in k or "101" in k or "sky" in k: return IMG["tower"]
    if "villa" in k or "house" in k: return IMG["villa"]
    # Other
    if c == "Watch": return IMG["watch"]
    if c == "Luxury": return IMG["bag"]
    return IMG["maybach"]

# ==========================================
# 2. 核心逻辑
# ==========================================
if 'cash' not in st.session_state: st.session_state.cash = 10000000000
if 'inventory' not in st.session_state: st.session_state.inventory = []

def buy(name, price, img):
    st.session_state.inventory.append({"name": name, "price": price, "img": img})
    st.toast(f"Bought {name}!")

def sell(i):
    st.session_state.inventory.pop(i)
    st.rerun()

# ==========================================
# 3. 极简数据库生成
# ==========================================
DB = {"Car":[], "Jet":[], "Yacht":[], "Estate":[], "Watch":[], "Luxury":[]}

# Cars
car_list = [
    ("Mercedes G63", 190000), ("Mercedes SL63", 185000), ("Maybach S680", 250000),
    ("Rolls-Royce Cullinan", 400000), ("Rolls-Royce Phantom", 600000),
    ("Ferrari SF90", 550000), ("Lamborghini Revuelto", 600000), ("Lamborghini Urus", 270000),
    ("Porsche 911 Turbo S", 240000), ("Bugatti Chiron", 3500000), ("McLaren 765LT", 380000),
    ("BMW M4", 95000), ("Audi RS6", 130000), ("Range Rover SV", 250000)
]
for n, p in car_list: DB["Car"].append({"name":n, "price":p, "img":get_img(n,"Car")})

# Jets
jet_list = [
    ("Gulfstream G700", 78000000), ("Bombardier Global 7500", 75000000), 
    ("Boeing BBJ 787", 250000000), ("Dassault Falcon 10X", 75000000)
]
for n, p in jet_list: DB["Jet"].append({"name":n, "price":p, "img":get_img(n,"Jet")})

# Yachts
yacht_list = [
    ("Lürssen Azzam", 600000000), ("Blohm+Voss Eclipse", 500000000), ("Oceanco Jubilee", 300000000)
]
for n, p in yacht_list: DB["Yacht"].append({"name":n, "price":p, "img":get_img(n,"Yacht")})

# Estate
est_list = [("NY Central Park Tower", 250000000), ("Beverly Hills Mansion", 100000000), ("Shanghai Villa", 80000000)]
for n, p in est_list: DB["Estate"].append({"name":n, "price":p, "img":get_img(n,"Estate")})

# Others
for i in range(5): 
    DB["Watch"].append({"name":f"Patek Philippe #{i}", "price":500000, "img":get_img("","Watch")})
    DB["Luxury"].append({"name":f"Hermes Birkin #{i}", "price":20000, "img":get_img("","Luxury")})

# ==========================================
# 4. 界面渲染
# ==========================================
with st.sidebar:
    st.title("👑 ULTIMATE")
    st.metric("Cash", f"${st.session_state.cash:,.0f}")

tabs = st.tabs(["🏎️ Cars", "✈️ Jets", "⚓ Yachts", "🏰 Estate", "⌚ Watch", "👜 Luxury", "💼 My Assets"])

# 渲染函数
def render_tab(cat_name):
    for item in DB[cat_name]:
        with st.container():
            c1, c2 = st.columns([2, 3])
            c1.image(item['img'])
            with c2:
                st.subheader(item['name'])
                st.write(f"Price: ${item['price']:,}")
                if st.button("Buy", key=f"b_{item['name']}"): buy(item['name'], item['price'], item['img'])
            st.divider()

with tabs[0]: render_tab("Car")
with tabs[1]: render_tab("Jet")
with tabs[2]: render_tab("Yacht")
with tabs[3]: render_tab("Estate")
with tabs[4]: render_tab("Watch")
with tabs[5]: render_tab("Luxury")

with tabs[6]:
    if not st.session_state.inventory: st.write("Empty")
    for i, item in enumerate(st.session_state.inventory):
        c1, c2 = st.columns([1, 3])
        c1.image(item['img'])
        with c2:
            st.write(f"**{item['name']}**")
            if st.button("Sell", key=f"s_{i}"): sell(i)
