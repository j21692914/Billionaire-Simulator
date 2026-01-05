import streamlit as st
import streamlit.components.v1 as components
import json
import random
import time

# ==========================================
# 0. 页面配置 (末日战争风格)
# ==========================================
st.set_page_config(page_title="COMMANDER X", layout="wide", page_icon="☢️")

st.markdown("""
<style>
    .stApp {background-color: #000000; color: #00ccff; font-family: 'Segoe UI', monospace;}
    [data-testid="stSidebar"] {background-color: #080808; border-right: 1px solid #330000;}
    header, footer {visibility: hidden;}
    
    /* 资产卡片 */
    .asset-card {
        background: rgba(0, 20, 30, 0.9);
        border: 1px solid #004488;
        border-left: 3px solid #00ccff;
        padding: 10px; margin-bottom: 5px;
    }
    .asset-card:hover { border-color: #fff; transform: translateX(5px); }
    
    h1, h2, h3 {color: #00ccff !important; text-shadow: 0 0 8px #00ccff; letter-spacing: 2px;}
    
    /* 红色核按钮 */
    .nuke-btn {
        background: linear-gradient(45deg, #550000, #aa0000);
        color: white !important;
        font-weight: 900 !important;
        border: 2px solid #ff0000 !important;
        box-shadow: 0 0 15px #ff0000;
        animation: pulse 2s infinite;
    }
    
    /* 蓝色拦截按钮 */
    .defense-btn {
        background: linear-gradient(45deg, #002255, #0044aa);
        color: white !important;
        font-weight: 900 !important;
        border: 2px solid #00aaff !important;
        box-shadow: 0 0 15px #00aaff;
    }
    
    @keyframes pulse { 0% {opacity: 1;} 50% {opacity: 0.8;} 100% {opacity: 1;} }
    
    /* Streamlit 按钮样式覆盖 */
    div.stButton > button {
        width: 100%; border-radius: 0; padding: 15px; font-size: 1.1em;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 1. 资产数据库 (全量 60+)
# ==========================================
def create_db():
    return {
        "⚔️ MILITARY": [
            ("USAF", "F-22 Raptor", 350000000), ("Northrop", "B-2 Spirit", 2100000000),
            ("Lockheed", "SR-72", 5000000000), ("Navy", "USS Gerald Ford", 13000000000),
            ("Navy", "Columbia Sub", 8500000000), ("SpaceX", "Starship Mil", 150000000)
        ],
        "🏎️ CARS": [
            ("Rolls-Royce", "Phantom VIII", 650000), ("Rolls-Royce", "Cullinan", 480000),
            ("Bugatti", "Chiron SS", 3900000), ("Bugatti", "La Voiture Noire", 18000000),
            ("Ferrari", "LaFerrari", 4500000), ("Lamborghini", "Revuelto", 600000),
            ("Mercedes", "G 63 6x6", 1200000), ("Koenigsegg", "Jesko", 3400000),
            ("Aston Martin", "Valkyrie", 3500000), ("Pagani", "Utopia", 2500000)
        ],
        "✈️ JETS": [
            ("Gulfstream", "G700", 78000000), ("Bombardier", "Global 8000", 78000000),
            ("Boeing", "BBJ 747-8", 450000000), ("Dassault", "Falcon 10X", 75000000)
        ],
        "⚓ YACHTS": [
            ("Lürssen", "Azzam", 650000000), ("Blohm+Voss", "Eclipse", 1200000000),
            ("Oceanco", "Black Pearl", 220000000)
        ],
        "🏰 ESTATES": [
            ("NY", "Central Park Tower", 250000000), ("London", "The Holme", 300000000),
            ("France", "Villa Leopolda", 750000000), ("LA", "The One", 140000000)
        ]
    }
DB = create_db()

# ==========================================
# 2. 状态管理 (资产 + 核战)
# ==========================================
if 'cash' not in st.session_state:
    st.session_state.cash = 1000000000000 # 1万亿
    st.session_state.inventory = []
    # 预设资产
    st.session_state.inventory.append({"brand":"USAF", "name":"F-22 Raptor", "lat":35, "lng":-118})

# --- 核战状态 ---
if 'nukes' not in st.session_state:
    st.session_state.nukes = [] # 存储飞行中的导弹
if 'impacts' not in st.session_state:
    st.session_state.impacts = [] # 存储爆炸点

def buy(brand, name, price):
    if st.session_state.cash >= price:
        st.session_state.cash -= price
        st.session_state.inventory.append({
            "brand": brand, "name": name, 
            "lat": random.uniform(-60, 60), "lng": random.uniform(-180, 180)
        })
        st.toast(f"✅ ASSET DEPLOYED: {name}")

def launch_nukes():
    # 一次发射 10 枚
    for _ in range(10):
        st.session_state.nukes.append({
            "startLat": random.uniform(-60, 70),
            "startLng": random.uniform(-180, 180),
            "endLat": random.uniform(-60, 70),
            "endLng": random.uniform(-180, 180)
        })
    st.toast("⚠️ WARNING: 10 ICBMs LAUNCHED!")

def intercept():
    destroyed = 0
    leaked = 0
    surviving_nukes = []
    
    for nuke in st.session_state.nukes:
        if random.random() < 0.9: # 90% 拦截率
            destroyed += 1
        else:
            leaked += 1
            # 漏网之鱼变成了爆炸点
            st.session_state.impacts.append({
                "lat": nuke['endLat'], "lng": nuke['endLng']
            })
            
    st.session_state.nukes = [] # 清空飞行列表（要么被拦截，要么爆炸）
    
    msg = f"🛡️ INTERCEPTION REPORT: {destroyed} DESTROYED"
    if leaked > 0:
        msg += f" | ❌ {leaked} IMPACTS CONFIRMED!"
        st.error(msg)
    else:
        msg += " | ✅ 100% SECURE"
        st.success(msg)

# ==========================================
# 3. 混合引擎 (线框地球 + 资产 + 核弹)
# ==========================================
assets_json = json.dumps(st.session_state.inventory)
nukes_json = json.dumps(st.session_state.nukes)
impacts_json = json.dumps(st.session_state.impacts)

html_code = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <style>
        body {{ margin: 0; background: #000; overflow: hidden; }}
        #hud {{
            position: absolute; top: 20px; left: 20px; z-index: 100;
            font-family: 'Courier New', monospace; pointer-events: none;
        }}
        .title {{ color: #00aaff; font-size: 24px; font-weight: bold; text-shadow: 0 0 10px #00aaff; }}
        .war-status {{ color: #ff3300; font-size: 16px; font-weight: bold; margin-top: 5px; text-shadow: 0 0 10px #ff0000; }}
        
        .asset-label {{
            background: rgba(0, 20, 40, 0.8); border: 1px solid #00aaff;
            color: #fff; padding: 2px 5px; font-size: 10px; pointer-events: none;
        }}
    </style>
    <script src="https://cdn.bootcdn.net/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/globe.gl@2.26.4/dist/globe.gl.min.js"></script>
</head>
<body>
    <div id="hud">
        <div class="title">COMMANDER X // SYSTEM</div>
        <div style="color:#00ccff; font-size:12px;">ASSETS SECURE: {len(st.session_state.inventory)}</div>
        <div class="war-status">INCOMING THREATS: {len(st.session_state.nukes)}</div>
        <div class="war-status" style="color:#ffaa00;">DETONATIONS: {len(st.session_state.impacts)}</div>
    </div>
    
    <div id="globeViz"></div>

    <script>
        const myAssets = {assets_json};
        const nukes = {nukes_json};
        const impacts = {impacts_json};

        // 1. 卫星群 (红色警戒)
        const satellites = [...Array(30).keys()].map(() => ({{
            lat: (Math.random() - 0.5) * 180,
            lng: (Math.random() - 0.5) * 360,
            alt: 0.3 + Math.random() * 0.5,
            radius: 0.8,
            color: '#ff3300',
            speed: (Math.random() * 0.5 + 0.1) * (Math.random()>0.5?1:-1)
        }}));

        // 2. 初始化地球 (线框版)
        const world = Globe()
            (document.getElementById('globeViz'))
            .backgroundColor('#000000')
            // 线框材质
            .globeMaterial(new THREE.MeshBasicMaterial({{
                color: 0x004466, wireframe: true, transparent: true, opacity: 0.4
            }}))
            .atmosphereColor('#0088ff').atmosphereAltitude(0.15)
            
            // --- 资产层 (文字标签) ---
            .htmlElementsData(myAssets)
            .htmlLat('lat').htmlLng('lng')
            .htmlElement(d => {{
                const el = document.createElement('div');
                el.className = 'asset-label';
                el.innerText = d.name;
                return el;
            }})

            // --- 核弹层 (红色轨迹) ---
            .arcsData(nukes)
            .arcStartLat('startLat').arcStartLng('startLng')
            .arcEndLat('endLat').arcEndLng('endLng')
            .arcColor(() => ['#ff5500', '#ff0000']) // 渐变红
            .arcDashLength(0.4)
            .arcDashGap(0.2)
            .arcDashAnimateTime(15000) // 15秒飞完全程 (极慢)
            .arcStroke(1.5) // 粗细
            
            // --- 爆炸层 (红色波纹) ---
            .ringsData(impacts)
            .ringColor(() => t => `rgba(255, 50, 0, ${{1-t}})`)
            .ringMaxRadius(15) // 巨大爆炸范围
            .ringPropagationSpeed(1) // 缓慢扩散
            .ringRepeatPeriod(800)

            // --- 卫星层 ---
            .customLayerData(satellites)
            .customThreeObject(d => {{
                return new THREE.Mesh(
                    new THREE.SphereGeometry(d.radius, 8, 8),
                    new THREE.MeshBasicMaterial({{ color: d.color }})
                );
            }})
            .customThreeObjectUpdate((obj, d) => {{
                Object.assign(obj.position, world.getCoords(d.lat, d.lng += d.speed, d.alt));
            }});

        // 3. 动画控制
        const scene = world.scene();
        const starGeo = new THREE.BufferGeometry();
        const starMat = new THREE.PointsMaterial({{color:0xffffff, size:0.5}});
        const stars = [];
        for(let i=0; i<4000; i++) stars.push((Math.random()-0.5)*4000);
        starGeo.setAttribute('position', new THREE.Float32BufferAttribute(stars, 3));
        scene.add(new THREE.Points(starGeo, starMat));

        world.controls().autoRotate = true;
        world.controls().autoRotateSpeed = 0.5;

        (function tick() {{
            world.controls().update(); 
            world.customLayerData(world.customLayerData()); 
            requestAnimationFrame(tick);
        }})();
        
        world.pointOfView({{ altitude: 2.2 }});
    </script>
</body>
</html>
"""

# ==========================================
# 4. 界面布局 (战争室 + 资产部)
# ==========================================
components.html(html_code, height=600, scrolling=False)

c1, c2 = st.columns([2, 1])

with c1:
    st.markdown("### 🛒 ASSET PROCUREMENT")
    tabs = st.tabs(list(DB.keys()))
    for i, (cat, items) in enumerate(DB.items()):
        with tabs[i]:
            for brand, name, price in items:
                col_a, col_b = st.columns([4, 1])
                with col_a:
                    st.markdown(f"""
                    <div class="asset-card">
                        <div style="color:#00aaff; font-size:0.8em;">{brand}</div>
                        <div style="font-size:1.1em; font-weight:bold; color:#fff;">{name}</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col_b:
                    if st.button("BUY", key=f"buy_{name}"): buy(brand, name, price); st.rerun()

with c2:
    st.markdown("### ☢️ WAR ROOM")
    
    # 核打击按钮
    st.markdown('<div style="margin-bottom: 10px;">', unsafe_allow_html=True)
    if st.button("🔴 LAUNCH 10 ICBMs", key="btn_nuke", help="Launch nuclear strike"):
        launch_nukes()
        st.rerun()
    
    # 拦截按钮
    if st.button("🛡️ DEPLOY INTERCEPTORS (90%)", key="btn_defend", help="Attempt interception"):
        intercept()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div style="border:1px solid #ffcc00; padding:15px; text-align:center; background:#111; margin-top:20px;">
        <div style="color:#888;">WAR CHEST</div>
        <div style="font-size:1.8em; color:#ffcc00; font-family:'Courier New';">
            ${st.session_state.cash:,.0f}
        </div>
    </div>
    """, unsafe_allow_html=True)
