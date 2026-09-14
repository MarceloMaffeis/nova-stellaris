"""
Nova Stellaris - Academia STEAM: Trilhas de Conhecimento Graduadas
Cobre Matemática, Física, Química e Tecnologia/Computação aplicadas à Astronomia.
Níveis: Cadete (6º ano / Básico), Explorador (7º-9º ano / Intermediário) e Astrofísico (Avançado).
"""

import streamlit as st
import math
from database import add_xp, unlock_badge

def render_steam_academy(user: dict):
    st.markdown("""
        <div class='cosmic-hero' style='background: linear-gradient(135deg, rgba(20,30,60,0.95), rgba(16,20,47,0.95)); border: 1px solid #00d4ff;'>
            <h1 style='color: #00d4ff; margin-bottom: 5px;'>🎓 Academia Cósmica STEAM — Trilhas do Conhecimento</h1>
            <p style='color: #cbd5e1; font-size: 1.1rem; margin: 0;'>
                Aprenda a ciência real do Universo: da matemática das órbitas à relatividade e à química das supernovas!
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    tab_math, tab_phys, tab_chem, tab_tech = st.tabs([
        "📐 Matemática Espacial",
        "⚛️ Física Cósmica",
        "🧪 Química Estelar",
        "💻 Tecnologia & Computação"
    ])
    
    with tab_math:
        _render_math_track(user)
        
    with tab_phys:
        _render_physics_track(user)
        
    with tab_chem:
        _render_chemistry_track(user)
        
    with tab_tech:
        _render_tech_track(user)


# ==============================================================================
# 📐 1. TRILHA DE MATEMÁTICA ESPACIAL
# ==============================================================================
def _render_math_track(user: dict):
    st.markdown("## 📐 Matemática Espacial & Geometria do Cosmos")
    st.write("Escolha seu nível de treinamento para começar a explorar os cálculos que governam o Universo:")
    
    level = st.radio(
        "Selecione o Nível de Dificuldade:",
        [
            "🟢 Nível 1: Cadete Espacial (Básico / 6º Ano)",
            "🟡 Nível 2: Explorador Orbital (Intermediário / 7º-9º Ano)",
            "🔴 Nível 3: Astrofísico de Vanguarda (Avançado / Ensino Médio)"
        ],
        key="math_level_select",
        horizontal=True
    )
    
    st.markdown("---")
    
    if "Nível 1" in level:
        st.markdown("""
            <div class='level-badge cadet'>🟢 NÍVEL 1 — CADETE ESPACIAL</div>
            <h3 style='color: #4ade80;'>Proporções Planetárias, Diâmetros e Unidades Astronômicas</h3>
        """, unsafe_allow_html=True)
        
        st.markdown(r"""
        ### 📖 1. Teoria & Fórmulas
        No espaço, as distâncias em quilômetros são tão gigantescas que usamos **Unidades Astronômicas (UA)**:
        - **1 UA (Unidade Astronômica):** Distância média da Terra ao Sol $\approx 150.000.000\text{ km}$ ($150\text{ milhões de km}$).
        - **Proporção de Tamanhos:** A Terra tem diâmetro de $\approx 12.742\text{ km}$. Júpiter é $\approx 11$ vezes maior ($\approx 140.000\text{ km}$), e o Sol é $\approx 109$ vezes maior!
        
        #### 💡 Fórmula da Escala de Maquetes:
        $$\text{Tamanho na Maquete (cm)} = \frac{\text{Diâmetro Real (km)}}{\text{Fator de Escala (km/cm)}}$$
        """)
        
        # Simulador de Maquete
        st.markdown("### 🧮 2. Simulador Interativo: Criador de Maquete Planetária")
        st.write("Quer criar uma maquete em escala do Sistema Solar na sua casa ou escola? Calcule o tamanho dos planetas:")
        
        scale_choice = st.selectbox(
            "Selecione o Diâmetro da Terra na sua maquete:",
            ["1 cm (Esferinha de gude)", "5 cm (Bolinha de tênis)", "10 cm (Bola de futebol)", "20 cm (Bola grande)"],
            key="math_l1_scale"
        )
        earth_cm = {"1 cm (Esferinha de gude)": 1.0, "5 cm (Bolinha de tênis)": 5.0, "10 cm (Bola de futebol)": 10.0, "20 cm (Bola grande)": 20.0}[scale_choice]
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("🌍 Terra", f"{earth_cm:.1f} cm", "Base da Escala")
        col2.metric("🌕 Lua", f"{(earth_cm * 0.27):.2f} cm", "0,27x Terra")
        col3.metric("🔴 Marte", f"{(earth_cm * 0.53):.2f} cm", "0,53x Terra")
        col4.metric("🪐 Júpiter", f"{(earth_cm * 11.2):.1f} cm", "11,2x Terra!")
        
        st.info(f"☀️ **Curiosidade:** Na sua maquete, o **Sol** teria nada menos que **{(earth_cm * 109.2) / 100:.2f} metros** de diâmetro!")
        
        # Exercício Interativo
        st.markdown("### 📝 3. Exercício Prático com Feedback Imediato")
        with st.container():
            st.markdown("""
                <div class='exercise-card'>
                    <h4 style='color: #ffd166; margin-top:0;'>Desafio 1: Viagem a Marte em UA</h4>
                    <p>Marte orbita o Sol a uma distância média de <strong>1,52 UA</strong>. Sabendo que 1 UA = 150 milhões de km, qual é a distância média de Marte ao Sol em quilômetros?</p>
                </div>
            """, unsafe_allow_html=True)
            
            ans_m1 = st.radio(
                "Escolha a resposta correta:",
                [
                    "A) 152.000.000 km",
                    "B) 228.000.000 km (228 milhões de km)",
                    "C) 304.000.000 km",
                    "D) 75.000.000 km"
                ],
                key="math_ex1"
            )
            
            if st.button("Verificar Resposta (Desafio 1)", key="math_btn1"):
                if "B)" in ans_m1:
                    st.success("🎉 **Correto!** $1,52 \\times 150.000.000\\text{ km} = 228.000.000\\text{ km}$. Você ganhou **+25 XP**!")
                    add_xp(user["id"], 25)
                else:
                    st.error("❌ Tente novamente! Dica: Multiplique 1,52 por 150 e adicione os 6 zeros dos milhões.")
                    
    elif "Nível 2" in level:
        st.markdown("""
            <div class='level-badge explorer'>🟡 NÍVEL 2 — EXPLORADOR ORBITAL</div>
            <h3 style='color: #fbbf24;'>Notação Científica, Velocidade da Luz e Atraso de Sinais</h3>
        """, unsafe_allow_html=True)
        
        st.markdown(r"""
        ### 📖 1. Teoria & Fórmulas
        Os astrônomos utilizam a **Notação Científica** para escrever números com muitos zeros no formato $N \times 10^n$:
        - Distância Terra-Sol: $150.000.000\text{ km} = 1,5 \times 10^8\text{ km}$.
        - Massa do Sol: $1.989.000.000.000.000.000.000.000.000.000\text{ kg} = 1,989 \times 10^{30}\text{ kg}$.
        - **Velocidade da Luz no Vácuo ($c$):** $300.000\text{ km/s} = 3 \times 10^5\text{ km/s}$.
        
        #### 📡 Fórmula do Atraso de Comunicação de Rádio:
        $$\Delta t = \frac{\text{Distância } (d)}{\text{Velocidade da Luz } (c)}$$
        """)
        
        # Calculadora de Sinal de Rádio
        st.markdown("### 🧮 2. Simulador: Tempo de Sinal de Rádio com as Sondas Espaciais")
        dest = st.selectbox("Escolha o destino da sonda:", ["Lua (384.400 km)", "Sol (150.000.000 km)", "Marte mais próximo (55.000.000 km)", "Marte mais distante (400.000.000 km)", "Sonda Voyager 1 (24.000.000.000 km)"], key="math_l2_dest")
        
        dists = {
            "Lua (384.400 km)": 384400,
            "Sol (150.000.000 km)": 150000000,
            "Marte mais próximo (55.000.000 km)": 55000000,
            "Marte mais distante (400.000.000 km)": 400000000,
            "Sonda Voyager 1 (24.000.000.000 km)": 24000000000
        }
        
        dist_km = dists[dest]
        delay_sec = dist_km / 300000.0
        
        st.markdown(f"""
            <div class='formula-box'>
                <p>📍 <strong>Distância em Notação:</strong> {dist_km:.3e} km</p>
                <p>⏱️ <strong>Tempo para o sinal de rádio ir (velocidade $c$):</strong></p>
                <h3 style='color: #00d4ff;'>{delay_sec:.2f} segundos ({delay_sec/60:.2f} minutos / {delay_sec/3600:.2f} horas)</h3>
                <p style='color: #94a3b8; font-size: 0.85rem;'>É por isso que os astronautas em Marte ou rovers não podem ser pilotados por controle remoto em tempo real!</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Exercício Interativo
        st.markdown("### 📝 3. Exercício de Notação e Velocidade da Luz")
        with st.container():
            st.markdown(r"""
                <div class='exercise-card'>
                    <h4 style='color: #ffd166; margin-top:0;'>Desafio 2: Luz Solar na Terra</h4>
                    <p>Sabendo que a distância da Terra ao Sol é de $150.000.000\text{ km}$ e a luz viaja a $300.000\text{ km/s}$, quantos minutos a luz do Sol leva para chegar até nossos olhos?</p>
                </div>
            """, unsafe_allow_html=True)
            
            ans_m2 = st.radio(
                "Escolha a alternativa:",
                [
                    "A) 500 minutos",
                    "B) 8 minutos e 20 segundos (500 segundos)",
                    "C) 1 hora e 15 minutos",
                    "D) É instantâneo (0 segundos)"
                ],
                key="math_ex2"
            )
            
            if st.button("Verificar Resposta (Desafio 2)", key="math_btn2"):
                if "B)" in ans_m2:
                    st.success("🎉 **Perfeito!** $t = \\frac{150.000.000}{300.000} = 500\\text{ s} = 8\\text{ min e } 20\\text{ s}$. Você ganhou **+30 XP**!")
                    add_xp(user["id"], 30)
                else:
                    st.error("❌ Tente novamente! Divida 150.000.000 por 300.000 para achar os segundos e depois converta para minutos.")
                    
    else: # Nível 3
        st.markdown("""
            <div class='level-badge astrophysicist'>🔴 NÍVEL 3 — ASTROFÍSICO DE VANGUARDA</div>
            <h3 style='color: #c084fc;'>Leis de Kepler, Elipses Orbitais e Paralaxe Estelar</h3>
        """, unsafe_allow_html=True)
        
        st.markdown(r"""
        ### 📖 1. Teoria & Fórmulas Avançadas
        Johannes Kepler descobriu que os planetas não orbitam em círculos perfeitos, mas em **elipses** com o Sol em um dos focos!
        
        #### 🪐 3ª Lei de Kepler (Lei dos Períodos):
        $$T^2 = a^3$$
        - $T$: Período orbital em **anos terrestres**.
        - $a$: Raio médio da órbita (semi-eixo maior) em **Unidades Astronômicas (UA)**.
        
        #### 📐 Paralaxe Estelar ($d$):
        Para medir a distância até estrelas próximas, medimos a mudança de ângulo aparente ($p$ em segundos de arco) quando a Terra viaja ao redor do Sol:
        $$d = \frac{1}{p} \quad (\text{em Parsecs, onde } 1\text{ pc} \approx 3,26\text{ anos-luz})$$
        """)
        
        # Simulador de Kepler
        st.markdown("### 🧮 2. Simulador da 3ª Lei de Kepler: Calcule o Ano de Qualquer Planeta!")
        a_input = st.slider("Distância média do planeta ao Sol ($a$ em UA):", min_value=0.2, max_value=40.0, value=5.2, step=0.1, key="kepler_a_slider")
        
        t_calculated = math.sqrt(a_input ** 3)
        
        st.markdown(f"""
            <div class='formula-box'>
                <p>🔭 Para uma distância orbital de <strong>{a_input} UA</strong>:</p>
                <p>$$T = \\sqrt{{a^3}} = \\sqrt{{{a_input:.1f}^3}} = \\sqrt{{{a_input**3:.2f}}}$$</p>
                <h3 style='color: #a855f7;'>⏱️ Período Orbital: {t_calculated:.2f} Anos Terrestres</h3>
                <p style='color: #94a3b8; font-size: 0.85rem;'>Para Júpiter ($a \\approx 5,2\\text{{ UA}}$), o ano dura quase 12 anos terrestres!</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Exercício
        st.markdown("### 📝 3. Desafio Astrofísico")
        with st.container():
            st.markdown(r"""
                <div class='exercise-card'>
                    <h4 style='color: #ffd166; margin-top:0;'>Desafio 3: O Período de um Asteroide</h4>
                    <p>Um asteroide no cinturão entre Marte e Júpiter tem um semi-eixo maior $a = 4\text{ UA}$. Usando $T^2 = a^3$, quantos anos terrestres ele leva para dar uma volta completa ao redor do Sol?</p>
                </div>
            """, unsafe_allow_html=True)
            
            ans_m3 = st.radio(
                "Escolha a resposta correta:",
                [
                    "A) 4 anos",
                    "B) 8 anos ($T = \\sqrt{4^3} = \\sqrt{64} = 8$)",
                    "C) 16 anos",
                    "D) 64 anos"
                ],
                key="math_ex3"
            )
            
            if st.button("Validar Desafio Astrofísico", key="math_btn3"):
                if "B)" in ans_m3:
                    st.success("🎉 **Brilhante!** $4^3 = 64$ e $\\sqrt{64} = 8\\text{ anos}$. Você ganhou **+40 XP** e desbloqueou a insígnia da Academia!")
                    add_xp(user["id"], 40)
                    unlock_badge(user["id"], "steam_math_master")
                else:
                    st.error("❌ Dica: Faça 4 x 4 x 4 = 64. Em seguida tire a raiz quadrada de 64!")


# ==============================================================================
# ⚛️ 2. TRILHA DE FÍSICA CÓSMICA
# ==============================================================================
def _render_physics_track(user: dict):
    st.markdown("## ⚛️ Física Cósmica: Gravitação, Foguetes & Relatividade")
    
    level = st.radio(
        "Selecione o Nível de Dificuldade:",
        [
            "🟢 Nível 1: Cadete Espacial (Básico / 6º Ano)",
            "🟡 Nível 2: Explorador Orbital (Intermediário / 7º-9º Ano)",
            "🔴 Nível 3: Astrofísico de Vanguarda (Avançado / Ensino Médio)"
        ],
        key="phys_level_select",
        horizontal=True
    )
    
    st.markdown("---")
    
    if "Nível 1" in level:
        st.markdown("""
            <div class='level-badge cadet'>🟢 NÍVEL 1 — CADETE ESPACIAL</div>
            <h3 style='color: #4ade80;'>Massa vs Peso, Gravidade nos Mundos e Eclipses</h3>
        """, unsafe_allow_html=True)
        
        st.markdown(r"""
        ### 📖 1. Teoria & Fórmulas Fundamentais
        Muitas pessoas confundem **Massa** com **Peso**, mas na física eles são muito diferentes:
        - **Massa ($m$):** É a quantidade de matéria de um corpo, medida em **quilogramas ($kg$)**. Ela **nunca muda**, esteja você na Terra, na Lua ou no espaço!
        - **Força Peso ($P$):** É a força de atração gravitacional com que o planeta puxa seu corpo, medida em **Newtons ($N$)**.
        
        #### ⚖️ Fórmula da Força Peso:
        $$P = m \cdot g$$
        - $P$: Peso em Newtons ($N$)
        - $m$: Massa em quilogramas ($kg$)
        - $g$: Aceleração da gravidade do planeta (Terra $= 9,8\text{ m/s}^2$; Lua $= 1,62\text{ m/s}^2$; Júpiter $= 24,79\text{ m/s}^2$)
        """)
        
        # Simulador de Gravidade
        st.markdown("### 🧮 2. Simulador: Sua Balança em Outros Mundos")
        user_mass = st.number_input("Digite sua massa em kg:", min_value=15.0, max_value=150.0, value=45.0, step=1.0, key="phys_l1_mass")
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("🌍 Terra (g=9,8)", f"{user_mass * 9.8:.1f} N", f"{user_mass:.1f} kg")
        c2.metric("🌕 Lua (g=1,62)", f"{user_mass * 1.62:.1f} N", f"Sente-se {(user_mass * 1.62)/9.8:.1f} kg!")
        c3.metric("🔴 Marte (g=3,72)", f"{user_mass * 3.72:.1f} N", f"Sente-se {(user_mass * 3.72)/9.8:.1f} kg")
        c4.metric("🪐 Júpiter (g=24,8)", f"{user_mass * 24.79:.1f} N", f"Sente-se {(user_mass * 24.79)/9.8:.1f} kg!")
        
        # Exercício
        st.markdown("### 📝 3. Exercício de Gravitação")
        with st.container():
            st.markdown(r"""
                <div class='exercise-card'>
                    <h4 style='color: #ffd166; margin-top:0;'>Desafio 1: O Astronauta na Lua</h4>
                    <p>Um astronauta com traje espacial tem uma massa total de <strong>100 kg</strong> na Terra. Ao pousar na Lua (onde a gravidade é $\approx 1/6$ da Terra), qual será a sua <strong>massa</strong> e o seu <strong>peso aproximado</strong>?</p>
                </div>
            """, unsafe_allow_html=True)
            
            ans_p1 = st.radio(
                "Escolha a opção correta:",
                [
                    "A) Massa = 16,6 kg e Peso = 1000 N",
                    "B) Massa = 100 kg (não muda!) e Peso ≈ 162 N",
                    "C) Massa = 0 kg e Peso = 0 N",
                    "D) Massa = 600 kg e Peso = 162 N"
                ],
                key="phys_ex1"
            )
            
            if st.button("Verificar Resposta (Física 1)", key="phys_btn1"):
                if "B)" in ans_p1:
                    st.success("🎉 **Exato!** A massa é sempre constante ($100\\text{ kg}$) e o peso na Lua é $100 \\times 1,62 = 162\\text{ N}$. Ganhou **+25 XP**!")
                    add_xp(user["id"], 25)
                else:
                    st.error("❌ Lembre-se: A massa nunca muda em nenhum lugar do Universo!")
                    
    elif "Nível 2" in level:
        st.markdown("""
            <div class='level-badge explorer'>🟡 NÍVEL 2 — EXPLORADOR ORBITAL</div>
            <h3 style='color: #fbbf24;'>3ª Lei de Newton, Propulsão de Foguetes e Velocidade Orbital</h3>
        """, unsafe_allow_html=True)
        
        st.markdown(r"""
        ### 📖 1. Teoria & Propulsão Espacial
        Os foguetes funcionam graças à **3ª Lei de Newton: Ação e Reação**:
        > *"A toda ação corresponde uma reação de mesma intensidade, mesma direção e sentido oposto."*
        
        Quando o motor do foguete expele gases superaquecidos em alta velocidade para baixo (ação), os gases empurram o foguete para cima com a mesma força (reação)!
        
        #### 🚀 Força de Empuxo e Aceleração ($2ª\text{ Lei}$):
        $$F_{\text{resultante}} = m \cdot a \implies a = \frac{F_{\text{empuxo}} - P}{m}$$
        
        #### 🛰️ Velocidade Orbital Circular:
        Para um satélite não cair na Terra nem escapar para o espaço, a gravidade atua como força centrípeta:
        $$v_{\text{orbital}} = \sqrt{\frac{G \cdot M}{r}} \approx 7,8\text{ km/s} \quad (\approx 28.000\text{ km/h na órbita baixa da ISS})$$
        """)
        
        # Simulador de Empuxo
        st.markdown("### 🧮 2. Simulador de Lançamento de Foguete")
        col_f1, col_f2 = st.columns(2)
        rocket_mass = col_f1.slider("Massa do Foguete (toneladas):", min_value=10, max_value=500, value=100, step=10, key="rkt_m") * 1000
        thrust_kn = col_f2.slider("Força de Empuxo dos Motores (kiloNewtons):", min_value=500, max_value=8000, value=2500, step=100, key="rkt_t") * 1000
        
        weight_n = rocket_mass * 9.8
        net_force = thrust_kn - weight_n
        accel = net_force / rocket_mass if net_force > 0 else 0
        
        st.markdown(f"""
            <div class='formula-box'>
                <p>⚖️ <strong>Força Peso do Foguete:</strong> {weight_n/1000:.1f} kN | 🔥 <strong>Empuxo:</strong> {thrust_kn/1000:.1f} kN</p>
                <h3 style='color: {"#4ade80" if accel > 0 else "#f43f5e"};'>
                    {"🚀 DECOLAGEM! Aceleração: " + f"{accel:.2f} m/s² ({accel/9.8:.2f} G)" if accel > 0 else "❌ FALHA: O empuxo é menor que o peso! O foguete não sai do chão."}
                </h3>
            </div>
        """, unsafe_allow_html=True)
        
        # Exercício
        st.markdown("### 📝 3. Exercício de Propulsão")
        with st.container():
            st.markdown("""
                <div class='exercise-card'>
                    <h4 style='color: #ffd166; margin-top:0;'>Desafio 2: Foguete no Vácuo do Espaço</h4>
                    <p>Como um foguete consegue acelerar no vácuo do espaço sideral, se não há ar para ele "empurrar"?</p>
                </div>
            """, unsafe_allow_html=True)
            
            ans_p2 = st.radio(
                "Escolha a explicação física correta:",
                [
                    "A) Ele empurra o vento solar com suas asas.",
                    "B) Ele empurra seus próprios gases expelidos para trás em alta velocidade (Ação e Reação de Newton), funcionando até melhor no vácuo!",
                    "C) Ele usa ímãs que se conectam aos planetas.",
                    "D) Foguetes não funcionam no vácuo."
                ],
                key="phys_ex2"
            )
            
            if st.button("Verificar Resposta (Física 2)", key="phys_btn2"):
                if "B)" in ans_p2:
                    st.success("🎉 **Perfeito!** O foguete empurra a própria massa dos gases de exaustão. Ganhou **+30 XP**!")
                    add_xp(user["id"], 30)
                else:
                    st.error("❌ Pense na 3ª Lei de Newton: a ação é expelir o combustível para trás!")
                    
    else: # Nível 3
        st.markdown("""
            <div class='level-badge astrophysicist'>🔴 NÍVEL 3 — ASTROFÍSICO DE VANGUARDA</div>
            <h3 style='color: #c084fc;'>Relatividade de Einstein, Dilatação do Tempo e Buracos Negros</h3>
        """, unsafe_allow_html=True)
        
        st.markdown(r"""
        ### 📖 1. Teoria & Relatividade Geral de Einstein
        No filme *Interestelar*, 1 hora no Planeta Miller equivalia a 7 anos na Terra. Isso acontece devido à **Dilatação Temporal Gravitacional** provocada pelo buraco negro supermassivo **Gargantua**!
        
        #### ⏳ Dilatação do Tempo Relativística (Velocidade):
        $$\Delta t' = \frac{\Delta t}{\sqrt{1 - \frac{v^2}{c^2}}} = \gamma \cdot \Delta t$$
        
        #### 🕳️ Raio de Schwarzschild (Horizonte de Eventos do Buraco Negro):
        O raio a partir do qual nada, nem mesmo a luz, consegue escapar:
        $$R_s = \frac{2 \cdot G \cdot M}{c^2}$$
        - $G = 6,674 \times 10^{-11}\text{ N m}^2/\text{kg}^2$
        - Se a Terra fosse comprimida em um buraco negro, seu raio seria de apenas **9 milímetros**!
        """)
        
        # Calculadora de Dilatação do Tempo
        st.markdown("### 🧮 2. Simulador Relativístico: Viagem Próxima à Velocidade da Luz")
        v_pct = st.slider("Velocidade da nave como porcentagem da velocidade da luz (% c):", min_value=10, max_value=99, value=90, step=1, key="rel_v") / 100.0
        
        gamma = 1.0 / math.sqrt(1.0 - (v_pct ** 2))
        
        st.markdown(f"""
            <div class='formula-box'>
                <p>🚀 <strong>Velocidade da Nave:</strong> {v_pct * 100:.0f}% da velocidade da luz ({v_pct * 300000:,.0f} km/s)</p>
                <p>⚡ <strong>Fator de Lorentz ($\gamma$):</strong> {gamma:.2f}</p>
                <h3 style='color: #c084fc;'>⏳ 1 Ano para o Astronauta na Nave = {gamma:.2f} Anos se passam na Terra!</h3>
                <p style='color: #94a3b8; font-size: 0.85rem;'>Se você viajar a 99% da velocidade da luz por 1 ano, ao voltar encontrará a Terra 7 anos mais velha!</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Exercício
        st.markdown("### 📝 3. Desafio Relativístico")
        with st.container():
            st.markdown("""
                <div class='exercise-card'>
                    <h4 style='color: #ffd166; margin-top:0;'>Desafio 3: O Paradoxo dos Gêmeos</h4>
                    <p>Por que os relógios atômicos a bordo dos satélites do sistema GPS precisam ser corrigidos pela Teoria da Relatividade de Einstein todos os dias?</p>
                </div>
            """, unsafe_allow_html=True)
            
            ans_p3 = st.radio(
                "Selecione a razão científica:",
                [
                    "A) As baterias dos satélites descarregam no frio espacial.",
                    "B) O tempo passa mais rápido no satélite (menor gravidade) e mais devagar pelo movimento orbital, acumulando microssegundos de diferença que errariam o GPS em quilômetros se não corrigidos!",
                    "C) A luz do Sol atrasa os circuitos eletrônicos.",
                    "D) A atmosfera terrestre bloqueia o horário exato."
                ],
                key="phys_ex3"
            )
            
            if st.button("Validar Desafio Relativístico", key="phys_btn3"):
                if "B)" in ans_p3:
                    st.success("🎉 **Magnífico!** Os satélites GPS são a maior prova diária da relatividade de Einstein na Terra! Ganhou **+40 XP**!")
                    add_xp(user["id"], 40)
                    unlock_badge(user["id"], "steam_phys_master")
                else:
                    st.error("❌ Pense nos efeitos da gravidade e velocidade sobre o fluxo do tempo!")


# ==============================================================================
# 🧪 3. TRILHA DE QUÍMICA ESTELAR & ASTROBIOLOGIA
# ==============================================================================
def _render_chemistry_track(user: dict):
    st.markdown("## 🧪 Química Estelar, Tabela Periódica & Astrobiologia")
    
    level = st.radio(
        "Selecione o Nível de Dificuldade:",
        [
            "🟢 Nível 1: Cadete Espacial (Básico / 6º Ano)",
            "🟡 Nível 2: Explorador Orbital (Intermediário / 7º-9º Ano)",
            "🔴 Nível 3: Astrofísico de Vanguarda (Avançado / Ensino Médio)"
        ],
        key="chem_level_select",
        horizontal=True
    )
    
    st.markdown("---")
    
    if "Nível 1" in level:
        st.markdown("""
            <div class='level-badge cadet'>🟢 NÍVEL 1 — CADETE ESPACIAL</div>
            <h3 style='color: #4ade80;'>Origem dos Elementos Químicos: 'Somos Poeira de Estrelas!'</h3>
        """, unsafe_allow_html=True)
        
        st.markdown(r"""
        ### 📖 1. Teoria & A Forja Cósmica
        Você sabia que todos os átomos do seu corpo (o cálcio dos ossos, o ferro do sangue e o carbono do DNA) foram fabricados dentro de estrelas que explodiram há bilhões de anos?
        
        1. **Big Bang:** Criou os elementos mais leves: **Hidrogênio ($H$)** ($75\%$) e **Hélio ($He$)** ($25\%$).
        2. **Coração das Estrelas Normais (como o Sol):** Fundem Hidrogênio em Hélio ($4^1H \rightarrow ^4He + \text{Luz}$).
        3. **Gigantes Vermelhas:** Fundem Hélio em **Carbono ($C$)** e **Oxigênio ($O$)**.
        4. **Supernovas (Explosões Estelares):** Criam os elementos mais pesados como **Ferro ($Fe$)**, **Ouro ($Au$)** e **Urânio ($U$)**!
        """)
        
        # Simulador de Elementos
        st.markdown("### 🧮 2. Simulador: Onde Foi Criado Cada Elemento do Seu Corpo?")
        element = st.selectbox(
            "Selecione um elemento químico:",
            ["Hidrogênio (H) - Água do corpo", "Carbono (C) - Base de toda a vida", "Cálcio (Ca) - Nossos ossos e dentes", "Ferro (Fe) - Glóbulos vermelhos do sangue", "Ouro (Au) - Joias e eletrônica espacial"],
            key="chem_l1_elem"
        )
        
        info_dict = {
            "Hidrogênio (H) - Água do corpo": ("🌌 Big Bang (há 13,8 bilhões de anos)", "#00d4ff", "O átomo mais simples do Universo! 1 próton e 1 elétron."),
            "Carbono (C) - Base de toda a vida": ("🔴 Interior de Estrelas Gigantes Vermelhas", "#fbbf24", "Capaz de formar 4 ligações químicas simultâneas, permitindo moléculas complexas como proteínas e DNA."),
            "Cálcio (Ca) - Nossos ossos e dentes": ("💥 Explosão de Supernovas", "#4ade80", "Forjado em temperaturas de centenas de milhões de graus na morte de estrelas massivas."),
            "Ferro (Fe) - Glóbulos vermelhos do sangue": ("💥 Supernovas e Gigantes Massivas", "#f43f5e", "O elemento mais estável da física nuclear. Quando a estrela cria ferro, ela perde a capacidade de gerar energia e explode!"),
            "Ouro (Au) - Joias e eletrônica espacial": ("🌟 Colisão de Estrelas de Nêutrons (Kilonova)", "#ffd700", "Condições tão extremas de densidade que átomos pesados capturam nêutrons em frações de segundo!")
        }
        
        origin, color, detail = info_dict[element]
        st.markdown(f"""
            <div class='formula-box' style='border-left-color: {color};'>
                <h4 style='color: {color}; margin:0;'>Origem Cósmica: {origin}</h4>
                <p style='color: #f1f5f9; margin-top: 8px;'>{detail}</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Exercício
        st.markdown("### 📝 3. Exercício de Astrostequiometria Básica")
        with st.container():
            st.markdown("""
                <div class='exercise-card'>
                    <h4 style='color: #ffd166; margin-top:0;'>Desafio 1: O Combustível do Sol</h4>
                    <p>Qual é o elemento químico mais abundante no Sol e no Universo, que alimenta as reações de fusão nuclear?</p>
                </div>
            """, unsafe_allow_html=True)
            
            ans_c1 = st.radio(
                "Escolha o elemento:",
                ["A) Ferro", "B) Hidrogênio (H)", "C) Oxigênio", "D) Chumbo"],
                key="chem_ex1"
            )
            
            if st.button("Verificar Resposta (Química 1)", key="chem_btn1"):
                if "B)" in ans_c1:
                    st.success("🎉 **Correto!** O Hidrogênio é o elemento primordial do Universo! Ganhou **+25 XP**!")
                    add_xp(user["id"], 25)
                else:
                    st.error("❌ Dica: É o primeiro e mais leve elemento da Tabela Periódica!")
                    
    elif "Nível 2" in level:
        st.markdown("""
            <div class='level-badge explorer'>🟡 NÍVEL 2 — EXPLORADOR ORBITAL</div>
            <h3 style='color: #fbbf24;'>Reações de Sobrevivência em Marte: Sabatier e Eletrólise</h3>
        """, unsafe_allow_html=True)
        
        st.markdown(r"""
        ### 📖 1. Teoria & Química no Domo Marciano (*Perdido em Marte*)
        A atmosfera de Marte é $95\%$ de $CO_2$ (gás carbônico) e não há rios de água líquida. Como os astronautas sobrevivem?
        
        #### 💧 1. Eletrólise da Água (Produção de Oxigênio Respirável):
        $$2H_2O_{(l)} \xrightarrow{\text{Energia Elétrica}} 2H_{2(g)} + O_{2(g)}$$
        
        #### 🚀 2. Reação de Sabatier (Produção de Metano/Combustível e Água):
        $$CO_{2(g)} + 4H_{2(g)} \xrightarrow{\text{Catalisador de Níquel}} CH_{4(g)} + 2H_2O_{(g)}$$
        - $CH_4$ (Metano): Usado como propelente para decolar o foguete de volta para a Terra!
        """)
        
        # Simulador Sabatier
        st.markdown("### 🧮 2. Simulador Químico: Usina de Oxigênio e Metano de Marte")
        moles_h2o = st.slider("Litros de Água ($H_2O$) submetidos à Eletrólise:", min_value=10, max_value=500, value=100, step=10, key="chem_l2_water")
        
        o2_liters = moles_h2o * 0.888 # Proporção mássica
        h2_liters = moles_h2o * 0.112
        
        st.markdown(f"""
            <div class='formula-box'>
                <p>🧪 A partir de <strong>{moles_h2o} kg de Água pura</strong>:</p>
                <h3 style='color: #38bdf8;'>💨 Oxigênio ($O_2$) Gerado: {o2_liters:.1f} kg (Suficiente para 1 astronauta respirar por {o2_liters/0.84:.1f} dias!)</h3>
                <h4 style='color: #4ade80;'>🔥 Hidrogênio ($H_2$) Disponível para Sabatier: {h2_liters:.1f} kg</h4>
            </div>
        """, unsafe_allow_html=True)
        
        # Exercício
        st.markdown("### 📝 3. Exercício de Estequiometria Espacial")
        with st.container():
            st.markdown(r"""
                <div class='exercise-card'>
                    <h4 style='color: #ffd166; margin-top:0;'>Desafio 2: Balanceamento da Reação de Sabatier</h4>
                    <p>Na reação de Sabatier $CO_2 + x H_2 \rightarrow CH_4 + 2 H_2O$, qual é o coeficiente $x$ necessário para balancear a quantidade de átomos de Hidrogênio?</p>
                </div>
            """, unsafe_allow_html=True)
            
            ans_c2 = st.radio(
                "Escolha o valor de x:",
                ["A) x = 2", "B) x = 3", "C) x = 4 (pois temos 4 átomos no CH4 e 4 átomos no 2H2O = 8 hidrogênios no total)", "D) x = 1"],
                key="chem_ex2"
            )
            
            if st.button("Verificar Resposta (Química 2)", key="chem_btn2"):
                if "C)" in ans_c2:
                    st.success("🎉 **Perfeito!** $CO_2 + 4H_2 \\rightarrow CH_4 + 2H_2O$. Você ganhou **+30 XP**!")
                    add_xp(user["id"], 30)
                else:
                    st.error("❌ Conte os átomos de Hidrogênio nos produtos: 4 no CH4 + 4 no 2H2O = 8 no total. Divida por 2!")
                    
    else: # Nível 3
        st.markdown("""
            <div class='level-badge astrophysicist'>🔴 NÍVEL 3 — ASTROFÍSICO DE VANGUARDA</div>
            <h3 style='color: #c084fc;'>Espectroscopia Estelar e Busca por Bioassinaturas em Exoplanetas</h3>
        """, unsafe_allow_html=True)
        
        st.markdown(r"""
        ### 📖 1. Teoria & Espectroscopia de Fraunhofer
        Como sabemos a composição química de uma estrela ou planeta a 100 anos-luz de distância sem nunca ter ido lá? **Através da Luz!**
        
        Cada elemento químico absorve e emite comprimentos de onda específicos de luz, funcionando como uma **impressão digital atômica**:
        - **Água ($H_2O$):** Absorve fortemente no infravermelho ($\approx 1,4\text{ }\mu m$ e $1,9\text{ }\mu m$).
        - **Metano ($CH_4$) + Oxigênio/Ozônio ($O_3$):** Quando encontrados juntos na atmosfera de um exoplaneta rochoso, são um forte indício de **atividade biológica (vida!)**, pois reagem rapidamente e precisam ser repostos continuamente.
        """)
        
        # Simulador Espectroscópico
        st.markdown("### 🧮 2. Simulador: Espectrômetro do Telescópio James Webb")
        exoplanet_type = st.selectbox(
            "Aponte o telescópio para um Exoplaneta candidato:",
            ["Exoplaneta K2-18b (Zona Habitável)", "Júpiter Quente (51 Pegasi b)", "Planeta Rochoso Seco tipo Marte"],
            key="jwst_target"
        )
        
        if "K2-18b" in exoplanet_type:
            st.markdown(r"""
                <div class='formula-box' style='border-left-color: #4ade80;'>
                    <h4 style='color: #4ade80;'>🧬 Bioassinatura Detectada!</h4>
                    <p>Linhas espectrais detectadas: <strong>Vapor de Água ($H_2O$), Metano ($CH_4$) e Dióxido de Carbono ($CO_2$)</strong> com baixa presença de amônia. Planeta oceânico potencialmente habitável!</p>
                </div>
            """, unsafe_allow_html=True)
        elif "Júpiter Quente" in exoplanet_type:
            st.markdown(r"""
                <div class='formula-box' style='border-left-color: #fbbf24;'>
                    <h4 style='color: #fbbf24;'>🔥 Atmosfera Hiperaquecida</h4>
                    <p>Linhas de absorção: <strong>Vapor de Sódio ($Na$) e Potássio ($K$) atômicos</strong> em temperaturas superiores a 1.200°C.</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(r"""
                <div class='formula-box' style='border-left-color: #f43f5e;'>
                    <h4 style='color: #f43f5e;'>🏜️ Planeta Árido</h4>
                    <p>Predomínio quase exclusivo de <strong>Dióxido de Carbono ($CO_2$)</strong> sem bioassinaturas ativas.</p>
                </div>
            """, unsafe_allow_html=True)
            
        # Exercício
        st.markdown("### 📝 3. Desafio de Espectroscopia")
        with st.container():
            st.markdown("""
                <div class='exercise-card'>
                    <h4 style='color: #ffd166; margin-top:0;'>Desafio 3: O Mistério das Linhas Escuras</h4>
                    <p>O que são as linhas escuras (linhas de absorção de Fraunhofer) observadas no arco-íris do espectro da luz solar?</p>
                </div>
            """, unsafe_allow_html=True)
            
            ans_c3 = st.radio(
                "Selecione a explicação científica:",
                [
                    "A) São sombras causadas por nuvens na Terra.",
                    "B) São comprimentos de onda de luz absorvidos pelos elementos químicos presentes na atmosfera externa do Sol antes da luz viajar pelo espaço!",
                    "C) São defeitos nas lentes do telescópio.",
                    "D) É a luz da Lua interferindo no Sol."
                ],
                key="chem_ex3"
            )
            
            if st.button("Validar Desafio Espectroscópico", key="chem_btn3"):
                if "B)" in ans_c3:
                    st.success("🎉 **Sensacional!** É assim que deciframos as estrelas a trilhões de quilômetros de distância! Ganhou **+40 XP**!")
                    add_xp(user["id"], 40)
                    unlock_badge(user["id"], "steam_chem_master")
                else:
                    st.error("❌ Lembre-se: os átomos absorvem fótons de cores bem específicas!")


# ==============================================================================
# 💻 4. TRILHA DE TECNOLOGIA & COMPUTAÇÃO ESPACIAL
# ==============================================================================
def _render_tech_track(user: dict):
    st.markdown("## 💻 Tecnologia, Telecomunicações Espaciais & IA")
    
    level = st.radio(
        "Selecione o Nível de Dificuldade:",
        [
            "🟢 Nível 1: Cadete Espacial (Básico / 6º Ano)",
            "🟡 Nível 2: Explorador Orbital (Intermediário / 7º-9º Ano)",
            "🔴 Nível 3: Astrofísico de Vanguarda (Avançado / Ensino Médio)"
        ],
        key="tech_level_select",
        horizontal=True
    )
    
    st.markdown("---")
    
    if "Nível 1" in level:
        st.markdown("""
            <div class='level-badge cadet'>🟢 NÍVEL 1 — CADETE ESPACIAL</div>
            <h3 style='color: #4ade80;'>Algoritmos e Lógica de Comando para Rovers Marcianos</h3>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        ### 📖 1. Teoria & Algoritmos
        Um **Algoritmo** é uma sequência ordenada de instruções claras e sem ambiguidades para resolver um problema.
        
        Como Marte fica a dezenas de milhões de quilômetros da Terra, o Rover **Perseverance** não pode ser controlado por joystick ao vivo. Os engenheiros da NASA escrevem uma **lista diária de comandos sequenciais** que o robô executa autonomamente usando sensores!
        """)
        
        # Simulador de Algoritmo do Rover
        st.markdown("### 🧮 2. Simulador: Programe a Missão do Rover")
        st.write("Monte a sequência de comandos para o Rover cruzar a cratera Jezero:")
        
        step1 = st.selectbox("1º Passo:", ["AVANÇAR 5 METROS", "GIRAR 90° DIREITA", "LIGAR CÂMERA"], key="r_s1")
        step2 = st.selectbox("2º Passo:", ["ANALISAR ROCHA COM LASER", "AVANÇAR 10 METROS", "PARAR"], key="r_s2")
        step3 = st.selectbox("3º Passo:", ["COLETAR AMOSTRA COM BROCA", "RETORNAR À BASE", "DESLIGAR"], key="r_s3")
        
        if st.button("🤖 Executar Algoritmo no Rover", key="exec_rover_btn"):
            st.markdown(f"""
                <div class='terminal-box'>
                    [ROVER LOG]: Inicializando subsistemas autônomos...<br>
                    [PASSO 1]: Executando -> {step1} (OK)<br>
                    [PASSO 2]: Executando -> {step2} (OK)<br>
                    [PASSO 3]: Executando -> {step3} (Sucesso Científico!)<br>
                    [STATUS]: Amostra catalogada com sucesso na memória Flash de 128GB!
                </div>
            """, unsafe_allow_html=True)
            
        # Exercício
        st.markdown("### 📝 3. Exercício de Lógica Computacional")
        with st.container():
            st.markdown("""
                <div class='exercise-card'>
                    <h4 style='color: #ffd166; margin-top:0;'>Desafio 1: O Loop de Segurança</h4>
                    <p>Qual estrutura de programação o Rover usa quando precisa dizer: <em>"ENQUANTO não encontrar obstáculo, CONTINUE AVANÇANDO; SE encontrar cratera, GIRE 45°"</em>?</p>
                </div>
            """, unsafe_allow_html=True)
            
            ans_t1 = st.radio(
                "Selecione o conceito de programação:",
                [
                    "A) Estrutura de Repetição (Loop While) e Condicional (If/Else)",
                    "B) Apenas multiplicação matemática",
                    "C) Formatação de texto",
                    "D) Desligamento manual"
                ],
                key="tech_ex1"
            )
            
            if st.button("Verificar Resposta (Tech 1)", key="tech_btn1"):
                if "A)" in ans_t1:
                    st.success("🎉 **Perfeito!** Loops e Condicionais são a espinha dorsal de qualquer robô autônomo! Ganhou **+25 XP**!")
                    add_xp(user["id"], 25)
                else:
                    st.error("❌ Dica: 'Enquanto' indica repetição e 'Se' indica uma condição!")
                    
    elif "Nível 2" in level:
        st.markdown("""
            <div class='level-badge explorer'>🟡 NÍVEL 2 — EXPLORADOR ORBITAL</div>
            <h3 style='color: #fbbf24;'>Código Binário, Redes do Espaço Profundo (DSN) e Bits</h3>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        ### 📖 1. Teoria & O Código Binário
        Toda a informação enviada pelo telescópio James Webb ou pelas sondas Voyager é transmitida por ondas de rádio codificadas em **Binário (0s e 1s)**:
        - **Bit:** A menor unidade de informação (um circuito desligado $= 0$ ou ligado $= 1$).
        - **Byte:** Conjunto de 8 bits (capaz de representar um número de $0$ a $255$ ou uma letra em código ASCII).
        - **Hexadecimal:** Usado pela sonda Pathfinder em *Perdido em Marte* para economizar caracteres na comunicação!
        """)
        
        # Simulador Binário
        st.markdown("### 🧮 2. Simulador: Codificador de Mensagens Interestelares em Binário")
        msg_input = st.text_input("Digite uma palavra curta para transmitir ao espaço:", value="MARTE", max_chars=10, key="bin_input")
        
        if msg_input:
            bin_output = " ".join(format(ord(c), '08b') for c in msg_input)
            hex_output = " ".join(format(ord(c), '02X') for c in msg_input)
            
            st.markdown(f"""
                <div class='terminal-box'>
                    📡 <strong>TRANSMISSÃO DEEP SPACE NETWORK (DSN):</strong><br>
                    <strong>Mensagem Original:</strong> {msg_input}<br>
                    <strong>Binário (8-bits por letra):</strong><br>
                    <span style='color: #00d4ff;'>{bin_output}</span><br><br>
                    <strong>Hexadecimal (Base 16):</strong><br>
                    <span style='color: #ffd166;'>{hex_output}</span>
                </div>
            """, unsafe_allow_html=True)
            
        # Exercício
        st.markdown("### 📝 3. Exercício de Binário Espacial")
        with st.container():
            st.markdown("""
                <div class='exercise-card'>
                    <h4 style='color: #ffd166; margin-top:0;'>Desafio 2: Decodificando o Sinal Alienígena</h4>
                    <p>Qual é o número decimal representado pelo byte binário <strong>00001010</strong>? (Dica: posições valem 128, 64, 32, 16, 8, 4, 2, 1)</p>
                </div>
            """, unsafe_allow_html=True)
            
            ans_t2 = st.radio(
                "Escolha o valor decimal:",
                ["A) 10 (8 + 2 = 10)", "B) 100", "C) 12", "D) 255"],
                key="tech_ex2"
            )
            
            if st.button("Verificar Resposta (Tech 2)", key="tech_btn2"):
                if "A)" in ans_t2:
                    st.success("🎉 **Excelente!** Na posição 8 temos 1 e na posição 2 temos 1. $8 + 2 = 10$. Ganhou **+30 XP**!")
                    add_xp(user["id"], 30)
                else:
                    st.error("❌ Some os valores das posições onde o bit é 1: posição 8 e posição 2!")
                    
    else: # Nível 3
        st.markdown("""
            <div class='level-badge astrophysicist'>🔴 NÍVEL 3 — ASTROFÍSICO DE VANGUARDA</div>
            <h3 style='color: #c084fc;'>Inteligência Artificial na Detecção de Exoplanetas e Simulação N-Corpos</h3>
        """, unsafe_allow_html=True)
        
        st.markdown(r"""
        ### 📖 1. Teoria & IA Astronômica
        Os telescópios espaciais modernos monitoram centenas de milhares de estrelas ao mesmo tempo, gerando **terabytes de dados por dia**. É humanamente impossível analisar cada curva de luz manualmente!
        
        #### 🤖 Como a IA descobre novos planetas (Método de Trânsito):
        Quando um planeta passa na frente de sua estrela, o brilho da estrela sofre uma leve queda periódica (ex: $0,01\%$).
        - Redes Neurais Convolucionais (CNNs) e algoritmos de Machine Learning analisam essas curvas de luz estelares e filtram ruídos de manchas solares, descobrindo planetas do tamanho da Terra com altíssima precisão!
        """)
        
        # Simulador de Trânsito
        st.markdown("### 🧮 2. Simulador: Detecção de Trânsito Planetário com IA")
        planet_radius_ratio = st.slider("Tamanho do Exoplaneta em relação à estrela (% do raio):", min_value=1, max_value=20, value=10, step=1, key="transit_r")
        
        dip_pct = (planet_radius_ratio / 100.0) ** 2 * 100.0
        
        st.markdown(f"""
            <div class='formula-box'>
                <p>🔭 <strong>Queda de Brilho da Estrela ($\Delta F/F$):</strong></p>
                <p>$$\\frac{{\\Delta F}}{{F}} = \\left(\\frac{{R_{{planeta}}}}{{R_{{estrela}}}}\\right)^2 = ({planet_radius_ratio/100:.2f})^2 = {dip_pct:.2f}\\%$$</p>
                <h3 style='color: #fbbf24;'>📉 Queda de Brilho Detectada pela Rede Neural: {dip_pct:.2f}%</h3>
                <p style='color: #4ade80;'>✅ IA Confirmação: Padrão periódico verificado! Exoplaneta confirmado no catálogo!</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Exercício
        st.markdown("### 📝 3. Desafio de IA Astronômica")
        with st.container():
            st.markdown("""
                <div class='exercise-card'>
                    <h4 style='color: #ffd166; margin-top:0;'>Desafio 3: O Problema dos N-Corpos</h4>
                    <p>Por que os astrônomos usam supercomputadores com simulações numéricas para prever o movimento de 3 ou mais planetas interagindo gravitacionalmente?</p>
                </div>
            """, unsafe_allow_html=True)
            
            ans_t3 = st.radio(
                "Selecione a resposta correta:",
                [
                    "A) Porque não existe uma fórmula analítica fechada simples para resolver o sistema gravitacional de 3 ou mais corpos (Problema dos 3 Corpos de Poincaré), exigindo cálculo computacional numérico iterativo passo a passo!",
                    "B) Porque as leis de Newton não se aplicam a planetas.",
                    "C) Porque os planetas mudam de tamanho aleatoriamente.",
                    "D) Apenas para desenhar gráficos coloridos."
                ],
                key="tech_ex3"
            )
            
            if st.button("Validar Desafio de IA", key="tech_btn3"):
                if "A)" in ans_t3:
                    st.success("🎉 **Sensacional!** O famoso Problema dos 3 Corpos é um dos pilares da física computacional! Ganhou **+40 XP**!")
                    add_xp(user["id"], 40)
                    unlock_badge(user["id"], "steam_tech_master")
                else:
                    st.error("❌ Pense no Problema dos 3 Corpos e no comportamento caótico da gravidade!")

    # Verificação de Polímata
    unlocked_badges = set()
    try:
        from database import get_user_badges
        unlocked_badges = set(get_user_badges(user["id"]))
    except:
        pass
        
    if {"steam_math_master", "steam_phys_master", "steam_chem_master", "steam_tech_master"}.issubset(unlocked_badges):
        if "steam_polymath" not in unlocked_badges:
            unlock_badge(user["id"], "steam_polymath")
            st.balloons()
            st.success("👑 **PARABÉNS LENDÁRIO!** Você dominou todas as 4 disciplinas da Academia STEAM e conquistou a insígnia máxima **POLÍMATA DAS GALÁXIAS** (+300 XP)!")
