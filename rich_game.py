import streamlit as st
import pandas as pd
import random
import json
import os

# ==========================================
# 0. UI & 基础配置 (HD优化版)
# ==========================================
st.set_page_config(page_title="World Owner HD", layout="wide", page_icon="🌍")

st.markdown("""
<style>
    .stApp {background-color: #050505;} /* 稍微提亮背景，增加层次感 */
    [data-testid="stSidebar"] {background-color: #0a0a0a; border-right: 1px solid #222;}
    h1, h2, h3, h4 {color: #E5C1CD !important; font-family: 'Didot', serif; letter-spacing: 1px;}
    div, p, span {color: #b0b0b0; font-family: 'Helvetica Neue', sans-serif;}
    
    /* 资产卡片优化 - 更宽，更奢华 */
    .asset-card {
        border: 1px solid #333; 
        background: linear-gradient(145deg, #111, #0a0a0a); 
        border-radius: 12px; 
        padding: 15px; 
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    
    .gold {color: #D4AF37; font-weight: bold; letter-spacing: 0.5px;}
    .price-tag {font-family: 'Courier New'; color: #50C878; font-weight: bold;}
    
    /* --- 核心：高清图片容器 --- */
    [data-testid="stImage"] {
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 10px rgba(0,0,0,0.3);
    }
    [data-testid="stImage"] > img {
        object-fit: cover; 
        aspect-ratio: 16/9; /* 强制电影感宽幅比例 */
        width: 100%; /* 强制撑满容器 */
        transition: transform 0.3s ease;
    }
    [data-testid="stImage"] > img:hover {
        transform: scale(1.02); /* 鼠标悬停微放大效果 */
    }
</style>
""", unsafe_allow_html=True)

SAVE_FILE = "/app/game_save_v10.json"

