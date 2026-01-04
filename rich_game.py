import streamlit as st
import streamlit.components.v1 as components
import json
import random

# ==========================================
# 0. 页面配置 (全屏黑金)
# ==========================================
st.set_page_config(page_title="JARVIS V9", layout="wide", page_icon="💠")

st.markdown("""
<style>
    .stApp {background-color: #000000; color: #00ccff; font-family: 'Segoe UI', monospace;}
    [data-testid="stSidebar"] {background-color: #050505; border-right: 1px solid #002222;}
    header, footer {visibility: hidden;}
    
    /* 资产卡片 */
    .asset-card {
        background: rgba(0, 10, 20, 0.9);
        border: 1px solid #004488;
        border-left: 3px solid #00ccff;
        padding: 12px; margin-bottom: 8px;
        transition: 0.2s;
    }
    .asset-card:hover { border-color: #00ffff; box-shadow: 0 0 15px rgba(0, 255, 255, 0.2); }
    
    h1, h2, h3 {color: #00ccff !important; text-shadow: 0 0 8px #00ccff; letter-spacing: 2px;}
    
    /* 发射按钮 */
    div.stButton > button {
        border: 1px solid #ff3300; color: #ff3300; background: transparent;
        width: 100%; font-weight: bold; letter-spacing: 2px; border-radius: 0;
    }
    div.stButton > button:hover {
        background: #ff3300; color: #000; box-shadow: 0 0 20px #ff3300;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 1. 资产数据库 (全量)
# ==========================================
def create_db():
    return {
        "⚔️ MILITARY": [
            ("USAF", "F-22 Raptor Squad", 350000000), ("Northrop", "B-2 Spirit", 2100000000),
            ("Lockheed", "SR-72 Darkstar", 5000000000), ("Navy", "USS Gerald Ford", 13000000000),
            ("Navy", "Columbia Nuke Sub", 8500000000), ("SpaceX", "Starship Cargo", 150000000)
        ],
        "🏎️ SUPERCARS": [
            ("Rolls-Royce", "Phantom VIII", 650000), ("Rolls-Royce", "Cullinan", 480000),
            ("Bugatti", "Chiron SS", 3900000), ("Bugatti", "La Voiture Noire", 18000000),
            ("Ferrari", "LaFerrari", 4500000), ("Lamborghini", "Revuelto", 600000),
            ("Mercedes", "G 63 6x6", 1200000), ("Koenigsegg", "Jesko", 3400000),
            ("Aston Martin", "Valkyrie", 3500000), ("Pagani", "Utopia", 2500000)
        ],
        "✈️ JETS & YACHTS": [
            ("Gulfstream", "G700", 78000000), ("Bombardier", "Global 8000", 78000000),
            ("Boeing", "BBJ 747-8", 450000000), ("Lürssen", "Azzam", 650000000),
            ("Oceanco", "Black Pearl", 220000000)
        ]
    }
DB = create_db()

# ==========================================
# 2. 状态管理
# ==========================================
if 'cash' not in st.session_state:
    st.session_state.cash = 1000000000000
    st.session_state.inventory = []
    st.session_state.inventory.append({"brand":"USAF", "name":"F-22 Raptor", "price":0, "lat":35, "lng":-118})

if 'launch_mode' not in st.session_state:
    st.session_state.launch_mode = False

def buy(brand, name, price):
    if st.session_state.cash >= price:
        st.session_state.cash -= price
        st.session_state.inventory.append({
            "brand": brand, "name": name, "price": price,
            "lat": random.uniform(-60, 60), "lng": random.uniform(-180, 180)
        })
        st.toast(f"DEPLOYED: {name}")

def trigger_launch():
    st.session_state.launch_mode = True

# ==========================================
# 3. 贾维斯线框引擎 V9.0 (稀疏网格+慢速发射)
# ==========================================
assets_json = json.dumps(st.session_state.inventory)
launch_flag = "true" if st.session_state.launch_mode else "false"
if st.session_state.launch_mode: st.session_state.launch_mode = False 

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
        .status {{ color: #006688; font-size: 12px; margin-top: 5px; }}
        .launch-alert {{
            color: #ff3300; font-size: 18px; font-weight: bold; 
            text-shadow: 0 0 20px #ff3300; margin-top: 10px; display: none;
        }}
        
        .asset-label {{
            background: rgba(0, 10, 20, 0.85);
            border: 1px solid #00aaff;
            color: #fff; padding: 4px 8px; border-radius: 2px;
            font-family: sans-serif; font-size: 9px;
            pointer-events: none;
            box-shadow: 0 0 8px rgba(0, 170, 255, 0.5);
            transform: translate(-50%, -120%);
        }}
        .asset-label::after {{
            content: ''; position: absolute; bottom: -10px; left: 50%;
            width: 1px; height: 10px; background: #00aaff;
        }}
    </style>
    
    <script src="https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/globe.gl@2.30.0/dist/globe.gl.min.js"></script>
</head>
<body>
    <div id="hud">
        <div class="title">JARVIS V9 // LOW-POLY</div>
        <div class="status">GRID DENSITY: 24x24 (SPARSE)</div>
        <div class="status">ACTIVE ASSETS: {len(st.session_state.inventory)}</div>
        <div id="launch-msg" class="launch-alert">⚠️ LAUNCH SEQUENCE: <span id="timer">10</span></div>
    </div>
    
    <div id="globeViz"></div>

    <script>
        const myAssets = {assets_json};
        const doLaunch = {launch_flag};

        // 1. 卫星群 (红色)
        const satellites = [...Array(30).keys()].map(() => ({{
            lat: (Math.random() - 0.5) * 180,
            lng: (Math.random() - 0.5) * 360,
            alt: 0.3 + Math.random() * 0.5,
            radius: 1.0,
            color: '#ff3300',
            speed: (Math.random() * 0.5 + 0.1) * (Math.random()>0.5?1:-1)
        }}));

        // 2. 初始化地球
        const world = Globe()
            (document.getElementById('globeViz'))
            .backgroundColor('#000000')
            
            // --- 核心：隐藏原本的地球 ---
            .globeMaterial(new THREE.MeshBasicMaterial({{
                color: 0x000000, 
                transparent: true,
                opacity: 0 // 完全透明，隐藏原本的高密度球体
            }}))
            .atmosphereColor('#0044ff') // 蓝色大气
            .atmosphereAltitude(0.2)
            
            // 卫星
            .customLayerData(satellites)
            .customThreeObject(d => {{
                const mesh = new THREE.Mesh(
                    new THREE.SphereGeometry(d.radius, 8, 8),
                    new THREE.MeshBasicMaterial({{ color: d.color }})
                );
                return mesh;
            }})
            .customThreeObjectUpdate((obj, d) => {{
                Object.assign(obj.position, world.getCoords(d.lat, d.lng += d.speed, d.alt));
            }})

            // 资产标签
            .htmlElementsData(myAssets)
            .htmlLat('lat').htmlLng('lng')
            .htmlElement(d => {{
                const el = document.createElement('div');
                el.className = 'asset-label';
                el.innerHTML = d.name;
                return el;
            }});

        // 3. 手动添加稀疏网格 (Low-Poly Grid)
        const scene = world.scene();
        
        // 创建一个只有 24x24 段数的球体网格，这样看起来就很稀疏
        const gridGeo = new THREE.SphereGeometry(100, 24, 24); 
        const gridMat = new THREE.MeshBasicMaterial({{
            color: 0x00ffff,  // 高亮青色
            wireframe: true,  // 线框模式
            transparent: true,
            opacity: 0.3      // 半透明
        }});
        const gridSphere = new THREE.Mesh(gridGeo, gridMat);
        scene.add(gridSphere);

        // 星空
        const starGeo = new THREE.BufferGeometry();
        const starMat = new THREE.PointsMaterial({{color:0xffffff, size:0.5}});
        const stars = [];
        for(let i=0; i<4000; i++) stars.push((Math.random()-0.5)*4000);
        starGeo.setAttribute('position', new THREE.Float32BufferAttribute(stars, 3));
        scene.add(new THREE.Points(starGeo, starMat));

        // 自转
        world.controls().autoRotate = true;
        world.controls().autoRotateSpeed = 0.6;

        // 4. 慢速火箭系统
        let rocket = null;
        let rAlt = 0;

        if (doLaunch) {{
            const msg = document.getElementById('launch-msg');
            const tmr = document.getElementById('timer');
            msg.style.display = 'block';
            
            let c = 10;
            const t = setInterval(() => {{
                c--; tmr.innerText = c;
                if (c <= 0) {{
                    clearInterval(t);
                    msg.innerHTML = "🚀 IGNITION...";
                    launch();
                }}
            }}, 1000);
        }}

        function launch() {{
            const geo = new THREE.ConeGeometry(1.5, 6, 16); // 巨大火箭
            const mat = new THREE.MeshBasicMaterial({{color: 0xff5500}});
            rocket = new THREE.Mesh(geo, mat);
            
            // 尾焰 (粒子效果)
            const trail = new THREE.Mesh(
                new THREE.ConeGeometry(1.0, 15, 16),
                new THREE.MeshBasicMaterial({{color: 0xffaa00, transparent:true, opacity:0.6}})
            );
            trail.position.y = -10;
            trail.rotation.x = Math.PI;
            rocket.add(trail);
            
            scene.add(rocket);
            rAlt = 0.1; // 初始高度
        }}

        (function tick() {{
            world.controls().update(); 
            world.customLayerData(world.customLayerData()); 

            if (rocket) {{
                // --- 极慢速爬升 ---
                rAlt += 0.015; // 速度减慢 10倍，慢慢欣赏
                
                const coords = world.getCoords(28.5, -80.6, rAlt);
                rocket.position.set(coords.x, coords.y, coords.z);
                rocket.lookAt(new THREE.Vector3(0,0,0));
                rocket.rotateX(Math.PI);
                
                // 慢慢消失
                if (rAlt > 35) {{ scene.remove(rocket); rocket = null; }}
            }}
            requestAnimationFrame(tick);
        }})();
        
        world.pointOfView({{ altitude: 2.5 }});
    </script>
</body>
</html>
"""

# ==========================================
# 4. 界面渲染
# ==========================================
components.html(html_code, height=600, scrolling=False)

c1, c2 = st.columns([2, 1])

with c1:
    st.markdown("### 🛒 ASSET MARKET")
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
                        <div class="price">${price:,}</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col_b:
                    st.write("")
                    if st.button("BUY", key=f"buy_{name}"):
                        buy(brand, name, price)
                        st.rerun()

with c2:
    st.markdown(f"""
    <div style="border:1px solid #ffcc00; padding:20px; text-align:center; background:#111; margin-bottom:20px;">
        <div style="color:#888;">TREASURY</div>
        <div style="font-size:2em; color:#ffcc00; font-family:'Courier New'; font-weight:bold;">
            ${st.session_state.cash:,.0f}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 INITIATE LAUNCH", type="primary"):
        trigger_launch()
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 📋 ACTIVE ASSETS")
    for item in reversed(st.session_state.inventory[-6:]):
        st.code(f"{item['name']}")
