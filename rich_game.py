import streamlit as st
import pandas as pd
import random
import time

# ==========================================
# 0. 极简奢华UI配置 (黑金风格)
# ==========================================
st.set_page_config(page_title="Centurion Bank OS", layout="wide", page_icon="💳")

st.markdown("""
<style>
    .stApp {background-color: #000000; color: #e0e0e0; font-family: 'Helvetica Neue', sans-serif;}
    [data-testid="stSidebar"] {background-color: #0a0a0a; border-right: 1px solid #222;}
    h1, h2, h3, h4, h5 {color: #D4AF37 !important; letter-spacing: 1px;} 
    
    /* 银行卡片 */
    .bank-card {
        background: linear-gradient(135deg, #1a1a1a 0%, #2c2c2c 100%);
        border: 2px solid #D4AF37;
        border-radius: 20px;
        padding: 40px;
        text-align: center;
        box-shadow: 0 10px 40px rgba(212, 175, 55, 0.15);
        margin-bottom: 40px;
    }
    .balance-title {color: #888; text-transform: uppercase; letter-spacing: 2px; font-size: 0.9rem;}
    .balance-amount {
        font-family: 'Courier New', monospace; font-size: 4.5rem; font-weight: bold; 
        color: #D4AF37; text-shadow: 0 0 15px rgba(212, 175, 55, 0.4); margin: 20px 0;
    }
    .income-tag {color: #4CAF50; background: rgba(76, 175, 80, 0.1); padding: 5px 15px; border-radius: 20px; font-size: 0.9rem;}
    
    /* 资产条目 */
    .text-asset-card {
        background-color: #111; border-left: 3px solid #333; padding: 20px; 
        margin-bottom: 12px; border-radius: 6px; transition: all 0.2s;
    }
    .text-asset-card:hover {background-color: #1a1a1a; border-left-color: #D4AF37;}
    
    .asset-header {display: flex; justify-content: space-between; align-items: center;}
    .asset-brand {color: #666; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px;}
    .asset-name {font-size: 1.2rem; font-weight: 600; color: #fff; margin: 5px 0;}
    .asset-price {font-family: monospace; color: #D4AF37; font-size: 1.1rem;}
    
    /* 配置单样式 */
    .config-box {
        background-color: #0e0e0e; border: 1px solid #333; padding: 15px; margin-top: 15px; border-radius: 8px;
    }
    .config-title {font-size: 0.9rem; color: #888; margin-bottom: 10px; text-transform: uppercase;}
    
    /* 按钮 */
    div.stButton > button {
        background: transparent; border: 1px solid #D4AF37; color: #D4AF37; 
        border-radius: 4px; padding: 8px 20px; width: 100%; transition: all 0.2s;
    }
    div.stButton > button:hover {
        background: #D4AF37; color: #000;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 1. 银行系统逻辑
# ==========================================
INITIAL_CAPITAL = 10000000000
PASSIVE_INCOME_BASE = 800000 

if 'cash' not in st.session_state:
    st.session_state.cash = INITIAL_CAPITAL
    st.session_state.inventory = []
    st.session_state.last_income = 0

# 自动复利增长
income_this_tick = random.randint(PASSIVE_INCOME_BASE, PASSIVE_INCOME_BASE * 5)
st.session_state.cash += income_this_tick
st.session_state.last_income = income_this_tick
st.toast(f"📈 Interest Paid: +${income_this_tick:,}")

def buy_asset(brand, name, base_price, selected_options, total_cost):
    if st.session_state.cash >= total_cost:
        st.session_state.cash -= total_cost
        st.session_state.inventory.append({
            "brand": brand, 
            "name": name, 
            "price": total_cost,
            "specs": selected_options
        })
        st.success(f"✅ ORDER CONFIRMED: {name}")
        time.sleep(1)
        st.rerun()
    else:
        st.error("❌ INSUFFICIENT FUNDS")

def sell_asset(i):
    item = st.session_state.inventory.pop(i)
    st.session_state.cash += item['price']
    st.toast(f"💰 Liquidated: {item['name']}")
    st.rerun()

# ==========================================
# 2. 超级配置单 (每一类 > 10 项)
# ==========================================
# 格式: ("选项名称", 额外价格)
CONFIG_MENUS = {
    "Car": [
        ("Matte Black Paint / 哑光黑车漆", 15000),
        ("23-inch Forged Wheels / 23寸锻造轮毂", 22000),
        ("Carbon Ceramic Brakes / 碳陶刹车", 18000),
        ("Hermès Leather Interior / 爱马仕真皮内饰", 55000),
        ("Starlight Headliner / 星空顶", 28000),
        ("Bespoke Audio System / 顶级音响", 12000),
        ("Rear Seat Entertainment / 后排娱乐系统", 15000),
        ("Champagne Cooler / 香槟冰箱", 8000),
        ("Gold Plated Spirit of Ecstasy / 镀金车标", 5000),
        ("Bulletproof Glass (B6) / 防弹玻璃", 85000),
        ("Exposed Carbon Fiber Body / 全碳纤维车身", 150000),
        ("Titanium Exhaust / 钛合金排气", 25000),
        ("Personalized Treadplates / 个性化迎宾踏板", 3000)
    ],
    "Jet": [
        ("Master Bedroom Suite / 主卧套房", 2500000),
        ("Full Stand-up Shower / 独立淋浴间", 1500000),
        ("Conference Room (6 Pax) / 6人会议室", 800000),
        ("Ka-Band High Speed WiFi / 极速卫星网", 500000),
        ("Anti-Missile System / 反导防御系统", 4500000),
        ("Exterior Custom Livery / 定制涂装", 300000),
        ("Gold Plated Sink Hardware / 镀金卫浴", 150000),
        ("Medical Bay / 医疗室", 1200000),
        ("Crew Rest Area / 机组休息区", 500000),
        ("Galley with Pizza Oven / 披萨烤箱厨房", 250000),
        ("Cinema Projector / 影院投影", 180000),
        ("Humidification System / 增湿系统", 350000),
        ("Encrypted Comms / 加密通讯", 2000000)
    ],
    "Yacht": [
        ("Helipad (Reinforced) / 加固停机坪", 5000000),
        ("Beach Club Extension / 亲水平台扩展", 2500000),
        ("Glass Bottom Pool / 玻璃底泳池", 3000000),
        ("Mini Submarine (Triton) / 迷你潜水艇", 4500000),
        ("Anti-Drone Shield / 反无人机盾", 1500000),
        ("Underwater Nemo Room / 水下观景厅", 6000000),
        ("Cinema (IMAX Certified) / IMAX影院", 2000000),
        ("Gym & Spa Center / 健身水疗中心", 1200000),
        ("Jet Ski Garage (Full) / 摩托艇库(满配)", 800000),
        ("Stabilizers (Zero Speed) / 零速稳定器", 1500000),
        ("Bulletproof Bridge / 防弹驾驶台", 1000000),
        ("Elevator (Glass) / 玻璃电梯", 1800000),
        ("Live Seafood Tank / 活海鲜缸", 50000)
    ],
    "Estate": [
        ("Panic Room / 恐慌室(避难所)", 2000000),
        ("Underground Vault / 地下金库", 1500000),
        ("Wine Cellar (stocked) / 满配酒窖", 3000000),
        ("Home Theatre (4D) / 4D家庭影院", 800000),
        ("Smart Home AI / 全屋智能AI", 500000),
        ("Heated Driveway / 车道加热", 200000),
        ("Infinity Pool / 无边泳池", 1200000),
        ("Staff Quarters / 佣人房独立栋", 800000),
        ("Professional Kitchen / 米其林级厨房", 600000),
        ("Art Gallery Lighting / 艺术馆级灯光", 300000),
        ("Private Bowling Alley / 私人保龄球道", 400000),
        ("Helipad / 直升机坪", 1000000),
        ("Japanese Garden / 枯山水庭院", 1500000)
    ],
    "Vault": [
        ("Diamond Setting / 钻石镶嵌", 250000),
        ("Platinum Bracelet / 铂金表带", 150000),
        ("Tourbillon Movement / 陀飞轮机芯", 500000),
        ("Custom Engraving / 个性化刻字", 5000),
        ("Crocodile Strap / 鳄鱼皮表带", 8000),
        ("Sapphire Case / 蓝宝石表壳", 1200000),
        ("Meteorite Dial / 陨石盘面", 50000),
        ("Insurance (Lifetime) / 终身保险", 100000),
        ("Museum Display Box / 博物馆级展示盒", 20000),
        ("Certificate of Origin / 原产地证书", 0),
        ("Extra Links / 备用表节", 2000),
        ("Polishing Service / 终身抛光", 15000)
    ]
}

# ==========================================
# 3. 资产数据库
# ==========================================
def create_db():
    db = {
        "Car": [
            ("Rolls-Royce", "Phantom VIII EWB", 650000),
            ("Rolls-Royce", "Cullinan Black Badge", 480000),
            ("Bugatti", "Chiron Super Sport", 3900000),
            ("Bugatti", "Tourbillon", 4500000),
            ("Ferrari", "Daytona SP3", 2200000),
            ("Ferrari", "Purosangue", 400000),
            ("Lamborghini", "Revuelto", 600000),
            ("Mercedes-Maybach", "S 680 Haute Voiture", 300000),
            ("Mercedes-AMG", "G 63 4x4²", 350000),
            ("Aston Martin", "Valkyrie", 3500000),
            ("Koenigsegg", "Jesko Absolut", 3400000),
            ("Pagani", "Utopia", 2500000)
        ],
        "Jet": [
            ("Gulfstream", "G700 Flagship", 78000000),
            ("Gulfstream", "G800 Long Range", 81500000),
            ("Bombardier", "Global 7500", 75000000),
            ("Bombardier", "Global 8000", 78000000),
            ("Boeing", "BBJ 777-9", 450000000),
            ("Boeing", "BBJ 787-9", 280000000),
            ("Airbus", "ACJ TwoTwenty", 90000000),
            ("Dassault", "Falcon 10X", 75000000),
            ("Embraer", "Lineage 1000E", 53000000)
        ],
        "Yacht": [
            ("Lürssen", "Azzam (180m)", 600000000),
            ("Lürssen", "Blue (160m)", 600000000),
            ("Lürssen", "Dilbar (156m)", 800000000),
            ("Blohm+Voss", "Eclipse (162m)", 1200000000),
            ("Feadship", "Project 1010", 300000000),
            ("Oceanco", "Y721 Koru", 500000000),
            ("Benetti", "Luminosity", 280000000),
            ("Nobiskrug", "Sailing Yacht A", 450000000)
        ],
        "Estate": [
            ("New York", "Central Park Tower PH", 250000000),
            ("London", "The Holme Regent's Park", 300000000),
            ("France", "Villa Leopolda", 750000000),
            ("Los Angeles", "The One Bel Air", 140000000),
            ("Monaco", "Tour Odéon Sky PH", 380000000),
            ("Hong Kong", "The Peak Barker Rd", 280000000),
            ("Mumbai", "Antilia", 2000000000),
            ("Shanghai", "Tan Gong Villa", 100000000),
            ("Beijing", "Houhai Courtyard", 180000000)
        ],
        "Vault": [
            ("Patek Philippe", "Grandmaster Chime", 31000000),
            ("Patek Philippe", "Nautilus Tiffany", 6500000),
            ("Rolex", "Paul Newman Daytona", 17800000),
            ("Jacob & Co", "Billionaire Watch", 18000000),
            ("Graff", "Diamonds Hallucination", 55000000),
            ("Art", "Da Vinci - Salvator Mundi", 450300000),
            ("Art", "De Kooning - Interchange", 300000000),
            ("Gem", "The Pink Star", 71200000)
        ]
    }
    return db

DB = create_db()

# ==========================================
# 4. 界面渲染
# ==========================================

# --- 私人银行卡片 ---
st.markdown(f"""
<div class="bank-card">
    <div style="font-size: 3rem; margin-bottom: 15px;">💳 CENTURION PRIVATE BANK</div>
    <div class="balance-title">TOTAL NET WORTH (LIQUID)</div>
    <div class="balance-amount">${st.session_state.cash:,.0f}</div>
    <div style="display: flex; justify-content: center; gap: 20px; align-items: center;">
        <span class="income-tag">🚀 Yield: +${PASSIVE_INCOME_BASE*2.5:,.0f} / Tick</span>
        <span style="color: #4CAF50; font-weight: bold;">▲ Last: +${st.session_state.last_income:,.0f}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# --- 侧边栏 ---
with st.sidebar:
    st.header("⚙️ Account Ops")
    if st.button("🔄 Refresh Market"): st.rerun()
    st.divider()
    if st.button("⚠️ Reset Portfolio"):
        st.session_state.cash = INITIAL_CAPITAL
        st.session_state.inventory = []
        st.rerun()

# --- 采购区 ---
st.subheader("🛍️ ACQUISITION MARKET")
tabs = st.tabs(DB.keys())

for i, (cat, items) in enumerate(DB.items()):
    with tabs[i]:
        for brand, name, base_price in items:
            # 渲染每个资产的卡片
            with st.container():
                st.markdown(f"""
                <div class="text-asset-card">
                    <div class="asset-info">
                        <div class="asset-brand">{brand}</div>
                        <div class="asset-name">{name}</div>
                        <div class="asset-price">Base: ${base_price:,}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # 配置展开区域
                with st.expander(f"🛠️ Configure & Purchase: {name}"):
                    st.markdown("<div class='config-title'>Select Options (Each adds to cost)</div>", unsafe_allow_html=True)
                    
                    # 获取该类别的配置单
                    options_list = CONFIG_MENUS.get(cat, CONFIG_MENUS["Car"])
                    selected_opts = []
                    current_price = base_price
                    
                    # 生成复选框
                    c1, c2 = st.columns(2)
                    for idx, (opt_name, opt_price) in enumerate(options_list):
                        col = c1 if idx % 2 == 0 else c2
                        if col.checkbox(f"{opt_name} (+${opt_price:,})", key=f"{name}_{idx}"):
                            selected_opts.append(opt_name)
                            current_price += opt_price
                    
                    st.divider()
                    st.markdown(f"#### Total Price: :green[${current_price:,}]")
                    if st.button(f"CONFIRM ORDER - ${current_price:,}", key=f"btn_{name}"):
                        buy_asset(brand, name, base_price, selected_options=selected_opts, total_cost=current_price)

st.divider()

# --- 资产清单 ---
st.subheader(f"💼 PORTFOLIO ({len(st.session_state.inventory)} Assets)")

if not st.session_state.inventory:
    st.caption("Your portfolio is currently empty. Acquire assets above.")
else:
    for i, item in enumerate(reversed(st.session_state.inventory)):
        with st.container():
            st.markdown(f"""
            <div class="text-asset-card" style="border-left-color: #4CAF50;">
                <div class="asset-info">
                    <div class="asset-brand">{item['brand']} <span style="color:#4CAF50; margin-left:10px;">● OWNED</span></div>
                    <div class="asset-name">{item['name']}</div>
                    <div class="asset-price">Valuation: ${item['price']:,}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # 显示已选配置
            if item['specs']:
                with st.expander("View Specs"):
                    for s in item['specs']:
                        st.write(f"- {s}")
            
            if st.button("LIQUIDATE ASSET", key=f"sell_{i}"):
                sell_asset(len(st.session_state.inventory)-1-i)
