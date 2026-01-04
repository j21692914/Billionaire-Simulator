import streamlit as st
import streamlit.components.v1 as components
import json
import random

# ==========================================
# 0. 页面配置 (全屏黑金)
# ==========================================
st.set_page_config(page_title="JARVIS V6", layout="wide", page_icon="💠")

st.markdown("""
<style>
    .stApp {background-color: #000000; color: #00ccff; font-family: 'Segoe UI', monospace;}
    [data-testid="stSidebar"] {background-color: #080808; border-right: 1px solid #003333;}
    header, footer {visibility: hidden;}
    
    /* 资产卡片 */
    .asset-card {
        background: rgba(0, 20, 30, 0.9);
        border: 1px solid #0044ff;
        border-left: 3px solid #00ccff;
        padding: 10px; margin-bottom: 8px;
    }
    h1, h2, h3 {color: #00ccff !important; text-shadow: 0 0 10px #00ccff;}
    
    /* 红色发射按钮 */
    div.stButton > button {
        border: 1px solid #ff3300; color: #ff3300; background: rgba(50,0,0,0.3);
        width: 100%; font-weight: bold; letter-spacing: 2px;
    }
    div.stButton > button:hover {
        background: #ff3300; color: white;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 1. 资产数据库 (全量)
# ==========================================
def create_db():
    return {
        "⚔️ MILITARY": [
            ("USAF", "F-22 Raptor", 350000000), ("Northrop", "B-2 Spirit", 2100000000),
            ("Navy", "USS Gerald Ford", 13000000000), ("Navy", "Nuclear Sub", 8500000000),
            ("SpaceX", "Starship Military", 150000000), ("Raytheon", "Patriot", 1000000000)
        ],
        "🏎️ CARS": [
            ("Rolls-Royce", "Phantom VIII", 650000), ("Rolls-Royce", "Cullinan", 480000),
            ("Bugatti", "Chiron SS", 3900000), ("Bugatti", "La Voiture Noire", 18000000),
            ("Ferrari", "LaFerrari", 4500000), ("Lamborghini", "Revuelto", 600000),
            ("Mercedes", "G 63 6x6", 1200000), ("Koenigsegg", "Jesko", 3400000)
        ],
        "✈️ JETS": [
            ("Gulfstream", "G700", 78000000), ("Gulfstream", "G800", 81500000),
            ("Bombardier", "Global 7500", 75000000), ("Boeing", "BBJ 747-8", 450000000),
            ("Dassault", "Falcon 10X", 75000000)
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
# 2. 状态管理
# ==========================================
if 'cash' not in st.session_state:
    st.session_state.cash = 1000000000000
    st.session_state.inventory = []
    # 预设
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

def trigger_launch():
    st.session_state.launch_mode = True

# ==========================================
# 3. 贾维斯全息引擎 (无贴图·纯代码生成)
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
        #loader {{ position: absolute; top: 50%; left: 50%; color: #00ccff; transform: translate(-50%,-50%); font-family: sans-serif; }}
        
        /* 倒计时 */
        #overlay {{
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            display: flex; justify-content: center; align-items: center;
            background: rgba(0,0,0,0.8); z-index: 999; 
            opacity: 0; transition: opacity 0.5s; pointer-events: none;
        }}
        .count {{ font-family: 'Courier New'; font-size: 20vw; color: #ff0000; font-weight: 900; text-shadow: 0 0 50px #ff0000; }}
        
        #hud {{ position: absolute; top: 20px; left: 20px; z-index: 100; font-family: 'Courier New'; color: #00ccff; pointer-events: none; }}
        .label {{ background: rgba(0,0,0,0.7); border: 1px solid #00ccff; color: #fff; padding: 2px 5px; font-size: 10px; }}
    </style>
    
    <script src="https://cdn.bootcdn.net/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/globe.gl@2.26.4/dist/globe.gl.min.js"></script>
</head>
<body>
    <div id="loader">INITIALIZING JARVIS SYSTEM...</div>
    <div id="overlay"><div id="cnt" class="count">10</div></div>
    
    <div id="hud">
        <h2>JARVIS // SYSTEM V6</h2>
        <div>STATUS: CONNECTED</div>
        <div>ASSETS: {len(st.session_state.inventory)} UNITS</div>
    </div>
    
    <div id="globeViz"></div>

    <script>
        document.getElementById('loader').style.display = 'none';
        const myAssets = {assets_json};
        const doLaunch = {launch_flag};

        // 1. 生成数据
        // 卫星
        const satellites = [...Array(40).keys()].map(() => ({{
            lat: (Math.random() - 0.5) * 180,
            lng: (Math.random() - 0.5) * 360,
            alt: 0.3 + Math.random() * 0.6,
            radius: 0.8,
            color: Math.random() > 0.5 ? '#ff0000' : '#00ffff',
            speed: (Math.random() * 0.5 + 0.2) * (Math.random()>0.5?1:-1)
        }}));

        // 2. 初始化地球 (纯代码生成，无图模式)
        // 我们使用 hexBin 来模拟陆地，这样不需要加载任何图片，百分百显示
        
        fetch('https://raw.githubusercontent.com/vasturiano/globe.gl/master/example/datasets/ne_110m_admin_0_countries.geojson')
            .then(res => res.json())
            .then(countries => {{
                
                const world = Globe()
                (document.getElementById('globeViz'))
                .backgroundColor('#000000')
                
                // === 核心修改：不加载图片，用网格线 ===
                .globeMaterial(new THREE.MeshPhongMaterial({{
                    color: 0x001133, // 深蓝底色
                    opacity: 0.7,
                    transparent: true,
                    emissive: 0x000022
                }}))
                .atmosphereColor('#00ccff')
                .atmosphereAltitude(0.25)
                
                // 用六边形显示陆地 (科技感)
                .hexPolygonsData(countries.features)
                .hexPolygonResolution(3)
                .hexPolygonMargin(0.3)
                .hexPolygonColor(() => 'rgba(0, 200, 255, 0.3)') // 浅蓝陆地
                .hexPolygonAltitude(0.02)

                // 卫星
                .customLayerData(satellites)
                .customThreeObject(d => {{
                    const mesh = new THREE.Mesh(
                        new THREE.SphereGeometry(d.radius, 8, 8),
                        new THREE.MeshBasicMaterial({{ color: d.color }})
                    );
                    const glow = new THREE.Mesh(
                        new THREE.SphereGeometry(d.radius * 3, 8, 8),
                        new THREE.MeshBasicMaterial({{ color: d.color, transparent: true, opacity: 0.5 }})
                    );
                    mesh.add(glow);
                    return mesh;
                }})
                .customThreeObjectUpdate((obj, d) => {{
                    Object.assign(obj.position, world.getCoords(d.lat, d.lng += d.speed, d.alt));
                }})

                // 资产
                .pointsData(myAssets)
                .pointLat('lat').pointLng('lng')
                .pointColor(() => '#ffaa00')
                .pointAltitude(0.1)
                .pointRadius(1.0)
                .pointPulseRipple(true)

                // 标签
                .htmlElementsData(myAssets)
                .htmlLat('lat').htmlLng('lng')
                .htmlElement(d => {{
                    const el = document.createElement('div');
                    el.className = 'label';
                    el.innerText = d.name;
                    return el;
                }});

                // 3. 动画控制
                const scene = world.scene();
                
                // 星空
                const starGeo = new THREE.BufferGeometry();
                const starMat = new THREE.PointsMaterial({{color:0xffffff, size:0.5}});
                const stars = [];
                for(let i=0; i<5000; i++) stars.push((Math.random()-0.5)*4000);
                starGeo.setAttribute('position', new THREE.Float32BufferAttribute(stars, 3));
                scene.add(new THREE.Points(starGeo, starMat));

                // 强制自转
                world.controls().autoRotate = true;
                world.controls().autoRotateSpeed = 1.0;

                // 4. 火箭
                let rocket = null;
                let rAlt = 0;

                if (doLaunch) {{
                    const ov = document.getElementById('overlay');
                    const cnt = document.getElementById('cnt');
                    ov.style.opacity = 1;
                    let c = 10;
                    const t = setInterval(() => {{
                        c--; cnt.innerText = c;
                        if (c <= 0) {{
                            clearInterval(t);
                            ov.style.opacity = 0;
                            launch();
                        }}
                    }}, 1000);
                }}

                function launch() {{
                    const geo = new THREE.ConeGeometry(0.5, 2, 8);
                    const mat = new THREE.MeshBasicMaterial({{color: 0xff0000}});
                    rocket = new THREE.Mesh(geo, mat);
                    const trail = new THREE.Mesh(
                        new THREE.ConeGeometry(0.8, 10, 8),
                        new THREE.MeshBasicMaterial({{color: 0xffaa00, transparent:true, opacity:0.6}})
                    );
                    trail.position.y = -5;
                    trail.rotation.x = Math.PI;
                    rocket.add(trail);
                    scene.add(rocket);
                    rAlt = 0.1;
                }}

                (function tick() {{
                    world.controls().update(); 
                    world.customLayerData(world.customLayerData()); 
                    
                    if (rocket) {{
                        rAlt += 0.1;
                        const coords = world.getCoords(28.5, -80.6, rAlt);
                        rocket.position.set(coords.x, coords.y, coords.z);
                        rocket.lookAt(new THREE.Vector3(0,0,0));
                        rocket.rotateX(Math.PI);
                        if (rAlt > 30) {{ scene.remove(rocket); rocket = null; }}
                    }}
                    requestAnimationFrame(tick);
                }})();
                
                world.pointOfView({{ altitude: 2.2 }});
            }});
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
