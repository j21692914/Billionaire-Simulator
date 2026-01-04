import streamlit as st
import streamlit.components.v1 as components
import json
import random

# ==========================================
# 0. 页面配置 (全屏黑金)
# ==========================================
st.set_page_config(page_title="HOLO-COMMANDER V5", layout="wide", page_icon="⚛️")

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
        padding: 10px;
        margin-bottom: 8px;
        transition: all 0.2s;
    }
    .asset-card:hover {
        background: rgba(0, 50, 80, 1);
        transform: translateX(5px);
        border-color: #fff;
    }
    
    /* 字体 */
    h1, h2, h3 {color: #00aaff !important; letter-spacing: 2px; text-shadow: 0 0 10px #00aaff;}
    .price {color: #ffcc00; font-family: 'Courier New'; font-weight: bold;}
    
    /* 发射按钮 */
    div.stButton > button {
        border: 1px solid #ff3300; color: #ff3300; background: rgba(50,0,0,0.5);
        width: 100%; font-weight: bold; letter-spacing: 2px;
    }
    div.stButton > button:hover {
        background: #ff3300; color: white;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 1. 资产数据库 (全量 60+)
# ==========================================
def create_db():
    return {
        "⚔️ MILITARY (TOP SECRET)": [
            ("USAF", "F-22 Raptor", 350000000), ("Northrop", "B-2 Spirit", 2100000000),
            ("Lockheed", "SR-71 Blackbird", 0), ("Navy", "USS Gerald Ford", 13000000000),
            ("Navy", "Nuclear Submarine", 8500000000), ("SpaceX", "Starship Mil-Spec", 150000000),
            ("Raytheon", "Patriot Missile", 1000000000)
        ],
        "🏎️ SUPERCARS": [
            ("Rolls-Royce", "Phantom VIII", 650000), ("Rolls-Royce", "Cullinan", 480000),
            ("Rolls-Royce", "Boat Tail", 28000000), ("Bugatti", "Chiron SS", 3900000),
            ("Bugatti", "La Voiture Noire", 18000000), ("Bugatti", "Mistral", 5000000),
            ("Ferrari", "Daytona SP3", 2200000), ("Ferrari", "LaFerrari", 4500000),
            ("Ferrari", "SF90 Spider", 550000), ("Lamborghini", "Revuelto", 600000),
            ("Lamborghini", "Countach LPI", 2600000), ("Mercedes-AMG", "G 63 6x6", 1200000),
            ("Aston Martin", "Valkyrie", 3500000), ("Pagani", "Utopia", 2500000),
            ("Koenigsegg", "Jesko", 3400000)
        ],
        "✈️ PRIVATE JETS": [
            ("Gulfstream", "G700", 78000000), ("Gulfstream", "G800", 81500000),
            ("Gulfstream", "G650ER", 70000000), ("Bombardier", "Global 7500", 75000000),
            ("Boeing", "BBJ 747-8", 450000000), ("Boeing", "BBJ 787", 280000000),
            ("Dassault", "Falcon 10X", 75000000), ("Sikorsky", "S-92 Helo", 25000000)
        ],
        "⚓ YACHTS": [
            ("Lürssen", "Azzam (180m)", 650000000), ("Lürssen", "Dilbar", 800000000),
            ("Blohm+Voss", "Eclipse", 1200000000), ("Oceanco", "Black Pearl", 220000000),
            ("Feadship", "Project 1010", 300000000)
        ],
        "🏰 ESTATES": [
            ("NY", "Central Park Tower", 250000000), ("London", "The Holme", 300000000),
            ("France", "Villa Leopolda", 750000000), ("LA", "The One", 140000000),
            ("Monaco", "Odeon Tower PH", 380000000), ("Hong Kong", "Barker Rd", 280000000)
        ]
    }

DB = create_db()

# ==========================================
# 2. 状态管理 (1万亿)
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
        st.toast(f"DEPLOYED: {name}")

def trigger_launch():
    st.session_state.launch_mode = True

# ==========================================
# 3. 全息引擎 V5.0 (国内CDN加速版)
# ==========================================
assets_json = json.dumps(st.session_state.inventory)
launch_flag = "true" if st.session_state.launch_mode else "false"

# 重置发射状态
if st.session_state.launch_mode:
    st.session_state.launch_mode = False 

html_code = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <style>
        body {{ margin: 0; background: #000; overflow: hidden; }}
        
        /* 倒计时 */
        #overlay {{
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            display: flex; justify-content: center; align-items: center;
            background: rgba(0,0,0,0.7); z-index: 999; 
            opacity: 0; transition: opacity 0.5s; pointer-events: none;
        }}
        .count {{
            font-family: 'Courier New'; font-size: 20vw; color: #ff0000;
            font-weight: 900; text-shadow: 0 0 40px #ff0000;
        }}
        
        /* HUD */
        #hud {{ position: absolute; top: 20px; left: 20px; z-index: 100; font-family: sans-serif; pointer-events: none; }}
        .title {{ color: #00aaff; font-size: 24px; font-weight: bold; letter-spacing: 2px; }}
        .sub {{ color: #006699; font-size: 12px; }}

        /* 标签 */
        .label {{
            background: rgba(0, 0, 0, 0.8); border: 1px solid #00aaff;
            color: #00aaff; padding: 2px 5px; font-size: 10px;
            pointer-events: none; box-shadow: 0 0 5px #00aaff;
        }}
    </style>
    
    <script src="https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/globe.gl@2.30.0/dist/globe.gl.min.js"></script>
</head>
<body>
    <div id="overlay"><div id="cnt" class="count">10</div></div>
    
    <div id="hud">
        <div class="title">HOLO-COMMAND V5</div>
        <div class="sub">NETWORK: SECURE | SATELLITES: ONLINE</div>
        <div class="sub">ASSETS: {len(st.session_state.inventory)} UNITS</div>
    </div>
    
    <div id="globeViz"></div>

    <script>
        const myAssets = {assets_json};
        const doLaunch = {launch_flag};

        // 1. 生成卫星 (数量增加，尺寸变大)
        const satellites = [...Array(30).keys()].map(() => ({{
            lat: (Math.random() - 0.5) * 180,
            lng: (Math.random() - 0.5) * 360,
            alt: 0.3 + Math.random() * 0.5,
            radius: 1.5, // 变大
            color: Math.random() > 0.5 ? '#ff0000' : '#00ffff',
            speed: (Math.random() * 0.5 + 0.1) * (Math.random()>0.5?1:-1)
        }}));

        // 2. 初始化地球
        const world = Globe()
            (document.getElementById('globeViz'))
            .backgroundColor('#000000')
            .globeImageUrl('https://cdn.jsdelivr.net/npm/three-globe/example/img/earth-night.jpg') // 同样用CDN
            .bumpImageUrl('https://cdn.jsdelivr.net/npm/three-globe/example/img/earth-topology.png')
            .atmosphereColor('#0088ff')
            .atmosphereAltitude(0.2)
            
            // 卫星图层
            .customLayerData(satellites)
            .customThreeObject(d => {{
                const mesh = new THREE.Mesh(
                    new THREE.SphereGeometry(d.radius, 8, 8),
                    new THREE.MeshBasicMaterial({{ color: d.color }})
                );
                // 卫星光晕
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

            // 资产点 (蓝色脉冲)
            .pointsData(myAssets)
            .pointLat('lat').pointLng('lng')
            .pointColor(() => '#00aaff')
            .pointAltitude(0.05)
            .pointRadius(0.8)
            .pointPulseRipple(true) // 开启脉冲
            
            // 资产标签
            .htmlElementsData(myAssets)
            .htmlLat('lat').htmlLng('lng')
            .htmlElement(d => {{
                const el = document.createElement('div');
                el.className = 'label';
                el.innerHTML = d.name;
                return el;
            }});

        // 3. 漫威风透明材质
        setTimeout(() => {{
            const scene = world.scene();
            scene.traverse(obj => {{
                if (obj.type === 'Mesh' && obj.material.name === 'globe-material') {{
                    obj.material.transparent = true;
                    obj.material.opacity = 0.8;
                    obj.material.color.setHex(0x2244ff); // 科技蓝
                }}
            }});
        }}, 1000);

        // 4. 环境配置 (自转 & 星空)
        const scene = world.scene();
        
        // 星空
        const starGeo = new THREE.BufferGeometry();
        const starMat = new THREE.PointsMaterial({{color:0xffffff, size:0.5}});
        const stars = [];
        for(let i=0; i<3000; i++) stars.push((Math.random()-0.5)*4000);
        starGeo.setAttribute('position', new THREE.Float32BufferAttribute(stars, 3));
        scene.add(new THREE.Points(starGeo, starMat));

        // 强制开启自转
        world.controls().autoRotate = true;
        world.controls().autoRotateSpeed = 0.8;

        // 5. 火箭发射系统
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
            // 火箭本体
            const geo = new THREE.ConeGeometry(0.5, 2, 8);
            const mat = new THREE.MeshBasicMaterial({{color: 0xff0000}});
            rocket = new THREE.Mesh(geo, mat);
            
            // 尾焰
            const trail = new THREE.Mesh(
                new THREE.ConeGeometry(0.8, 8, 8),
                new THREE.MeshBasicMaterial({{color: 0xffaa00, transparent:true, opacity:0.6}})
            );
            trail.position.y = -4;
            trail.rotation.x = Math.PI;
            rocket.add(trail);
            
            scene.add(rocket);
            rAlt = 0.1;
        }}

        // 6. 渲染循环
        (function tick() {{
            world.controls().update(); // 自转驱动
            world.customLayerData(world.customLayerData()); // 卫星驱动

            // 火箭飞行
            if (rocket) {{
                rAlt += 0.08;
                const coords = world.getCoords(28.5, -80.6, rAlt); // 佛罗里达发射
                rocket.position.set(coords.x, coords.y, coords.z);
                rocket.lookAt(new THREE.Vector3(0,0,0));
                rocket.rotateX(Math.PI);
                
                if (rAlt > 25) {{
                    scene.remove(rocket);
                    rocket = null;
                }}
            }}
            requestAnimationFrame(tick);
        }})();
        
        world.pointOfView({{ altitude: 2.2 }});
    </script>
</body>
</html>
"""

# ==========================================
# 4. 界面布局
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

with c2:
    st.markdown(f"""
    <div style="border:1px solid #ffcc00; padding:20px; text-align:center; background:#111; margin-bottom:20px;">
        <div style="color:#888;">TREASURY</div>
        <div style="font-size:2em; color:#ffcc00; font-family:'Courier New'; font-weight:bold;">
            ${st.session_state.cash:,.0f}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🚀 LAUNCH PAD")
    if st.button("INITIATE LAUNCH (10s)", type="primary"):
        trigger_launch()
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 📋 ACTIVE UNITS")
    if not st.session_state.inventory:
        st.info("NONE")
    else:
        for item in reversed(st.session_state.inventory[-6:]):
            st.code(f"{item['name']}")
