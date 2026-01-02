import streamlit as st
import pandas as pd
import random
import json
import os

# ==========================================
# 0. UI & 基础配置
# ==========================================
st.set_page_config(page_title="World Owner", layout="wide", page_icon="🌍")

st.markdown("""
<style>
    .stApp {background-color: #050505;}
    [data-testid="stSidebar"] {background-color: #0a0a0a; border-right: 1px solid #222;}
    h1, h2, h3, h4 {color: #E5C1CD !important; font-family: 'Didot', serif;}
    div, p, span {color: #b0b0b0;}
    
    /* 资产卡片优化 */
    .asset-card {
        border: 1px solid #333; 
        background: #111; 
        border-radius: 12px; 
        padding: 15px; 
        margin-bottom: 20px;
    }
    .gold {color: #D4AF37; font-weight: bold;}
    .price-tag {font-family: 'Courier New'; color: #50C878; font-weight: bold;}
    
    /* 图片容器优化 */
    [data-testid="stImage"] {
        border-radius: 8px;
        overflow: hidden;
    }
    [data-testid="stImage"] > img {
        object-fit: cover; 
        aspect-ratio: 16/9; 
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

SAVE_FILE = "game_save.json" 

# ==========================================
# 1. 精准图源映射 (手动校准版 - 告别大叔图)
# ==========================================
def get_real_img(name, cat):
    name = name.lower()
    
    # --- 🏎️ 豪车精准图 ---
    if cat == "Car":
        if "sl 63" in name: return "https://upload.wikimedia.org/wikipedia/commons/thumb/2/29/Mercedes-AMG_SL_63_4MATIC%2B_R232_IMG_6090.jpg/800px-Mercedes-AMG_SL_63_4MATIC%2B_R232_IMG_6090.jpg"
        if "g 63" in name: return "https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/Mercedes-AMG_G_63_%28W463_second_generation%29_IMG_4187.jpg/800px-Mercedes-AMG_G_63_%28W463_second_generation%29_IMG_4187.jpg"
        if "gt 63" in name: return "https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/Mercedes-AMG_GT_63_S_E_Performance_IAA_2021_1X7A0168.jpg/800px-Mercedes-AMG_GT_63_S_E_Performance_IAA_2021_1X7A0168.jpg"
        if "s 680" in name: return "https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Mercedes-Maybach_S_680_%28Z223%29_IAA_2021_1X7A0222.jpg/800px-Mercedes-Maybach_S_680_%28Z223%29_IAA_2021_1X7A0222.jpg"
        if "pullman" in name: return "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/Mercedes-Maybach_S_600_Pullman_Genf_2018.jpg/800px-Mercedes-Maybach_S_600_Pullman_Genf_2018.jpg"
        if "g800" in name: return "https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Brabus_800_Widestar.jpg/800px-Brabus_800_Widestar.jpg"
        if "m4" in name: return "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/BMW_G82_IAA_2021_1X7A0064.jpg/800px-BMW_G82_IAA_2021_1X7A0064.jpg"
        if "i8" in name: return "https://upload.wikimedia.org/wikipedia/commons/thumb/8/86/BMW_i8_Roadster_IMG_1523.jpg/800px-BMW_i8_Roadster_IMG_1523.jpg"
        if "rs 6" in name: return "https://upload.wikimedia.org/wikipedia/commons/thumb/2/20/Audi_RS6_Avant_C8_IAA_2019_JM_0485.jpg/800px-Audi_RS6_Avant_C8_IAA_2019_JM_0485.jpg"
        if "navigator" in name: return "https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/2018_Lincoln_Navigator_Reserve_AWD_front_4.16.18.jpg/800px-2018_Lincoln_Navigator_Reserve_AWD_front_4.16.18.jpg"
        if "range rover" in name: return "https://upload.wikimedia.org/wikipedia/commons/thumb/2/20/Land_Rover_Range_Rover_L460_Autobiography_IAA_2023_1X7A0388.jpg/800px-Land_Rover_Range_Rover_L460_Autobiography_IAA_2023_1X7A0388.jpg"
        if "cullinan" in name: return "https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/Rolls-Royce_Cullinan_at_IAA_2019_IMG_0372.jpg/800px-Rolls-Royce_Cullinan_at_IAA_2019_IMG_0372.jpg"
        if "phantom" in name: return "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Rolls-Royce_Phantom_VIII_IMG_4473.jpg/800px-Rolls-Royce_Phantom_VIII_IMG_4473.jpg"
        if "revuelto" in name: return "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/Lamborghini_Revuelto_1X7A6673.jpg/800px-Lamborghini_Revuelto_1X7A6673.jpg"
        if "sf90" in name: return "https://upload.wikimedia.org/wikipedia/commons/thumb/1/13/Ferrari_SF90_Stradale_front_2019_Plastiglas.jpg/800px-Ferrari_SF90_Stradale_front_2019_Plastiglas.jpg"
        if "chiron" in name: return "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/Bugatti_Chiron_Super_Sport_300%2B_IMG_4682.jpg/800px-Bugatti_Chiron_Super_Sport_300%2B_IMG_4682.jpg"
        
        # 默认车图
        return "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Bentley_Continental_GT_Speed_%282021%29_IMG_4379.jpg/800px-Bentley_Continental_GT_Speed_%282021%29_IMG_4379.jpg"

    # --- ✈️ 舰队精准图 ---
    if cat == "Fleet":
        if "yacht" in name:
            if "azzam" in name: return "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Azzam_2012.jpg/800px-Azzam_2012.jpg"
            if "dilbar" in name: return "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e2/Dilbar_Antibes_02_06_2016.jpg/800px-Dilbar_Antibes_02_06_2016.jpg"
            if "eclipse" in name: return "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8d/Yacht_Eclipse_Antibes.jpg/800px-Yacht_Eclipse_Antibes.jpg"
            return "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/L%C3%BCrssen_Nord.jpg/800px-L%C3%BCrssen_Nord.jpg"
            
        if "gulfstream" in name: 
            if "g700" in name: return "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/Gulfstream_G700_N702GD_at_EBACE_2022.jpg/800px-Gulfstream_G700_N702GD_at_EBACE_2022.jpg"
            return "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Gulfstream_G700_%28N702GD%29_in_flight.jpg/800px-Gulfstream_G700_%28N702GD%29_in_flight.jpg"
            
        if "global" in name: return "https://upload.wikimedia.org/wikipedia/commons/thumb/8/86/Bombardier_Global_7500_N750GX_at_EBACE_2019.jpg/800px-Bombardier_Global_7500_N750GX_at_EBACE_2019.jpg"
        if "falcon" in name: return "https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/Dassault_Falcon_8X_F-WWQA_PAS_2015_02.jpg/800px-Dassault_Falcon_8X_F-WWQA_PAS_2015_02.jpg"
        if "bbj" in name: return "https://upload.wikimedia.org/wikipedia/commons/thumb/1/16/Boeing_Business_Jet_737-700_BBJ%2C_Private_JP7397145.jpg/800px-Boeing_Business_Jet_737-700_BBJ%2C_Private_JP7397145.jpg"
        
        # 默认飞机
        return "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/Cessna_Citation_Longitude_%28N702CL%29_at_EBACE_2019.jpg/800px-Cessna_Citation_Longitude_%28N702CL%29_at_EBACE_2019.jpg"

    # --- 🏰 地产精准图 ---
    if cat == "Estate":
        if "101" in name or "park" in name: return "https://upload.wikimedia.org/wikipedia/commons/thumb/6/63/Central_Park_Tower_%2852233633214%29.jpg/800px-Central_Park_Tower_%2852233633214%29.jpg"
        if "courtyard" in name: return "https://upload.wikimedia.org/wikipedia/commons/thumb/1/14/Siheyuan_Beijing.jpg/800px-Siheyuan_Beijing.jpg"
        if "the one" in name: return "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a8/The_Manor_at_Holmby_Hills.jpg/800px-The_Manor_at_Holmby_Hills.jpg"
        if "hyde" in name: return "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/One_Hyde_Park_Knightsbridge.jpg/800px-One_Hyde_Park_Knightsbridge.jpg"
        if "odéon" in name: return "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Tour_Od%C3%A9on_from_Jardin_Exotique.jpg/800px-Tour_Od%C3%A9on_from_Jardin_Exotique.jpg"
        return "https://upload.wikimedia.org/wikipedia/commons/thumb/9/90/Chateau_de_Vaux_le_Vicomte.jpg/800px-Chateau_de_Vaux_le_Vicomte.jpg"

    return "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Hermes_Birkin_Himalaya.jpg/800px-Hermes_Birkin_Himalaya.jpg"

# ==========================================
# 2. 深度选配矩阵 (无错版)
# ==========================================
OPTS_CAR = {
    "Paint": {"Standard":0, "Metallic":5000, "Matte":15000, "Bespoke":45000},
    "Wheels": {"Standard":0, "Forged":12000, "Black":8000},
    "Interior": {"Leather":0, "Red":0, "White":5000, "Hermes":50000},
    "Tech": {"Standard":0, "Full Assist":12000}
}
OPTS_JET = {
    "Layout": {"Executive":0, "Bedroom":2000000, "Majlis":1500000},
    "Livery": {"White":0, "Matte Black":250000, "Custom":500000},
    "Defense": {"None":0, "Anti-Missile":4500000}
}
OPTS_MEGA_YACHT = {
    "Helipad": {"Touch&Go":0, "Hangar":2000000}, 
    "Sub": {"None":0, "Triton":4000000}, 
    "Defense": {"None":0, "Anti-Drone":1500000}, 
    "Pool": {"Deck":0, "Infinity":2000000}
}
OPTS_ESTATE = {"Style": {"Modern":0, "Classic":500000}, "Security": {"Std":0, "Armed":800000}, "Staff": {"None":0, "Full Team":800000}}
OPTS_WATCH = {"Material": {"Steel":0, "Gold":35000}, "Dial": {"Std":0, "Meteorite":15000}}
OPTS_LUXURY = {"Leather": {"Togo":0, "Croc":45000}, "Hardware": {"Gold":0, "Diamond":85000}}

# ==========================================
# 3. 数据工厂
# ==========================================
def generate_db():
    db = {"Car":[], "Estate":[], "Watch":[], "Fleet":[], "Luxury":[]}
    
    # 1. 地产
    estates = [
        ("New York", "Central Park Tower 101st PH", 250000000), 
        ("Beverly Hills", "The One Hilltop Mansion", 145000000),
        ("Shanghai", "Tan Gong Villa No.2", 100000000),
        ("Hong Kong", "35 Barker Road Villa", 280000000),
        ("Beijing", "Houhai Courtyard", 180000000),
        ("Monaco", "Tour Odéon Sky Penthouse", 380000000),
        ("London", "One Hyde Park Penthouse", 120000000)
    ]
    for i, (loc, name, price) in enumerate(estates):
        db["Estate"].append({"id":f"e_{i}", "brand":loc, "name":name, "price":price, "type":"Ultra Prime", "img":get_real_img(name, "Estate"), "opts":OPTS_ESTATE})

    # 2. 舰队 (飞机+游艇)
    # 飞机
    jets = [
        ("Gulfstream", "G700", 78000000), ("Gulfstream", "G650ER", 70000000), ("Gulfstream", "G280", 25000000),
        ("Bombardier", "Global 7500", 75000000), ("Bombardier", "Global 6500", 56000000),
        ("Dassault", "Falcon 8X", 58000000), ("Dassault", "Falcon 10X", 75000000),
        ("Boeing", "BBJ MAX 8", 110000000), ("Boeing", "BBJ 787", 250000000)
    ]
    for i, (brand, name, price) in enumerate(jets):
        db["Fleet"].append({"id":f"j_{i}", "brand":brand, "name":name, "price":price, "type":"Private Jet", "img":get_real_img(name, "Fleet"), "opts":OPTS_JET})
    
    # 游艇
    yachts = [
        ("Lürssen", "Azzam", 600000000), ("Blohm+Voss", "Eclipse", 1200000000), ("Lürssen", "Dilbar", 800000000),
        ("Oceanco", "Jubilee", 300000000), ("Lürssen", "Flying Fox", 400000000)
    ]
    for i, (brand, name, price) in enumerate(yachts):
        db["Fleet"].append({"id":f"y_{i}", "brand":brand, "name":name, "price":price, "type":"Mega Yacht", "img":get_real_img(name, "Fleet"), "opts":OPTS_MEGA_YACHT})

    # 3. 车辆
    cars = [
        ("Mercedes-AMG", "SL 63", 185000), ("Mercedes-AMG", "G 63", 190000), ("Mercedes-AMG", "GT 63 S", 195000),
        ("Maybach", "S 680", 250000), ("Maybach", "Pullman Guard", 1600000), ("Brabus", "G800", 450000),
        ("BMW", "M4 Comp", 95000), ("BMW", "M8 Comp", 140000), ("BMW", "i8 Roadster", 165000),
        ("Audi", "RS 6", 130000), ("Audi", "RS 7", 135000), ("Lincoln", "Navigator", 120000), ("Land Rover", "Range Rover SV", 240000),
        ("Porsche", "911 Turbo S", 240000), ("Porsche", "Taycan Turbo GT", 230000),
        ("Maserati", "MC20", 220000), ("McLaren", "720S", 320000), ("McLaren", "Speedtail", 2500000),
        ("Aston Martin", "DB12", 250000), ("Aston Martin", "Valkyrie", 3500000),
        ("Ferrari", "SF90", 550000), ("Ferrari", "Purosangue", 400000), ("Ferrari", "812 Comp", 650000),
        ("Lamborghini", "Revuelto", 620000), ("Lamborghini", "Urus", 270000),
        ("Rolls-Royce", "Spectre", 450000), ("Rolls-Royce", "Cullinan", 400000), ("Rolls-Royce", "Phantom", 600000),
        ("Bentley", "Conti GT", 300000), ("Bugatti", "Chiron", 3300000)
    ]
    for i, (brand, name, price) in enumerate(cars):
        db["Car"].append({"id":f"c_{i}", "brand":brand, "name":name, "price":price, "type":"Car", "img":get_real_img(name, "Car"), "opts":OPTS_CAR})

    # 4. 补全
    for i in range(10):
        db["Watch"].append({"id":f"w_{i}","brand":"Rolex","name":f"Daytona #{i}","price":35000,"img":"https://upload.wikimedia.org/wikipedia/commons/thumb/2/23/Rolex_Daytona_116500LN.jpg/600px-Rolex_Daytona_116500LN.jpg","opts":OPTS_WATCH})
        db["Luxury"].append({"id":f"l_{i}","brand":"Hermes","name":f"Birkin #{i}","price":15000,"img":"https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Hermes_Birkin_Himalaya.jpg/600px-Hermes_Birkin_Himalaya.jpg","opts":OPTS_LUXURY})

    return db

DB = generate_db()

# ==========================================
# 4. 逻辑层
# ==========================================
if 'cash' not in st.session_state: st.session_state.cash = 10000000000.0
if 'inventory' not in st.session_state: st.session_state.inventory = []

def buy_item(item, final_price, specs):
    if st.session_state.cash >= final_price:
        st.session_state.cash -= final_price
        st.session_state.inventory.append({
            "name": item['name'], "brand": item['brand'], "specs": specs,
            "val": final_price, "img": item['img']
        })
        st.toast("✅ Purchased!")
        st.rerun()
    else: st.error("Insufficient Funds")

# ==========================================
# 5. 界面渲染
# ==========================================
with st.sidebar:
    st.title("🌍 WORLD OWNER")
    st.metric("Liquid Cash", f"${st.session_state.cash:,.0f}")

def render_configurator(item):
    with st.expander(f"🛠️ Configure: {item['name']}", expanded=False):
        c_price = item['price']
        specs = []
        for cat, opts in item['opts'].items():
            sel = st.selectbox(f"{cat}", list(opts.keys()), key=f"{item['id']}_{cat}")
            c_price += opts[sel]
            specs.append(f"{cat}: {sel}")
        st.write(f"Total: :red[${c_price:,.0f}]")
        if st.button("Buy Now", key=f"btn_{item['id']}"):
            buy_item(item, c_price, " | ".join(specs))

tabs = st.tabs(["🏰 Estate", "✈️ Fleet", "🏎️ Cars", "⌚ Watches", "👜 Luxury", "💼 My Assets"])

# 渲染 Estate
with tabs[0]:
    for item in DB["Estate"]:
        with st.container():
            st.markdown(f"<div class='asset-card'>", unsafe_allow_html=True)
            c1, c2 = st.columns([2, 3])
            c1.image(item['img'])
            with c2:
                st.markdown(f"### {item['name']}")
                st.markdown(f"Price: ${item['price']:,}")
                render_configurator(item)
            st.markdown("</div>", unsafe_allow_html=True)

# 渲染 Fleet
with tabs[1]:
    for item in DB["Fleet"]:
        with st.container():
            st.markdown(f"<div class='asset-card'>", unsafe_allow_html=True)
            c1, c2 = st.columns([2, 3])
            c1.image(item['img'])
            with c2:
                st.markdown(f"### {item['name']}")
                st.caption(item['type'])
                st.markdown(f"Price: ${item['price']:,}")
                render_configurator(item)
            st.markdown("</div>", unsafe_allow_html=True)

# 渲染 Cars
with tabs[2]:
    search = st.text_input("Search Car...", "")
    items = [x for x in DB["Car"] if search.lower() in x['name'].lower()]
    for item in items:
        with st.container():
            st.markdown(f"<div class='asset-card'>", unsafe_allow_html=True)
            c1, c2 = st.columns([2, 3])
            c1.image(item['img'])
            with c2:
                st.markdown(f"### {item['name']}")
                st.markdown(f"Price: ${item['price']:,}")
                render_configurator(item)
            st.markdown("</div>", unsafe_allow_html=True)

# 渲染资产
with tabs[5]:
    if not st.session_state.inventory: st.info("Inventory Empty")
    for item in st.session_state.inventory:
        with st.container():
            c1, c2 = st.columns([1, 3])
            c1.image(item['img'])
            with c2:
                st.write(f"**{item['name']}**")
                st.caption(item['specs'])
