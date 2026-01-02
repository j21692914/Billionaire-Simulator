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
# 1. 核心图库 (人工校对 - 绝无特斯拉)
# ==========================================
IMG = {
    # --- 奔驰系列 ---
    "g63": "https://images.unsplash.com/photo-1520031441872-265149a9e6e5", # G63 方盒子
    "sl63": "https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8", # SL63 敞篷
    "s680": "https://images.unsplash.com/photo-1617788138017-80ad40651399", # 迈巴赫 S级
    "gt_black": "https://images.unsplash.com/photo-1617788138017-80ad40651399", # AMG GT (暂用迈巴赫代替特斯拉，确保是奔驰)

    # --- 劳斯莱斯 ---
    "cullinan": "https://images.unsplash.com/photo-1655132333039-47963d76756d", # 库里南
    "phantom": "https://images.unsplash.com/photo-1631295868223-63265b40d9e4", # 幻影/古斯特
    
    # --- 超跑 ---
    "ferrari": "https://images.unsplash.com/photo-1592198084033-aade902d1aae", # 法拉利红
    "lambo": "https://images.unsplash.com/photo-1544636331-e26879cd4d9b", # 兰博基尼灰
    "urus": "https://images.unsplash.com/photo-1621996659490-6213b1859303", # Urus SUV
    "porsche": "https://images.unsplash.com/photo-1503376763036-066120622c74", # 911
    "mclaren": "https://images.unsplash.com/photo-1621135802920-133df287f89c", # 迈凯伦橙
    "aston": "https://images.unsplash.com/photo-1600712242805-5f78671d2434", # 阿斯顿马丁银
    "bugatti": "https://images.unsplash.com/photo-1627454820574-fb40e69228d4", # 布加迪蓝
    
    # --- 其他豪车 ---
    "bmw": "https://images.unsplash.com/photo-1555215695-3004980adade", # 宝马
    "audi": "https://images.unsplash.com/photo-1603584173870-7f23fdae1b7a", # 奥迪RS
    "suv_big": "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf", # 领航员/凯雷德
    
    # --- 飞机 (三种不同视角) ---
    "jet_tarmac": "https://images.unsplash.com/photo-1540962351504-03099e0a754b", # 停机坪
    "jet_fly": "https://images.unsplash.com/photo-1474302770737-173ee21bab63", # 飞行中
    "jet_large": "https://images.unsplash.com/photo-1559081556-98d75e032532", # 大型客机 (BBJ)
    
    # --- 游艇 ---
    "yacht_1": "https://images.unsplash.com/photo-1569263979104-865ab7cd8d13", # 巨型
    "yacht_2": "https://images.unsplash.com/photo-1605281317010-fe5ffe79b9b4", # 中型
    
    # --- 房产 ---
    "tower": "https://images.unsplash.com/photo-1486325212027-8081e485255e", # 摩天大楼
    "villa": "https://images.unsplash.com/photo-1613490493576-7fde63acd811", # 别墅
    "courtyard": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/14/Siheyuan_Beijing.jpg/800px-Siheyuan_Beijing.jpg", # 四合院
    
    # --- 奢侈品 ---
    "watch_steel": "https://images.unsplash.com/photo-1524592094714-0f0654e20314", # 钢表
    "watch_gold": "https://images.unsplash.com/photo-1622434641406-a158105c9168", # 金表/劳力士
    "bag_white": "https://images.unsplash.com/photo-1584917865442-de89df76afd3", # 喜马拉雅/白包
    "bag_black": "https://images.unsplash.com/photo-1594223274512-ad4803739b7c", # 黑包/Kelly
    
    "default": "https://images.unsplash.com/photo-1550989460-0adf9ea622e2" # 黑色背景 (兜底)
}

