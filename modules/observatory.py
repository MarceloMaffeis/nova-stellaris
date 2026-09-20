"""
Nova Stellaris - Módulo Observatório do Cosmos
Atlas Celeste com Imagens Reais da NASA/Wikimedia, Balança Planetária, 
Calculadora de Viagem Espacial e Galeria de Imagens em Alta Resolução do James Webb & Hubble.
"""

import os
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import requests
from database import add_xp, unlock_badge

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_DIR = os.path.join(BASE_DIR, "assets", "images")

def get_img(filename: str) -> str:
    local_p = os.path.join(IMG_DIR, filename)
    if os.path.exists(local_p):
        return local_p
    return filename

CELESTIAL_BODIES = {
    "Sol": {
        "type": "Estrela (Anã Amarela)",
        "icon": "☀️",
        "image_url": get_img("sun.jpg"),
        "diameter_km": 1392700,
        "gravity_ms2": 274.0,
        "gravity_ratio": 27.9,
        "temp_c": 5500,
        "day_duration": "25 a 35 dias terrestres",
        "year_duration": "230 milhões de anos (órbita galáctica)",
        "curiosity": "No núcleo do Sol, 600 milhões de toneladas de Hidrogênio se fundem em Hélio a cada segundo!",
        "scifi_link": "Em 'Devoradores de Estrelas', os microrganismos Astrofagos absorvem a luz da superfície solar."
    },
    "Mercúrio": {
        "type": "Planeta Rochoso",
        "icon": "🪨",
        "image_url": get_img("mercury.jpg"),
        "diameter_km": 4879,
        "gravity_ms2": 3.7,
        "gravity_ratio": 0.38,
        "temp_c": 167,
        "day_duration": "59 dias terrestres",
        "year_duration": "88 dias terrestres",
        "curiosity": "É o planeta mais próximo do Sol, mas não o mais quente (não tem atmosfera para reter calor).",
        "scifi_link": "Seu núcleo de ferro ocupa mais de 80% do raio do planeta!"
    },
    "Vênus": {
        "type": "Planeta Rochoso",
        "icon": "🟡",
        "image_url": get_img("venus.jpg"),
        "diameter_km": 12104,
        "gravity_ms2": 8.87,
        "gravity_ratio": 0.90,
        "temp_c": 464,
        "day_duration": "243 dias terrestres",
        "year_duration": "225 dias terrestres",
        "curiosity": "Um dia em Vênus dura mais do que o ano inteiro dele! E o efeito estufa descontrolado faz chover ácido sulfúrico.",
        "scifi_link": "Em ficção científica, Vênus é o exemplo máximo do que o efeito estufa descontrolado pode causar a um planeta."
    },
    "Terra": {
        "type": "Planeta Rochoso (Nosso Lar)",
        "icon": "🌍",
        "image_url": get_img("earth.jpg"),
        "diameter_km": 12742,
        "gravity_ms2": 9.81,
        "gravity_ratio": 1.0,
        "temp_c": 15,
        "day_duration": "24 horas",
        "year_duration": "365,25 dias",
        "curiosity": "É o único planeta conhecido com água líquida em abundância e vida biológica diversa.",
        "scifi_link": "O berço de todas as missões espaciais da humanidade!"
    },
    "Lua": {
        "type": "Satélite Natural",
        "icon": "🌕",
        "image_url": get_img("moon.jpg"),
        "diameter_km": 3474,
        "gravity_ms2": 1.62,
        "gravity_ratio": 0.165,
        "temp_c": -20,
        "day_duration": "27,3 dias terrestres",
        "year_duration": "27,3 dias terrestres (órbita)",
        "curiosity": "A Lua está sempre com a mesma face voltada para a Terra devido ao acoplamento de maré!",
        "scifi_link": "12 astronautas do programa Apollo caminharam e pularam na poeira lunar (regolito)."
    },
    "Marte": {
        "type": "Planeta Rochoso (Planeta Vermelho)",
        "icon": "🔴",
        "image_url": get_img("mars.jpg"),
        "diameter_km": 6779,
        "gravity_ms2": 3.72,
        "gravity_ratio": 0.38,
        "temp_c": -63,
        "day_duration": "24h 39min (1 Sol)",
        "year_duration": "687 dias terrestres",
        "curiosity": "Possui o Monte Olimpo, o maior vulcão do Sistema Solar, com 22 km de altura (quase 3 vezes o Everest!).",
        "scifi_link": "Cenário de 'Perdido em Marte', onde Mark Watney desafiou todas as probabilidades para sobreviver."
    },
    "Júpiter": {
        "type": "Gigante Gasoso",
        "icon": "🪐",
        "image_url": get_img("jupiter.jpg"),
        "diameter_km": 139820,
        "gravity_ms2": 24.79,
        "gravity_ratio": 2.53,
        "temp_c": -110,
        "day_duration": "9h 55min",
        "year_duration": "11,86 anos terrestres",
        "curiosity": "Sua 'Grande Mancha Vermelha' é uma tempestade ciclônica maior que o planeta Terra inteiro!",
        "scifi_link": "Possui mais de 90 luas, incluindo Europa e Ganímedes."
    },
    "Europa (Lua de Júpiter)": {
        "type": "Lua Oceânica Gelada",
        "icon": "🧊",
        "image_url": get_img("europa.jpg"),
        "diameter_km": 3121,
        "gravity_ms2": 1.31,
        "gravity_ratio": 0.134,
        "temp_c": -160,
        "day_duration": "3,5 dias terrestres",
        "year_duration": "3,5 dias terrestres",
        "curiosity": "Abaixo de sua crosta de gelo de 20 km, esconde um oceano líquido com mais água do que todos os oceanos da Terra juntos!",
        "scifi_link": "Principal candidata para a busca por vida alienígena microbiana no Sistema Solar."
    },
    "Saturno": {
        "type": "Gigante Gasoso com Anéis",
        "icon": "🪐",
        "image_url": get_img("saturn.jpg"),
        "diameter_km": 116460,
        "gravity_ms2": 10.44,
        "gravity_ratio": 1.06,
        "temp_c": -140,
        "day_duration": "10h 33min",
        "year_duration": "29,45 anos terrestres",
        "curiosity": "Seus anéis são formados por bilhões de pedaços de gelo e rocha, variando do tamanho de grãos de areia até montanhas!",
        "scifi_link": "Saturno é tão pouco denso que, se houvesse uma banheira gigante de água, ele flutuaria!"
    },
    "Titã (Lua de Saturno)": {
        "type": "Lua com Atmosfera Densa",
        "icon": "🌫️",
        "image_url": get_img("titan.jpg"),
        "diameter_km": 5149,
        "gravity_ms2": 1.35,
        "gravity_ratio": 0.138,
        "temp_c": -179,
        "day_duration": "15,9 dias terrestres",
        "year_duration": "15,9 dias terrestres",
        "curiosity": "Tem chuva, rios e lagos líquidos, mas não de água: são lagos de Metano e Etano líquidos!",
        "scifi_link": "A atmosfera é tão espessa e a gravidade tão baixa que um humano com asas de papelão conseguiria voar batendo os braços!"
    },
    "Urano": {
        "type": "Gigante de Gelo",
        "icon": "🌀",
        "image_url": get_img("uranus.jpg"),
        "diameter_km": 50724,
        "gravity_ms2": 8.69,
        "gravity_ratio": 0.89,
        "temp_c": -195,
        "day_duration": "17h 14min",
        "year_duration": "84 anos terrestres",
        "curiosity": "Gira 'deitado' de lado com inclinação de 98°, provavelmente devido a um impacto titânico no passado!",
        "scifi_link": "Possui uma cor azul-esverdeada brilhante provocada pela absorção de luz vermelha pelo gás metano em sua atmosfera."
    },
    "Netuno": {
        "type": "Gigante de Gelo (Planeta dos Ventos)",
        "icon": "💨",
        "image_url": get_img("neptune.jpg"),
        "diameter_km": 49244,
        "gravity_ms2": 11.15,
        "gravity_ratio": 1.14,
        "temp_c": -200,
        "day_duration": "16h 06min",
        "year_duration": "165 anos terrestres",
        "curiosity": "Possui os ventos mais violentos de todo o Sistema Solar, ultrapassando 2.100 km/h (mais rápidos que a velocidade do som)!",
        "scifi_link": "Foi descoberto através de cálculos puramente matemáticos antes de ser visto pelo telescópio!"
    },
    "Plutão": {
        "type": "Planeta Anão do Cinturão de Kuiper",
        "icon": "❄️",
        "image_url": get_img("pluto.jpg"),
        "diameter_km": 2376,
        "gravity_ms2": 0.62,
        "gravity_ratio": 0.063,
        "temp_c": -230,
        "day_duration": "6,4 dias terrestres",
        "year_duration": "248 anos terrestres",
        "curiosity": "Possui uma gigantesca geleira de nitrogênio em formato de coração chamada Tombaugh Regio!",
        "scifi_link": "Fotografado em detalhes estonteantes pela sonda New Horizons da NASA em 2015."
    },
    "Gargantua (Buraco Negro)": {
        "type": "Buraco Negro Supermassivo (Sci-Fi / Astrofísica)",
        "icon": "🕳️",
        "image_url": get_img("blackhole.jpg"),
        "diameter_km": 300000000,
        "gravity_ms2": 99999.0,
        "gravity_ratio": 10000.0,
        "temp_c": -273,
        "day_duration": "Singularidade",
        "year_duration": "Indefinido",
        "curiosity": "Concentra a massa de 100 milhões de sóis! Sua atração é tão violenta que o tempo ao seu redor desacelera drasticamente.",
        "scifi_link": "O buraco negro central do filme 'Interestelar', gerado com equações físicas reais por Kip Thorne (Nobel de Física)."
    }
}

