import streamlit as st
import pandas as pd
import random

# ==========================================
# 0. 基础配置
# ==========================================
st.set_page_config(page_title="World Owner Pro", layout="wide", page_icon="👑")

st.markdown("""
<style>
    .stApp {background-color: #000000;}
    .asset-card {border: 1px solid #333; background: #111; border-radius: 12px; padding: 15px; margin-bottom: 15px;}
    h1, h2, h3, p, span, div {font-family: 'Helvetica Neue', sans-serif; color: #e0e0e0;}
    h3 {color: #d4af37 !important;} /* 金色标题 */
    [data-testid="stImage"] img {object-fit: cover; aspect-ratio: 16/9; width: 100%; border-radius: 8px;}
    .price {color: #4CAF50; font-family: monospace; font-weight: bold;}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 1. 高清精准图库 (绝对不是特斯拉)
# ==========================================
IMG = {
    # Cars
    "g63": "https://images.unsplash.com/photo-1520031441872-265149a9e6e5", # 奔驰大G
    "sl63": "https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8", # 奔驰敞篷
    "s680": "https://images.unsplash.com/photo-1617788138017-80ad40651399", # 迈巴赫轿车
    "cullinan": "https://images.unsplash.com/photo-1655132333039-47963d76756d", # 劳斯SUV
    "phantom": "https://images.unsplash.com/photo-1631295868223-63265b40d9e4", # 劳斯轿车
    "ferrari": "https://images.unsplash.com/photo-1592198084033-aade902d1aae", # 法拉利红
    "lambo_suv": "https://images.unsplash.com/photo-1621996659490-6213b1859303", # Urus
    "lambo_car": "https://images.unsplash.com/photo-1544636331-e26879cd4d9b", # 兰博超跑
    "porsche_911": "https://images.unsplash.com/photo-1503376763036-066120622c74", # 911
    "bugatti": "https://images.unsplash.com/photo-1627454820574-fb40e69228d4", # 布加迪
    "mclaren": "https://images.unsplash.com/photo-1621135802920-133df287f89c", # 迈凯伦
    "suv": "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf", # 大型SUV(领航员等)
    "bmw": "https://images.unsplash.com/photo-1555215695-3004980adade", # 宝马
    "audi": "https://images.unsplash.com/photo-1603584173870-7f23fdae1b7a", # 奥迪RS
    
    # Fleet
    "gulfstream": "https://images.unsplash.com/photo-1540962351504-03099e0a754b", # 湾流
    "bbj": "https://images.unsplash.com/photo-1583417319070-4a69db38a482", # BBJ大客机
    "bombardier": "https://images.unsplash.com/photo-1624623190870-1329dc334b07", # 庞巴迪
    "azzam": "https://images.unsplash.com/photo-1569263979104-865ab7cd8d13", # 巨型游艇
    "yacht": "https://images.unsplash.com/photo-1605281317010-fe5ffe79b9b4", # 普通超游
    
    # Estate
    "tower": "https://images.unsplash.com/photo-1512917774080-9991f1c4c750", # 摩天大楼
    "mansion": "https://images.unsplash.com/photo-1613490493576-7fde63acd811", # 现代豪宅
    "courtyard": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/14/Siheyuan_Beijing.jpg/800px-Siheyuan_Beijing.jpg", # 四合院
    
    # Goods
    "nautilus": "https://images.unsplash.com/photo-1622434641406-a158105c9168", # 鹦鹉螺
    "rolex": "https://images.unsplash.com/photo-1523170335258-f5ed11844a49", # 劳力士
    "birkin": "https://images.unsplash.com/photo-1584917865442-de89df76afd3", # 铂金包
    "kelly": "https://images.unsplash.com/photo-1594223274512-ad4803739b7c", # 凯莉包
    
    "default": "https://images.unsplash.com/photo-1550989460-0adf9ea622e2" # 黑色背景防错
}

def get_img(name, cat):
    n = name.lower().replace(" ", "").replace("-", "")
    # 车辆匹配
    if cat == "Car":
        if "g63" in n or "g800" in n: return IMG["g63"]
        if "sl63" in n or "roadster" in n: return IMG["sl63"]
        if "s680" in n or "maybach" in n or "pullman" in n: return IMG["s680"]
        if "cullinan" in n or "dbx" in n or "bentayga" in n: return IMG["cullinan"]
        if "phantom" in n or "spectre" in n or "ghost" in n: return IMG["phantom"]
        if "ferrari" in n or "sf90" in n or "f80" in n: return IMG["ferrari"]
        if "urus" in n: return IMG["lambo_suv"]
        if "lamborghini" in n or "revuelto" in n: return IMG["lambo_car"]
        if "porsche" in n or "911" in n: return IMG["porsche_911"]
        if "bugatti" in n or "chiron" in n: return IMG["bugatti"]
        if "mclaren" in n: return IMG["mclaren"]
        if "navigator" in n or "escalade" in n or "range" in n: return IMG["suv"]
        if "bmw" in n: return IMG["bmw"]
        if "audi" in n: return IMG["audi"]
        return IMG["s680"] # 默认豪车
        
    # 飞机匹配
    if cat == "Jet":
        if "bbj" in n or "787" in n: return IMG["bbj"]
        if "global" in n or "challenger" in n: return IMG["bombardier"]
        return IMG["gulfstream"]
        
    # 游艇匹配
    if cat == "Yacht":
        if "azzam" in n or "eclipse" in n or "dilbar" in n: return IMG["azzam"]
        return IMG["yacht"]
        
    # 房产匹配
    if cat == "Estate":
        if "tower" in n or "101" in n or "bay" in n or "penthouse" in n: return IMG["tower"]
        if "courtyard" in n: return IMG["courtyard"]
        return IMG["mansion"]
    
    # 奢侈品匹配
    if cat == "Watch":
        if "patek" in n: return IMG["nautilus"]
        return IMG["rolex"]
    if cat == "Luxury":
        if "birkin" in n: return IMG["birkin"]
        return IMG["kelly"]
        
    return IMG["default"]

# ==========================================
# 2. 数据工厂 (Full Data)
# ==========================================
def create_db():
    db = {"Car":[], "Jet":[], "Yacht":[], "Estate":[], "Watch":[], "Luxury":[]}
    
    # --- Cars (60+) ---
    car_data = [
        ("Mercedes-AMG SL63", 185000), ("Mercedes-AMG G63", 190000), ("Maybach S680", 250000), 
        ("Maybach Pullman", 1600000), ("Brabus G800", 450000), ("Mercedes AMG GT Black", 350000),
        ("BMW M4 Competition", 95000), ("BMW M8", 140000), ("BMW i8 Roadster", 165000),
        ("Audi RS6 Avant", 130000), ("Audi RS7", 135000), ("Audi A8 Horch", 180000),
        ("Cadillac Escalade-V", 155000), ("Lincoln Navigator", 120000), ("Range Rover SV", 240000),
        ("Porsche 911 Turbo S", 240000), ("Porsche 911 GT3 RS", 280000), ("Porsche Taycan GT", 230000),
        ("Maserati MC20", 220000), ("McLaren 765LT", 390000), ("McLaren Speedtail", 2500000),
        ("Aston Martin DB12", 250000), ("Aston Martin Valkyrie", 3500000), ("Aston Martin DBX", 245000),
        ("Ferrari SF90", 550000), ("Ferrari Purosangue", 400000), ("Ferrari F80", 4000000), 
        ("Ferrari 488 Pista", 450000), ("Ferrari 812 Comp", 650000), ("Ferrari LaFerrari", 3000000),
        ("Lamborghini Revuelto", 620000), ("Lamborghini Urus", 270000), ("Lamborghini Countach", 2700000),
        ("Rolls-Royce Spectre", 450000), ("Rolls-Royce Cullinan", 400000), ("Rolls-Royce Phantom", 600000),
        ("Rolls-Royce Boat Tail", 28000000), ("Bentley Continental GT", 300000), ("Bentley Bentayga", 280000),
        ("Koenigsegg Jesko", 3400000), ("Pagani Utopia", 2500000), ("Bugatti Chiron", 3300000),
        ("Bugatti La Voiture Noire", 18000000), ("Bugatti Mistral", 5000000)
    ]
    for n, p in car_data:
        db["Car"].append({"name":n, "price":p, "img":get_img(n, "Car"), "opts":["Paint", "Wheels", "Interior"]})

    # --- Jets (Full Fleet) ---
    jet_data = [
        ("Gulfstream G700", 78000000), ("Gulfstream G650ER", 70000000), ("Gulfstream G280", 25000000),
        ("Bombardier Global 7500", 75000000), ("Bombardier Global 6500", 56000000),
        ("Dassault Falcon 10X", 75000000), ("Dassault Falcon 8X", 58000000),
        ("Boeing BBJ MAX 7", 100000000), ("Boeing BBJ 787 Dreamliner", 250000000), ("Boeing BBJ 777X", 400000000)
    ]
    for n, p in jet_data:
        db["Jet"].append({"name":n, "price":p, "img":get_img(n, "Jet"), "opts":["Layout", "Livery", "Defense"]})

    # --- Yachts (Mega) ---
    yacht_data = [
        ("Lürssen Azzam (180m)", 600000000), ("Blohm+Voss Eclipse", 1200000000), ("Lürssen Dilbar", 800000000),
        ("Oceanco Jubilee", 300000000), ("Feadship Anna", 250000000), ("Lürssen Flying Fox", 400000000)
    ]
    for n, p in yacht_data:
        db["Yacht"].append({"name":n, "price":p, "img":get_img(n, "Yacht"), "opts":["Helipad", "Submarine", "Pool"]})

    # --- Estate ---
    est_data = [
        ("NY Central Park Tower PH", 250000000), ("Beverly Hills The One", 145000000),
        ("Shanghai Tan Gong Villa", 100000000), ("Hong Kong Barker Rd", 280000000),
        ("Shenzhen Bay No.1", 85000000), ("Beijing Houhai Courtyard", 180000000),
        ("London One Hyde Park", 120000000), ("Monaco Odeon Tower", 380000000)
    ]
    for n, p in est_data:
        db["Estate"].append({"name":n, "price":p, "img":get_img(n, "Estate"), "opts":["Decor", "Security", "Art"]})

    # --- Watches (Specific) ---
    watches = [
        ("Patek Philippe Nautilus 5711", 150000), ("Patek Philippe Grandmaster Chime", 2500000),
        ("Patek Philippe Sky Moon", 1200000), ("Rolex Daytona Rainbow", 350000),
        ("Rolex Daytona Paul Newman", 200000), ("Audemars Piguet Royal Oak", 80000),
        ("Richard Mille RM 52-01", 800000), ("Jacob & Co Astronomia", 500000)
    ]
    for n, p in watches:
        db["Watch"].append({"name":n, "price":p, "img":get_img(n, "Watch"), "opts":["Material", "Dial"]})

    # --- Luxury (Specific) ---
    bags = [
        ("Hermès Birkin Himalaya", 200000), ("Hermès Birkin Faubourg", 150000),
        ("Hermès Kelly Crocodile", 80000), ("Hermès Constance Lizard", 40000),
        ("Louis Vuitton Trunk", 60000), ("Chanel Classic Flap", 12000)
    ]
    for n, p in bags:
        db["Luxury"].append({"name":n, "price":p, "img":get_img(n, "Luxury"), "opts":["Leather", "Hardware"]})

    return db

DB = create_db()

# ==========================================
# 3. 逻辑与渲染
# ==========================================
if 'cash' not in st.session_state: st.session_state.cash = 10000000000
if 'inventory' not in st.session_state: st.session_state.inventory = []

def buy(item):
    if st.session_state.cash >= item['price']:
        st.session_state.cash -= item['price']
        st.session_state.inventory.append(item)
        st.toast(f"Bought {item['name']}!")
        st.rerun()

def sell(i):
    item = st.session_state.inventory.pop(i)
    st.session_state.cash += item['price']
    st.toast("Sold!")
    st.rerun()

with st.sidebar:
    st.title("👑 World Owner")
    st.metric("Cash Available", f"${st.session_state.cash:,.0f}")
    if st.button("Reset Game"): 
        st.session_state.cash = 10000000000
        st.session_state.inventory = []
        st.rerun()

tabs = st.tabs(["🏎️ Cars", "✈️ Jets", "⚓ Yachts", "🏰 Estate", "⌚ Watches", "👜 Luxury", "💼 Assets"])

categories = ["Car", "Jet", "Yacht", "Estate", "Watch", "Luxury"]

for i, cat in enumerate(categories):
    with tabs[i]:
        # Filter for Cars
        if cat == "Car":
            search = st.text_input("Search Car", "").lower()
            items = [x for x in DB[cat] if search in x['name'].lower()]
        else:
            items = DB[cat]
            
        for item in items:
            with st.container():
                st.markdown(f"<div class='asset-card'>", unsafe_allow_html=True)
                c1, c2 = st.columns([2, 3])
                c1.image(item['img'])
                with c2:
                    st.markdown(f"### {item['name']}")
                    st.markdown(f"<span class='price'>${item['price']:,}</span>", unsafe_allow_html=True)
                    with st.expander("Configure"):
                        for opt in item['opts']: st.selectbox(opt, ["Standard", "Upgrade", "Bespoke"], key=f"{item['name']}_{opt}")
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