# ==========================================
# 1. 深度选配矩阵 (保持不变)
# ==========================================
# 🏎️ 豪车选配
OPTS_CAR = {
    "Paint": {"Standard":0, "Metallic":5000, "Matte":15000, "PTS/Bespoke":45000, "Exposed Carbon":150000, "Chameleon":20000},
    "Wheels": {"Standard":0, "Forged Light":12000, "Center Lock":18000, "Carbon Fiber":45000, "Gold Plated":30000},
    "Interior": {"Leather":0, "Alcantara":5000, "Hermès Leather":55000, "Full Carbon Buckets":25000},
    "Brakes": {"Steel":0, "Ceramic Composite":12000, "Painted Calipers":2000, "Gold Calipers":5000},
    "Exhaust": {"Standard":0, "Sport Exhaust":5000, "Titanium System":15000, "Inconel":25000},
    "Aero": {"Standard":0, "Carbon Splitters":15000, "Active Wing":35000, "Roof Scoop":20000},
    "Tech": {"Standard":0, "Track Telemetry":8000, "Night Vision":5000, "High-End Audio":12000},
    "Roof": {"Standard":0, "Glass Roof":5000, "Carbon Roof":12000, "Convertible":15000},
    "Livery": {"None":0, "Racing Stripes":8000, "Hand Painted Art":35000, "Gold Leaf":50000},
    "Steering": {"Leather":0, "Alcantara":2000, "Carbon + LEDs":8000},
    "Glazing": {"Standard":0, "Privacy Glass":2000, "Lightweight Glass":15000},
    "Delivery": {"Dealer":0, "Factory VIP":5000, "Air Freight":15000}
}
# ✈️ 公务机选配
OPTS_JET = {
    "Layout": {"Executive 14 Pax":0, "Master Bedroom + Shower":2000000, "Majlis Style":1500000, "Flying Hospital":3000000},
    "Connectivity": {"Ka-Band WiFi":500000, "Military Encrypted Sat-Link":2500000, "Starlink":100000},
    "Defense": {"None":0, "Anti-Missile Jammer (DIRCM)":4500000, "Chaff/Flare Dispensers":2000000},
    "Livery": {"White":0, "Matte Black":250000, "Custom Art":500000, "Chrome Polish":1000000},
    "Galley": {"Standard":0, "Chef Kitchen + Oven":800000, "Walk-in Cooler":300000},
    "Crew": {"Standard":0, "Top Tier (24/7)":800000, "Medical Team":1200000},
    "Range": {"Standard":0, "Auxiliary Fuel Tanks":1500000, "Aerial Refueling Probe (Mock)":500000},
    "Entertainment": {"HD Screens":0, "4K OLED Theatre":500000, "Gaming Suite":200000},
    "Bathroom": {"Standard":0, "Full Shower":800000, "Gold Bidet":150000, "Sauna":1200000},
    "Air Quality": {"HEPA":0, "Plasma Ionization":150000, "Humidification System":300000},
    "Maintenance": {"Pay-as-you-go":0, "Prepaid 5yr Program":5000000},
    "Veneer": {"Walnut":0, "Carbon Fiber":150000, "Piano Black":100000, "Rare Stone":500000}
}
# 🏰 豪宅选配
OPTS_ESTATE = {
    "Style": {"Modern":0, "Classic French":500000, "Zen Minimalist":800000, "Cyberpunk":1200000},
    "Security": {"Standard":0, "Biometric Access":150000, "Armed Guards (Yearly)":800000, "Safe Room":500000},
    "Staff": {"None":0, "Butler & Chef":300000, "Full Team (Maids/Driver)":800000},
    "Furniture": {"Unfurnished":0, "Fendi Casa":2000000, "Visionnaire":3000000, "Antique":5000000},
    "Art": {"None":0, "Curated Prints":50000, "Original Contemporary":5000000, "Blue Chip Masters":20000000},
    "Wellness": {"Gym":50000, "Spa & Sauna":300000, "Indoor Pool":1000000, "Hyperbaric Chamber":150000},
    "Garage": {"Standard":0, "Showroom Gallery":500000, "Automated Stacker":1000000},
    "Wine": {"Empty":0, "Stocked Vintage":500000, "Rare Collection":2000000},
    "Cinema": {"Home Theater":150000, "IMAX Private":2000000},
    "Smart Home": {"Standard":0, "Full AI Integration":300000}
}
# ⚓️ 超级游艇选配
OPTS_MEGA_YACHT = {
    "Hull": {"White":0, "Navy":500000}, "Helipad": {"Touch&Go":0, "Hangar":2000000}, "Sub": {"None":0, "Triton":4000000}, 
    "Defense": {"None":0, "Anti-Drone":1500000}, "Pool": {"Deck":0, "Infinity":2000000}, "Cinema": {"Std":0, "IMAX":3000000}, 
    "Spa": {"Std":0, "Full":1000000}, "Tenders": {"RIB":0, "Limo":1500000}, "Staff": {"Std":0, "Michelin":1500000}, 
    "Propulsion": {"Diesel":0, "Hybrid":12000000}
}
# ⌚ 表 / 👜 奢品
OPTS_WATCH = {"Material": {"Steel":0, "Gold":35000}, "Dial": {"Std":0, "Meteorite":15000}, "Gem": {"None":0, "Diamond":25000}, "Strap": {"Rubber":0, "Gold":15000}, "Movement": {"Std":0, "Tourbillon":100000}, "Box": {"Std":0, "Winder":5000}, "Engraving": {"None":0, "Custom":2000}, "Warranty": {"2yr":0, "Lifetime":50000}}
OPTS_LUXURY = {"Leather": {"Togo":0, "Croc":45000}, "Hardware": {"Gold":0, "Diamond":85000}, "Size": {"25":0, "30":2000}, "Color": {"Black":0, "Himalaya":150000}, "Stamp": {"Std":0, "Horseshoe":20000}, "Condition": {"New":0, "Vintage":5000}}

# ==========================================
# 2. 数据工厂 (HD图源精选版)
# ==========================================
# 注意：这里替换了一部分关键图片为更高质量的源，作为示范。
# 真正的极致体验需要您后续自己建立本地图库。

