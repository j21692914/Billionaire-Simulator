import streamlit as st
import pandas as pd
import random
import json
import os

# ==========================================
# 0. UI & 基础配置
# ==========================================
st.set_page_config(page_title="Ultimate Collector", layout="wide", page_icon="👑")

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
    
    /* 强制宽幅高清显示 */
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
# 1. 深度选配矩阵 (10+ Items)
# ==========================================
OPTS_CAR = {
    "Paint": {"Standard":0, "Metallic":5000, "Matte":15000, "PTS/Bespoke":45000, "Exposed Carbon":150000},
    "Wheels": {"Standard":0, "Forged":12000, "Center Lock":18000, "Carbon Fiber":45000, "Gold Plated":30000},
    "Interior": {"Leather":0, "Alcantara":5000, "Hermès Leather":55000, "Full Carbon Buckets":25000},
    "Brakes": {"Steel":0, "Ceramic Composite":12000, "Painted Calipers":2000, "Gold Calipers":5000},
    "Exhaust": {"Standard":0, "Sport Exhaust":5000, "Titanium System":15000, "Inconel":25000},
    "Aero": {"Standard":0, "Carbon Splitters":15000, "Active Wing":35000, "Roof Scoop":20000},
    "Tech": {"Standard":0, "Track Telemetry":8000, "Night Vision":5000, "High-End Audio":12000},
    "Roof": {"Standard":0, "Glass Roof":5000, "Carbon Roof":12000, "Convertible":15000},
    "Livery": {"None":0, "Racing Stripes":8000, "Hand Painted Art":35000, "Gold Leaf":50000},
    "Steering": {"Leather":0, "Alcantara":2000, "Carbon + LEDs":8000},
    "Glazing": {"Standard":0, "Privacy Glass":2000, "Bulletproof (Light)":85000},
    "Delivery": {"Dealer":0, "Factory VIP":5000, "Air Freight":15000}
}

OPTS_JET = {
    "Layout": {"Executive 14 Pax":0, "Master Bedroom + Shower":2000000, "Majlis Style":1500000, "Flying Hospital":3000000},
    "Connectivity": {"Ka-Band WiFi":500000, "Military Encrypted Sat-Link":2500000, "Starlink":100000},
    "Defense": {"None":0, "Anti-Missile Jammer (DIRCM)":4500000, "Chaff/Flare Dispensers":2000000},
    "Livery": {"White":0, "Matte Black":250000, "Custom Art":500000, "Chrome Polish":1000000},
    "Galley": {"Standard":0, "Chef Kitchen + Oven":800000, "Walk-in Cooler":300000},
    "Crew": {"Standard":0, "Top Tier (24/7)":800000, "Medical Team":1200000},
    "Range": {"Standard":0, "Auxiliary Fuel Tanks":1500000, "Aerial Refueling Probe (Mock)":500000},
    "Entertainment": {"HD Screens":0, "4K OLED Theatre":500000, "Gaming Suite":200000},
    "Bathroom": {"Standard":0, "Full Shower":800000, "Gold Bidet":150000},
    "Air Quality": {"HEPA":0, "Plasma Ionization":150000, "Humidification System":300000},
    "Maintenance": {"Pay-as-you-go":0, "Prepaid 5yr Program":5000000},
    "Veneer": {"Walnut":0, "Carbon Fiber":150000, "Piano Black":100000, "Rare Stone":500000}
}

OPTS_YACHT = {
    "Hull Color": {"White":0, "Navy Blue":500000, "Gunmetal Grey":800000, "Pearlescent":1500000},
    "Helipad": {"Touch & Go":0, "Single Hangar":2000000, "Dual Helipads":5000000},
    "Security": {"Standard":0, "Drone Jammer":1500000, "Anti-Piracy Cannons (Sonic)":3000000},
    "Tenders": {"Standard RIBs":0, "Limousine Tender":1500000, "Mini-Submarine (Triton)":4500000},
    "Wellness": {"Gym":0, "Full Spa (Hammam)":1200000, "Snow Room":2500000},
    "Pool": {"Jacuzzi":0, "Infinity Pool":2000000, "Glass Bottom Pool":5000000},
    "Interior": {"Luxury":0, "Bespoke Italian":5000000, "Versailles Gold":8000000},
    "Entertainment": {"Cinema":500000, "IMAX Private Theatre":3000000, "Underwater Lounge":6000000},
    "Beach Club": {"Standard":0, "Fold-out Terraces":2500000, "Dive Centre":1500000},
    "Propulsion": {"Diesel":0, "Hybrid Electric (Silent)":12000000, "Nuclear (Concept)":50000000},
    "Elevator": {"None":0, "Glass Lift":2000000},
    "Staffing": {"Standard":0, "Michelin Chef Team":1500000}
}

