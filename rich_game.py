import streamlit as st
import streamlit.components.v1 as components

# ==========================================
# 0. 基础配置 (黑色全屏风格)
# ==========================================
st.set_page_config(page_title="GLOBAL COMMAND", layout="wide", page_icon="🌍")

# 隐藏 Streamlit 默认的白色边框，让画面更沉浸
st.markdown("""
<style>
    .stApp {background-color: #000000;}
    header {visibility: hidden;}
    .block-container {padding: 0 !important; margin: 0 !important; max-width: 100% !important;}
    iframe {width: 100%; height: 100vh;}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 1. 核心 3D 地球代码 (HTML/JS 封装进 Python)
# ==========================================
# 这是一个完整的网页，被包裹在 Python 字符串里
html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <style>
        body { margin: 0; background: #000; overflow: hidden; font-family: 'Segoe UI', monospace; }
        
        /* HUD 界面 */
        #hud {
            position: absolute; top: 20px; left: 20px; z-index: 100;
            color: #00ffcc; pointer-events: none;
        }
        h1 { margin: 0; font-size: 24px; letter-spacing: 2px; text-shadow: 0 0 10px #00ffcc; }
        .stat { font-size: 12px; color: #0088aa; margin-top: 5px; }
        
        /* 交互提示卡片 */
        .card {
            position: absolute; background: rgba(0, 20, 30, 0.9);
            border: 1px solid #00ffcc; color: #fff; padding: 10px;
            border-radius: 4px; width: 180px; font-size: 12px;
            box-shadow: 0 0 20px rgba(0, 255, 204, 0.3);
            pointer-events: none; opacity: 0; transition: opacity 0.3s;
            transform: translate(-50%, -100%); margin-top: -20px;
        }
        .card-title { color: #00ffcc; font-weight: bold; border-bottom: 1px solid #004455; padding-bottom: 5px; margin-bottom: 5px;}
        
        /* 扫描线 */
        .scan {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background: linear-gradient(to bottom, transparent 50%, rgba(0, 255, 204, 0.03) 51%);
            background-size: 100% 4px; pointer-events: none; z-index: 99;
        }
    </style>
    <script src="https://unpkg.com/three"></script>
    <script src="https://unpkg.com/globe.gl"></script>
</head>
<body>
    <div id="hud">
        <h1>GLOBAL ASSET COMMAND</h1>
        <div class="stat">SYSTEM ONLINE | SATELLITE LINK: ACTIVE</div>
        <div class="stat" style="margin-top: 10px; color: #fff;">>> CLICK EARTH TO DEPLOY ASSET <<</div>
    </div>
    <div class="scan"></div>
    <div id="globeViz"></div>

    <script>
        // --- 1. 数据模拟 ---
        const N_SATS = 6; // 卫星数量
        const N_RINGS = 8; // 雷达波数量
        
        // 卫星数据
        const satellites = [...Array(N_SATS).keys()].map(() => ({
            lat: (Math.random() - 0.5) * 180,
            lng: (Math.random() - 0.5) * 360,
            alt: 0.4 + Math.random() * 0.3,
            speed: (Math.random() * 0.5 + 0.2) * (Math.random()>0.5?1:-1),
            color: Math.random() > 0.5 ? '#ff0055' : '#00ccff'
        }));

        // 雷达波数据
        const rings = [...Array(N_RINGS).keys()].map(() => ({
            lat: (Math.random() - 0.5) * 140,
            lng: (Math.random() - 0.5) * 360,
            maxR: Math.random() * 15 + 5,
            speed: Math.random() * 2 + 1,
            repeat: Math.random() * 2000 + 1000
        }));

        // 资产类型
        const assets = [
            {name: "GULFSTREAM G700", type: "AIR UNIT", color: "#00ffcc"},
            {name: "AEGIS DESTROYER", type: "NAVAL UNIT", color: "#00ccff"},
            {name: "COMMAND BUNKER", type: "LAND BASE", color: "#ffcc00"},
            {name: "INTERCEPTOR DRONE", type: "AIR UNIT", color: "#ff0055"}
        ];

        let myAssets = []; // 存储用户点击生成的资产

        // --- 2. 地球初始化 ---
        const world = Globe()
            (document.getElementById('globeViz'))
            .globeImageUrl('https://unpkg.com/three-globe/example/img/earth-blue-marble.jpg')
            .bumpImageUrl('https://unpkg.com/three-globe/example/img/earth-topology.png')
            .backgroundColor('#000000')
            .atmosphereColor('#0044ff')
            .atmosphereAltitude(0.2)
            
            // 卫星 (3D球体)
            .objectsData(satellites)
            .objectLat('lat').objectLng('lng').objectAltitude('alt')
            .objectThreeObject(d => {
                const g = new THREE.Group();
                g.add(new THREE.Mesh(new THREE.SphereGeometry(1.5,8,8), new THREE.MeshLambertMaterial({color: d.color, emissive: d.color, emissiveIntensity:1})));
                return g;
            })
            
            // 雷达波
            .ringsData(rings)
            .ringColor(() => t => `rgba(0,150,255,${1-t})`)
            .ringMaxRadius('maxR').ringPropagationSpeed('speed').ringRepeatPeriod('repeat')
            
            // HTML 交互标记 (点击生成)
            .htmlElementsData(myAssets)
            .htmlLat('lat').htmlLng('lng')
            .htmlElement(d => {
                const el = document.createElement('div');
                el.innerHTML = `
                    <div class="card" style="opacity:1;">
                        <div class="card-title">${d.data.name}</div>
                        <div>TYPE: ${d.data.type}</div>
                        <div style="font-size:10px; color:#888;">LAT: ${d.lat.toFixed(2)} | LNG: ${d.lng.toFixed(2)}</div>
                    </div>
                    <div style="width:4px; height:4px; background:#fff; border-radius:50%; box-shadow:0 0 10px #fff;"></div>
                `;
                return el;
            })
            
            // 点击事件
            .onGlobeClick(({ lat, lng }) => {
                const item = assets[Math.floor(Math.random() * assets.length)];
                myAssets.push({ lat, lng, data: item });
                world.htmlElementsData([...myAssets]); // 刷新
                
                // 镜头平滑移动
                const p = world.pointOfView();
                world.pointOfView({ lat, lng, altitude: p.altitude }, 1000);
            });

        // --- 3. 动画循环 ---
        // 添加星空
        const scene = world.scene();
        const starGeo = new THREE.BufferGeometry();
        const starMat = new THREE.PointsMaterial({color:0xffffff, size:0.5});
        const starArr = [];
        for(let i=0; i<3000; i++) starArr.push((Math.random()-0.5)*4000);
        starGeo.setAttribute('position', new THREE.Float32BufferAttribute(starArr, 3));
        scene.add(new THREE.Points(starGeo, starMat));

        // 动起来
        (function tick() {
            satellites.forEach(s => s.lng += s.speed);
            world.objectsData([...satellites]);
            world.controls().autoRotate = true;
            world.controls().autoRotateSpeed = 0.3;
            requestAnimationFrame(tick);
        })();
        
        // 自动缩放
        world.pointOfView({ altitude: 2.2 });
    </script>
</body>
</html>
"""

# ==========================================
# 2. 在 Streamlit 中渲染全屏地球
# ==========================================
# height=8000 确保填满屏幕，scrolling=False 禁止滚动条
components.html(html_code, height=1000, scrolling=False)
