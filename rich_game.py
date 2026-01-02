import streamlit as st
import pandas as pd
import random
import time

# ==========================================
# 0. 极简奢华UI配置 (黑金风格，无图)
# ==========================================
st.set_page_config(page_title="Centurion Bank OS", layout="wide", page_icon="💳")

st.markdown("""
<style>
    /* 全局深色背景 */
    .stApp {
        background-color: #000000;
        color: #e0e0e0;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    
    /* 侧边栏 */
    [data-testid="stSidebar"] {
        background-color: #0a0a0a;
        border-right: 1px solid #222;
    }
    
    /* 标题和文本 */
    h1, h2, h3 { color: #D4AF37 !important; letter-spacing: 1px; } /* 金色标题 */
    .big-icon { font-size: 3rem; margin-bottom: 10px; }
    
    /* --- 私人银行卡片风格 --- */
    .bank-card {
        background: linear-gradient(135deg, #1a1a1a 0%, #2c2c2c 100%);
        border: 2px solid #D4AF37;
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(212, 175, 55, 0.2);
        margin-bottom: 30px;
    }
    .balance-title {
        color: #888;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-size: 0.9rem;
    }
    .balance-amount {
        font-family: 'Courier New', monospace;
        font-size: 4rem;
        font-weight: bold;
        color: #D4AF37;
        text-shadow: 0 0 10px rgba(212, 175, 55, 0.5);
        margin: 15px 0;
    }
    .income-tag {
        background-color: rgba(76, 175, 80, 0.1);
        color: #4CAF50;
        padding: 5px 15px;
        border-radius: 15px;
        font-size: 0.8rem;
    }
    
    /* --- 资产列表卡片风格 (纯文本) --- */
    .text-asset-card {
        background-color: #111;
        border-left: 4px solid #D4AF37;
        padding: 20px;
        margin-bottom: 15px;
        border-radius: 8px;
        transition: transform 0.2s;
    }
    .text-asset-card:hover {
        transform: translateX(5px);
        background-color: #161616;
    }
    .asset-name { font-size: 1.2rem; font-weight: bold; color: #fff; }
    .asset-price { font-family: monospace; color: #D4AF37; font-size: 1.1rem; }
    .asset-brand { color: #666; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px;}
    
    /* 按钮美化 */
    div.stButton > button {
        background-color: transparent;
        border: 1px solid #D4AF37;
        color: #D4AF37;
        border-radius: 5px;
        padding: 5px 15px;
    }
    div.stButton > button:hover {
        background-color: #D4AF37;
        color: black;
        border-color: #D4AF37;
    }

</style>
""", unsafe_allow_html=True)

# ==========================================
# 1. 核心逻辑：银行系统与被动收入
# ==========================================
# 初始资金：100亿
INITIAL_CAPITAL = 10000000000
# 被动收入速率：每次操作赚取 $500,000 到 $2,000,000 不等
PASSIVE_INCOME_BASE = 500000 

if 'cash' not in st.session_state:
    st.session_state.cash = INITIAL_CAPITAL
    st.session_state.inventory = []
    st.session_state.last_income = 0

# --- 被动收入引擎 ---
# 每次页面重新加载（任何点击操作）都会触发
income_this_tick = random.randint(PASSIVE_INCOME_BASE, PASSIVE_INCOME_BASE * 4)
st.session_state.cash += income_this_tick
st.session_state.last_income = income_this_tick
# 弹出提示
st.toast(f"📈 Global Business Income: +${income_this_tick:,}")


def buy(item):
    if st.session_state.cash >= item['price']:
        st.session_state.cash -= item['price']
        st.session_state.inventory.append(item)
        st.toast(f"✅ Acquired: {item['name']}")
        st.rerun() # 强制刷新以更新余额显示

def sell(i):
    item = st.session_state.inventory.pop(i)
    st.session_state.cash += item['price'] # 原价卖出
    st.toast(f"💰 Sold: {item['name']}")
    st.rerun()