DISTANCES_KM = {
    "Lua": 384400,
    "Marte (Ponto Mais Próximo)": 54600000,
    "Marte (Distância Média)": 225000000,
    "Júpiter (Distância Média)": 778000000,
    "Saturno (Distância Média)": 1430000000,
    "Netuno (Fronteira dos Planetas)": 4500000000,
    "Plutão (Cinturão de Kuiper)": 5900000000,
    "Próxima Centauri (Estrela Mais Próxima)": 40140000000000
}

SPEED_MODES = {
    "🚶 Caminhada Humana (5 km/h)": 5,
    "🚗 Carro de Corrida (200 km/h)": 200,
    "✈️ Avião a Jato Comercial (900 km/h)": 900,
    "🚀 Ônibus Espacial / ISS (28.000 km/h)": 28000,
    "⚡ Sonda New Horizons (58.000 km/h)": 58000,
    "☀️ Sonda Solar Parker (700.000 km/h)": 700000,
    "💡 Velocidade da Luz (1.079.252.848 km/h - 300.000 km/s)": 1079252848
}

JWST_HUBBLE_GALLERY = [
    {
        "title": "Pilares da Criação (Telescópio James Webb)",
        "telescope": "JWST (Infravermelho Próximo / NIRCam)",
        "image_url": get_img("pillars.jpg"),
        "description": "Colunas majestosas de poeira cósmica e gás hidrogênio na Nebulosa da Águia (a 6.500 anos-luz de nós), onde novas estrelas estão se acendendo agora!"
    },
    {
        "title": "Primeiro Registro Real de um Buraco Negro (M87*)",
        "telescope": "Event Horizon Telescope (EHT)",
        "image_url": get_img("blackhole_gallery.jpg"),
        "description": "A histórica primeira foto direta da sombra do horizonte de eventos de um buraco negro supermassivo no centro da galáxia Messier 87 (a 55 milhões de anos-luz)."
    },
    {
        "title": "Galáxia de Andrômeda (M31)",
        "telescope": "Observatórios Espaciais & Terrestres",
        "image_url": get_img("andromeda.jpg"),
        "description": "A galáxia espiral gigante mais próxima da nossa Via Láctea, contendo mais de 1 trilhão de estrelas a 2,5 milhões de anos-luz de distância."
    },
    {
        "title": "A Terra Vista da Apollo 17 (The Blue Marble)",
        "telescope": "Missão Apollo 17 da NASA (1972)",
        "image_url": get_img("earth_apollo.jpg"),
        "description": "A fotografia mais icônica de nosso lar no Cosmos: um oásis azul e branco flutuando no vácuo escuro do espaço."
    },
    {
        "title": "O Planeta Marte em Alta Resolução (Sonda OSIRIS)",
        "telescope": "Sonda Espacial Rosetta / OSIRIS",
        "image_url": get_img("mars_gallery.jpg"),
        "description": "O Planeta Vermelho em cores reais: suas calotas polares de gelo seco e crateras gigantescas que outrora abrigaram rios e lagos de água líquida."
    },
    {
        "title": "Júpiter e a Grande Mancha Vermelha",
        "telescope": "Telescópio Espacial Hubble (NASA/ESA)",
        "image_url": get_img("jupiter_gallery.jpg"),
        "description": "O rei dos planetas com suas faixas de nuvens turbulentas de amônia e a tempestade anticiclônica que ruge há centenas de anos."
    }
]