OPTS_ESTATE = {"Style": {"Modern":0, "Classic":500000}, "Security": {"Std":0, "Armed":800000}, "Staff": {"None":0, "Full Team":800000}, "Art": {"None":0, "Museum Grade":10000000}, "Garage": {"Std":0, "Showroom":1000000}, "Wine": {"Empty":0, "Rare Vintage":2000000}, "Smart Home": {"Std":0, "Full AI":500000}, "Wellness": {"Gym":0, "Spa":500000}, "Cinema": {"TV":0, "IMAX":1000000}, "Furniture": {"Empty":0, "Fendi Casa":2000000}}
OPTS_WATCH = {"Material": {"Steel":0, "Gold":35000}, "Dial": {"Std":0, "Meteorite":15000}, "Gem": {"None":0, "Diamond":25000}, "Strap": {"Rubber":0, "Gold":15000}, "Movement": {"Std":0, "Tourbillon":100000}, "Box": {"Std":0, "Winder":5000}, "Engraving": {"None":0, "Custom":2000}, "Warranty": {"2yr":0, "Lifetime":50000}, "Glass": {"Sapphire":0, "Dome":2000}, "Hands": {"Std":0, "Blue":1000}}
OPTS_LUXURY = {"Leather": {"Togo":0, "Croc":45000}, "Hardware": {"Gold":0, "Diamond":85000}, "Size": {"25":0, "30":2000}, "Color": {"Black":0, "Himalaya":150000}, "Stamp": {"Std":0, "Horseshoe":20000}, "Condition": {"New":0, "Vintage":5000}, "Strap": {"Std":0, "Canvas":1000}, "Charm": {"None":0, "Rodeo":800}, "Box": {"Std":0, "Hard":5000}, "Receipt": {"Yes":0, "Gift":0}}

# ==========================================
# 2. 智能图库系统 (Smart Image Engine)
# ==========================================
# 针对不同品牌和车型，分配特定的高清图
IMG_DB = {
    # --- Cars ---
    "rolls_dark": "https://images.unsplash.com/photo-1631295868223-63265b40d9e4", # 幻影/古斯特
    "rolls_suv": "https://images.unsplash.com/photo-1655132333039-47963d76756d", # 库里南
    "ferrari_red": "https://images.unsplash.com/photo-1592198084033-aade902d1aae", # 红色法拉利
    "lambo_sharp": "https://images.unsplash.com/photo-1544636331-e26879cd4d9b", # 兰博基尼
    "lambo_suv": "https://images.unsplash.com/photo-1621996659490-6213b1859303", # Urus
    "porsche_911": "https://images.unsplash.com/photo-1503376763036-066120622c74", # 911
    "porsche_taycan": "https://images.unsplash.com/photo-1614207287498-35f191b7d551", # Taycan
    "mercedes_g": "https://images.unsplash.com/photo-1601362840469-51e4d8d58785", # G63
    "mercedes_sl": "https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8", # 敞篷奔驰
    "mercedes_sedan": "https://images.unsplash.com/photo-1617788138017-80ad40651399", # S级/迈巴赫
    "bmw_sport": "https://images.unsplash.com/photo-1555215695-3004980adade", # M4/M8
    "audi_rs": "https://images.unsplash.com/photo-1603584173870-7f23fdae1b7a", # RS6
    "bugatti": "https://images.unsplash.com/photo-1627454820574-fb40e69228d4", # Chiron
    "mclaren": "https://images.unsplash.com/photo-1621135802920-133df287f89c", # McLaren
    "aston": "https://images.unsplash.com/photo-1600712242805-5f78671d2434", # Aston Martin
    "suv_lux": "https://images.unsplash.com/photo-1609521263047-f8f205293f24", # 揽胜/领航员
    
    # --- Jets ---
    "gulfstream": "https://images.unsplash.com/photo-1540962351504-03099e0a754b", # 湾流内饰/外观
    "bbj": "https://images.unsplash.com/photo-1583417319070-4a69db38a482", # 大型客机公务机
    "bombardier": "
