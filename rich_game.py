import random
import json
import time
import streamlit as st
import streamlit.components.v1 as components

# ==========================================
# 0. 页面配置 (全屏黑金)
# ==========================================
st.set_page_config(page_title="GOD MODE COMMANDER", layout="wide", page_icon="☢️")

st.markdown("""
<style>
    .stApp {background-color: #000000; color: #00aaff; font-family: 'Segoe UI', monospace;}
    [data-testid="stSidebar"] {background-color: #050505; border-right: 1px solid #003333;}
    header, footer {visibility: hidden;}
    
    /* 资产卡片 */
    .asset-card {
        background: rgba(0, 15, 30, 0.9);
        border: 1px solid #0044ff;
        border-left: 4px solid #00aaff;
        border-radius: 4px;
        padding: 12px;
        margin-bottom: 8px;
        transition: all 0.2s;
    }
    .asset-card:hover {
        background: rgba(0, 40, 60, 1);
        box-shadow: 0 0 20px rgba(0, 170, 255, 0.5);
        transform: translateX(5px);
    }
    
    /* 字体 */
    h1, h2, h3 {color: #00aaff !important; text-transform: uppercase; letter-spacing: 2px; text-shadow: 0 0 10px #00aaff;}
    .price {color: #ffcc00; font-family: 'Courier New'; font-weight: bold;}
    .brand {color: #0088cc; font-size: 0.8em; letter-spacing: 1px;}
    
    /* 红色发射按钮 */
    div.stButton > button {
        border: 1px solid #00aaff; color: #00aaff; background: transparent;
        width: 100%; border-radius: 0;
    }
    div.stButton > button:hover {
        background: #00aaff; color: #000;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 1. 超级资产数据库 (全量回归 + 军事)
# ==========================================
def create_db():
    return {
        "⚔️ MILITARY (TOP SECRET)": [
            ("USAF", "F-22 Raptor Squadron", 350000000),
            ("Northrop", "B-2 Spirit Stealth", 2100000000),
            ("Lockheed", "SR-72 Darkstar", 5000000000),
            ("Navy", "USS Gerald R. Ford", 13000000000),
            ("Navy", "Columbia Class Sub", 8500000000),
            ("SpaceX", "Starship Heavy Cargo", 150000000),
            ("Raytheon", "Iron Dome System", 100000000)
        ],
        "🏎️ SUPERCARS (The Garage)": [
            ("Rolls-Royce", "Phantom VIII EWB", 650000), ("Rolls-Royce", "Cullinan Black", 480000),
            ("Rolls-Royce", "Spectre", 420000), ("Rolls-Royce", "Boat Tail", 28000000),
            ("Bugatti", "Chiron Super Sport", 3900000), ("Bugatti", "Tourbillon", 4500000),
            ("Bugatti", "La Voiture Noire", 18000000), ("Bugatti", "Mistral", 5000000),
            ("Ferrari", "Daytona SP3", 2200000), ("Ferrari", "Purosangue", 400000),
            ("Ferrari", "LaFerrari Aperta", 4500000), ("Ferrari", "SF90 Spider", 550000),
            ("Lamborghini", "Revuelto", 600000), ("Lamborghini", "Countach LPI", 2600000),
            ("Lamborghini", "Urus Performante", 270000), ("Mercedes-AMG", "G 63 6x6", 1200000),
            ("Mercedes-Maybach", "S 680 Haute Voiture", 300000), ("Aston Martin", "Valkyrie", 3500000),
            ("Pagani", "Utopia", 2500000), ("Koenigsegg", "Jesko Absolut", 3400000)
        ],
        "✈️ PRIVATE AIR WING": [
            ("Gulfstream", "G700 Flagship", 78000000), ("Gulfstream", "G800 Long Range", 81500000),
            ("Gulfstream", "G650ER", 70000000), ("Bombardier", "Global 7500", 75000000),
            ("Bombardier", "Global 8000", 78000000), ("Boeing", "BBJ 747-8i Palace", 450000000),
            ("Boeing", "BBJ 787 Dreamliner", 280000000), ("Boeing", "BBJ 777X", 400000000),
            ("Dassault", "Falcon 10X", 75000000), ("Sikorsky", "S-92 VIP Helo", 25000000)
        ],
        "⚓ NAVAL FLEET": [
            ("Lürssen", "Azzam (180m)", 600000000), ("Lürssen", "Blue (160m)", 600000000),
            ("Lürssen", "Dilbar (156m)", 800000000), ("Blohm+Voss", "Eclipse", 1200000000),
            ("Feadship", "Project 1010", 300000000), ("Oceanco", "Y721 Koru", 500000000),
            ("Oceanco", "Black Pearl", 220000000), ("Benetti", "Luminosity", 280000000)
        ],
        "🏰 GLOBAL ESTATES": [
            ("New York", "Central Park Tower PH", 250000000), ("London", "The Holme", 300000000),
            ("France", "Villa Leopolda", 750000000), ("Los Angeles", "The One", 140000000),
            ("Monaco", "Tour Odéon Sky PH", 380000000), ("Hong Kong", "Barker Road", 280000000),
            ("Shanghai", "Tan Gong Villa", 100000000), ("Beijing", "Houhai Courtyard", 180000000)
        ]
    }

DB = create_db()

# ==========================================
# 2. 状态管理 (1万亿资金)
# ==========================================
if 'cash' not in st.session_state:
    st.session_state.cash = 1000000000000 # 10,000亿
    st.session_state.inventory = [] 
    # 预设几个资产让地图不空
    st.session_state.inventory.append({"brand":"USAF", "name":"F-22 Raptor [PATROL]", "price":0, "lat":35, "lng":-118})
    st.session_state.inventory.append({"brand":"Navy", "name":"USS Ford [DEPLOYED]", "price":0, "lat":20, "lng":-160})

if 'launch_mode' not in st.session_state:
    st.session_state.launch_mode = False

# 购买逻辑
def buy(brand, name, price):
    if st.session_state.cash >= price:
        st.session_state.cash -= price
        st.session_state.inventory.append({
            "brand": brand, "name": name, "price": price,
            "lat": random.uniform(-60, 60), "lng": random.uniform(-180, 180)
        })
        st.toast(f"✅ UNIT DEPLOYED: {name}")
        # 不使用 rerun，利用 Streamlit 的自动刷新特性

# 发射触发器
def trigger_launch():
    st.session_state.launch_mode = True

# ==========================================
# 3. 全息引擎 V4.0 (透明地球 + 卫星 + 火箭)
# ==========================================
assets_json = json.dumps(st.session_state.inventory)
launch_flag = "true" if st.session_state.launch_mode else "false"

if st.session_state.launch_mode:
    st.session_state.launch_mode = False 

html_code = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <style>
        body {{ margin: 0; background: #000; overflow: hidden; }}
        
        /* 倒计时覆盖层 */
        #launch-overlay {{
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            display: flex; flex-direction: column; justify-content: center; align-items: center;
            background: rgba(20, 0, 0, 0.5);
            z-index: 999; pointer-events: none; opacity: 0; transition: opacity 0.5s;
        }}
        .countdown-num {{
            font-family: 'Courier New', monospace;
            font-size: 15vw; font-weight: 900; color: #ff0000;
            text-shadow: 0 0 50px #ff0000; animation: pulse 1s infinite;
        }}
        .launch-status {{ font-family: sans-serif; font-size: 2vw; color: #ff5555; letter-spacing: 5px; margin-top: 20px; }}
        
        @keyframes pulse {{
            0% {{ transform: scale(1); opacity: 1; }}
            50% {{ transform: scale(1.1); opacity: 0.8; }}
            100% {{ transform: scale(1); opacity: 1; }}
        }}

        /* HUD */
        #hud {{
            position: absolute; top: 20px; left: 20px; pointer-events: none; z-index: 100;
            font-family: 'Segoe UI', sans-serif;
        }}
        .hud-title {{ color: #00aaff; font-size: 24px; font-weight: bold; letter-spacing: 3px; text-shadow: 0 0 10px #00aaff; }}
        .hud-info {{ color: #0088cc; font-size: 12px; margin-top: 5px; }}
        
        /* 资产标签 */
        .label {{
            background: rgba(0, 20, 40, 0.8); border: 1px solid #00aaff;
            color: #fff; padding: 4px 8px; font-size: 10px; border-radius: 2px;
            pointer-events: none; box-shadow: 0 0 10px rgba(0, 170, 255, 0.5);
        }}
    </style>
    <script src="https://unpkg.com/three"></script>
    <script src="https://unpkg.com/globe.gl"></script>
</head>
<body>
    <div id="launch-overlay">
        <div id="countdown-text" class="countdown-num">10</div>
        <div class="launch-status">ICBM LAUNCH SEQUENCE</div>
    </div>

    <div id="hud">
        <div class="hud-title">GOD MODE // COMMANDER</div>
        <div class="hud-info">ORBITAL SATELLITES: ACTIVE (20)</div>
        <div class="hud-info">GLOBAL ASSETS: {len(st.session_state.inventory)} UNITS</div>
    </div>
    
    <div id="globeViz"></div>

    <script>
        const myAssets = {assets_json};
        const startLaunch = {launch_flag};

        // --- 1. 卫星群 (确保肉眼可见) ---
        const satellites = [...Array(25).keys()].map(() => ({{
            lat: (Math.random() - 0.5) * 160,
            lng: (Math.random() - 0.5) * 360,
            alt: 0.4 + Math.random() * 0.5,
            radius: 1.2, 
            color: Math.random() > 0.5 ? '#ff0000' : '#00ffff',
            speed: (Math.random() * 0.3 + 0.1) * (Math.random()>0.5?1:-1)
        }}));

        // --- 2. 初始化地球 ---
        const world = Globe()
            (document.getElementById('globeViz'))
            .backgroundColor('#000000')
            .globeImageUrl('https://unpkg.com/three-globe/example/img/earth-night.jpg')
            .bumpImageUrl('https://unpkg.com/three-globe/example/img/earth-topology.png')
            .atmosphereColor('#0066ff')
            .atmosphereAltitude(0.25)
            
            // 卫星
            .customLayerData(satellites)
            .customThreeObject(d => {{
                const mesh = new THREE.Mesh(
                    new THREE.SphereGeometry(d.radius, 8, 8),
                    new THREE.MeshBasicMaterial({{ color: d.color }})
                );
                const glow = new THREE.Mesh(
                    new THREE.SphereGeometry(d.radius * 3, 8, 8),
                    new THREE.MeshBasicMaterial({{ color: d.color, transparent: true, opacity: 0.4 }})
                );
                mesh.add(glow);
                return mesh;
            }})
            .customThreeObjectUpdate((obj, d) => {{
                Object.assign(obj.position, world.getCoords(d.lat, d.lng += d.speed, d.alt));
            }})

            // 资产光柱
            .pointsData(myAssets)
            .pointLat('lat').pointLng('lng')
            .pointColor(() => '#00aaff')
            .pointAltitude(0.15)
            .pointRadius(0.6)
            
            // 资产标签
            .htmlElementsData(myAssets)
            .htmlLat('lat').htmlLng('lng')
            .htmlElement(d => {{
                const el = document.createElement('div');
                el.className = 'label';
                el.innerHTML = `<div>${{d.name}}</div>`;
                return el;
            }});

        // --- 3. 漫威风：透明地球材质 ---
        setTimeout(() => {{
            const scene = world.scene();
            scene.traverse(obj => {{
                if (obj.type === 'Mesh' && obj.material.name === 'globe-material') {{
                    obj.material.transparent = true;
                    obj.material.opacity = 0.8; 
                    obj.material.color.setHex(0x3366ff); // 蓝
                }}
            }});
        }}, 500);

        // --- 4. 动画循环 ---
        const scene = world.scene();
        // 星空
        const starGeo = new THREE.BufferGeometry();
        const starMat = new THREE.PointsMaterial({{color:0xffffff, size:0.6}});
        const stars = [];
        for(let i=0; i<3000; i++) stars.push((Math.random()-0.5)*4000);
        starGeo.setAttribute('position', new THREE.Float32BufferAttribute(stars, 3));
        scene.add(new THREE.Points(starGeo, starMat));

        // 强制自转
        world.controls().autoRotate = true;
        world.controls().autoRotateSpeed = 0.6;

        let rocketMesh = null;
        let rocketAlt = 0;

        // --- 5. 发射逻辑 ---
        if (startLaunch) {{
            const overlay = document.getElementById('launch-overlay');
            const txt = document.getElementById('countdown-text');
            overlay.style.opacity = 1;
            
            let count = 10;
            const timer = setInterval(() => {{
                count--;
                txt.innerText = count;
                if (count <= 0) {{
                    clearInterval(timer);
                    overlay.style.opacity = 0;
                    fireRocket();
                }}
            }}, 1000);
        }}

        function fireRocket() {{
            const geo = new THREE.ConeGeometry(0.5, 2, 8);
            const mat = new THREE.MeshBasicMaterial({{color: 0xff3300}});
            rocketMesh = new THREE.Mesh(geo, mat);
            
            const trail = new THREE.Mesh(
                new THREE.ConeGeometry(0.8, 6, 8),
                new THREE.MeshBasicMaterial({{color: 0xffaa00, transparent:true, opacity:0.6}})
            );
            trail.position.y = -3;
            trail.rotation.x = Math.PI;
            rocketMesh.add(trail);
            
            scene.add(rocketMesh);
            rocketAlt = 0.1;
        }}

        (function tick() {{
            world.controls().update(); 
            world.customLayerData(world.customLayerData()); // 刷新卫星

            if (rocketMesh) {{
                rocketAlt += 0.08; // 飞得更快一点
                const coords = world.getCoords(28.5, -80.6, rocketAlt);
                rocketMesh.position.set(coords.x, coords.y, coords.z);
                rocketMesh.lookAt(new THREE.Vector3(0,0,0));
                rocketMesh.rotateX(Math.PI);
                
                if (rocketAlt > 20) {{
                    scene.remove(rocketMesh);
                    rocketMesh = null;
                }}
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
    st.markdown("### 🛒 ASSET MARKET (CLASS 5)")
    tabs = st.tabs(list(DB.keys()))
    
    for i, (cat, items) in enumerate(DB.items()):
        with tabs[i]:
            for brand, name, price in items:
                col_a, col_b = st.columns([4, 1])
                with col_a:
                    st.markdown(f"""
                    <div class="asset-card">
                        <div class="brand">{brand}</div>
                        <div style="font-size:1.1em; font-weight:bold; color:#fff;">{name}</div>
                        <div class="price">${price:,}</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col_b:
                    st.write("")
                    if st.button("ACQUIRE", key=f"buy_{name}"):
                        buy(brand, name, price)

with c2:
    st.markdown(f"""
    <div style="border:1px solid #ffcc00; padding:20px; text-align:center; background:#0a0a0a; margin-bottom:20px;">
        <div style="color:#888;">TREASURY BALANCE</div>
        <div style="font-size:2.5em; color:#ffcc00; font-family:'Courier New'; font-weight:bold;">
            ${st.session_state.cash:,.0f}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🚀 STRATEGIC COMMAND")
    if st.button("INITIATE LAUNCH (10s)", type="primary"):
        trigger_launch()
        st.rerun() # 强制刷新以触发前端动画
        
    st.markdown("---")
    st.markdown("### 📋 ACTIVE UNITS")
    if not st.session_state.inventory:
        st.info("NO ACTIVE ASSETS")
    else:
        for item in reversed(st.session_state.inventory[-6:]):
            st.code(f"{item['name']}")