def render_observatory(user: dict, default_tool: str = None, *args, **kwargs):
    if not default_tool:
        default_tool = st.session_state.get("observatory_tool_default", "Atlas")
    
    t = str(default_tool).lower()
    
    # ------------------------------------------------------------------
    # FERRAMENTA 1: ATLAS PLANETÁRIO
    # ------------------------------------------------------------------
    if "atlas" in t:
        st.subheader("🪐 Atlas do Sistema Solar e Mundos Fascinantes")
        st.write("Clique em um astro para inspecionar seus dados físicos, imagens reais e conexões científicas:")
        
        selected_body = st.selectbox("Selecione um Corpo Celeste:", list(CELESTIAL_BODIES.keys()), index=3)
        body = CELESTIAL_BODIES[selected_body]
        
        col_img, col_data = st.columns([1, 1.4])
        
        with col_img:
            st.image(body["image_url"], caption=f"{body['icon']} {selected_body} ({body['type']})", use_container_width=True)
            
        with col_data:
            st.markdown(f"""
                <div class='cosmic-card'>
                    <div style='display: flex; align-items: center; justify-content: space-between;'>
                        <h2 style='margin: 0; color: #00d4ff;'>{body['icon']} {selected_body}</h2>
                        <span class='steam-tag physics'>{body['type']}</span>
                    </div>
                    <hr style='border-color: rgba(0,212,255,0.2); margin: 12px 0;'>
                    <p style='font-size: 0.95rem; color: #cbd5e1;'><strong>📏 Diâmetro Equatorial:</strong> {body['diameter_km']:,} km</p>
                    <p style='font-size: 0.95rem; color: #cbd5e1;'><strong>⚡ Aceleração da Gravidade:</strong> {body['gravity_ms2']} m/s² ({body['gravity_ratio']}x da Terra)</p>
                    <p style='font-size: 0.95rem; color: #cbd5e1;'><strong>🌡️ Temperatura Média:</strong> {body['temp_c']} °C</p>
                    <p style='font-size: 0.95rem; color: #cbd5e1;'><strong>⏱️ Duração do Dia:</strong> {body['day_duration']}</p>
                    <p style='font-size: 0.95rem; color: #cbd5e1;'><strong>📅 Duração do Ano:</strong> {body['year_duration']}</p>
                    <div style='background: rgba(0, 212, 255, 0.1); border-left: 3px solid #00d4ff; padding: 8px 12px; border-radius: 4px; margin-top: 10px;'>
                        <p style='margin: 0; color: #f1f5f9; font-size: 0.85rem;'>💡 <strong>Fato Curioso:</strong> {body['curiosity']}</p>
                    </div>
                    <div style='background: rgba(157, 78, 221, 0.15); border-left: 3px solid #9d4edd; padding: 8px 12px; border-radius: 4px; margin-top: 8px;'>
                        <p style='margin: 0; color: #f1f5f9; font-size: 0.85rem;'>🎬 <strong>Conexão Científica / Sci-Fi:</strong> {body['scifi_link']}</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
        st.markdown("---")
        st.markdown("### 📊 Comparação Interativa de Tamanhos dos Mundos")
        
        df_bodies = pd.DataFrame([
            {"Corpo": k, "Diâmetro (km)": v["diameter_km"], "Tipo": v["type"]}
            for k, v in CELESTIAL_BODIES.items()
            if k != "Gargantua (Buraco Negro)"
        ]).sort_values("Diâmetro (km)", ascending=True)
        
        fig_size = px.bar(
            df_bodies,
            x="Diâmetro (km)",
            y="Corpo",
            orientation="h",
            color="Diâmetro (km)",
            color_continuous_scale="Viridis",
            title="Escala de Diâmetro dos Mundos do Sistema Solar (km)"
        )
        fig_size.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(19, 23, 43, 0.6)",
            font=dict(color="#cbd5e1"),
            height=450
        )
        st.plotly_chart(fig_size, use_container_width=True)

    # ----------------------------------------------------
    # FERRAMENTA 2: BALANÇA INTERPLANETÁRIA
    # ----------------------------------------------------
    elif "balan" in t or "balance" in t:
        st.subheader("⚖️ Balança Gravitacional Interplanetária")
        st.write("A sua massa em quilogramas (kg) é constante em qualquer lugar do cosmos, mas o seu **PESO (Força Gravitacional)** muda drasticamente!")
        
        user_weight = st.number_input("Digite sua massa na Terra (kg):", min_value=10.0, max_value=250.0, value=50.0, step=1.0)
        
        cols = st.columns(4)
        for i, (name, b_info) in enumerate(CELESTIAL_BODIES.items()):
            equiv_weight = user_weight * b_info["gravity_ratio"]
            target_col = cols[i % 4]
            
            with target_col:
                st.markdown(f"""
                    <div style='background: rgba(19, 23, 43, 0.7); border: 1px solid rgba(0,212,255,0.25); border-radius: 12px; padding: 12px; text-align: center; margin-bottom: 12px;'>
                        <span style='font-size: 2rem;'>{b_info['icon']}</span>
                        <h4 style='color: #00d4ff; margin: 4px 0;'>{name}</h4>
                        <p style='color: #ffd166; font-size: 1.2rem; font-weight: 800; margin: 0;'>{equiv_weight:.1f} kgf</p>
                        <p style='color: #94a3b8; font-size: 0.75rem; margin: 0;'>Gravidade: {b_info['gravity_ratio']}x</p>
                    </div>
                """, unsafe_allow_html=True)
                
        if st.button("🌟 Registrar Experimento de Gravidade (+15 XP)"):
            add_xp(user["id"], 15)
            unlock_badge(user["id"], "observatory_explorer")
            st.success("Experimento registrado com sucesso no seu Diário de Bordo! (+15 XP)")

    # ----------------------------------------------------
    # FERRAMENTA 3: CALCULADORA DE VIAGEM ESPACIAL
    # ----------------------------------------------------
    elif "calc" in t:
        st.subheader("🚀 Calculadora de Tempo de Viagem Interplanetária")
        st.write("Descubra quanto tempo levaria para alcançar as fronteiras do espaço com diferentes veículos da humanidade:")
        
        col_calc1, col_calc2 = st.columns(2)
        with col_calc1:
            dest = st.selectbox("Escolha seu Destino:", list(DISTANCES_KM.keys()))
            dist_km = DISTANCES_KM[dest]
            st.info(f"📏 Distância em linha reta: **{dist_km:,.0f} km**".replace(",", "."))
            
        with col_calc2:
            veh = st.selectbox("Escolha seu Meio de Transporte:", list(SPEED_MODES.keys()), index=3)
            spd = SPEED_MODES[veh]
            st.info(f"⚡ Velocidade de deslocamento: **{spd:,.0f} km/h**".replace(",", "."))
            
        hours = dist_km / spd
        days = hours / 24
        years = days / 365.25
        
        st.markdown(f"""
            <div class='cosmic-hero' style='background: linear-gradient(135deg, rgba(6,30,40,0.9), rgba(16,20,47,0.9)); border: 1px solid #06d6a0; margin-top: 15px;'>
                <h3 style='color: #06d6a0; margin: 0;'>⏱️ Tempo Estimado de Viagem:</h3>
                <h1 style='color: #ffffff; margin: 10px 0;'>
                    {f"{years:,.1f} ANOS".replace(",", ".") if years >= 1.0 else (f"{days:,.1f} DIAS".replace(",", ".") if days >= 1.0 else f"{hours:,.1f} HORAS".replace(",", "."))}
                </h1>
                <p style='color: #cbd5e1; margin: 0;'>
                    Equivale a exatamente <strong>{hours:,.0f} horas</strong> ({days:,.1f} dias terrestres) viajando ininterruptamente!
                </p>
            </div>
        """, unsafe_allow_html=True)

    # ----------------------------------------------------
    # FERRAMENTA 4: GALERIA JAMES WEBB & HUBBLE (ALTA RESOLUÇÃO)
    # ----------------------------------------------------
    elif "galeria" in t or "gallery" in t:
        st.subheader("📸 Galeria Cósmica em Alta Resolução (NASA, JWST & Hubble)")
        st.write("Imagens reais captadas pelos maiores observatórios e sondas da história da humanidade:")
        
        c_gal1, c_gal2 = st.columns(2)
        
        for idx, item in enumerate(JWST_HUBBLE_GALLERY):
            target_col = c_gal1 if idx % 2 == 0 else c_gal2
            with target_col:
                with st.container():
                    st.image(item["image_url"], caption=item["title"], use_container_width=True)
                    st.markdown(f"""
                        <div style='background: rgba(19, 23, 43, 0.75); border-left: 3px solid #00d4ff; padding: 10px 14px; border-radius: 8px; margin-bottom: 20px;'>
                            <span class='steam-tag' style='background: rgba(0,212,255,0.15); color: #00d4ff; font-size: 0.75rem;'>🔭 {item['telescope']}</span>
                            <h4 style='color: #f1f5f9; margin: 6px 0 4px 0;'>{item['title']}</h4>
                            <p style='color: #cbd5e1; font-size: 0.85rem; margin: 0;'>{item['description']}</p>
                        </div>
                    """, unsafe_allow_html=True)

    # ----------------------------------------------------
    # TAB 5: APOD (NASA ASTRONOMY PICTURE OF THE DAY)
    # ----------------------------------------------------
    else:
        st.subheader("🌠 Imagem Astronômica do Dia (NASA APOD)")
        st.write("A cada 24 horas, a NASA publica uma fotografia deslumbrante do cosmos acompanhada por uma explicação escrita por astrofísicos:")
        
        if st.button("🛰️ Conectar ao Feed Oficial da NASA APOD"):
            try:
                with st.spinner("Sintonizando telescópios da NASA..."):
                    res = requests.get("https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY", timeout=6)
                    if res.status_code == 200:
                        data = res.json()
                        st.markdown(f"### {data.get('title', 'Maravilha Cósmica')}")
                        st.caption(f"📅 Data da Captura: {data.get('date', 'Hoje')}")
                        
                        media_type = data.get("media_type", "image")
                        if media_type == "image":
                            st.image(data.get("url"), caption=data.get("title"), use_container_width=True)
                        else:
                            st.video(data.get("url"))
                            
                        st.markdown(f"""
                            <div style='background: rgba(19, 23, 43, 0.7); border-left: 4px solid #00d4ff; padding: 14px; border-radius: 8px; margin-top: 15px;'>
                                <h4 style='color: #00d4ff; margin-top: 0;'>📖 Explicação Científica Oficial (NASA):</h4>
                                <p style='color: #e2e8f0; font-size: 0.9rem; line-height: 1.5;'>{data.get('explanation', 'Sem descrição disponível.')}</p>
                            </div>
                        """, unsafe_allow_html=True)
                        add_xp(user["id"], 20)
                    else:
                        st.info("O feed da NASA está em manutenção de rotina no momento. Aproveite a Galeria James Webb na aba ao lado!")
            except Exception:
                st.info("Conexão ao feed da NASA indisponível no modo offline. Explore as imagens em alta resolução na aba **📸 Galeria James Webb & Hubble**!")
