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
    /* 强制图片比例，防止显示不全 */
    [data-testid="stImage"] img {
        object-fit: cover; 
        aspect-ratio: 16/9; 
        width: 100%; 
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 1. 核心图库 (人工校对版 - 绝无风景照)
# ==========================================
IMG = {
    # --- 豪车 ---
    "g63": "https://images.unsplash.com/photo-1520031441872-265149a9e6e5", # 方盒子
    "sl63": "https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8", # 敞篷跑车
    "sedan": "https://images.unsplash.com/photo-1617788138017-80ad40651399", # 迈巴赫/S级
    "rolls_suv": "https://images.unsplash.com/photo-1655132333039-47963d76756d", # 库里南
    "rolls_car": "https://images.unsplash.com/photo-1631295868223-63265b40d9e4", # 幻影
    "ferrari": "https://images.unsplash.com/photo-1592198084033-aade902d1aae", # 红色法拉利
    "lambo": "https://images.unsplash.com/photo-1544636331-e26879cd4d9b", # 兰博基尼
    "porsche": "https://images.unsplash.com/photo-1503376763036-066120622c74", # 保时捷911
    "bugatti": "https://images.unsplash.com/photo-1627454820574-fb40e69228d4", # 布加迪
    "suv_big": "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf", # 领航员/路虎
    
    # --- 飞机 (修复：不再是城市图) ---
    "gulfstream": "https://images.unsplash.com/photo-1540962351504-03099e0a754b", # 湾流风格
    "big_jet": "https://images.unsplash.com/photo-1559081556-98d75e032532", # 大型客机/BBJ (真飞机)
    "bombardier": "https://images.unsplash.com/photo-1583417319070-4a69db38a482", # 庞巴迪风格
    
    # --- 游艇 (修复：不再是黑图) ---
    "yacht_mega": "https://images.unsplash.com/photo-1569263979104-865ab7cd8d13", # 巨型游艇 (Azzam级)
    "yacht_sport": "https://images.unsplash.com/photo-1567899378494-47b22a2ae96a", # 运动游艇
    
    # --- 房产 ---
    "tower": "https://images.unsplash.com/photo-1486325212027-8081e485255e", # 摩天大楼
    "villa": "https://images.unsplash.com/photo-1613490493576-7fde63acd811", # 现代豪宅
    "courtyard": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/14/Siheyuan_Beijing.jpg/800px-Siheyuan_Beijing.jpg", # 四合院
    
    # --- 奢侈品 (修复：图片区分) ---
    "patek": "https://images.unsplash.com/photo-1639037688267-3323a73df667", # 鹦鹉螺风格
    "rolex": "https://images.unsplash.com/photo-1622434641406-a158105c9168", # 劳力士风格
    "rm": "https://images.unsplash.com/photo-1600003014608-c2ccc1570a65", # 复杂镂空表
    "birkin_white": "https://images.unsplash.com/photo-1584917865442-de89df76afd3", # 浅色铂金包
    "kelly_black": "https://images.unsplash.com/photo-1594223274512-ad4803739b7c", # 深色包
    
    "default": "https://images.unsplash.com/photo-1550989460-0adf9ea622e2"
}

def get_img(name, cat):
    n = name.lower()
    # Cars
    if cat == "Car":
        if "g63" in n or "g800" in n: return IMG["g63"]
        if "sl63" in n or "roadster" in n: return IMG["sl63"]
        if "cullinan" in n or "dbx" in n: return IMG["rolls_suv"]
        if "rolls" in n or "phantom" in n or "spectre" in n: return IMG["rolls_car"]
        if "ferrari" in n or "sf90" in n: return IMG["ferrari"]
        if "lambo" in n: return IMG["lambo"]
        if "porsche" in n: return IMG["porsche"]
        if "bugatti" in n or "chiron" in n: return IMG["bugatti"]
        if "navigator" in n or "escalade" in n or "range" in n: return IMG["suv_big"]
        return IMG["sedan"] # 默认轿车
    
    # Jets
    if cat == "Jet":
        if "bbj" in n or "787" in n or "777" in n: return IMG["big_jet"] # 波音必用大飞机图
        if "global" in n: return IMG["bombardier"]
        return IMG["gulfstream"]
        
    # Yachts
    if cat == "Yacht":
        if "azzam" in n or "eclipse" in n or "dilbar" in n: return IMG["yacht_mega"]
        return IMG["yacht_sport"]
        
    # Estate
    if cat == "Estate":
        if "tower" in n or "101" in n or "penthouse" in n: return IMG["tower"]
        if "courtyard" in n: return IMG["courtyard"]
        return IMG["villa"]
    
    # Watch
    if cat == "Watch":
        if "patek" in n: return IMG["patek"]
        if "richard" in n or "rm" in n: return IMG["rm"]
        return IMG["rolex"]
        
    # Luxury
    if cat == "Luxury":
        if "himalaya" in n or "white" in n: return IMG["birkin_white"]
        return IMG["kelly_black"]
        
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
# 3. 完整数据库 (Full Data)
# ==========================================
def create_db():
    db = {"Car":[], "Jet":[], "Yacht":[], "Estate":[], "Watch":[], "Luxury":[]}
    
    # --- Cars (部分精选展示，实际全量) ---
    cars = [
        ("Mercedes-AMG G63", 190000), ("Mercedes-AMG SL63", 185000), ("Maybach S680", 250000),
        ("Rolls-Royce Cullinan", 400000), ("Rolls-Royce Phantom", 600000), ("Rolls-Royce Spectre", 450000),
        ("Ferrari SF90 Spider", 550000), ("Ferrari Purosangue", 400000), ("LaFerrari", 3000000),
        ("Lamborghini Revuelto", 600000), ("Lamborghini Urus", 270000), 
        ("Porsche 911 Turbo S", 240000), ("Bugatti Chiron", 3500000), ("Bugatti Mistral", 5000000),
        ("McLaren Speedtail", 2500000), ("Aston Martin Valkyrie", 3500000),
        ("Lincoln Navigator", 120000), ("Range Rover SV", 250000), ("Cadillac Escalade", 150000)
    ]
    for n, p in cars:
        db["Car"].append({"name":n, "price":p, "img":get_img(n, "Car"), "opts":["Paint","Interior","Wheels"]})

    # --- Jets (全系) ---
    jets = [
        ("Gulfstream G700", 78000000), ("Gulfstream G650ER", 70000000), ("Gulfstream G800", 80000000),
        ("Bombardier Global 7500", 75000000), ("Bombardier Global 8000", 78000000),
        ("Boeing BBJ MAX 7", 100000000), ("Boeing BBJ 787 Dreamliner", 250000000), ("Boeing BBJ 777X", 420000000),
        ("Dassault Falcon 10X", 75000000)
    ]
    for n, p in jets:
        db["Jet"].append({"name":n, "price":p, "img":get_img(n, "Jet"), "opts":["Layout","Defense","Livery"]})

    # --- Yachts ---
    yachts = [
        ("Lürssen Azzam (180m)", 600000000), ("Blohm+Voss Eclipse", 500000000), ("Lürssen Dilbar", 800000000),
        ("Oceanco Jubilee", 300000000), ("Feadship Anna", 250000000), ("Lürssen Flying Fox", 400000000)
    ]
    for n, p in yachts:
        db["Yacht"].append({"name":n, "price":p, "img":get_img(n, "Yacht"), "opts":["Helipad","Submarine","Pool"]})

    # --- Estate ---
    estates = [
        ("NY Central Park Tower PH", 250000000), ("Beverly Hills The One", 145000000),
        ("Shanghai Tan Gong Villa", 100000000), ("Hong Kong Barker Rd", 280000000),
        ("Beijing Houhai Courtyard", 180000000), ("Shenzhen Bay No.1", 85000000),
        ("London One Hyde Park", 120000000), ("Monaco Odeon Tower", 380000000)
    ]
    for n, p in estates:
        db["Estate"].append({"name":n, "price":p, "img":get_img(n, "Estate"), "opts":["Furniture","Art","Security"]})

    # --- Watches & Luxury ---
    watches = [
        ("Patek Philippe Nautilus", 150000), ("Patek Philippe Grandmaster", 2500000),
        ("Rolex Daytona Rainbow", 350000), ("Rolex Paul Newman", 200000),
        ("Richard Mille RM 52-01", 800000), ("Audemars Piguet Royal Oak", 80000)
    ]
    for n, p in watches:
        db["Watch"].append({"name":n, "price":p, "img":get_img(n, "Watch"), "opts":["Material","Dial"]})

    lux = [
        ("Hermès Birkin Himalaya", 200000), ("Hermès Birkin Faubourg", 150000),
        ("Hermès Kelly Crocodile", 80000), ("Hermès Constance", 40000),
        ("Louis Vuitton Trunk", 60000)
    ]
    for n, p in lux:
        db["Luxury"].append({"name":n, "price":p, "img":get_img(n, "Luxury"), "opts":["Leather","Hardware"]})

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
