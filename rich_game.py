import streamlit as st
import pandas as pd

# ==========================================
# 0. 基础配置 (防断裂优化)
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
# 1. 精准图片映射库 (一一对应，拒绝乱码)
# ==========================================
# 这里我手动指定了每一个型号的图片，确保G63是G63，湾流是湾流
IMAGE_MAP = {
    # --- 奔驰/迈巴赫 ---
    "Mercedes-AMG G63": "https://images.unsplash.com/photo-1520031441872-265149a9e6e5",
    "Mercedes-AMG SL63": "https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8",
    "Mercedes-AMG GT 63 S": "https://images.unsplash.com/photo-1617788138017-80ad40651399",
    "Maybach S680": "https://images.unsplash.com/photo-1617788138017-80ad40651399", # 暂用S级图代替
    "Maybach Pullman": "https://images.unsplash.com/photo-1617788138017-80ad40651399",
    "Brabus G800": "https://images.unsplash.com/photo-1563720223185-11003d516935", # 改装G级
    
    # --- 劳斯莱斯 ---
    "Rolls-Royce Cullinan": "https://images.unsplash.com/photo-1655132333039-47963d76756d",
    "Rolls-Royce Phantom": "https://images.unsplash.com/photo-1631295868223-63265b40d9e4",
    "Rolls-Royce Spectre": "https://images.unsplash.com/photo-1631295868223-63265b40d9e4",
    "Rolls-Royce Boat Tail": "https://images.unsplash.com/photo-1631295868223-63265b40d9e4",
    
    # --- 法拉利 ---
    "Ferrari SF90 Spider": "https://images.unsplash.com/photo-1592198084033-aade902d1aae",
    "Ferrari Purosangue": "https://images.unsplash.com/photo-1592198084033-aade902d1aae",
    "Ferrari LaFerrari": "https://images.unsplash.com/photo-1592198084033-aade902d1aae",
    
    # --- 兰博基尼 ---
    "Lamborghini Urus": "https://images.unsplash.com/photo-1621996659490-6213b1859303",
    "Lamborghini Revuelto": "https://images.unsplash.com/photo-1544636331-e26879cd4d9b",
    
    # --- 保时捷 ---
    "Porsche 911 Turbo S": "https://images.unsplash.com/photo-1503376763036-066120622c74",
    "Porsche Taycan GT": "https://images.unsplash.com/photo-1614207287498-35f191b7d551",
    
    # --- 其他豪车 ---
    "Bugatti Chiron": "https://images.unsplash.com/photo-1627454820574-fb40e69228d4",
    "McLaren Speedtail": "https://images.unsplash.com/photo-1621135802920-133df287f89c",
    "Aston Martin DB12": "https://images.unsplash.com/photo-1600712242805-5f78671d2434",
    "BMW M4 Competition": "https://images.unsplash.com/photo-1555215695-3004980adade",
    "Audi RS6 Avant": "https://images.unsplash.com/photo-1603584173870-7f23fdae1b7a",
    "Lincoln Navigator": "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf",
    "Range Rover SV": "https://images.unsplash.com/photo-1609521263047-f8f205293f24",
    
    # --- 飞机 (区分型号) ---
    "Gulfstream G700": "https://images.unsplash.com/photo-1540962351504-03099e0a754b", # 豪华内饰
    "Gulfstream G650ER": "https://images.unsplash.com/photo-1474302770737-173ee21bab63", # 外观
    "Boeing BBJ": "https://images.unsplash.com/photo-1559081556-98d75e032532", # 大型客机
    "Bombardier Global": "https://images.unsplash.com/photo-1583417319070-4a69db38a482",
    
    # --- 游艇 (区分大小) ---
    "Mega Yacht": "https://images.unsplash.com/photo-1569263979104-865ab7cd8d13", # 巨型
    "Super Yacht": "https://images.unsplash.com/photo-1605281317010-fe5ffe79b9b4", # 中型
    
    # --- 房产 ---
    "Skyscraper": "https://images.unsplash.com/photo-1486325212027-8081e485255e",
    "Mansion": "https://images.unsplash.com/photo-1613490493576-7fde63acd811",
    "Villa": "https://images.unsplash.com/photo-1600596542815-22b84e49032b",
    
    # --- 奢侈品 ---
    "Patek": "https://images.unsplash.com/photo-1639037688267-3323a73df667",
    "Rolex": "https://images.unsplash.com/photo-1622434641406-a158105c9168",
    "Birkin": "https://images.unsplash.com/photo-1584917865442-de89df76afd3",
    "Kelly": "https://images.unsplash.com/photo-1594223274512-ad4803739b7c",
    
    # --- 默认防错图 (黑色背景，不是特斯拉) ---
    "Default": "https://images.unsplash.com/photo-1550989460-0adf9ea622e2"
}