def get_img(key, cat):
    key = key.lower()
    if cat == "Estate":
        # 替换为更高清、更具代表性的图片
        if "101" in key: return "https://images.pexels.com/photos/290275/pexels-photo-290275.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2" # 纽约天际线
        if "the one" in key: return "https://i.pinimg.com/originals/15/29/3d/15293d7625a2537230324c577504d82d.jpg" # The One 实拍
        if "tan gong" in key or "villa" in key: return "https://images.pexels.com/photos/2287310/pexels-photo-2287310.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2" # 现代别墅
        if "hong kong" in key or "peak" in key: return "https://images.pexels.com/photos/1440476/pexels-photo-1440476.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2" # 香港夜景
        if "shenzhen" in key or "huiyuetai" in key: return "https://images.pexels.com/photos/323780/pexels-photo-323780.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2" # 摩天大楼顶层
        if "courtyard" in key or "siheyuan" in key: return "https://upload.wikimedia.org/wikipedia/commons/thumb/1/14/Siheyuan_Beijing.jpg/1280px-Siheyuan_Beijing.jpg" # 更大尺寸的四合院
        return "https://images.pexels.com/photos/258154/pexels-photo-258154.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2" # 默认奢华度假屋
    if cat == "Fleet":
        if "yacht" in key:
             if "azzam" in key: return "https://www.lurssen.com/wp-content/uploads/sites/2/2023/04/Azzam-Aerial-Running-Shot.jpg" # 乐顺官网图
             return "https://images.pexels.com/photos/163236/luxury-yacht-boat-speed-water-163236.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2"
        if "g700" in key: return "https://www.gulfstream.com/images/content/aircraft/g700/gallery/exterior/g700-exterior-04.jpg" # 湾流官网图
        if "global 7500" in key: return "https://businessaircraft.bombardier.com/sites/default/files/2022-05/Global7500_Gallery_Exterior_4.jpg" # 庞巴迪官网图
        if "bbj" in key: return "https://www.boeing.com/content/dam/boeing/images/commercial/bbj/777x/BBJ-777X-Exterior-Rendering-1.jpg" # 波音官网图
        return "https://images.pexels.com/photos/220444/pexels-photo-220444.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2" # 默认飞机
    # 默认豪车图
    return "https://images.pexels.com/photos/12311379/pexels-photo-12311379.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2" # 更现代的超跑图

