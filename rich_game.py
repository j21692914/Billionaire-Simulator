import streamlit as st
import streamlit.components.v1 as components
import json
import random

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
        padding: 15px;
        margin-bottom: 10px;
        transition: all 0.2s;
    }
    .asset-card:hover {
        background: rgba(0, 40, 60, 1);
        box-shadow: 0 0 20px rgba(0, 170, 255, 0.5);
        transform: scale(1.02);
    }
    
    /* 字体 */
    h1, h2, h3 {color: #00aaff !important; text-transform: uppercase; letter-spacing: 3px; text-shadow: 0 0 10px #00aaff;}
    .price {color: #ffcc00; font-family: 'Courier New'; font-weight: bold; font-size: 1.1em;}
    
    /* 红色发射按钮 */
    div.stButton > button {
        border: 1px solid #00aaff; color: #00aaff; background: transparent;
        width: 100%; padding: 10px; border-radius: 0;
    }
    div.stButton > button:hover {
        background: #00aaff; color: #000;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 1. 资产数据库 (含顶级军事装备)
# ==========================================
def create_db():
    return {
        "⚔️ MILITARY (TOP SECRET)": [
            ("USAF", "F-22 Raptor Squadron", 350000000),
            ("Northrop", "B-2 Spirit Stealth Bomber", 2100000000),
            ("Lockheed", "SR-72 Darkstar (Hypersonic)", 5000000000),
            ("Navy", "Gerald R. Ford Carrier", 13000000000),
            ("Navy", "Columbia Class Nuke Sub", 8500000000),
            ("SpaceX", "Starship Military Cargo", 150000000),
            ("Raytheon", "Iron Dome Battery", 100000000)
        ],
        "🏎️ LAND COLLECTION": [
            ("Mercedes-AMG", "G 63 6x6 Armored", 1200000),
            ("Rolls-Royce", "Phantom VIII Bulletproof", 2500000),
            ("Bugatti", "La Voiture Noire", 18000000),
            ("Tesla", "Cybertruck Beast Foundation", 120000)
        ],
        "✈️ AIR FLEET": [
            ("Gulfstream", "G700 World Tourer", 78000000),
            ("Boeing", "BBJ 747-8i Palace", 450000000),
            ("Sikorsky", "S-92 VIP Helo", 25000000)
        ],
        "⚓ MEGA YACHTS": [
            ("Lürssen", "Project Azzam (180m)", 650000000),
            ("Oceanco", "Y721 Koru (Sailing)", 550000000)
        ]
    }

DB = create_db()

# ==========================================
# 2. 状态管理 (1万亿资金 + 发射状态)
# ==========================================
if 'cash' not in st.session_state:
    st.session_state.cash = 1000000000000 # 1万亿美元
    st.session_state.inventory = [] # 资产库
    
    # 预设几个资产让地图不空
    st.session_state.inventory.append({"brand":"USAF", "name":"F-22 Raptor [PATROL]", "price":0, "lat":35, "lng":-118})
    st.session_state.inventory.append({"brand":"Navy", "name":"Ford Carrier [DEPLOYED]", "price":0, "lat":20, "lng":-160})

# 购买逻辑
def buy(brand, name, price):
    if st.session_state.cash >= price:
        st.session_state.cash -= price
        st.session_state.inventory.append({
            "brand": brand, "name": name, "price": price,
            "lat": random.uniform(-60, 60), "lng": random.uniform(-180, 180)
        })
        st.toast(f"✅ UNIT DEPLOYED: {name}")
        st.rerun()

# 发射状态处理 (利用 Session State 传递给前端)
if 'launch_mode' not in st.session_state:
    st.session_state.launch_mode = False

def trigger_launch():
    st.session_state.launch_mode = True
    # 不重新运行，直接利用下面的渲染逻辑

# ==========================================
# 3. 全息引擎 V3.0 (增强动画版)
# ==========================================
assets_json = json.dumps(st.session_state.inventory)
launch_flag = "true" if st.session_state.launch_mode else "false"

# 渲染完成后重置发射状态，防止无限发射
if st.session_state.launch_mode:
    st.session_state.launch_mode = False 

html_code = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <style>
        body {{ margin: 0; background: #000; overflow: hidden; font-family: 'Segoe UI', sans-serif; }}
        
        /* 倒计时层 */
        #launch-overlay {{
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            display: flex; flex-direction: column; justify-content: center; align-items: center;
            background: rgba(20, 0, 0, 0.4);
            z-index: 999; pointer-events: none; opacity: 0; transition: opacity 0.5s;
        }}
        .countdown-num {{
            font-size: 15vw; font-weight: 900; color: #ff0000;
            text-shadow: 0 0 50px #ff0000; animation: pulse 1s infinite;
        }}
        .launch-status {{ font-size: 2vw; color: #ff5555; letter-spacing: 5px; margin-top: 20px; }}
        
        @keyframes pulse {{
            0% {{ transform: scale(1); opacity: 1; }}
            50% {{ transform: scale(1.1); opacity: 0.8; }}
            100% {{ transform: scale(1); opacity: 1; }}
        }}

        /* HUD */
        #hud {{
            position: absolute; top: 20px; left: 20px; pointer-events: none; z-index: 100;
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
        <div class="launch-status">ICBM LAUNCH SEQUENCE INITIATED</div>
    </div>

    <div id="hud">
        <div class="hud-title">GOD MODE // COMMANDER</div>
        <div class="hud-info">ORBITAL SATELLITES: ACTIVE (20)</div>
        <div class="hud-info">GLOBAL ASSETS: {len(st.session_state.inventory)} UNITS</div>
    </div>
    
    <div id="globeViz"></div>

    <script>
        // 1. 接收 Python 数据
        const myAssets = {assets_json};
        const startLaunch = {launch_flag};

        // 2. 生成卫星群数据 (确保能看见)
        const N_SATS = 25;
        const satellites = [...Array(N_SATS).keys()].map(() => ({{
            lat: (Math.random() - 0.5) * 160,
            lng: (Math.random() - 0.5) * 360,
            alt: 0.4 + Math.random() * 0.5,
            radius: 1.0, // 增大尺寸
            color: Math.random() > 0.5 ? '#ff0000' : '#00ffff', // 红/青色
            speed: (Math.random() * 0.3 + 0.1) * (Math.random()>0.5?1:-1)
        }}));

        // 3. 初始化地球
        const world = Globe()
            (document.getElementById('globeViz'))
            .backgroundColor('#000000')
            
            // --- 全息地球材质 (半透明蓝) ---
            .globeImageUrl('https://unpkg.com/three-globe/example/img/earth-night.jpg')
            .bumpImageUrl('https://unpkg.com/three-globe/example/img/earth-topology.png')
            .atmosphereColor('#0066ff')
            .atmosphereAltitude(0.25)
            
            // --- 卫星 (发光球体) ---
            .customLayerData(satellites)
            .customThreeObject(d => {{
                const mesh = new THREE.Mesh(
                    new THREE.SphereGeometry(d.radius, 8, 8),
                    new THREE.MeshBasicMaterial({{ color: d.color }})
                );
                // 加光晕
                const glow = new THREE.Mesh(
                    new THREE.SphereGeometry(d.radius * 3, 8, 8),
                    new THREE.MeshBasicMaterial({{ color: d.color, transparent: true, opacity: 0.4 }})
                );
                mesh.add(glow);
                return mesh;
            }})
            .customThreeObjectUpdate((obj, d) => {{
                // 卫星飞行逻辑 (每帧更新经度)
                Object.assign(obj.position, world.getCoords(d.lat, d.lng += d.speed, d.alt));
            }})

            // --- 资产展示 (HTML标签 + 蓝色光柱) ---
            .htmlElementsData(myAssets)
            .htmlLat('lat').htmlLng('lng')
            .htmlElement(d => {{
                const el = document.createElement('div');
                el.className = 'label';
                el.innerHTML = `<div>${{d.name}}</div>`;
                return el;
            }})
            
            // --- 资产光柱 (替代原来的HTML点，更有科技感) ---
            .pointsData(myAssets)
            .pointLat('lat').pointLng('lng')
            .pointColor(() => '#00aaff')
            .pointAltitude(0.1)
            .pointRadius(0.5);

        // 4. 材质黑客：让地球变透明 (Holo Effect)
        setTimeout(() => {{
            const scene = world.scene();
            scene.traverse(obj => {{
                if (obj.type === 'Mesh' && obj.material.name === 'globe-material') {{
                    obj.material.transparent = true;
                    obj.material.opacity = 0.85; 
                    obj.material.color.setHex(0x2244ff); // 强蓝色叠加
                }}
            }});
        }}, 500);

        // 5. 动画循环 (星空 + 自转)
        const scene = world.scene();
        const starGeo = new THREE.BufferGeometry();
        const starMat = new THREE.PointsMaterial({{color:0xffffff, size:0.6}});
        const stars = [];
        for(let i=0; i<3000; i++) stars.push((Math.random()-0.5)*4000);
        starGeo.setAttribute('position', new THREE.Float32BufferAttribute(stars, 3));
        scene.add(new THREE.Points(starGeo, starMat));

        world.controls().autoRotate = true;
        world.controls().autoRotateSpeed = 0.5;

        // 火箭对象 (全局变量)
        let rocketMesh = null;
        let rocketAlt = 0;

        // 6. 发射逻辑
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
            // 创建火箭
            const geo = new THREE.ConeGeometry(0.5, 2, 8);
            const mat = new THREE.MeshBasicMaterial({{color: 0xff3300}});
            rocketMesh = new THREE.Mesh(geo, mat);
            
            // 尾焰粒子
            const trail = new THREE.Mesh(
                new THREE.ConeGeometry(0.8, 6, 8),
                new THREE.MeshBasicMaterial({{color: 0xffaa00, transparent:true, opacity:0.6}})
            );
            trail.position.y = -3;
            trail.rotation.x = Math.PI;
            rocketMesh.add(trail);
            
            scene.add(rocketMesh);
            rocketAlt = 0.1; // 初始高度
        }}

        // 7. 渲染帧循环
        (function tick() {{
            world.controls().update(); // 维持自转
            
            // 更新卫星位置
            world.customLayerData(world.customLayerData()); 

            // 火箭升空动画
            if (rocketMesh) {{
                rocketAlt += 0.05;
                const coords = world.getCoords(28.5, -80.6, rocketAlt); // 卡纳维拉尔角
                rocketMesh.position.set(coords.x, coords.y, coords.z);
                rocketMesh.lookAt(new THREE.Vector3(0,0,0)); // 尾部对准地心
                rocketMesh.rotateX(Math.PI); // 修正头部朝外
                
                if (rocketAlt > 15) {{ // 飞出视野销毁
                    scene.remove(rocketMesh);
                    rocketMesh = null;
                }}
            }}

            requestAnimationFrame(tick);
        }})();
        
        world.pointOfView({{ altitude: 2.5 }}); // 拉远视角
    </script>
</body>
</html>
"""

# ==========================================
# 4. 界面布局 (控制台)
# ==========================================
# 渲染全息地球
components.html(html_code, height=600, scrolling=False)

# 控制面板
c1, c2 = st.columns([2, 1])

with c1:
    st.markdown("### 🛒 ASSET PROCUREMENT (CLASS 5 CLEARANCE)")
    tabs = st.tabs(list(DB.keys()))
    
    for i, (cat, items) in enumerate(DB.items()):
        with tabs[i]:
            for brand, name, price in items:
                col_a, col_b = st.columns([4, 1])
                with col_a:
                    st.markdown(f"""
                    <div class="asset-card">
                        <div style="color:#0088aa; font-size:0.8em;">{brand}</div>
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
    <div style="border:1px solid #ffcc00; padding:20px; text-align:center; background:#111; margin-bottom:20px;">
        <div style="color:#888;">TREASURY BALANCE</div>
        <div style="font-size:2.5em; color:#ffcc00; font-family:'Courier New'; font-weight:bold;">
            ${st.session_state.cash:,.0f}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 红色发射按钮
    st.markdown("### 🚀 STRATEGIC LAUNCH")
    if st.button("INITIATE ICBM LAUNCH (10s TIMER)", type="primary"):
        trigger_launch()
        
    st.markdown("---")
    st.markdown("### 📋 ACTIVE DEPLOYMENTS")
    if not st.session_state.inventory:
        st.info("NO ACTIVE UNITS")
    else:
        for i, item in enumerate(reversed(st.session_state.inventory[-6:])):
            st.code(f"[{item['brand']}] {item['name']}")