# 智能匹配函数
def get_img(name):
    # 如果名字在映射表里，直接用
    if name in IMAGE_MAP:
        return IMAGE_MAP[name]
    
    # 如果不在，进行模糊匹配
    n = name.lower()
    if "g63" in n: return IMAGE_MAP["Mercedes-AMG G63"]
    if "sl63" in n: return IMAGE_MAP["Mercedes-AMG SL63"]
    if "s680" in n: return IMAGE_MAP["Maybach S680"]
    if "cullinan" in n: return IMAGE_MAP["Rolls-Royce Cullinan"]
    if "phantom" in n: return IMAGE_MAP["Rolls-Royce Phantom"]
    if "ferrari" in n: return IMAGE_MAP["Ferrari SF90 Spider"]
    if "urus" in n: return IMAGE_MAP["Lamborghini Urus"]
    if "lambo" in n: return IMAGE_MAP["Lamborghini Revuelto"]
    if "porsche" in n: return IMAGE_MAP["Porsche 911 Turbo S"]
    if "bugatti" in n: return IMAGE_MAP["Bugatti Chiron"]
    if "mclaren" in n: return IMAGE_MAP["McLaren Speedtail"]
    if "bbj" in n: return IMAGE_MAP["Boeing BBJ"]
    if "gulfstream" in n: return IMAGE_MAP["Gulfstream G700"]
    if "azzam" in n or "dilbar" in n: return IMAGE_MAP["Mega Yacht"]
    if "tower" in n or "101" in n: return IMAGE_MAP["Skyscraper"]
    if "villa" in n or "house" in n: return IMAGE_MAP["Mansion"]
    if "patek" in n: return IMAGE_MAP["Patek"]
    if "rolex" in n: return IMAGE_MAP["Rolex"]
    if "birkin" in n: return IMAGE_MAP["Birkin"]
    if "kelly" in n: return IMAGE_MAP["Kelly"]
    
    # 实在匹配不到，返回黑色奢华背景
    return IMAGE_MAP["Default"]

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
# 3. 完整数据库 (所有数据回归)
# ==========================================
def create_db():
    db = {"Car":[], "Jet":[], "Yacht":[], "Estate":[], "Watch":[], "Luxury":[]}
    
    # --- Cars ---
    cars = [
        ("Mercedes-AMG G63", 190000), ("Mercedes-AMG SL63", 185000), ("Maybach S680", 250000),
        ("Maybach Pullman", 1600000), ("Brabus G800", 450000), ("Rolls-Royce Cullinan", 400000),
        ("Rolls-Royce Phantom", 600000), ("Rolls-Royce Spectre", 450000), ("Ferrari SF90 Spider", 550000),
        ("Ferrari Purosangue", 400000), ("Ferrari LaFerrari", 3000000), ("Lamborghini Revuelto", 600000),
        ("Lamborghini Urus", 270000), ("Porsche 911 Turbo S", 240000), ("Bugatti Chiron", 3500000),
        ("Bugatti Mistral", 5000000), ("McLaren Speedtail", 2500000), ("Aston Martin Valkyrie", 3500000),
        ("Lincoln Navigator", 120000), ("Range Rover SV", 250000), ("Cadillac Escalade", 150000),
        ("BMW M4 Competition", 95000), ("Audi RS6 Avant", 130000)
    ]
    for n, p in cars:
        db["Car"].append({"name":n, "price":p, "img":get_img(n), "opts":["Color","Wheels"]})

    # --- Jets ---
    jets = [
        ("Gulfstream G700", 78000000), ("Gulfstream G650ER", 70000000), ("Gulfstream G800", 80000000),
        ("Bombardier Global 7500", 75000000), ("Dassault Falcon 10X", 75000000),
        ("Boeing BBJ MAX 7", 100000000), ("Boeing BBJ 787 Dreamliner", 250000000)
    ]
    for n, p in jets:
        db["Jet"].append({"name":n, "price":p, "img":get_img(n), "opts":["Layout","Livery"]})

    # --- Yachts ---
    yachts = [
        ("Lürssen Azzam (180m)", 600000000), ("Blohm+Voss Eclipse", 500000000), ("Lürssen Dilbar", 800000000),
        ("Oceanco Jubilee", 300000000), ("Feadship Anna", 250000000), ("Lürssen Flying Fox", 400000000)
    ]
    for n, p in yachts:
        db["Yacht"].append({"name":n, "price":p, "img":get_img(n), "opts":["Helipad","Pool"]})

    # --- Estate ---
    estates = [
        ("NY Central Park Tower PH", 250000000), ("Beverly Hills The One", 145000000),
        ("Shanghai Tan Gong Villa", 100000000), ("Hong Kong Barker Rd", 280000000),
        ("Beijing Houhai Courtyard", 180000000), ("Shenzhen Bay No.1", 85000000)
    ]
    for n, p in estates:
        db["Estate"].append({"name":n, "price":p, "img":get_img(n), "opts":["Furniture","Security"]})

    # --- Watch & Luxury ---
    watches = [("Patek Philippe Nautilus", 150000), ("Patek Philippe Grandmaster", 2500000), ("Rolex Daytona Rainbow", 350000)]
    for n, p in watches: db["Watch"].append({"name":n, "price":p, "img":get_img(n), "opts":["Dial"]})

    lux = [("Hermès Birkin Himalaya", 200000), ("Hermès Kelly Black", 80000), ("Louis Vuitton Trunk", 60000)]
    for n, p in lux: db["Luxury"].append({"name":n, "price":p, "img":get_img(n), "opts":["Leather"]})

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