def generate_db():
    db = {"Car":[], "Estate":[], "Watch":[], "Fleet":[], "Luxury":[]}
    
    # 1. 地产
    estates = [
        ("New York", "Central Park Tower 101st PH", 250000000), 
        ("Beverly Hills", "The One Hilltop Mansion", 145000000),
        ("Shanghai", "Tan Gong Villa No.2 (檀宫)", 100000000),
        ("Hong Kong", "35 Barker Road Villa (白加道)", 280000000),
        ("Hong Kong", "75 Peak Road Villa (山顶道)", 250000000),
        ("Shenzhen", "Shenzhen Bay No.1 Top Duplex", 85000000),
        ("Guangzhou", "Ersha Island Villa (宏城花园)", 55000000),
        ("Guangzhou", "Qiaoxin Huiyuetai Top PH", 45000000),
        ("Beijing", "Houhai Courtyard (后海四合院)", 180000000),
        ("Beijing", "Xiagongfu Top Apt (霞公府)", 35000000),
        ("Monaco", "Tour Odéon Sky Penthouse", 380000000),
        ("London", "One Hyde Park Penthouse B", 120000000)
    ]
    for i, (loc, name, price) in enumerate(estates):
        db["Estate"].append({"id":f"e_{i}", "brand":loc, "name":name, "price":price, "type":"Ultra Prime", "img":get_img(name, "Estate"), "opts":OPTS_ESTATE})

    # 2. 飞机
    jets = [
        ("Gulfstream", "G280", 25000000), ("Gulfstream", "G400", 35000000), ("Gulfstream", "G500", 45000000),
        ("Gulfstream", "G600", 58000000), ("Gulfstream", "G650ER", 70000000), ("Gulfstream", "G700", 78000000), ("Gulfstream", "G800", 82000000),
        ("Bombardier", "Challenger 3500", 27000000), ("Bombardier", "Challenger 650", 32000000),
        ("Bombardier", "Global 5500", 46000000), ("Bombardier", "Global 6500", 56000000),
        ("Bombardier", "Global 7500", 75000000), ("Bombardier", "Global 8000", 78000000),
        ("Dassault", "Falcon 2000LXS", 35000000), ("Dassault", "Falcon 900LX", 44000000),
        ("Dassault", "Falcon 6X", 47000000), ("Dassault", "Falcon 8X", 58000000), ("Dassault", "Falcon 10X", 75000000),
        ("Boeing", "BBJ MAX 7", 100000000), ("Boeing", "BBJ MAX 8", 110000000), ("Boeing", "BBJ MAX 9", 120000000),
        ("Boeing", "BBJ 787 Dreamliner", 250000000), ("Boeing", "BBJ 777-9", 400000000)
    ]
    for i, (brand, name, price) in enumerate(jets):
        db["Fleet"].append({"id":f"j_{i}", "brand":brand, "name":name, "price":price, "type":"Private Jet", "img":get_img(name, "Fleet"), "opts":OPTS_JET})

    # 3. 游艇
    yachts = [
        ("Lürssen", "Azzam", 600000000), ("Blohm+Voss", "Eclipse", 1200000000), ("Lürssen", "Dilbar", 800000000),
        ("Oceanco", "Jubilee", 300000000), ("Feadship", "Symphony", 150000000), ("Benetti", "Luminosity", 270000000),
        ("Heesen", "Galactica Super Nova", 100000000), ("Lürssen", "Flying Fox", 400000000),
        ("Oceanco", "Black Pearl", 220000000), ("Feadship", "Anna", 250000000)
    ]
    for i, (brand, name, price) in enumerate(yachts):
        db["Fleet"].append({"id":f"y_{i}", "brand":brand, "name":name, "price":price, "type":"Mega Yacht", "img":get_img(name, "Fleet"), "opts":OPTS_MEGA_YACHT})

    # 4. 车辆 (使用默认高质量图，后续需手动替换为特定车型图)
    cars = [
        ("Mercedes-AMG", "SL 63", 185000), ("Mercedes-AMG", "G 63", 190000), ("Mercedes-AMG", "GT 63 S", 195000), ("Mercedes-AMG", "S 63", 200000),
        ("Maybach", "S 680", 250000), ("Maybach", "Pullman Guard", 1600000), ("Brabus", "G800", 450000), ("Mercedes-AMG", "AMG GT BS", 350000),
        ("BMW", "M4 Comp", 95000), ("BMW", "M8 Comp", 140000), ("BMW", "i8 Roadster", 165000), ("BMW", "740i", 100000),
        ("Audi", "RS 6", 130000), ("Audi", "RS 7", 135000), ("Audi", "RS e-tron GT", 145000), ("Audi", "A8 Horch", 180000),
        ("Cadillac", "Escalade-V", 155000), ("Lincoln", "Navigator", 120000), ("Land Rover", "Range Rover SV", 240000),
        ("Porsche", "911 Turbo S", 240000), ("Porsche", "911 GT3 RS", 280000), ("Porsche", "Taycan Turbo GT", 230000), ("Porsche", "911 Targa 4S", 160000),
        ("Maserati", "MC20", 220000), ("McLaren", "720S", 320000), ("McLaren", "765LT", 390000), ("McLaren", "Speedtail", 2500000),
        ("Aston Martin", "DB11", 220000), ("Aston Martin", "DB12", 250000), ("Aston Martin", "DBS", 340000), ("Aston Martin", "DBX 707", 245000), ("Aston Martin", "Valkyrie", 3500000),
        ("Ferrari", "SF90", 550000), ("Ferrari", "F80", 4000000), ("Ferrari", "296 GTB", 330000), ("Ferrari", "Purosangue", 400000), ("Ferrari", "FXX-K", 3000000),
        ("Ferrari", "488 Pista", 450000), ("Ferrari", "458 Speciale", 350000), ("Ferrari", "812 Comp", 650000),
        ("Lamborghini", "Revuelto", 620000), ("Lamborghini", "Huracán STO", 340000), ("Lamborghini", "Urus", 270000), ("Lamborghini", "Countach", 2700000),
        ("Rolls-Royce", "Spectre", 450000), ("Rolls-Royce", "Cullinan", 400000), ("Rolls-Royce", "Phantom", 600000), ("Rolls-Royce", "Wraith", 380000), ("Rolls-Royce", "Ghost", 360000), ("Rolls-Royce", "Boat Tail", 28000000),
        ("Bentley", "Conti GT", 300000), ("Bentley", "Mulsanne", 350000), ("Bentley", "Bentayga", 280000),
        ("Pininfarina", "Battista", 2200000), ("Koenigsegg", "Jesko", 3400000), ("Koenigsegg", "Gemera", 1900000),
        ("Pagani", "Zonda R", 6500000), ("Pagani", "Huayra BC", 2800000), ("Pagani", "Utopia", 2500000),
        ("Bugatti", "Chiron", 3300000), ("Bugatti", "Divo", 5800000), ("Bugatti", "Tourbillon", 4500000), ("Bugatti", "La Voiture Noire", 18000000)
    ]
    for i, (brand, name, price) in enumerate(cars):
        db["Car"].append({"id":f"c_{i}", "brand":brand, "name":name, "price":price, "type":"Car", "img":get_img(name, "Car"), "opts":OPTS_CAR})

    # 5. 补全其他
    for i in range(20):
        db["Watch"].append({"id":f"w_{i}","brand":"Patek/Rolex","name":f"Grand Complication #{i}","price":random.randint(5,50)*10000,"img":"https://images.pexels.com/photos/280250/pexels-photo-280250.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2","opts":OPTS_WATCH})
        db["Luxury"].append({"id":f"l_{i}","brand":"Hermes","name":f"Birkin #{i}","price":random.randint(1,20)*10000,"img":"https://images.pexels.com/photos/1303082/pexels-photo-1303082.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2","opts":OPTS_LUXURY})

    return db

