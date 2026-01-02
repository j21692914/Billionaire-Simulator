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
    
    .asset-card {
        border: 1px solid #333; 
        background: #111; 
        border-radius: 12px; 
        padding: 15px; 
        margin-bottom: 20px;
    }
    .gold {color: #D4AF37; font-weight: bold;}
    .price-tag {font-family: 'Courier New'; color: #50C878; font-weight: bold;}
    
    /* 图片容器强制 16:9 宽幅 */
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
# 1. 深度选配矩阵
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
OPTS_WATCH = {"Material": {"Steel":0, "Gold":35000}, "Dial": {"Std":0, "Meteorite":15000}, "Gem": {"None":0, "Diamond":25000}}
OPTS_LUXURY = {"Leather": {"Togo":0, "Croc":45000}, "Hardware": {"Gold":0, "Diamond":85000}, "Condition": {"New":0, "Vintage":5000}}

# ==========================================
# 2. 稳定的高清图库 (国内可用源)
# ==========================================
# 使用 Unsplash/Pexels 的稳定图链，不使用随机搜索，确保是车不是人
IMG_LIB = {
    "Rolls-Royce": "https://images.unsplash.com/photo-1631295868223-63265b40d9e4?auto=format&fit=crop&q=80&w=1200", # 劳斯莱斯
    "Ferrari": "https://images.unsplash.com/photo-1592198084033-aade902d1aae?auto=format&fit=crop&q=80&w=1200", # 法拉利红
    "Lamborghini": "https://images.unsplash.com/photo-1544636331-e26879cd4d9b?auto=format&fit=crop&q=80&w=1200", # 兰博基尼
    "Porsche": "https://images.unsplash.com/photo-1503376763036-066120622c74?auto=format&fit=crop&q=80&w=1200", # 保时捷
    "Mercedes": "https://images.unsplash.com/photo-1617788138017-80ad40651399?auto=format&fit=crop&q=80&w=1200", # 奔驰GT
    "BMW": "https://images.unsplash.com/photo-1555215695-3004980adade?auto=format&fit=crop&q=80&w=1200", # 宝马
    "Bugatti": "https://images.unsplash.com/photo-1627454820574-fb40e69228d4?auto=format&fit=crop&q=80&w=1200", # 布加迪
    "McLaren": "https://images.unsplash.com/photo-1621135802920-133df287f89c?auto=format&fit=crop&q=80&w=1200", # 迈凯伦
    "Jet": "https://images.unsplash.com/photo-1540962351504-03099e0a754b?auto=format&fit=crop&q=80&w=1200", # 私人飞机内部
    "Yacht": "https://images.unsplash.com/photo-1605281317010-fe5ffe79b9b4?auto=format&fit=crop&q=80&w=1200", # 超级游艇
    "Mansion": "https://images.unsplash.com/photo-1613490493576-7fde63acd811?auto=format&fit=crop&q=80&w=1200", # 豪宅
    "CityPH": "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&q=80&w=1200", # 城市大平层
    "Watch": "https://images.unsplash.com/photo-1524592094714-0f0654e20314?auto=format&fit=crop&q=80&w=1200", # 名表
    "Bag": "https://images.unsplash.com/photo-1584917865442-de89df76afd3?auto=format&fit=crop&q=80&w=1200", # 铂金包
    "Default": "https://images.unsplash.com/photo-1566373733075-bd74c4380eb9?auto=format&fit=crop&q=80&w=1200" # 奢华氛围
}

def get_safe_img(name, cat):
    name = name.lower()
    # 按照优先级匹配图片
    if cat == "Car":
        if "rolls" in name or "phantom" in name or "cullinan" in name or "spectre" in name: return IMG_LIB["Rolls-Royce"]
        if "ferrari" in name or "sf90" in name or "488" in name: return IMG_LIB["Ferrari"]
        if "lambo" in name or "urus" in name or "revuelto" in name: return IMG_LIB["Lamborghini"]
        if "porsche" in name or "911" in name: return IMG_LIB["Porsche"]
        if "mercedes" in name or "amg" in name or "maybach" in name: return IMG_LIB["Mercedes"]
        if "bmw" in name: return IMG_LIB["BMW"]
        if "bugatti" in name or "chiron" in name: return IMG_LIB["Bugatti"]
        if "mclaren" in name: return IMG_LIB["McLaren"]
        return IMG_LIB["Mercedes"] # 默认好车
    
    if cat == "Fleet":
        if "yacht" in name or "azzam" in name or "eclipse" in name: return IMG_LIB["Yacht"]
        return IMG_LIB["Jet"]
    
    if cat == "Estate":
        if "villa" in name or "house" in name or "mansion" in name or "gong" in name: return IMG_LIB["Mansion"]
        return IMG_LIB["CityPH"] # 公寓/顶复
    
    if cat == "Watch": return IMG_LIB["Watch"]
    if cat == "Luxury": return IMG_LIB["Bag"]
    
    return IMG_LIB["Default"]

# ==========================================
# 3. 数据工厂 (Data Factory)
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
        db["Estate"].append({"id":f"e_{i}", "brand":loc, "name":name, "price":price, "type":"Ultra Prime", "img":get_safe_img(name, "Estate"), "opts":OPTS_ESTATE})

    # 2. 舰队
    jets = [
        ("Gulfstream", "G700", 78000000), ("Gulfstream", "G650ER", 70000000), 
        ("Bombardier", "Global 7500", 75000000), ("Dassault", "Falcon 10X", 75000000),
        ("Boeing", "BBJ 787", 250000000)
    ]
    for i, (brand, name, price) in enumerate(jets):
        db["Fleet"].append({"id":f"j_{i}", "brand":brand, "name":name, "price":price, "type":"Private Jet", "img":get_safe_img(name, "Fleet"), "opts":OPTS_JET})
    
    yachts = [
        ("Lürssen", "Azzam", 600000000), ("Blohm+Voss", "Eclipse", 1200000000), 
        ("Oceanco", "Jubilee", 300000000), ("Lürssen", "Flying Fox", 400000000)
    ]
    for i, (brand, name, price) in enumerate(yachts):
        db["Fleet"].append({"id":f"y_{i}", "brand":brand, "name":name, "price":price, "type":"Mega Yacht", "img":get_safe_img(name, "Fleet"), "opts":OPTS_MEGA_YACHT})

    # 3. 车辆
    cars = [
        ("Mercedes-AMG", "SL 63", 185000), ("Mercedes-AMG", "G 63", 190000), ("Mercedes-AMG", "GT 63 S", 195000),
        ("Maybach", "S 680", 250000), ("Brabus", "G800", 450000),
        ("BMW", "M4 Comp", 95000), ("BMW", "M8 Comp", 140000),
        ("Audi", "RS 6", 130000), ("Lincoln", "Navigator", 120000), ("Land Rover", "Range Rover SV", 240000),
        ("Porsche", "911 Turbo S", 240000), ("Porsche", "911 GT3 RS", 280000),
        ("Maserati", "MC20", 220000), ("McLaren", "765LT", 390000), ("McLaren", "Speedtail", 2500000),
        ("Aston Martin", "DB12", 250000), ("Aston Martin", "Valkyrie", 3500000),
        ("Ferrari", "SF90", 550000), ("Ferrari", "Purosangue", 400000), ("Ferrari", "812 Comp", 650000),
        ("Lamborghini", "Revuelto", 620000), ("Lamborghini", "Urus", 270000),
        ("Rolls-Royce", "Spectre", 450000), ("Rolls-Royce", "Cullinan", 400000), ("Rolls-Royce", "Phantom", 600000),
        ("Bentley", "Conti GT", 300000), ("Bugatti", "Chiron", 3300000)
    ]
    for i, (brand, name, price) in enumerate(cars):
        db["Car"].append({"id":f"c_{i}", "brand":brand, "name":name, "price":price, "type":"Car", "img":get_safe_img(name, "Car"), "opts":OPTS_CAR})

    # 4. 补全
    for i in range(10):
        db["Watch"].append({"id":f"w_{i}","brand":"Rolex","name":f"Daytona #{i}","price":35000,"img":get_safe_img("","Watch"),"opts":OPTS_WATCH})
        db["Luxury"].append({"id":f"l_{i}","brand":"Hermes","name":f"Birkin #{i}","price":15000,"img":get_safe_img("","Luxury"),"opts":OPTS_LUXURY})

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

def sell_item(idx):
    item = st.session_state.inventory[idx]
    st.session_state.cash += item['val']
    st.session_state.inventory.pop(idx); st.toast("Sold!"); st.rerun()

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
    for i, item in enumerate(st.session_state.inventory):
        with st.container():
            c1, c2, c3 = st.columns([2, 3, 1])
            c1.image(item['img'])
            with c2:
                st.write(f"**{item['name']}**")
                st.caption(item['specs'])
            with c3:
                if st.button("Sell", key=f"sell_{i}"): sell_item(i)
