import streamlit as st
import pandas as pd
import random
import json
import os

# ==========================================
# 0. UI & 基础配置
# ==========================================
st.set_page_config(page_title="World Owner Ultimate", layout="wide", page_icon="👑")

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
    
    /* 图片强制宽幅，修复显示问题 */
    [data-testid="stImage"] {
        border-radius: 8px; 
        overflow: hidden;
        box-shadow: 0 4px 12px rgba(0,0,0,0.5);
    }
    [data-testid="stImage"] > img {
        object-fit: cover; 
        aspect-ratio: 16/9; 
        width: 100%;
        transition: transform 0.3s ease;
    }
    [data-testid="stImage"] > img:hover {
        transform: scale(1.02);
    }
</style>
""", unsafe_allow_html=True)

SAVE_FILE = "game_save.json"

# ==========================================
# 1. 深度选配矩阵
# ==========================================
OPTS_CAR = {
    "Paint": {"Standard":0, "Metallic":5000, "Matte":15000, "Bespoke":45000},
    "Wheels": {"Standard":0, "Forged":12000, "Black":8000, "Gold":25000},
    "Interior": {"Leather":0, "Alcantara":5000, "Hermes":55000, "Carbon":25000},
    "Tech": {"Standard":0, "Track Telemetry":8000, "Night Vision":5000}
}
OPTS_JET = {
    "Layout": {"Executive":0, "Bedroom":2000000, "Majlis":1500000, "Medical":3000000},
    "Livery": {"White":0, "Matte Black":250000, "Custom Art":500000},
    "Defense": {"None":0, "Anti-Missile Jammer":4500000},
    "Connect": {"Ka-Band":500000, "Encrypted":2000000}
}
OPTS_YACHT = {
    "Helipad": {"Touch&Go":0, "Hangar":2000000}, 
    "Sub": {"None":0, "Triton Sub":4000000}, 
    "Defense": {"None":0, "Anti-Drone":1500000}, 
    "Pool": {"Deck":0, "Infinity":2000000, "Glass Bottom":5000000}
}
OPTS_ESTATE = {"Style": {"Modern":0, "Classic":500000}, "Security": {"Std":0, "Armed":800000}, "Staff": {"None":0, "Full Team":800000}}
OPTS_WATCH = {"Material": {"Steel":0, "Gold":35000}, "Dial": {"Std":0, "Meteorite":15000}, "Gem": {"None":0, "Diamond":25000}}
OPTS_LUXURY = {"Leather": {"Togo":0, "Croc":45000}, "Hardware": {"Gold":0, "Diamond":85000}, "Condition": {"New":0, "Vintage":5000}}

# ==========================================
# 2. 智能图库 (安全无断裂版)
# ==========================================
# 这里就是之前报错的地方，我已经做了特别检查，确保引号闭合。
IMG_DB = {
    "mercedes_g": "https://images.unsplash.com/photo-1520031441872-265149a9e6e5",
    "mercedes_sl": "https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8",
    "mercedes_sedan": "https://images.unsplash.com/photo-1617788138017-80ad40651399",
    "rolls_suv": "https://images.unsplash.com/photo-1655132333039-47963d76756d",
    "rolls_sedan": "https://images.unsplash.com/photo-1631295868223-63265b40d9e4",
    "ferrari": "https://images.unsplash.com/photo-1592198084033-aade902d1aae",
    "lambo_suv": "https://images.unsplash.com/photo-1621996659490-6213b1859303",
    "lambo_car": "https://