DB = generate_db()

# ==========================================
# 3. 逻辑层
# ==========================================
def load_data():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, 'r') as f:
                data = json.load(f)
                return data.get('cash', 10000000000.0), data.get('inventory', []), data.get('year', 2025)
        except: pass
    return 10000000000.0, [], 2025

def save_data():
    with open(SAVE_FILE, 'w') as f:
        json.dump({"cash": st.session_state.cash, "inventory": st.session_state.inventory, "year": st.session_state.game_year}, f)

if 'init_done' not in st.session_state:
    c, i, y = load_data()
    st.session_state.cash = c; st.session_state.inventory = i; st.session_state.game_year = y; st.session_state.init_done = True

def buy_item(item, final_price, specs):
    if st.session_state.cash >= final_price:
        st.session_state.cash -= final_price
        st.session_state.inventory.append({
            "name": item['name'], "brand": item['brand'], "specs": specs,
            "buy_price": final_price, "val": final_price, "year": st.session_state.game_year, "img": item['img']
        })
        save_data(); st.toast("✅ Purchased!", icon="💰"); st.rerun()
    else: st.error("Insufficient Funds")

def sell_item(idx):
    item = st.session_state.inventory[idx]
    st.session_state.cash += item['val']
    st.session_state.inventory.pop(idx); save_data(); st.toast("Sold!", icon="💸"); st.rerun()

# ==========================================
# 4. 界面渲染
# ==========================================
with st.sidebar:
    st.title("🌍 WORLD OWNER HD")
    val = sum([x['val'] for x in st.session_state.inventory])
    st.metric("Net Worth", f"${st.session_state.cash+val:,.0f}")
    st.metric("Liquid Cash", f"${st.session_state.cash:,.0f}")
    if st.button("📅 Advance Year (Market)"):
        st.session_state.game_year += 1
        for x in st.session_state.inventory: x['val'] *= random.uniform(0.9, 1.15)
        save_data(); st.rerun()

def render_configurator(item):
    with st.expander(f"🛠️ Configure: {item['name']}", expanded=False):
        c_price = item['price']
        specs = []
        for cat, opts in item['opts'].items():
            sel = st.selectbox(f"{cat}", list(opts.keys()), key=f"{item['id']}_{cat}")
            price = opts[sel]
            c_price += price
            if price > 0: specs.append(f"{cat}: {sel}")
        st.write(f"Total: :red[${c_price:,.0f}]")
        if st.button("Buy Now", key=f"btn_{item['id']}"):
            buy_item(item, c_price, " | ".join(specs) if specs else "Standard")

