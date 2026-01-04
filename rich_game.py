import streamlit as st
import streamlit.components.v1 as components
import json
import random
import time

# ==========================================
# 0. 页面配置
# ==========================================
st.set_page_config(page_title="JARVIS GLOBAL COMMAND", layout="wide", page_icon="⚛️")

st.markdown("""
<style>
    .stApp {background-color: #000000; color: #00aaff; font-family: 'Segoe UI', monospace;}
    [data-testid="stSidebar"] {background-color: #050505; border-right: 1px solid #003333;}
    header, footer {visibility: hidden;}
    
    /* 资产卡片 */
    .asset-card {
        background: rgba(0, 10, 20, 0.9);
        border: 1px solid #0044ff;
        border-left: 3px solid #00aaff;
        border-radius: 2px;
        padding: 12px;
        margin-bottom: 8px;
        transition: all 0.3s;
    }
    .asset-card:hover {
        background: rgba(0, 30, 50, 1);
        transform: translateX(10px);
        box-shadow: 0 0 15px rgba(0, 170, 255, 0.4);
    }
    
    /* 字体 */
    h1, h2, h3 {color: #00aaff !important; text-transform: uppercase; letter-spacing: 2px; text-shadow: 0 0 8px #00aaff;}
    .price {color: #00ffcc; font-family: 'Courier New'; font-weight: bold;}
    
    /* 红色发射按钮 */
    .launch-btn {
        border: 1px solid #ff3300 !important;
        color: #ff3300 !important;
        background: rgba(255, 50, 0, 0.1) !important;
    }
    .launch-btn:hover {
        background: #ff3300 !important;
        color: #000 !important;
        box-shadow: 0 0 20px #ff3300;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 1. 资产数据库 (含军事)
# ==========================================
def create_db():
    return {
        "⚔️ MILITARY (Classified)": [
            ("Lockheed Martin", "F-22 Raptor Squad", 350000000),
            ("Northrop", "B-2 Spirit Stealth", 2100000000),
            ("General Dynamics", "F-16 Fighting Falcon", 60000000),
            ("Navy", "Nimitz Class Carrier", 8500000000),
            ("Navy", "Virginia Class Sub", 2800000000),
            ("Army", "M1A2 Abrams Batallion", 90000000),
            ("Raytheon", "Patriot Missile Battery", 1000000000)
        ],
        "🏎️ LAND ASSETS": [
            ("Mercedes-AMG", "G 63 6x6", 650000), ("Rolls-Royce", "Phantom VIII Armor", 1200000),
            ("Bugatti", "Centodieci", 9000000), ("Tesla", "Cybertruck Foundation", 120000)
        ],
        "✈️ AIR ASSETS": [
            ("Gulfstream", "G700 Executive", 78000000), ("Boeing", "BBJ 747-8i", 420000000),
            ("Sikorsky", "S-76D Helicopter", 15000000)
        ],
        "⚓ NAVAL ASSETS": [
            ("Lürssen", "Project Blue", 600000000), ("Oceanco", "Black Pearl", 220000000)
        ]
    }

DB = create_db()

# ==========================================
# 2. 状态管理
# ==========================================
if 'cash' not in st.session_state:
    st.session_state.cash = 50000000000
    st.session_state.inventory = []
if 'launch_trigger' not in st.session_state:
    st.session_state.launch_trigger = False

# 购买逻辑
def buy(brand, name, price):
    if st.session_state.cash >= price:
        st.session_state.cash -= price
        st.session_state.inventory.append({
            "brand": brand, "name": name, "price": price,
            "lat": random.uniform(-60, 60), "lng": random.uniform(-180, 180)
        })
        st.toast(f"✅ UNIT ACQUIRED: {name}")
        st.rerun()

# 发射逻辑
def trigger_launch():
    st.session_state.launch_trigger = True
    st.rerun()

# ==========================================
# 3. 全息引擎 (Transparent Marvel Style)
# ==========================================
assets_data = json.dumps(st.session_state.inventory)
launch_status = "true" if st.session_state.launch_trigger else "false"

# 发射后重置状态，防止刷新页面重复发射
if st.session_state.launch_trigger:
    st.session_state.launch_trigger = False

html_code = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <style>
        body {{ margin: 0; background: #000; overflow: hidden; }}
        
        /* 倒计时覆盖层 */
        #countdown-layer {{
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            display: flex; justify-content: center; align-items: center;
            pointer-events: none; z-index: 100;
            display: none;
        }}
        #countdown-text {{
            font-family: 'Courier New', monospace;
            font-size: 10vw; color: #ff3300; font-weight: bold;
            text-shadow: 0 0 30px #ff3300;
            animation: pulse 0.8s infinite;
        }}
        
        @keyframes pulse {{
            0% {{ transform: scale(1); opacity: 1; }}
            50% {{ transform: scale(1.1); opacity: 0.8; }}
            100% {{ transform: scale(1); opacity: 1; }}
        }}

        /* HUD */
        #hud {{
            position: absolute; top: 20px; left: 20px; z-index: 50;
            font-family: 'Segoe UI', sans-serif; color: #00aaff;
            pointer-events: none;
        }}
        .hud-line {{ border-left: 2px solid #00aaff; padding-left: 10px; margin-bottom: 5px; }}
        
    </style>
    <script src="https://unpkg.com/three"></script>
    <script src="https://unpkg.com/globe.gl"></script>
</head>
<body>
    <div id="countdown-layer"><div id="countdown-text">10</div></div>
    
    <div id="hud">
        <h1 style="margin:0; text-shadow:0 0 15px #00aaff;">STARK WORLD SYSTEM</h1>
        <div class="hud-line">ORBITAL DEFENSE: ONLINE</div>
        <div class="hud-line">GLOBAL ASSETS: {len(st.session_state.inventory)}</div>
        <div class="hud-line" id="status-msg">STATUS: MONITORING</div>
    </div>
    
    <div id="globeViz"></div>

    <script>
        // 1. 数据准备
        const assets = {assets_data};
        const shouldLaunch = {launch_status};
        
        // 生成大量卫星 (红/蓝发光点)
        const satellites = [...Array(20).keys()].map(() => ({{
            lat: (Math.random() - 0.5) * 160,
            lng: (Math.random() - 0.5) * 360,
            alt: 0.3 + Math.random() * 0.4,
            radius: 1.5,
            color: Math.random() > 0.5 ? '#ff3300' : '#00aaff',
            speed: (Math.random() * 0.5 + 0.2) * (Math.random()>0.5?1:-1)
        }}));

        // 2. 初始化地球 (透明全息风)
        const world = Globe()
            (document.getElementById('globeViz'))
            .backgroundColor('#000000')
            // 使用夜景图作为基础，但会调整材质使其透明
            .globeImageUrl('https://unpkg.com/three-globe/example/img/earth-night.jpg')
            .bumpImageUrl('https://unpkg.com/three-globe/example/img/earth-topology.png')
            .atmosphereColor('#0088ff')
            .atmosphereAltitude(0.3)
            
            // --- 卫星 (自定义发光球体) ---
            .customLayerData(satellites)
            .customThreeObject(d => {{
                const mesh = new THREE.Mesh(
                    new THREE.SphereGeometry(d.radius, 8, 8),
                    new THREE.MeshBasicMaterial({{ color: d.color }})
                );
                // 添加发光光晕
                const glow = new THREE.Mesh(
                    new THREE.SphereGeometry(d.radius * 3, 8, 8),
                    new THREE.MeshBasicMaterial({{ color: d.color, transparent: true, opacity: 0.3 }})
                );
                mesh.add(glow);
                return mesh;
            }})
            .customThreeObjectUpdate((obj, d) => {{
                // 卫星运动逻辑
                Object.assign(obj.position, world.getCoords(d.lat, d.lng += d.speed, d.alt));
            }})

            // --- 资产点 (改为蓝色全息波纹，去掉了黄色柱子) ---
            .ringsData(assets)
            .ringColor(() => t => `rgba(0, 170, 255, ${{1-t}})`)
            .ringMaxRadius(5)
            .ringPropagationSpeed(2)
            .ringRepeatPeriod(2000);

        // 3. 材质黑客：让地球变透明 (Marvel Style)
        // 等待材质加载完成后修改
        setTimeout(() => {{
            const globeObj = world.scene().children.find(obj => obj.type === 'Group');
            if(globeObj) {{
                globeObj.traverse(child => {{
                    if (child.isMesh && child.material.name === 'globe-material') {{
                        child.material.transparent = true;
                        child.material.opacity = 0.85; // 半透明
                        child.material.color.setHex(0x4444ff); // 偏蓝色调
                        child.material.emissive.setHex(0x001133); // 自发光微蓝
                    }}
                }});
            }}
        }}, 1000);

        // 4. 场景特效 (星空 & 自转)
        const scene = world.scene();
        
        // 增加星空
        const starGeo = new THREE.BufferGeometry();
        const starMat = new THREE.PointsMaterial({{color:0xffffff, size:0.5}});
        const stars = [];
        for(let i=0; i<5000; i++) stars.push((Math.random()-0.5)*4000);
        starGeo.setAttribute('position', new THREE.Float32BufferAttribute(stars, 3));
        scene.add(new THREE.Points(starGeo, starMat));

        // 自动旋转控制器
        world.controls().autoRotate = true;
        world.controls().autoRotateSpeed = 0.6; // 转速

        // 5. 火箭发射系统
        if (shouldLaunch) {{
            const countdownEl = document.getElementById('countdown-layer');
            const numEl = document.getElementById('countdown-text');
            const statusEl = document.getElementById('status-msg');
            
            countdownEl.style.display = 'flex';
            statusEl.innerText = "STATUS: LAUNCH SEQUENCE INITIATED";
            statusEl.style.color = "#ff3300";
            
            let count = 10;
            const timer = setInterval(() => {{
                count--;
                numEl.innerText = count;
                
                if(count <= 0) {{
                    clearInterval(timer);
                    countdownEl.style.display = 'none';
                    launchRocket();
                    statusEl.innerText = "STATUS: ROCKET IN TRAJECTORY";
                }}
            }}, 1000);
        }}

        function launchRocket() {{
            // 创建火箭对象
            const rocketGeo = new THREE.ConeGeometry(0.5, 2, 8);
            const rocketMat = new THREE.MeshBasicMaterial({{ color: 0xff3300 }});
            const rocket = new THREE.Mesh(rocketGeo, rocketMat);
            
            // 尾焰
            const trailGeo = new THREE.ConeGeometry(0.8, 5, 8);
            const trailMat = new THREE.MeshBasicMaterial({{ color: 0xffaa00, transparent: true, opacity: 0.6 }});
            const trail = new THREE.Mesh(trailGeo, trailMat);
            trail.position.y = -3;
            trail.rotation.x = Math.PI;
            rocket.add(trail);

            scene.add(rocket);

            // 发射动画参数
            let altitude = 1.1; // 初始高度 (地表)
            const launchLat = 28.5; // 卡纳维拉尔角附近
            const launchLng = -80.6;
            
            function animateRocket() {{
                altitude += 0.05; // 上升速度
                const coords = world.getCoords(launchLat, launchLng, altitude);
                rocket.position.set(coords.x, coords.y, coords.z);
                
                // 让火箭头朝外
                rocket.lookAt(new THREE.Vector3(0,0,0));
                rocket.rotateX(Math.PI); // 修正朝向

                if(altitude < 10) {{ // 飞到一定高度停止或消失
                    requestAnimationFrame(animateRocket);
                }} else {{
                    scene.remove(rocket);
                }}
            }}
            animateRocket();
        }}

        // 强制刷新渲染循环
        (function tick() {{
            // 确保自转持续
            world.controls().update();
            requestAnimationFrame(tick);
        }})();

    </script>
</body>
</html>
"""

# ==========================================
# 4. 界面布局
# ==========================================
# 顶部全息屏
components.html(html_code, height=600, scrolling=False)

# 控制台区域
c1, c2 = st.columns([3, 1])

with c1:
    st.markdown("### 🛒 MILITARY & ASSET PROCUREMENT")
    tabs = st.tabs(list(DB.keys()))
    
    for i, (cat, items) in enumerate(DB.items()):
        with tabs[i]:
            for brand, name, price in items:
                col_a, col_b = st.columns([4, 1])
                with col_a:
                    st.markdown(f"""
                    <div class="asset-card">
                        <div style="color:#00aaff; font-size:0.8em;">{brand}</div>
                        <div style="font-size:1.2em; font-weight:bold; color:#fff;">{name}</div>
                        <div class="price">${price:,}</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col_b:
                    st.write("")
                    if st.button("ACQUIRE", key=f"buy_{name}"):
                        buy(brand, name, price)

with c2:
    st.markdown("### 🛑 DANGER ZONE")
    # 火箭发射按钮 (特殊样式)
    if st.button("🚀 INITIATE LAUNCH", key="btn_launch", help="Start 10s Countdown"):
        trigger_launch()
    
    st.markdown("---")
    st.markdown("### 💰 TREASURY")
    st.markdown(f"""
    <div style="border:1px solid #00ffcc; padding:20px; text-align:center; border-radius:4px;">
        <div style="color:#888;">LIQUID FUNDS</div>
        <div style="font-size:2em; color:#00ffcc; font-family:'Courier New';">
            ${st.session_state.cash:,.0f}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📋 ACTIVE UNITS")
    if not st.session_state.inventory:
        st.info("NO ACTIVE ASSETS")
    else:
        for item in reversed(st.session_state.inventory[-5:]): # 只显示最近5个
            st.code(f"{item['name']}\nCOORD: {item['lat']:.2f}, {item['lng']:.2f}")
