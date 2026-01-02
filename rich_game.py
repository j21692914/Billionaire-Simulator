import streamlit as st
import pandas as pd

# ==========================================
# 0. 基础配置
# ==========================================
st.set_page_config(page_title="World Owner Pro", layout="wide", page_icon="👑")

st.markdown("""
<style>
    .stApp {background-color: #050505;}
    .asset-card {border: 1px solid #333; background: #111; border-radius: 12px; padding: 15px; margin-bottom: 15px;}
    h1, h2, h3 {color: #E5C1CD !important;} 
    p, span, div {color: #b0b0b0;}
    /* 强制图片比例 */
    [data-testid="stImage"] img {
        object-fit: cover; 
        aspect-ratio: 16/9; 
        width: 100%; 
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 1. 核心图库 (绝对无特斯拉)
# ==========================================
IMG = {
    # --- 豪车 ---
    "g_wagon": "https://images.unsplash.com/photo-1520031441872-265149a9e6e5", # 奔驰G
    "sl_amg": "https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8", # 奔驰敞篷
    "maybach": "https://images.unsplash.com/photo-1617788138017-80ad40651399", # 迈巴赫前脸
    "cullinan": "https://images.unsplash.com/photo-1655132333039-47963d76756d", # 库里南
    "phantom": "https://images.unsplash.com/photo-1631295868223-63265b40d9e4", # 幻影
    "ferrari": "https://images.unsplash.com/photo-1592198084033-aade902d1aae", # 法拉利
    "lambo_suv": "https://images.unsplash.com/photo-1621996659490-6213b1859303", # Urus
    "lambo_car": "https://images.unsplash.com/photo-1544636331-e26879cd4d9b", # 兰博超跑
    "porsche": "https://images.unsplash.com/photo-1503376763036-066120622c74", # 911
    "bugatti": "https://images.unsplash.com/photo-1627454820574-fb40e69228d4", # 布加迪
    "mclaren": "https://images.unsplash.com/photo-1621135802920-133df287f89c", # 迈凯伦
    "aston": "https://images.unsplash.com/photo-1600712242805-5f78671d2434", # 阿斯顿马丁
    "suv_big": "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf", # 领航员/路虎
    "bmw": "https://images.unsplash.com/photo-1555215695-3004980adade", # 宝马
    "audi": "https://images.unsplash.com/photo-1603584173870-7f23fdae1b7a", # 奥迪
    
    # --- 飞机 ---
    "g700": "https://images.unsplash.com/photo-1540962351504-03099e0a754b", # 湾流内饰/窗
    "g_ext": "https://images.unsplash.com/photo-1474302770737-173ee21bab63", # 湾流外观
    "bbj": "https://images.unsplash.com/photo-1559081556-98d75e032532", # 波音大客机
    "bombardier": "https://images.unsplash.com/photo-1583417319070-4a69db38a482", # 庞巴迪
    
    # --- 游艇 ---
    "yacht_huge": "https://images.unsplash.com/photo-1569263979104-865ab7cd8d13", # 巨型游艇
    "yacht_std": "https://images.unsplash.com/photo-1605281317010-fe5ffe79b9b4", # 标准超游
    
    # --- 房产 ---
    "tower": "https://images.unsplash.com/photo-1486325212027-8081e485255e", # 摩天大楼
    "mansion": "https://images.unsplash.com/photo-1613490493576-7fde63acd811", # 豪宅
    "courtyard": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/14/Siheyuan_Beijing.jpg/800px-Siheyuan_Beijing.jpg",
    
    # --- 奢侈品 ---
    "patek": "https://images.unsplash.com/photo-1639037688267-3323a73df667", # 鹦鹉螺
    "rolex": "https://images.unsplash.com/photo-1622434641406-a158105c9168", # 迪通拿
    "rm": "https://images.unsplash.com/photo-1600003014608-c2ccc1570a65", # 镂空表
    "birkin_him": "https://images.unsplash.com/photo-1584917865442-de89df76afd3", # 浅色包
    "kelly": "https://images.unsplash.com/photo-1594223274512-ad4803739b7c", # 深色包
    
    "default": "https://images.unsplash.com/photo-1550989460-0adf9ea622e2" # 黑色背景
}

def get_img(name, cat):
    n = name.lower() # 只转小写，不删空格
    
    # Cars
    if cat == "Car":
        if "g 63" in n or "g800" in n: return IMG["g_wagon"]
        if "sl" in n or "roadster" in n: return IMG["sl_amg"]
        if "maybach" in n or "s 680" in n or "pullman" in n: return IMG["maybach"]
        if "cullinan" in n or "dbx" in n: return IMG["cullinan"]
        if "phantom" in n or "spectre" in n or "ghost" in n: return IMG["phantom"]
        if "ferrari" in n or "sf90" in n: return IMG["ferrari"]
        if "urus" in n: return IMG["lambo_suv"]
        if "lambo" in n or "revuelto" in n: return IMG["lambo_car"]
        if "porsche" in n: return IMG["porsche"]
        if "bugatti" in n or "chiron" in n: return IMG["bugatti"]
        if "mclaren" in n: return IMG["mclaren"]
        if "aston" in n: return IMG["aston"]
        if "navigator" in n or "escalade" in n or "range" in n: return IMG["suv_big"]
        if "bmw" in n: return IMG["bmw"]
        if "audi" in n: return IMG["audi"]
        return IMG["maybach"] # 默认给个奔驰脸
    
    # Jets
    if cat == "Jet":
        if "bbj" in n or "787" in n or "777" in n: return IMG["bbj"]
        if "g700" in n: return IMG["g700"] # 湾流特写
        if "gulfstream" in n: return IMG["g_ext"] # 湾流外观
        return IMG["bombardier"]
        
    # Yachts
    if cat == "Yacht":
        if "azzam" in n or "eclipse" in n or "dilbar" in n: return IMG["yacht_huge"]
        return IMG["yacht_std"]
        
    # Estate
    if cat == "Estate":
        if "tower" in n or "101" in n or "penthouse" in n or "sky" in n: return IMG["tower"]
        if "courtyard" in n: return IMG["courtyard"]
        return IMG["mansion"]
    
    # Watch
    if cat == "Watch":
        if "patek" in n: return IMG["patek"]
        if "richard" in n or "rm" in n: return IMG["rm"]
        return IMG["rolex"]
        
    # Luxury
    if cat == "Luxury":
        if "himalaya" in n or "white" in n: return IMG["birkin_him"]
        return IMG["kelly"]
        
    return IMG["default"]

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
# 3. 完整数据库
# ==========================================
def create_db():
    db = {"Car":[], "Jet":[], "Yacht":[], "Estate":[], "Watch":[], "Luxury":[]}
    
    # --- Cars ---
    cars = [
        ("Mercedes-AMG G63", 190000), ("Mercedes-AMG SL63", 185000), ("Maybach S680", 250000),
        ("Rolls-Royce Cullinan", 400000), ("Rolls-Royce Phantom", 600000), ("Rolls-Royce Spectre", 450000),
        ("Ferrari SF90 Spider", 550000), ("Ferrari Purosangue", 400000), ("LaFerrari", 3000000),
        ("Lamborghini Revuelto", 600000), ("Lamborghini Urus", 270000), 
        ("Porsche 911 Turbo S", 240000), ("Bugatti Chiron", 3500000), ("Bugatti Mistral", 5000000),
        ("McLaren Speedtail", 2500000), ("Aston Martin Valkyrie", 3500000),
        ("Lincoln Navigator", 120000), ("Range Rover SV", 250000), ("Cadillac Escalade", 150000),
        ("BMW M4 Competition", 95000), ("Audi RS6 Avant", 130000)
    ]
    for n, p in cars:
        db["Car"].append({"name":n, "price":p, "img":get_img(n, "Car"), "opts":["Paint","Interior"]})

    # --- Jets ---
    jets = [
        ("Gulfstream G700", 78000000), ("Gulfstream G650ER", 70000000), ("Gulfstream G280", 25000000),
        ("Bombardier Global 7500", 75000000), ("Dassault Falcon 10X", 75000000),
        ("Boeing BBJ MAX 7", 100000000), ("Boeing BBJ 787 Dreamliner", 250000000)
    ]
    for n, p in jets:
        db["Jet"].append({"name":n, "price":p, "img":get_img(n, "Jet"), "opts":["Layout","Livery"]})

    # --- Yachts ---
    yachts = [
        ("Lürssen Azzam (180m)", 600000000), ("Blohm+Voss Eclipse", 500000000), ("Lürssen Dilbar", 800000000),
        ("Oceanco Jubilee", 300000000), ("Feadship Anna", 250000000)
    ]
    for n, p in yachts:
        db["Yacht"].append({"name":n, "price":p, "img":get_img(n, "Yacht"), "opts":["Helipad","Pool"]})

    # --- Estate ---
    estates = [
        ("NY Central Park Tower PH", 250000000), ("Beverly Hills The One", 145000000),
        ("Shanghai Tan Gong Villa", 100000000), ("Hong Kong Barker Rd", 280000000),
        ("Beijing Houhai Courtyard", 180000000), ("Shenzhen Bay No.1", 85000000)
    ]
    for n, p in estates:
        db["Estate"].append({"name":n, "price":p, "img":get_img(n, "Estate"), "opts":["Furniture","Security"]})

    # --- Watches ---
    watches = [
        ("Patek Philippe Nautilus", 150000), ("Patek Philippe Grandmaster", 2500000),
        ("Rolex Daytona Rainbow", 350000), ("Rolex Paul Newman", 200000),
        ("Richard Mille RM 52-01", 800000)
    ]
    for n, p in watches:
        db["Watch"].append({"name":n, "price":p, "img":get_img(n, "Watch"), "opts":["Material"]})

    # --- Luxury ---
    lux = [
        ("Hermès Birkin Himalaya", 200000), ("Hermès Birkin Faubourg", 150000),
        ("Hermès Kelly Crocodile", 80000), ("Louis Vuitton Trunk", 60000)
    ]
    for n, p in lux:
        db["Luxury"].append({"name":n, "price":p, "img":get_img(n, "Luxury"), "opts":["Leather"]})

    return db

DB = create_db()

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

tabs = st.tabs(["🏎️ Cars", "✈️ Jets", "⚓ Yachts", "🏰 Estate", "⌚ Watches", "👜 Luxury", "💼 Assets"])
cats = ["Car", "Jet", "Yacht", "Estate", "Watch", "Luxury"]

for i, cat in enumerate(cats):
    with tabs[i]:
        items = DB[cat]
        # 简单搜索
        if cat == "Car":
            search = st.text_input("Search", key="s_car").lower()
            items = [x for x in items if search in x['name'].lower()]
            
        for item in items:
            with st.container():
                st.markdown(f"<div class='asset-card'>", unsafe_allow_html=True)
                c1, c2 = st.columns([2, 3])
                c1.image(item['img'])
                with c2:
                    st.markdown(f"### {item['name']}")
                    st.markdown(f"**${item['price']:,}**")
                    with st.expander("Configure"):
                        for o in item['opts']: st.selectbox(o, ["Standard", "Upgrade", "Bespoke"], key=f"{item['name']}_{o}")
                        if st.button("BUY", key=f"btn_{item['name']}"): buy(item)
                st.markdown("</div>", unsafe_allow_html=True)

with tabs[6]:
    if not st.session_state.inventory: st.info("Inventory Empty")
    for i, item in enumerate(st.session_state.inventory):
        with st.container():
            c1, c2 = st.columns([1, 3])
            c1.image(item['img'])
            with c2:
                st.write(f"**{item['name']}**")
                if st.button("SELL", key=f"sell_{i}"): sell(i)