# ==========================================
# 2. 纯文本数据库 (无图版)
# ==========================================
def create_db():
    # 格式: (品牌, 型号, 价格)
    db = {
        "🚗 Supercars": [
            ("Rolls-Royce", "Phantom EWB", 650000), ("Rolls-Royce", "Cullinan Black Badge", 450000),
            ("Rolls-Royce", "Spectre", 420000), ("Bugatti", "Chiron Super Sport", 3800000),
            ("Bugatti", "Tourbillon", 4500000), ("Ferrari", "Daytona SP3", 2200000),
            ("Ferrari", "Purosangue", 400000), ("Lamborghini", "Revuelto", 600000),
            ("Lamborghini", "Countach LPI 800-4", 2600000), ("Mercedes-Maybach", "S 680 Haute Voiture", 300000),
            ("Mercedes-AMG", "G 63 4x4²", 350000)
        ],
        "✈️ Private Jets": [
            ("Gulfstream", "G700 Flagship", 78000000), ("Gulfstream", "G800 Long Range", 81500000),
            ("Bombardier", "Global 7500", 75000000), ("Bombardier", "Global 8000 (Mach 0.94)", 78000000),
            ("Boeing", "BBJ 777-9 (Flying Palace)", 450000000), ("Boeing", "BBJ 787 Dreamliner", 250000000),
            ("Dassault", "Falcon 10X", 75000000)
        ],
        "⚓ Mega Yachts": [
            ("Lürssen", "Project Blue (160m)", 600000000), ("Lürssen", "Dilbar (156m)", 800000000),
            ("Feadship", "Project 1010 (118m)", 300000000), ("Oceanco", "Y721 (Jeff Bezos)", 500000000),
            ("Benetti", "Luminosity Hybrid", 280000000)
        ],
        "🏰 Global Estates": [
            ("New York", "Central Park Tower Penthouse", 250000000), ("London", "The Holme, Regent's Park", 300000000),
            ("Cote d'Azur", "Villa Leopolda", 750000000), ("Los Angeles", "The One Bel Air", 140000000),
            ("Monaco", "Tour Odéon Sky Penthouse", 380000000), ("Hong Kong", "The Peak Estate", 280000000)
        ],
        "💎 Vault (Watches & Art)": [
            ("Patek Philippe", "Grandmaster Chime 6300A", 31000000), ("Patek Philippe", "Nautilus Tiffany 5711", 6500000),
            ("Rolex", "Paul Newman Daytona", 17800000), ("Jacob & Co", "Billionaire Watch", 18000000),
            ("Art", "Da Vinci - Salvator Mundi", 450300000), ("Diamond", "The Pink Star (59.6ct)", 71200000)
        ]
    }
    return db

DB = create_db()

# ==========================================
# 3. 界面渲染 (仪表盘 + 列表)
# ==========================================

# --- 顶部私人银行仪表盘 ---
st.markdown(f"""
<div class="bank-card">
    <div class="big-icon">💳 CENTURION PRIVATE BANK</div>
    <div class="balance-title">Total Net Worth (Liquid)</div>
    <div class="balance-amount">${st.session_state.cash:,.0f}</div>
    <div>
        <span class="income-tag">🚀 Passive Income Rate: +${PASSIVE_INCOME_BASE*2.5:,.0f} / Tick</span>
        <span style="color: #4CAF50; margin-left: 10px;"> ▲ Last Tick: +${st.session_state.last_income:,.0f}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# --- 侧边栏控制 ---
with st.sidebar:
    st.header("🏦 Account Ops")
    st.write("Your wealth grows automatically with every interaction derived from global business interests.")
    if st.button("🔄 Force Refresh (Trigger Income)"):
        st.rerun()
    st.divider()
    if st.button("⚠️ Reset Account (Wipe Data)"):
        st.session_state.cash = INITIAL_CAPITAL
        st.session_state.inventory = []
        st.rerun()

# --- 资产采购区 (纯文本列表) ---
st.subheader("🛍️ Acquire Assets")
tabs = st.tabs(DB.keys())

for i, (cat_name, items) in enumerate(DB.items()):
    with tabs[i]:
        for brand, name, price in items:
            # 使用纯文本卡片渲染
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"""
                <div class="text-asset-card">
                    <div class="asset-brand">{brand}</div>
                    <div class="asset-name">{name}</div>
                    <div class="asset-price">${price:,}</div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                # 按钮垂直居中
                st.write("") 
                st.write("")
                if st.button("BUY", key=f"buy_{name}"):
                    buy({"brand":brand, "name":name, "price":price})

st.divider()

# --- 我的资产清单 ---
st.subheader("💼 Portfolio Inventory")
if not st.session_state.inventory:
    st.info("Your portfolio is currently empty. Start acquiring.")
else:
    for i, item in enumerate(st.session_state.inventory):
        col1, col2 = st.columns([4, 1])
        with col1:
             st.markdown(f"""
                <div class="text-asset-card" style="border-color: #4CAF50;">
                    <div class="asset-brand">{item['brand']} (Owned)</div>
                    <div class="asset-name">{item['name']}</div>
                    <div class="asset-price">Value: ${item['price']:,}</div>
                </div>
                """, unsafe_allow_html=True)
        with col2:
            st.write("")
            st.write("")
            if st.button("LIQUIDATE", key=f"sell_{i}"): sell(i)
