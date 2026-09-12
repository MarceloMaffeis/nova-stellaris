"""
Nova Stellaris - Módulo Observatório do Cosmos
Atlas Celeste, Balança Planetária, Calculadora de Velocidade e Imagem Astronômica do Dia.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import requests
from database import add_xp, unlock_badge

CELESTIAL_BODIES = {
    "Sol": {
        "type": "Estrela (Anã Amarela)",
        "icon": "☀️",
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
        "diameter_km": 5149,
        "gravity_ms2": 1.35,
        "gravity_ratio": 0.138,
        "temp_c": -179,
        "day_duration": "15,9 dias terrestres",
        "year_duration": "15,9 dias terrestres",
        "curiosity": "Tem chuva, rios e lagos líquidos, mas não de água: são lagos de Metano e Etano líquidos!",
        "scifi_link": "A atmosfera é tão espessa e a gravidade tão baixa que um humano com asas de papelão conseguiria voar batendo os braços!"
    },
    "Gargantua (Buraco Negro)": {
        "type": "Buraco Negro Supermassivo (Sci-Fi)",
        "icon": "🕳️",
        "diameter_km": 300000000,
        "gravity_ms2": 99999.0,
        "gravity_ratio": 10000.0,
        "temp_c": -273,
        "day_duration": "Singularidade",
        "year_duration": "Indefinido",
        "curiosity": "Concentra a massa de 100 milhões de sóis! Sua atração é tão violenta que o tempo ao seu redor desacelera drasticamente.",
        "scifi_link": "O buraco negro central do filme 'Interestelar', gerado com equações físicas reais por Kip Thorne."
    }
}

DISTANCES_KM = {
    "Lua": 384400,
    "Marte (Ponto Mais Próximo)": 54600000,
    "Marte (Ponto Mais Distante)": 401000000,
    "Júpiter": 628700000,
    "Saturno": 1275000000,
    "Plutão": 5900000000,
    "Próxima Centauri (Estrela mais próxima)": 40140000000000,  # ~4.24 anos luz
    "Centro da Via Láctea": 245000000000000000,                # ~26.000 anos luz
}

SPEEDS_KMH = {
    "🚶 Caminhada Humana (5 km/h)": 5,
    "🚗 Carro em Rodovia (100 km/h)": 100,
    "✈️ Avião a Jato Comercial (900 km/h)": 900,
    "🚀 Foguete Apollo 11 (39.000 km/h)": 39000,
    "🛰️ Sonda New Horizons (58.500 km/h)": 58500,
    "⚡ 10% da Velocidade da Luz (108.000.000 km/h)": 108000000,
    "💫 Velocidade da Luz (1.080.000.000 km/h)": 1080000000
}

def render_observatory(user: dict):
    st.markdown("""
        <div class='cosmic-hero'>
            <h1 style='color: #00d4ff; margin-bottom: 5px;'>🌌 Observatório do Cosmos & Escala Espacial</h1>
            <p style='color: #94a3b8; font-size: 1.1rem; margin: 0;'>
                Explore os corpos celestes, calcule seu peso em outros mundos e viaje pelas distâncias do universo!
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "🪐 Atlas dos Mundos",
        "⚖️ Balança Planetária (Física & Peso)",
        "🚀 Calculadora de Viagem Cósmica",
        "📸 Foto Astronômica do Dia (APOD)"
    ])
    
    # ----------------------------------------------------
    # TAB 1: ATLAS DOS MUNDOS
    # ----------------------------------------------------
    with tab1:
        st.subheader("🪐 Enciclopédia Interativa do Sistema Solar & Além")
        
        selected_body = st.selectbox(
            "Selecione um corpo celeste para analisar:",
            list(CELESTIAL_BODIES.keys()),
            index=5 # Marte como default
        )
        
        body_data = CELESTIAL_BODIES[selected_body]
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown(f"""
                <div class='cosmic-card'>
                    <h2 style='color: #00d4ff;'>{body_data['icon']} {selected_body}</h2>
                    <p><strong>Classificação:</strong> <span style='color: #ffd166;'>{body_data['type']}</span></p>
                    <hr style='border-color: rgba(0,212,255,0.2);'>
                    <p>📏 <strong>Diâmetro:</strong> {body_data['diameter_km']:,} km</p>
                    <p>⚖️ <strong>Gravidade:</strong> {body_data['gravity_ms2']} m/s² ({body_data['gravity_ratio']}x a da Terra)</p>
                    <p>🌡️ <strong>Temperatura Média:</strong> {body_data['temp_c']} °C</p>
                    <p>🔄 <strong>Duração do Dia:</strong> {body_data['day_duration']}</p>
                    <p>📅 <strong>Duração do Ano / Órbita:</strong> {body_data['year_duration']}</p>
                </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown(f"""
                <div class='cosmic-card' style='border-left: 4px solid #9d4edd;'>
                    <h3 style='color: #9d4edd;'>💡 Fato Científico Curioso</h3>
                    <p style='color: #e2e8f0;'>{body_data['curiosity']}</p>
                    
                    <h3 style='color: #06d6a0; margin-top: 20px;'>🎬 Conexão Sci-Fi & Filmes</h3>
                    <p style='color: #e2e8f0;'>{body_data['scifi_link']}</p>
                </div>
            """, unsafe_allow_html=True)
            
        # Gráfico Comparativo de Tamanhos
        st.markdown("### 📊 Comparador de Diâmetros Planetários (Escala)")
        planets_only = {k: v for k, v in CELESTIAL_BODIES.items() if k not in ["Sol", "Gargantua (Buraco Negro)"]}
        df_planets = pd.DataFrame([
            {"Nome": k, "Diâmetro (km)": v["diameter_km"], "Tipo": v["type"]}
            for k, v in planets_only.items()
        ])
        
        fig = px.bar(
            df_planets,
            x="Nome",
            y="Diâmetro (km)",
            color="Diâmetro (km)",
            color_continuous_scale="Viridis",
            title="Comparação de Tamanho dos Planetas e Luas (em km)"
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(19, 23, 43, 0.6)",
            font=dict(color="#f1f5f9"),
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)

    # ----------------------------------------------------
    # TAB 2: BALANÇA PLANETÁRIA
    # ----------------------------------------------------
    with tab2:
        st.subheader("⚖️ Quanto você pesaria em outros mundos?")
        st.markdown("""
            A sua **Massa** (a quantidade de matéria no seu corpo) é a mesma em qualquer lugar do universo! 
            Mas o seu **Peso** é uma força: **$P = m \cdot g$** (Peso = Massa × Gravidade local).
        """)
        
        user_weight = st.number_input(
            "Digite seu peso na Terra (em kg):",
            min_value=10.0,
            max_value=150.0,
            value=45.0,
            step=1.0
        )
        
        col_w1, col_w2, col_w3 = st.columns(3)
        
        # Rastrear visualizações na sessão
        if "tested_planets" not in st.session_state:
            st.session_state.tested_planets = set()
            
        cards_data = [
            ("Lua", "🌕", CELESTIAL_BODIES["Lua"]["gravity_ratio"], "#38bdf8", "Você daria pulos gigantes de astronauta!"),
            ("Marte", "🔴", CELESTIAL_BODIES["Marte"]["gravity_ratio"], "#fb923c", "Carregar mochilas pesadas é muito fácil aqui!"),
            ("Júpiter", "🪐", CELESTIAL_BODIES["Júpiter"]["gravity_ratio"], "#f43f5e", "Você mal conseguiria ficar em pé, pareceria chumbo!"),
            ("Vênus", "🟡", CELESTIAL_BODIES["Vênus"]["gravity_ratio"], "#eab308", "Quase idêntico ao peso na Terra."),
            ("Europa", "🧊", CELESTIAL_BODIES["Europa (Lua de Júpiter)"]["gravity_ratio"], "#06d6a0", "Flutuação suave sobre o manto de gelo!"),
            ("Sol", "☀️", CELESTIAL_BODIES["Sol"]["gravity_ratio"], "#f59e0b", "Esmagamento instantâneo se pudesse pisar lá.")
        ]
        
        for i, (name, icon, ratio, color, tip) in enumerate(cards_data):
            calculated_weight = round(user_weight * ratio, 1)
            st.session_state.tested_planets.add(name)
            
            target_col = [col_w1, col_w2, col_w3][i % 3]
            with target_col:
                st.markdown(f"""
                    <div class='cosmic-card' style='border-top: 4px solid {color}; text-align: center;'>
                        <h3 style='margin: 0;'>{icon} {name}</h3>
                        <p style='color: #94a3b8; font-size: 0.9rem;'>Gravidade: {ratio}x Terra</p>
                        <h1 style='color: {color}; font-size: 2.4rem; margin: 10px 0;'>{calculated_weight} <span style='font-size: 1.2rem;'>kg</span></h1>
                        <p style='font-size: 0.85rem; color: #cbd5e1;'>{tip}</p>
                    </div>
                """, unsafe_allow_html=True)
                
        # Conquista de Gravidade
        if len(st.session_state.tested_planets) >= 5:
            if unlock_badge(user["id"], "gravity_explorer"):
                add_xp(user["id"], 100)
                st.balloons()
                st.success("🎉 **Nova Conquista Desbloqueada:** ⚖️ Mestre da Gravidade! (+100 XP)")

    # ----------------------------------------------------
    # TAB 3: CALCULADORA DE VIAGEM CÓSMICA
    # ----------------------------------------------------
    with tab3:
        st.subheader("🚀 Calculadora de Distâncias e Tempo de Viagem Espacial")
        st.markdown("""
            O espaço é incomensuravelmente gigante! Veja quanto tempo levaria para viajar da Terra até diferentes destinos usando vários veículos.
        """)
        
        c_dest, c_speed = st.columns(2)
        with c_dest:
            chosen_dest = st.selectbox("Selecione o Destino:", list(DISTANCES_KM.keys()), index=1)
        with c_speed:
            chosen_speed_label = st.selectbox("Selecione a Velocidade:", list(SPEEDS_KMH.keys()), index=3)
            
        dist_km = DISTANCES_KM[chosen_dest]
        speed_kmh = SPEEDS_KMH[chosen_speed_label]
        
        hours = dist_km / speed_kmh
        days = hours / 24
        years = days / 365.25
        
        st.markdown(f"""
            <div class='cosmic-card' style='background: linear-gradient(135deg, rgba(16,20,47,0.9), rgba(30,16,60,0.9)); border: 1px solid #00d4ff;'>
                <h3 style='color: #00d4ff;'>🛰️ Relatório de Voo: Terra ➔ {chosen_dest}</h3>
                <p>📍 <strong>Distância Total:</strong> {dist_km:,.0f} km (<span style='color: #f72585;'>{dist_km:.2e} km em Notação Científica</span>)</p>
                <p>⚡ <strong>Velocidade de Cruzeiro:</strong> {speed_kmh:,.0f} km/h</p>
                <hr style='border-color: rgba(255,255,255,0.1);'>
                <h2 style='color: #ffd166; margin-top: 10px;'>⏱️ Tempo de Viagem Estimado:</h2>
        """, unsafe_allow_html=True)
        
        if years >= 1.0:
            st.markdown(f"<h1 style='color: #06d6a0;'>{years:,.1f} ANOS terrestres</h1>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: #94a3b8;'>({days:,.0f} dias ou {hours:,.0f} horas)</p>", unsafe_allow_html=True)
        elif days >= 1.0:
            st.markdown(f"<h1 style='color: #06d6a0;'>{days:,.1f} DIAS terrestres</h1>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: #94a3b8;'>({hours:,.1f} horas)</p>", unsafe_allow_html=True)
        else:
            st.markdown(f"<h1 style='color: #06d6a0;'>{hours:,.2f} HORAS ({hours*60:,.1f} minutos)</h1>", unsafe_allow_html=True)
            
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.info("💡 **Dica Científica:** A luz do Sol leva cerca de **8 minutos e 20 segundos** para viajar 150 milhões de km e chegar aos nossos olhos na Terra!")

    # ----------------------------------------------------
    # TAB 4: APOD (FOTO ASTRONÔMICA DO DIA)
    # ----------------------------------------------------
    with tab4:
        st.subheader("📸 Imagem Astronômica do Dia (NASA APOD)")
        st.markdown("Imagens reais capturadas pelos telescópios espaciais James Webb, Hubble e observatórios mundiais.")
        
        try:
            # Tentar requisição NASA APOD
            res = requests.get("https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY", timeout=4)
            if res.status_code == 200:
                apod_data = res.json()
                st.markdown(f"### {apod_data.get('title', 'Maravilha Cósmica')}")
                st.markdown(f"*Data: {apod_data.get('date', '')}*")
                
                if apod_data.get("media_type") == "image":
                    st.image(apod_data.get("url"), use_container_width=True, caption=apod_data.get("title"))
                else:
                    st.video(apod_data.get("url"))
                    
                st.write(apod_data.get("explanation", ""))
            else:
                render_fallback_apod()
        except Exception:
            render_fallback_apod()

def render_fallback_apod():
    st.markdown("### 🌌 Os Pilares da Criação (Telescópio Espacial James Webb)")
    st.image(
        "https://images-assets.nasa.gov/image/PIA25432/PIA25432~orig.jpg",
        caption="Os Pilares da Criação na Nebulosa da Águia (M16) em luz infravermelha próxima (NASA/ESA/CSA/STScI)",
        use_container_width=True
    )
    st.markdown("""
        <div class='cosmic-card'>
            <h4 style='color: #00d4ff;'>O que estamos vendo aqui?</h4>
            <p>
                Esta é uma das imagens mais famosas de toda a astronomia! Localizados a 6.500 anos-luz da Terra na 
                <strong>Nebulosa da Águia</strong>, estes imensos 'dedos' são gigantescas colunas de gás e poeira interestelar.
            </p>
            <p>
                🧪 <strong>Química & Física:</strong> Dentro dessas nuvens densas de Hidrogênio, a gravidade está colapsando o gás, 
                dando início às reações de fusão nuclear e criando <strong>novas estrelas e sistemas solares</strong> bem diante dos nossos olhos!
            </p>
        </div>
    """, unsafe_allow_html=True)