tabs = st.tabs(["🏰 Estate (Global)", "✈️ Fleet (Jets/Yachts)", "🏎️ Cars", "⌚ Watches", "👜 Luxury", "💼 My Assets"])

with tabs[0]:
    st.subheader("Ultra Prime Real Estate")
    for item in DB["Estate"]:
        with st.container():
            st.markdown(f"<div class='asset-card'>", unsafe_allow_html=True)
            c1, c2 = st.columns([2, 3]) # 调整图片比例以适应宽幅
            c1.image(item['img'], use_container_width=True)
            with c2:
                st.markdown(f"<span class='gold'>{item['brand']}</span>", unsafe_allow_html=True)
                st.markdown(f"### {item['name']}")
                st.markdown(f"Price: <span class='price-tag'>${item['price']:,}</span>", unsafe_allow_html=True)
                render_configurator(item)
            st.markdown("</div>", unsafe_allow_html=True)

with tabs[1]:
    st.subheader("Private Aviation & Mega Yachts")
    filter_type = st.radio("Filter", ["All", "Private Jet", "Mega Yacht"], horizontal=True)
    items = DB["Fleet"]
    if filter_type != "All": items = [x for x in items if x['type'] == filter_type]
    
    for item in items:
        with st.container():
            st.markdown(f"<div class='asset-card'>", unsafe_allow_html=True)
            c1, c2 = st.columns([2, 3])
            c1.image(item['img'], use_container_width=True)
            with c2:
                st.markdown(f"<span class='gold'>{item['brand']}</span>", unsafe_allow_html=True)
                st.markdown(f"### {item['name']}")
                st.caption(item['type'])
                st.markdown(f"Price: <span class='price-tag'>${item['price']:,}</span>", unsafe_allow_html=True)
                render_configurator(item)
            st.markdown("</div>", unsafe_allow_html=True)

with tabs[2]:
    filter_brand = st.selectbox("Filter Brand", ["All"] + sorted(list(set([x['brand'] for x in DB["Car"]]))))
    search = st.text_input("Search Car...", "")
    items = DB["Car"]
    if filter_brand != "All": items = [x for x in items if x['brand'] == filter_brand]
    if search: items = [x for x in items if search.lower() in x['name'].lower()]
    
    for item in items:
        with st.container():
            st.markdown(f"<div class='asset-card'>", unsafe_allow_html=True)
            c1, c2 = st.columns([2, 3])
            c1.image(item['img'], use_container_width=True)
            with c2:
                st.markdown(f"<span class='gold'>{item['brand']}</span>", unsafe_allow_html=True)
                st.markdown(f"### {item['name']}")
                st.markdown(f"Price: ${item['price']:,}")
                render_configurator(item)
            st.markdown("</div>", unsafe_allow_html=True)

for idx, cat in enumerate(["Watch", "Luxury"], 3):
    with tabs[idx]:
        for item in DB[cat][:20]:
             with st.container():
                st.markdown(f"<div class='asset-card'>", unsafe_allow_html=True)
                c1, c2 = st.columns([2, 3])
                c1.image(item['img'], use_container_width=True)
                with c2:
                    st.markdown(f"### {item['name']}")
                    st.markdown(f"Price: ${item['price']:,}")
                    render_configurator(item)
                st.markdown("</div>", unsafe_allow_html=True)

with tabs[5]:
    if not st.session_state.inventory: st.info("Inventory Empty")
    for i, x in enumerate(st.session_state.inventory):
        with st.container():
            c1, c2, c3 = st.columns([2, 3, 1])
            c1.image(x['img'], use_container_width=True)
            with c2:
                st.write(f"**{x['brand']} {x['name']}**")
                st.caption(x['specs'])
            with c3:
                st.write(f"Val: ${x['val']:,.0f}")
                if st.button("Sell", key=f"sell_{i}"): sell_item(i)
