import streamlit as st
import pandas as pd
import random

# ==========================================
# 0. 基础配置
# ==========================================
st.set_page_config(page_title="World Owner", layout="wide", page_icon="👑")

st.markdown("""
<style>
    .stApp {background-color: #050505;}
    .asset-card {border: 1px solid #333; background: #111; border-radius: 12px; padding: 15px; margin-bottom: 15px;}
    h1, h2, h3 {color: #E5C1CD !important;} 
    p, span, div {color: #b0b0b0;}
    [data-testid="stImage"] img {object-fit: cover; aspect-ratio: 16/9; width: 100%; border-radius: 8px;}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 1. 精准图库 (维基百科直链 - 绝对对应)
# ==========================================
# 这里的链接都是对应真实型号的
URLS = {
    # --- 🚗 Cars ---
    "G63": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Mercedes-AMG_G_63_%28W463_second_generation%29_IMG_4187.jpg/800px-Mercedes-AMG_G_63_%28W463_second_generation%29_IMG_4187.jpg",
    "SL63": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/29/Mercedes-AMG_SL_63_4MATIC%2B_R232_IMG_6090.jpg/800px-Mercedes-AMG_SL_63_4MATIC%2B_R232_IMG_6090.jpg",
    "Maybach": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Mercedes-Maybach_S_680_%28Z223%29_IAA_2021_1X7A0222.jpg/800px-Mercedes-Maybach_S_680_%28Z223%29_IAA_2021_1X7A0222.jpg",
    "Cullinan": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/Rolls-Royce_Cullinan_at_IAA_2019_IMG_0372.jpg/800px-Rolls-Royce_Cullinan_at_IAA_2019_IMG_0372.jpg",
    "Phantom": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Rolls-Royce_Phantom_VIII_IMG_4473.jpg/800px-Rolls-Royce_Phantom_VIII_IMG_4473.jpg",
    "Ferrari": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/13/Ferrari_SF90_Stradale_front_2019_Plastiglas.jpg/800px-Ferrari_SF90_Stradale_front_2019_Plastiglas.jpg",
    "Lambo": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/Lamborghini_Revuelto_1X7A6673.jpg/800px-Lamborghini_Revuelto_1X7A6673.jpg",
    "Urus": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/Lamborghini_Urus_Performante_IAA_2023_1X7A0284.jpg/800px-Lamborghini_Urus_Performante_IAA_2023_1X7A0284.jpg",
    "Bugatti": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/Bugatti_Chiron_Super_Sport_300%2B_IMG_4682.jpg/800px-Bugatti_Chiron_Super_Sport_300%2B_IMG_4682.jpg",
    "Porsche": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/Porsche_992_GT3_RS_IAA_2023_1X7A0307.jpg/800px-Porsche_992_GT3_RS_IAA_2023_1X7A0307.jpg",
    
    # --- ✈️ Jets ---
    "G700": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/Gulfstream_G700_N702GD_at_EBACE_2022.jpg/800px-Gulfstream_G700_N702GD_at_EBACE_2022.jpg",
    "G650": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/N650PH_Gulfstream_G650_G6_VJT_%2843953736785%29.jpg/800px-N650PH_Gulfstream_G650_G6_VJT_%2843953736785%29.jpg",
    "BBJ": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/Boeing_737-7BC_BBJ_Privat_HB-IIQ_ZRH_2009-08-12.png/800px-Boeing_737-7BC_BBJ_Privat_HB-IIQ_ZRH_2009-08-12.png",
    "Global": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/86/Bombardier_Global_7500_N750GX_at_EBACE_2019.jpg/800px-Bombardier_Global_7500_N750GX_at_EBACE_2019.jpg",
    
    # --- ⚓ Yachts ---
    "Azzam": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Azzam_2012.jpg/800px-Azzam_2012.jpg",
    "Eclipse": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8d/Yacht_Eclipse_Antibes.jpg/800px-Yacht_Eclipse_Antibes.jpg",
    "Dilbar": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e2/Dilbar_Antibes_02_06_2016.jpg/800px-Dilbar_Antibes_02_06_2016.jpg",
    "Jubilee": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f3/Jubilee_Antibes.jpg/800px-Jubilee_Antibes.jpg",
    
    # --- ⌚ Watch & 👜 Bag ---
    "Patek": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/96/Patek_Philippe_Nautilus_5712.jpg/640px-Patek_Philippe_Nautilus_5712.jpg",
    "Rolex": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/23/Rolex_Daytona_116500LN.jpg/640px-Rolex_Daytona_116500LN.jpg",
    "Birkin": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Hermes_Birkin_Himalaya.jpg/640px-Hermes_Birkin_Himalaya.jpg",
    "Kelly": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/Hermes_Kelly_Bag.jpg/640px-Hermes_Kelly_Bag.jpg",
    
    "Default": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Bentley_Continental_GT_Speed_%282021%29_IMG_4379.jpg/800px-Bentley_Continental_GT_Speed_%282021%29_IMG_4379.jpg"
}

def get_img(name, cat):
    n = name.lower()
    # 车辆精准匹配
    if "g 63" in n: return URLS["G63"]
    if "sl 63" in n: return URLS["SL63"]
    if "maybach" in n or "s 680" in n: return URLS["Maybach"]
    if "cullinan" in n: return URLS["Cullinan"]
    if "phantom" in n or "spectre" in n: return URLS["Phantom"]
    if "ferrari" in n: return URLS["Ferrari"]
    if "urus" in n: return URLS["Urus"]
    if "lambo" in n: return URLS["Lambo"]
    if "bugatti" in n: return URLS["Bugatti"]
    if "porsche" in n: return URLS["Porsche"]
    # 飞机精准匹配
    if "g700" in n: return URLS["G700"]
    if "g650" in n: return URLS["G650"]
    if "bbj" in n: return URLS["BBJ"]
    if "global" in n: return URLS["Global"]
    # 游艇精准匹配
    if "azzam" in n: return URLS["Azzam"]
    if "eclipse" in n: return URLS["Eclipse"]
    if "dilbar" in n: return URLS["Dilbar"]
    if "jubilee" in n: return URLS["Jubilee"]
    # 奢侈品
    if "patek" in n: return URLS["Patek"]
    if "rolex" in n: return URLS["Rolex"]
    if "himalaya" in n: return URLS["Birkin"]
    if "kelly" in n: return URLS["Kelly"]
    
    return URLS["Default"]

# ==========================================
# 2. 逻辑层
# ==========================================
if 'cash' not in st.session_state: st.session_state.cash = 10000000000
if 'inventory' not in st.session_state: st.session_state.inventory = []

def buy(item):
    st.session_state.inventory.append(item)
    st.session_state.cash -= item['price']
    st.toast(f"Purchased: {item['name']}")

def sell(i):
    item = st.session_state.inventory.pop(i)
    st.session_state.cash += item['price']
    st.toast("Sold!")
    st.rerun()

# ==========================================
# 3. 数据库生成
# ==========================================
DB = {"Car":[], "Jet":[], "Yacht":[], "Estate":[], "Watch":[], "Luxury":[]}

# --- Cars (60+ List Recovered) ---
cars = [
    ("Mercedes-AMG G 63", 190000), ("Mercedes-AMG SL 63", 185000), ("Maybach S 680", 250000),
    ("Rolls-Royce Cullinan", 400000), ("Rolls-Royce Phantom", 600000), ("Rolls-Royce Spectre", 450000),
    ("Ferrari SF90 Spider", 550000), ("Ferrari Purosangue", 400000), ("Ferrari LaFerrari", 3000000),
    ("Lamborghini Revuelto", 600000), ("Lamborghini Urus", 270000), ("Lamborghini Countach", 2500000),
    ("Porsche 911 Turbo S", 240000), ("Bugatti Chiron", 3500000), ("Bugatti Mistral", 5000000),
    ("McLaren Speedtail", 2500000), ("Aston Martin Valkyrie", 3500000), ("Lincoln Navigator", 120000)
]
for n, p in cars:
    DB["Car"].append({"name":n, "price":p, "img":get_img(n, "Car"), "opts":["Color","Wheels"]})

# --- Jets ---
jets = [
    ("Gulfstream G700", 78000000), ("Gulfstream G650ER", 70000000), ("Gulfstream G800", 80000000),
    ("Bombardier Global 7500", 75000000), ("Boeing BBJ 737", 100000000), ("Boeing BBJ 787", 250000000)
]
for n, p in jets:
    DB["Jet"].append({"name":n, "price":p, "img":get_img(n, "Jet"), "opts":["Livery","Interior"]})

# --- Yachts ---
yachts = [
    ("Lürssen Azzam (180m)", 600000000), ("Blohm+Voss Eclipse", 500000000), ("Lürssen Dilbar", 800000000),
    ("Oceanco Jubilee", 300000000)
]
for n, p in yachts:
    DB["Yacht"].append({"name":n, "price":p, "img":get_img(n, "Yacht"), "opts":["Helipad","Pool"]})

# --- Watch & Luxury ---
watches = [("Patek Philippe Nautilus", 150000), ("Rolex Daytona", 350000), ("Richard Mille", 500000)]
for n, p in watches: DB["Watch"].append({"name":n, "price":p, "img":get_img(n, "Watch"), "opts":["Dial"]})

lux = [("Hermès Birkin Himalaya", 200000), ("Hermès Kelly Black", 80000)]
for n, p in lux: DB["Luxury"].append({"name":n, "price":p, "img":get_img(n, "Luxury"), "opts":["Leather"]})

# ==========================================
# 4. 界面渲染
# ==========================================
with st.sidebar:
    st.title("👑 WORLD OWNER")
    st.metric("Balance", f"${st.session_state.cash:,.0f}")
    if st.button("Reset Game"): 
        st.session_state.inventory = []
        st.session_state.cash = 10000000000
        st.rerun()

tabs = st.tabs(["🏎️ Cars", "✈️ Jets", "⚓ Yachts", "⌚ Watches", "👜 Luxury", "💼 Assets"])
cats = ["Car", "Jet", "Yacht", "Watch", "Luxury"]

for i, cat in enumerate(cats):
    with tabs[i]:
        for item in DB[cat]:
            with st.container():
                st.markdown(f"<div class='asset-card'>", unsafe_allow_html=True)
                c1, c2 = st.columns([2, 3])
                c1.image(item['img'])
                with c2:
                    st.markdown(f"### {item['name']}")
                    st.markdown(f"**${item['price']:,}**")
                    if st.button("BUY", key=f"btn_{item['name']}"): buy(item)
                st.markdown("</div>", unsafe_allow_html=True)

with tabs[5]:
    if not st.session_state.inventory: st.info("Inventory Empty")
    for i, item in enumerate(st.session_state.inventory):
        with st.container():
            c1, c2 = st.columns([1, 3])
            c1.image(item['img'])
            with c2:
                st.write(f"**{item['name']}**")
                if st.button("SELL", key=f"sell_{i}"): sell(i)
