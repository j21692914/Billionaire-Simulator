import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import random
import json

# ==========================================
# 0. 页面配置 (全屏黑金)
# ==========================================
st.set_page_config(page_title="HOLO-COMMANDER", layout="wide", page_icon="🌐")

st.markdown("""
<style>
    .stApp {background-color: #000000; color: #00ffcc; font-family: 'Segoe UI', monospace;}
    
    /* 隐藏默认元素 */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* 侧边栏 */
    [data-testid="stSidebar"] {background-color: #050505; border-right: 1px solid #003333;}
    
    /* 资产卡片 */
    .asset-card {
        background: rgba(0, 20, 20, 0.8);
        border: 1px solid #00ffcc;
        border-radius: 4px;
        padding: 15px;
        margin-bottom: 10px;
        box-shadow: 0 0 10px rgba(0, 255, 204, 0.1);
        transition: all 0.3s;
    }
    .asset-card:hover {
        background: rgba(0, 40, 40, 0.9);
        box-shadow: 0 0 20px rgba(0, 255, 204, 0.3);
        transform: translateX(5px);
    }
    
    /* 字体样式 */
    h1, h2, h3 {color: #00ffcc !important; text-shadow: 0 0 10px #00ffcc; letter-spacing: 2px;}
    .price-tag {color: #ffcc00; font-weight: bold; font-family: 'Courier New';}
    .brand-tag {color: #0088aa; font-size: 0.8em; text-transform: uppercase;}
    
    /* 按钮特效 */
    div.stButton > button {
        background: transparent;
        border: 1px solid #00ffcc;
        color: #00ffcc;
        border-radius: 0px;
        transition: 0.2s;
    }
    div.stButton > button:hover {
        background: #00ffcc;
        color: black;
        box-shadow: 0 0 15px #00ffcc;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 1. 资产数据库 (V17.0 全量回归)
# ==========================================
def create_db():
    return {
        "🏎️ LAND UNITS (Cars)": [
            ("Mercedes-AMG", "G 63 Squared", 350000), ("Rolls-Royce", "Cullinan Black", 480000),
            ("Rolls-Royce", "Phantom VIII", 650000), ("Ferrari", "SF90 Stradale", 550000),
            ("Lamborghini", "Revuelto", 600000), ("Bugatti", "Chiron Super Sport", 3900000),
            ("Aston Martin", "Valkyrie", 3500000), ("Land Rover", "Range Rover SV", 250000)
        ],
        "✈️ AIR UNITS (Jets)": [
            ("Gulfstream", "G700 Flagship", 78000000), ("Gulfstream", "G650ER", 70000000),
            ("Bombardier", "Global 8000", 78000000), ("Boeing", "BBJ 787 Dreamliner", 250000000),
            ("Dassault", "Falcon 10X", 75000000), ("Embraer", "Lineage 1000E", 53000000)
        ],
        "⚓ NAVAL UNITS (Yachts)": [
            ("Lürssen", "Azzam (180m)", 600000000), ("Blohm+Voss", "Eclipse", 500000000),
            ("Oceanco", "Black Pearl", 220000000), ("Feadship", "Project 1010", 300000000)
        ],
        "🏰 BASE UNITS (Estates)": [
            ("New York", "Central Park Tower PH", 250000000), ("London", "The Holme", 300000000),
            ("Shanghai", "Tan Gong Villa", 100000000), ("Hong Kong", "Barker Road", 280000000)
        ]
    }

DB = create_db()

# ==========================================
# 2. 核心逻辑 (银行 & 库存)
# ==========================================
if 'cash' not in st.session_state:
    st.session_state.cash = 10000000000 # 100亿
    st.session_state.inventory = [] # 资产清单
    # 预设几个资产以便展示地图效果
    st.session_state.inventory.append({"brand":"Gulfstream", "name":"G650ER [PRE-OWNED]", "price":65000000, "lat": 34.0, "lng": -118.2})
    st.session_state.inventory.append({"brand":"Lürssen", "name":"Azzam [DEPLOYED]", "price":600000000, "lat": 25.0, "lng": 55.0})

def buy(brand, name, price):
    if st.session_state.cash >= price:
        st.session_state.cash -= price
        # 随机生成一个坐标用于地图展示
        lat = random.uniform(-60, 70)
        lng = random.uniform(-180, 180)
        st.session_state.inventory.append({"brand": brand, "name": name, "price": price, "lat": lat, "lng": lng})
        st.toast(f"✅ UNIT DEPLOYED: {name}")
        st.rerun()

def sell(i):
    item = st.session_state.inventory.pop(i)
    st.session_state.cash += item['price']
    st.toast(f"💰 UNIT LIQUIDATED: {item['name']}")
    st.rerun()

# ==========================================
# 3. 全息地球引擎 (HTML/JS 嵌入)
# ==========================================
# 将Python数据转换为JSON传递给JS
assets_json = json.dumps(st.session_state.inventory)

html_code = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <style>
        body {{ margin: 0; background: #000; overflow: hidden; }}
        
        /* 扫描线滤镜 */
        .scanline {{
            position: fixed; left: 0; top: 0; width: 100%; height: 100%;
            background: linear-gradient(to bottom, rgba(255,255,255,0), rgba(255,255,255,0) 50%, rgba(0,0,0,0.2) 50%, rgba(0,0,0,0.2));
            background-size: 100% 4px;
            pointer-events: none; z-index: 10;
        }}
        
        /* HUD 标题 */
        #hud {{
            position: absolute; top: 20px; left: 20px; z-index: 20;
            font-family: 'Courier New', monospace; color: #00ffcc;
            pointer-events: none;
        }}
        
        /* 交互卡片 */
        .label-card {{
            background: rgba(0, 20, 30, 0.9);
            border: 1px solid #00ffcc;
            color: #00ffcc;
            padding: 8px;
            border-radius: 2px;
            font-family: monospace;
            font-size: 10px;
            box-shadow: 0 0 15px rgba(0, 255, 204, 0.5);
            pointer-events: none;
        }}
    </style>
    <script src="https://unpkg.com/three"></script>
    <script src="https://unpkg.com/globe.gl"></script>
</head>
<body>
    <div class="scanline"></div>
    <div id="hud">
        <h2 style="margin:0; text-shadow: 0 0 10px #00ffcc;">GLOBAL ASSET COMMAND</h2>
        <div style="font-size:12px; opacity:0.8;">SYSTEM ONLINE | SAT-LINK: STABLE</div>
        <div style="font-size:12px; opacity:0.8;">ACTIVE UNITS: {len(st.session_state.inventory)}</div>
    </div>
    <div id="globeViz"></div>

    <script>
        // 1. 获取Python传来的资产数据
        const myAssets = {assets_json};
        
        // 2. 生成装饰性数据 (卫星 & 雷达)
        const N_SATS = 12;
        const satellites = [...Array(N_SATS).keys()].map(() => ({{
            lat: (Math.random() - 0.5) * 180,
            lng: (Math.random() - 0.5) * 360,
            alt: 0.3 + Math.random() * 0.4,
            speed: (Math.random() * 0.2 + 0.05) * (Math.random()>0.5?1:-1),
            color: Math.random() > 0.3 ? '#00ffcc' : '#ff3300'
        }}));

        const N_RINGS = 8;
        const rings = [...Array(N_RINGS).keys()].map(() => ({{
            lat: (Math.random() - 0.5) * 100,
            lng: (Math.random() - 0.5) * 360,
            maxR: Math.random() * 10 + 3,
            speed: Math.random() * 2 + 0.5,
            repeat: Math.random() * 2000 + 1000
        }}));

        // 3. 初始化地球
        const world = Globe()
            (document.getElementById('globeViz'))
            .backgroundColor('#000000')
            // 全息风格贴图 (夜景 + 拓扑)
            .globeImageUrl('https://unpkg.com/three-globe/example/img/earth-night.jpg')
            .bumpImageUrl('https://unpkg.com/three-globe/example/img/earth-topology.png')
            // 大气发光效果
            .atmosphereColor('#00ccff')
            .atmosphereAltitude(0.25)
            
            // --- 资产点 (光柱) ---
            .pointsData(myAssets)
            .pointLat('lat')
            .pointLng('lng')
            .pointColor(() => '#ffcc00') // 金色代表资产
            .pointAltitude(0.1)
            .pointRadius(0.5)
            
            // --- 卫星系统 (3D球体) ---
            .objectsData(satellites)
            .objectLat('lat')
            .objectLng('lng')
            .objectAltitude('alt')
            .objectThreeObject(d => {{
                const g = new THREE.Group();
                // 卫星本体
                const mesh = new THREE.Mesh(
                    new THREE.SphereGeometry(1, 8, 8),
                    new THREE.MeshLambertMaterial({{ color: d.color, emissive: d.color, emissiveIntensity: 1 }})
                );
                g.add(mesh);
                return g;
            }})
            
            // --- 雷达波 ---
            .ringsData(rings)
            .ringColor(() => t => `rgba(0, 255, 204, ${{1-t}})`)
            .ringMaxRadius('maxR')
            .ringPropagationSpeed('speed')
            .ringRepeatPeriod('repeat')
            
            // --- HTML 标签 (显示资产名字) ---
            .htmlElementsData(myAssets)
            .htmlLat('lat')
            .htmlLng('lng')
            .htmlElement(d => {{
                const el = document.createElement('div');
                el.className = 'label-card';
                el.innerHTML = `<div>${{d.name}}</div><div style="font-size:8px; opacity:0.7;">${{d.brand}}</div>`;
                return el;
            }});

        // 4. 动画循环 (确保旋转和卫星飞行)
        // 添加星空背景
        const scene = world.scene();
        const starGeo = new THREE.BufferGeometry();
        const starMat = new THREE.PointsMaterial({{color:0xffffff, size:0.5}});
        const stars = [];
        for(let i=0; i<4000; i++) stars.push((Math.random()-0.5)*4000);
        starGeo.setAttribute('position', new THREE.Float32BufferAttribute(stars, 3));
        scene.add(new THREE.Points(starGeo, starMat));

        // 自动旋转 & 卫星运动
        world.controls().autoRotate = true;
        world.controls().autoRotateSpeed = 0.5;

        (function tick() {{
            // 更新卫星位置
            satellites.forEach(s => s.lng += s.speed);
            world.objectsData([...satellites]);
            
            requestAnimationFrame(tick);
        }})();
        
        // 初始视角
        world.pointOfView({{ altitude: 2.0 }});
    </script>
</body>
</html>
"""

# ==========================================
# 4. 界面布局
# ==========================================

# --- 顶部：全息地球 (高度600px) ---
components.html(html_code, height=600, scrolling=False)

# --- 底部：资产控制台 ---
c1, c2 = st.columns([3, 1])

with c1:
    st.markdown("### 🛒 ASSET ACQUISITION MARKET")
    tabs = st.tabs(list(DB.keys()))
    
    for i, (cat_name, items) in enumerate(DB.items()):
        with tabs[i]:
            for brand, name, price in items:
                col_a, col_b = st.columns([4, 1])
                with col_a:
                    st.markdown(f"""
                    <div class="asset-card">
                        <div class="brand-tag">{brand}</div>
                        <div style="font-size:1.2em; font-weight:bold;">{name}</div>
                        <div class="price-tag">${price:,}</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col_b:
                    st.write("")
                    if st.button("DEPLOY", key=f"buy_{name}"):
                        buy(brand, name, price)

with c2:
    st.markdown("### 🏦 TREASURY")
    st.markdown(f"""
    <div style="background:#111; padding:20px; border:1px solid #ffcc00; text-align:center;">
        <div style="color:#888; font-size:0.8em;">LIQUID ASSETS</div>
        <div style="font-size:2em; color:#ffcc00; font-family:'Courier New'; font-weight:bold;">
            ${st.session_state.cash:,.0f}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📋 ACTIVE UNITS")
    if not st.session_state.inventory:
        st.info("NO ACTIVE UNITS")
    else:
        for i, item in enumerate(st.session_state.inventory):
            with st.expander(f"{item['name']}"):
                st.caption(f"Coords: {item['lat']:.2f}, {item['lng']:.2f}")
                if st.button("RECALL (SELL)", key=f"sell_{i}"):
                    sell(i)