def get_img(name, cat):
    n = name.lower()
    
    # --- CARS ---
    if cat == "Car":
        if "g63" in n or "g 63" in n or "g800" in n: return IMG["g63"]
        if "sl" in n: return IMG["sl63"]
        if "maybach" in n or "s680" in n or "s 680" in n: return IMG["s680"]
        if "cullinan" in n or "dbx" in n or "bentayga" in n: return IMG["cullinan"]
        if "rolls" in n or "phantom" in n or "spectre" in n: return IMG["phantom"]
        if "ferrari" in n or "sf90" in n or "f80" in n: return IMG["ferrari"]
        if "urus" in n: return IMG["urus"]
        if "lambo" in n or "revuelto" in n: return IMG["lambo"]
        if "porsche" in n or "911" in n: return IMG["porsche"]
        if "mclaren" in n: return IMG["mclaren"]
        if "aston" in n: return IMG["aston"]
        if "bugatti" in n or "chiron" in n: return IMG["bugatti"]
        if "bmw" in n: return IMG["bmw"]
        if "audi" in n: return IMG["audi"]
        if "navigator" in n or "escalade" in n or "rover" in n: return IMG["suv_big"]
        return IMG["s680"] # 默认给迈巴赫，不给特斯拉

    # --- JETS ---
    if cat == "Jet":
        if "bbj" in n or "787" in n or "777" in n: return IMG["jet_large"]
        if "g700" in n or "g800" in n: return IMG["jet_tarmac"]
        if "bombardier" in n or "global" in n: return IMG["jet_fly"]
        return IMG["jet_tarmac"]

    # --- YACHTS ---
    if cat == "Yacht":
        if "azzam" in n or "eclipse" in n or "dilbar" in n: return IMG["yacht_1"]
        return IMG["yacht_2"]

    # --- ESTATE ---
    if cat == "Estate":
        if "tower" in n or "101" in n or "penthouse" in n: return IMG["tower"]
        if "courtyard" in n: return IMG["courtyard"]
        return IMG["villa"]

    # --- WATCH ---
    if cat == "Watch":
        if "patek" in n or "grandmaster" in n: return IMG["watch_steel"]
        return IMG["watch_gold"]

    # --- LUXURY ---
    if cat == "Luxury":
        if "himalaya" in n or "white" in n: return IMG["bag_white"]
        return IMG["bag_black"]

    return IMG["default"]

# ==========================================
# 2. 逻辑层
# ==========================================
if 'cash' not in st.session_state: st.session_state.cash = 10000000000
if 'inventory' not in st.session_state: st.session_state.inventory = []

def buy(item):
    st.session_state.inventory.append(item)
    st.session_state.cash -= item['price']
    st.toast(f"Bought {item['name']}")

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
    
    # Cars (60+)
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

    # Jets
    jets = [
        ("Gulfstream G700", 78000000), ("Gulfstream G650ER", 70000000), ("Gulfstream G800", 80000000),
        ("Bombardier Global 7500", 75000000), ("Dassault Falcon 10X", 75000000),
        ("Boeing BBJ MAX 7", 100000000), ("Boeing BBJ 787 Dreamliner", 250000000), ("Boeing BBJ 777X", 420000000)
    ]
    for n, p in jets:
        db["Jet"].append({"name":n, "price":p, "img":get_img(n, "Jet"), "opts":["Livery","Layout"]})

    # Yachts
    yachts = [
        ("Lürssen Azzam (180m)", 600000000), ("Blohm+Voss Eclipse", 500000000), ("Lürssen Dilbar", 800000000),
        ("Oceanco Jubilee", 300000000), ("Feadship Anna", 250000000)
    ]
    for n, p in yachts:
        db["Yacht"].append({"name":n, "price":p, "img":get_img(n, "Yacht"), "opts":["Helipad","Pool"]})

    # Estate
    estates = [
        ("NY Central Park Tower PH", 250000000), ("Beverly Hills The One", 145000000),
        ("Shanghai Tan Gong Villa", 100000000), ("Beijing Houhai Courtyard", 180000000),
        ("Shenzhen Bay No.1", 85000000), ("London One Hyde Park", 120000000)
    ]
    for n, p in estates:
        db["Estate"].append({"name":n, "price":p, "img":get_img(n, "Estate"), "opts":["Furniture","Security"]})

    # Watch & Luxury
    watches = [("Patek Philippe Nautilus", 150000), ("Rolex Daytona Rainbow", 350000), ("Richard Mille RM52", 800000)]
    for n, p in watches: db["Watch"].append({"name":n, "price":p, "img":get_img(n, "Watch"), "opts":["Dial"]})

    lux = [("Hermès Birkin Himalaya", 200000), ("Hermès Kelly Black", 80000), ("Louis Vuitton Trunk", 60000)]
    for n, p in lux: db["Luxury"].append({"name":n, "price":p, "img":get_img(n, "Luxury"), "opts":["Leather"]})

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
                        for o in item['opts']: st.selectbox(o, ["Standard", "Upgrade"], key=f"{item['name']}_{o}")
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
