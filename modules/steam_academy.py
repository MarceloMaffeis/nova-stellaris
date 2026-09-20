"""
Nova Stellaris - Academia Nova Stellaris: Fundamentos Científicos & Exploração Cósmica
Pedagogia: Ensino dos Fundamentos Essenciais da Disciplina PRIMEIRO (com analogias cotidianas e passo a passo)
seguido da Aplicação Prática no Cosmos e Astronomia.
Disciplinas: Matemática, Física, Química e Tecnologia & Computação.
Níveis: Cadete Espacial (6º Ano / Básico), Explorador Orbital (7º-9º Ano) e Astrofísico de Vanguarda (Ensino Médio / Avançado).
"""

import streamlit as st
import math
from database import add_xp, unlock_badge

def render_steam_academy(user: dict, default_track: str = None, *args, **kwargs):
    if not default_track:
        default_track = st.session_state.get("steam_academy_default")
    st.markdown("""
        <div class='cosmic-hero' style='background: linear-gradient(135deg, rgba(16,24,50,0.95), rgba(10,15,35,0.95)); border: 1px solid #00d4ff;'>
            <h1 style='color: #00d4ff; margin-bottom: 5px;'>🎓 Academia Nova Stellaris — Fundamentos & Espaço</h1>
            <p style='color: #cbd5e1; font-size: 1.1rem; margin: 0;'>
                Aprenda primeiro a <strong>base científica e matemática</strong> aqui na Terra e depois veja como ela decifra os maiores mistérios do <strong>Universo</strong>!
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    track_options = [
        "📐 1. Matemática",
        "⚡ 2. Física",
        "🧪 3. Química",
        "💻 4. Tecnologia & Computação"
    ]
    
    default_idx = 0
    if default_track:
        for i, opt in enumerate(track_options):
            if default_track.lower() in opt.lower():
                default_idx = i
                break
    elif "steam_academy_idx" in st.session_state:
        default_idx = st.session_state.steam_academy_idx

    active_track = st.radio(
        "Trilha da Academia:",
        track_options,
        index=default_idx,
        horizontal=True,
        label_visibility="collapsed",
        key="steam_academy_selector"
    )
    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    
    if active_track == track_options[0]:
        _render_math_track(user)
    elif active_track == track_options[1]:
        _render_physics_track(user)
    elif active_track == track_options[2]:
        _render_chemistry_track(user)
    else:
        _render_tech_track(user)


# ==============================================================================
# 📐 1. TRILHA DE MATEMÁTICA
# ==============================================================================
def _render_math_track(user: dict):
    st.markdown("## 📐 Matemática: Fundamentos do Raciocínio & Geometria do Cosmos")
    st.write("Escolha seu nível de aprendizado. Você aprenderá primeiro a regra matemática básica e depois a sua aplicação no espaço:")
    
    level = st.radio(
        "Selecione seu Nível de Treinamento:",
        [
            "🟢 Nível 1: Cadete (Fundamentos: Proporções, Frações e Diâmetros / 6º Ano)",
            "🟡 Nível 2: Explorador (Fundamentos: Potências de 10, Notação Científica e Velocidade / 7º-9º Ano)",
            "🔴 Nível 3: Astrofísico (Fundamentos: Trigonometria, Expoentes e Geometria Orbital / Avançado)"
        ],
        key="math_level_select"
    )
    
    st.markdown("---")
    
    # -------------------------------------------------------------------------
    # NÍVEL 1: MATEMÁTICA
    # -------------------------------------------------------------------------
    if "Nível 1" in level:
        st.markdown("""
            <div class='level-badge cadet'>🟢 NÍVEL 1 — CADETE (FUNDAMENTOS & 6º ANO)</div>
            <h3 style='color: #4ade80;'>Proporções, Razões, Diâmetros e Escalas</h3>
        """, unsafe_allow_html=True)
        
        # ETAPA 1: FUNDAMENTOS
        st.markdown("""
            <div class='fundamento-box'>
                <h4 style='color: #ffd166; margin-top:0;'>🧱 ETAPA 1: O FUNDAMENTO BÁSICO (O que você precisa saber primeiro)</h4>
                <p>Antes de olharmos para as estrelas, vamos entender como funciona a <strong>Proporção</strong> e a <strong>Geometria de Círculos</strong> no nosso dia a dia:</p>
                <ul>
                    <li><strong>O que é uma Razão/Proporção?</strong> É comparar dois números por meio de uma divisão. Por exemplo: se numa receita você usa 2 xícaras de farinha para cada 1 de leite, a proporção é de $2:1$ (2 para 1). Se você quiser fazer o dobro do bolo, multiplicará tudo por 2!</li>
                    <li><strong>Raio ($r$) e Diâmetro ($D$):</strong> 
                        <ul>
                            <li><strong>Raio ($r$):</strong> A distância do centro de um círculo exato até a borda.</li>
                            <li><strong>Diâmetro ($D$):</strong> A linha reta que vai de uma borda a outra passando pelo centro. O diâmetro é sempre o <strong>dobro do raio</strong>: $D = 2 \cdot r$.</li>
                        </ul>
                    </li>
                    <li><strong>O que é Escala?</strong> Quando você desenha sua casa ou um mapa numa folha de papel, você reduz o tamanho real mantendo as mesmas proporções. Ex: $1\text{ cm no papel} = 100\text{ metros na realidade}$.</li>
                </ul>
                <p><strong>Exemplo Terrestre Resolvido:</strong> Se uma bola de basquete tem $24\text{ cm}$ de diâmetro e uma bolinha de pingue-pongue tem $4\text{ cm}$, quantas bolinhas cabem no diâmetro da bola de basquete?<br>
                $\text{Razão} = \frac{24\text{ cm}}{4\text{ cm}} = 6$. Ou seja, a bola de basquete é <strong>6 vezes maior</strong>!</p>
            </div>
        """, unsafe_allow_html=True)
        
        # ETAPA 2: APLICAÇÃO NO ESPAÇO
        st.markdown(r"""
        ### 🚀 ETAPA 2: Como Usamos Isso na Astronomia?
        No espaço, os planetas são esferas gigantescas. Para podermos estudar o Sistema Solar na sala de aula ou criar maquetes, os astrônomos usam **escalas proporcionais**:
        - **Diâmetro da Terra ($D_{\text{Terra}}$):** $\approx 12.742\text{ km}$. Usamos a Terra como nossa **unidade de referência (1,0x)**.
        - **Lua:** $\approx 3.474\text{ km}$ ($\approx 0,27\text{x}$ ou pouco mais de $\frac{1}{4}$ da Terra).
        - **Marte:** $\approx 6.779\text{ km}$ ($\approx 0,53\text{x}$ ou cerca de metade da Terra).
        - **Júpiter:** $\approx 139.820\text{ km}$ ($\approx 11\text{x}$ o diâmetro da Terra!).
        - **Sol:** $\approx 1.392.700\text{ km}$ ($\approx 109\text{x}$ o diâmetro da Terra!).
        
        #### 💡 Fórmula da Escala de Maquetes:
        $$\text{Tamanho na Maquete (cm)} = \text{Diâmetro Real (km)} \times \text{Fator de Redução}$$
        """)
        
        # ETAPA 3: SIMULADOR
        st.markdown("### 🧮 ETAPA 3: Simulador Interativo de Escalas Planetárias")
        st.write("Defina o tamanho da **Terra** na sua maquete escolar e veja o tamanho exato dos outros astros:")
        
        scale_choice = st.selectbox(
            "Escolha o objeto para representar a Terra na maquete:",
            ["1 cm (Bolinha de gude pequena)", "5 cm (Bolinha de tênis)", "10 cm (Laranja grande)", "20 cm (Bola de futebol)"],
            key="math_l1_scale"
        )
        earth_cm = {"1 cm (Bolinha de gude pequena)": 1.0, "5 cm (Bolinha de tênis)": 5.0, "10 cm (Laranja grande)": 10.0, "20 cm (Bola de futebol)": 20.0}[scale_choice]
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("🌍 Terra", f"{earth_cm:.1f} cm", "Base da Escala (1,0x)")
        col2.metric("🌕 Lua", f"{(earth_cm * 0.27):.2f} cm", "0,27x da Terra")
        col3.metric("🔴 Marte", f"{(earth_cm * 0.53):.2f} cm", "0,53x da Terra")
        col4.metric("🪐 Júpiter", f"{(earth_cm * 11.2):.1f} cm", "11,2x da Terra!")
        
        st.info(f"☀️ **Impressionante:** Na sua maquete, para manter a proporção correta, o **Sol** precisaria ter **{(earth_cm * 109.2) / 100:.2f} metros** de largura!")
        
        # ETAPA 4: TESTES & EXERCÍCIOS
        st.markdown("### 📝 ETAPA 4: Testes de Fixação (Fundamento + Espaço)")
        
        # Exercício 1: Fundamento
        with st.container():
            st.markdown("""
                <div class='exercise-card'>
                    <span class='steam-tag math'>Desafio 1: Fundamento Matemático</span>
                    <h4>📐 Calculando Diâmetros e Raios</h4>
                    <p>Um astrônomo mirim mediu que o <strong>raio</strong> de uma lente de telescópio é de <strong>7,5 cm</strong>. Qual é o <strong>diâmetro</strong> dessa lente?</p>
                </div>
            """, unsafe_allow_html=True)
            
            q1_ans = st.radio("Selecione a resposta correta:", ["3,75 cm", "15,0 cm", "22,5 cm", "7,5 cm"], key="math_q1_l1")
            if st.button("Verificar Desafio 1", key="btn_math_q1_l1"):
                if q1_ans == "15,0 cm":
                    st.success("🎉 Correto! O diâmetro é sempre o dobro do raio: $D = 2 \times 7,5\text{ cm} = 15,0\text{ cm}$. (+15 XP)")
                    add_xp(user["id"], 15)
                else:
                    st.error("❌ Dica: Lembre-se que o diâmetro é $D = 2 \cdot r$. Multiplique o raio por 2!")
        
        # Exercício 2: Aplicação
        with st.container():
            st.markdown("""
                <div class='exercise-card' style='margin-top: 15px;'>
                    <span class='steam-tag math'>Desafio 2: Aplicação Astronômica</span>
                    <h4>🪐 Comparação de Escala Júpiter vs Terra</h4>
                    <p>Sabendo que o diâmetro da Terra é de cerca de <strong>12.700 km</strong> e o de Júpiter é de aproximadamente <strong>140.000 km</strong>, quantas Terras enfileiradas cabem aproximadamente no diâmetro de Júpiter?</p>
                </div>
            """, unsafe_allow_html=True)
            
            q2_ans = st.radio("Escolha a melhor aproximação:", ["Aproximadamente 3 Terras", "Aproximadamente 11 Terras", "Aproximadamente 50 Terras", "Aproximadamente 100 Terras"], key="math_q2_l1")
            if st.button("Verificar Desafio 2", key="btn_math_q2_l1"):
                if "11 Terras" in q2_ans:
                    st.success("🎉 Excelente! $\\frac{140.000}{12.700} \\approx 11,02$. Júpiter é tão colossal que cabem 11 Terras lado a lado pelo seu equador! (+20 XP)")
                    add_xp(user["id"], 20)
                    unlock_badge(user["id"], "steam_math_master")
                else:
                    st.error("❌ Tente novamente! Divida $140.000$ por $12.700$ para achar a razão.")

    # -------------------------------------------------------------------------
    # NÍVEL 2: MATEMÁTICA
    # -------------------------------------------------------------------------
    elif "Nível 2" in level:
        st.markdown("""
            <div class='level-badge explorer'>🟡 NÍVEL 2 — EXPLORADOR (7º A 9º ANO)</div>
            <h3 style='color: #38bdf8;'>Notação Científica, Potências de 10 e Tempo de Viagem da Luz</h3>
        """, unsafe_allow_html=True)
        
        # ETAPA 1: FUNDAMENTOS
        st.markdown(r"""
            <div class='fundamento-box'>
                <h4 style='color: #ffd166; margin-top:0;'>🧱 ETAPA 1: O FUNDAMENTO BÁSICO (Potências de 10 e Notação Científica)</h4>
                <p>Na ciência, trabalhamos com números com muitos zeros (como a distância até as estrelas ou o tamanho de uma bactéria). Para não nos perdermos em tantos zeros, usamos a <strong>Notação Científica</strong>:</p>
                <ul>
                    <li><strong>Regra da Notação Científica:</strong> Todo número é escrito na forma:
                        $$N = a \times 10^b$$
                        Onde <strong>$a$</strong> (chamado de mantissa) deve ser um número <strong>maior ou igual a 1 e menor que 10</strong> ($1 \le a < 10$), e <strong>$b$</strong> é o expoente inteiro (quantas casas a vírgula andou).
                    </li>
                    <li><strong>Exemplos do Dia a Dia:</strong>
                        <ul>
                            <li>$1.000$ (mil) $= 1,0 \times 10^3$ (a vírgula andou 3 casas para a esquerda).</li>
                            <li>$1.000.000$ (um milhão) $= 1,0 \times 10^6$.</li>
                            <li>$150.000.000$ (150 milhões) $= 1,5 \times 10^8$.</li>
                        </ul>
                    </li>
                    <li><strong>Cálculo de Tempo com Velocidade Média:</strong>
                        $$v = \frac{\Delta s}{\Delta t} \implies \Delta t = \frac{\Delta s}{v}$$
                        O tempo gasto ($\Delta t$) é simplesmente a distância ($\Delta s$) dividida pela velocidade ($v$).
                    </li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
        # ETAPA 2: APLICAÇÃO NO ESPAÇO
        st.markdown(r"""
        ### 🚀 ETAPA 2: A Velocidade da Luz e a Comunicação Espacial
        No vácuo do espaço, nada viaja mais rápido que a luz (e os sinais de rádio emitidos pelas nossas antenas).
        - **Velocidade da Luz ($c$):** $\approx 300.000\text{ km/s} = 3 \times 10^5\text{ km/s} = 3 \times 10^8\text{ m/s}$.
        - **Por que isso é vital?** Quando a NASA envia um comando de rádio para o Rover *Perseverance* em Marte, o comando não chega instantaneamente! O sinal viaja na velocidade da luz e demora minutos para chegar lá e mais minutos para a resposta voltar para a Terra.
        """)
        
        # ETAPA 3: SIMULADOR
        st.markdown("### 🧮 ETAPA 3: Simulador de Atraso de Sinal da Deep Space Network (DSN)")
        st.write("Calcule quanto tempo um sinal de rádio demora para ir da Terra até qualquer destino do Sistema Solar:")
        
        target_dist_options = {
            "🌕 Lua (Distância média)": 384400,
            "☀️ Sol (1 UA)": 149600000,
            "🔴 Marte (Aproximação Máxima)": 54600000,
            "🔴 Marte (Distância Média)": 225000000,
            "🔴 Marte (Distância Máxima)": 401000000,
            "🪐 Júpiter (Média)": 778000000,
            "🛰️ Sonda Voyager 1 (Fronteira Interestelar)": 24000000000
        }
        
        dest_choice = st.selectbox("Escolha o destino no espaço:", list(target_dist_options.keys()), index=3)
        dist_km = target_dist_options[dest_choice]
        c_speed = 300000 # km/s
        
        time_sec = dist_km / c_speed
        time_min = time_sec / 60
        time_hours = time_min / 60
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Distância em km", f"{dist_km:,.0f} km".replace(",", "."), f"{dist_km:.2e} em notação")
        c2.metric("Tempo Só de Ida (Luz/Rádio)", f"{time_min:.1f} minutos" if time_min < 60 else f"{time_hours:.2f} horas", f"{time_sec:.1f} segundos")
        c3.metric("Tempo de Ida e Volta (Ping)", f"{(time_min*2):.1f} min" if time_min < 60 else f"{(time_hours*2):.2f} horas", "Comunicação Total")
        
        st.caption("🛰️ É por causa desse atraso que os robôs em Marte precisam ser inteligentes e autônomos: não é possível pilotá-los com controle remoto em tempo real!")
        
        # ETAPA 4: TESTES
        st.markdown("### 📝 ETAPA 4: Testes de Fixação")
        with st.container():
            st.markdown("""
                <div class='exercise-card'>
                    <span class='steam-tag math'>Desafio 1: Fundamento de Notação</span>
                    <h4>📐 Escrevendo em Notação Científica</h4>
                    <p>A distância média da Terra à Lua é de <strong>384.400 km</strong>. Como esse número é corretamente escrito em notação científica?</p>
                </div>
            """, unsafe_allow_html=True)
            
            q1_n2 = st.radio("Escolha a opção correta:", ["38,44 x 10^4 km", "3,844 x 10^5 km", "3,844 x 10^6 km", "0,3844 x 10^6 km"], key="math_q1_l2")
            if st.button("Verificar Notação", key="btn_math_q1_l2"):
                if q1_n2 == "3,844 x 10^5 km":
                    st.success("🎉 Perfeito! A vírgula andou 5 casas para a esquerda e o número ficou entre 1 e 10: $3,844 \\times 10^5\\text{ km}$. (+20 XP)")
                    add_xp(user["id"], 20)
                else:
                    st.error("❌ Atenção: a mantissa deve estar entre 1 e 10 ($1 \\le a < 10$). Conte quantas casas a vírgula precisa andar!")
                    
        with st.container():
            st.markdown("""
                <div class='exercise-card' style='margin-top: 15px;'>
                    <span class='steam-tag math'>Desafio 2: Aplicação de Velocidade da Luz</span>
                    <h4>🚀 Tempo de Luz do Sol à Terra</h4>
                    <p>Sabendo que o Sol está a <strong>150.000.000 km</strong> de nós e a luz viaja a <strong>300.000 km/s</strong>, quanto tempo a luz solar leva para chegar à Terra?</p>
                </div>
            """, unsafe_allow_html=True)
            
            q2_n2 = st.radio("Selecione o tempo aproximado:", ["8 minutos e 20 segundos (500 s)", "1 minuto exato (60 s)", "1 hora e 15 minutos", "Instantâneo (0 segundos)"], key="math_q2_l2")
            if st.button("Verificar Tempo da Luz", key="btn_math_q2_l2"):
                if "8 minutos" in q2_n2:
                    st.success("🎉 Sensacional! $\\Delta t = \\frac{150.000.000}{300.000} = 500\\text{ segundos} = 8\\text{ minutos e } 20\\text{ segundos}$. A luz que você vê do Sol agora saiu de lá há 8 minutos! (+25 XP)")
                    add_xp(user["id"], 25)
                else:
                    st.error("❌ Dica: Divida $150.000.000$ por $300.000$ para obter os segundos, depois divida por 60 para achar os minutos.")

    # -------------------------------------------------------------------------
    # NÍVEL 3: MATEMÁTICA
    # -------------------------------------------------------------------------
    else:
        st.markdown("""
            <div class='level-badge astrophysicist'>🔴 NÍVEL 3 — ASTROFÍSICO (AVANÇADO / ENSINO MÉDIO)</div>
            <h3 style='color: #c084fc;'>Paralaxe Trigonométrica e a 3ª Lei de Kepler ($T^2 = a^3$)</h3>
        """, unsafe_allow_html=True)
        
        # ETAPA 1: FUNDAMENTOS
        st.markdown(r"""
            <div class='fundamento-box'>
                <h4 style='color: #ffd166; margin-top:0;'>🧱 ETAPA 1: O FUNDAMENTO BÁSICO (Trigonometria de Ângulos Pequenos & Relações de Potência)</h4>
                <p>Como medir a distância de algo sem ir até lá? Usamos <strong>Trigonometria</strong>!</p>
                <ul>
                    <li><strong>O Efeito Paralaxe no Dia a Dia:</strong> Estique seu braço, aponte o polegar para a frente e feche o olho esquerdo. Agora feche o direito e abra o esquerdo. O polegar parece "pular" em relação ao fundo da sala! O ângulo desse "pulo" diminui quanto mais longe o objeto estiver.</li>
                    <li><strong>Divisão de Graus em Segundos de Arco:</strong> 
                        $$1^\circ (\text{grau}) = 60' (\text{minutos de arco}) = 3.600'' (\text{segundos de arco})$$
                        $1''$ de arco é um ângulo tão incrivelmente minúsculo que equivale a ver a espessura de um fio de cabelo a 20 metros de distância!
                    </li>
                    <li><strong>Relações de Potência e Raízes:</strong> Se $y^2 = x^3$, então podemos isolar $y$ tirando a raiz quadrada: $y = \sqrt{x^3} = x^{3/2}$.</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
        # ETAPA 2: APLICAÇÃO NO ESPAÇO
        st.markdown(r"""
        ### 🚀 ETAPA 2: Como Astrônomos Medem Distâncias e Órbitas no Cosmos?
        1. **Paralaxe Estelar:** A Terra orbita o Sol com um diâmetro de base de $2\text{ UA}$. Observando uma estrela próxima em janeiro e depois em julho, ela "muda de posição" contra as estrelas de fundo. A distância $d$ em **Parsecs (pc)** é dada por:
        $$d\text{ (parsecs)} = \frac{1}{p\text{ (segundos de arco)}}$$
        *(Onde $1\text{ Parsec} \approx 3,26\text{ anos-luz} \approx 3,086 \times 10^{13}\text{ km}$)*.
        
        2. **3ª Lei de Johannes Kepler (Lei dos Períodos):** O quadrado do período orbital ($T$) em anos terrestres é exatamente igual ao cubo da distância média ao Sol ($a$) em Unidades Astronômicas:
        $$T^2 = a^3 \implies T = \sqrt{a^3}$$
        """)
        
        # ETAPA 3: SIMULADOR
        st.markdown("### 🧮 ETAPA 3: Calculadora de Kepler & Distância de Paralaxe")
        col_k1, col_k2 = st.columns(2)
        
        with col_k1:
            st.markdown("#### 🪐 Calculadora da 3ª Lei de Kepler")
            dist_ua = st.slider("Distância média do planeta ao Sol ($a$ em UA):", min_value=0.2, max_value=40.0, value=5.2, step=0.1)
            period_years = math.sqrt(dist_ua ** 3)
            st.metric("Período Orbital ($T$)", f"{period_years:.2f} Anos Terrestres", f"Equivale a {period_years*365.25:.0f} dias")
            st.caption(f"Verificação: $T^2 = {period_years**2:.2f}$ e $a^3 = {dist_ua**3:.2f}$ ✅")
            
        with col_k2:
            st.markdown("#### 🔭 Medidor de Paralaxe Estelar")
            parallax_arcsec = st.slider("Ângulo de Paralaxe medido ($p$ em segundos de arco ''):", min_value=0.01, max_value=1.0, value=0.768, step=0.01)
            dist_pc = 1.0 / parallax_arcsec
            dist_ly = dist_pc * 3.26156
            st.metric("Distância da Estrela ($d$)", f"{dist_pc:.2f} Parsecs", f"{dist_ly:.2f} Anos-Luz")
            st.caption("Exemplo: Próxima Centauri tem paralaxe de $\\approx 0,768''$ (a estrela mais perto de nós a 4,24 anos-luz).")
            
        # ETAPA 4: TESTES
        st.markdown("### 📝 ETAPA 4: Testes de Astrofísica")
        with st.container():
            st.markdown("""
                <div class='exercise-card'>
                    <span class='steam-tag math'>Desafio de Vanguarda: 3ª Lei de Kepler</span>
                    <h4>🪐 Calculando a Órbita de um Asteroide</h4>
                    <p>Um asteroide no cinturão principal orbita a uma distância média de <strong>$a = 4\text{ UA}$</strong> do Sol. Quantos anos terrestres ele leva para dar uma volta completa ao redor do Sol?</p>
                </div>
            """, unsafe_allow_html=True)
            
            q_k = st.radio("Escolha o período correto:", ["2 Anos", "4 Anos", "8 Anos ($T = \\sqrt{4^3} = \\sqrt{64}$)", "16 Anos"], key="math_q_kepler")
            if st.button("Verificar Órbita", key="btn_math_kepler"):
                if "8 Anos" in q_k:
                    st.success("🎉 Brilhante! $a^3 = 4^3 = 64$. O período é $T = \\sqrt{64} = 8\\text{ anos terrestres}$. (+30 XP)")
                    add_xp(user["id"], 30)
                else:
                    st.error("❌ Faça a conta: $4^3 = 4 \\times 4 \\times 4 = 64$. Depois tire a raiz quadrada de 64!")


# ==============================================================================
# ⚡ 2. TRILHA DE FÍSICA
# ==============================================================================
def _render_physics_track(user: dict):
    st.markdown("## ⚡ Física: Fundamentos da Mecânica & Forças do Universo")
    st.write("Aprenda as leis que regem o movimento dos objetos aqui na Terra e veja como elas governam foguetes, estrelas e buracos negros:")
    
    level = st.radio(
        "Selecione seu Nível de Treinamento:",
        [
            "🟢 Nível 1: Cadete (Fundamentos: Massa vs Peso, Força Gravitacional / 6º Ano)",
            "🟡 Nível 2: Explorador (Fundamentos: As 3 Leis de Newton e Propulsão de Foguetes / 7º-9º Ano)",
            "🔴 Nível 3: Astrofísico (Fundamentos: Relatividade, Velocidade da Luz e Buracos Negros / Avançado)"
        ],
        key="phys_level_select"
    )
    
    st.markdown("---")
    
    # -------------------------------------------------------------------------
    # NÍVEL 1: FÍSICA
    # -------------------------------------------------------------------------
    if "Nível 1" in level:
        st.markdown("""
            <div class='level-badge cadet'>🟢 NÍVEL 1 — CADETE (FUNDAMENTOS & 6º ANO)</div>
            <h3 style='color: #4ade80;'>Massa vs Peso e a Gravidade nos Corpos Celestes</h3>
        """, unsafe_allow_html=True)
        
        # ETAPA 1: FUNDAMENTOS
        st.markdown(r"""
            <div class='fundamento-box'>
                <h4 style='color: #ffd166; margin-top:0;'>🧱 ETAPA 1: O FUNDAMENTO BÁSICO (Massa NÃO É Peso!)</h4>
                <p>No dia a dia, as pessoas dizem: <em>"Eu vou me pesar na balança da farmácia para ver quantos quilos eu tenho"</em>. Em física, isso mistura dois conceitos bem diferentes:</p>
                <ul>
                    <li><strong>Massa ($m$):</strong> É a quantidade de matéria que forma o seu corpo (átomos, ossos, músculos). É medida em <strong>quilogramas (kg)</strong>. A sua massa <strong>NUNCA MUDA</strong>, não importa se você está na Terra, na Lua ou flutuando no vácuo!</li>
                    <li><strong>Peso ($P$ ou $F_g$):</strong> É a <strong>força de atração invisível</strong> com que a gravidade de um planeta puxa a sua massa para o chão. Como é uma força, o peso é medido na unidade científica chamada <strong>Newton (N)</strong>.</li>
                    <li><strong>A Fórmula Fundamental do Peso:</strong>
                        $$P = m \cdot g$$
                        Onde $m$ é sua massa (kg) e $g$ é a aceleração da gravidade local ($\text{m/s}^2$).
                    </li>
                    <li><strong>Na Terra:</strong> A gravidade média é de $g \approx 9,8\text{ m/s}^2$ (geralmente arredondada para $10\text{ m/s}^2$ nos exercícios escolares). Assim, uma pessoa com massa de $50\text{ kg}$ tem um peso de $P = 50 \times 9,8 = 490\text{ N}$.</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
        # ETAPA 2: APLICAÇÃO NO ESPAÇO
        st.markdown(r"""
        ### 🚀 ETAPA 2: Como Funciona a Gravidade em Outros Mundos?
        A gravidade de um planeta depende da sua **massa total** e do seu **raio**. Planetas menores ou menos densos puxam você com menos força; planetas gigantescos puxam com muito mais força!
        - **Lua:** Gravidade fraca ($g \approx 1,62\text{ m/s}^2$, cerca de $\frac{1}{6}$ da Terra). Por isso os astronautas da Apollo saltitavam como se fossem penas!
        - **Marte:** Gravidade intermediária ($g \approx 3,71\text{ m/s}^2$, cerca de $38\%$ da Terra).
        - **Júpiter:** Gravidade esmagadora ($g \approx 24,79\text{ m/s}^2$, cerca de $2,5\text{x}$ a da Terra).
        """)
        
        # ETAPA 3: SIMULADOR
        st.markdown("### 🧮 ETAPA 3: Balança & Pulo Interplanetário")
        st.write("Digite sua massa terrestre e veja quanto você pesaria e qual a altura do seu salto em outros mundos:")
        
        user_mass = st.number_input("Sua massa na Terra (em kg):", min_value=10.0, max_value=200.0, value=50.0, step=1.0, key="phys_user_mass")
        earth_jump_cm = 40.0 # salto normal de 40 cm
        
        gravity_table = {
            "🌍 Terra": 9.81,
            "🌕 Lua": 1.62,
            "🔴 Marte": 3.71,
            "🪐 Júpiter": 24.79,
            "☄️ Cometa 67P": 0.001
        }
        
        cols = st.columns(5)
        for i, (world, g_val) in enumerate(gravity_table.items()):
            weight_n = user_mass * g_val
            weight_kg_equivalent = weight_n / 9.81
            jump_cm = (earth_jump_cm * 9.81) / g_val
            
            with cols[i]:
                st.markdown(f"**{world}**")
                st.metric("Força Peso", f"{weight_n:.1f} N", f"{weight_kg_equivalent:.1f} kgf")
                st.metric("Salto Máximo", f"{jump_cm:.0f} cm" if jump_cm < 1000 else f"{jump_cm/100:.1f} m")
                
        # ETAPA 4: TESTES
        st.markdown("### 📝 ETAPA 4: Testes de Fixação")
        with st.container():
            st.markdown("""
                <div class='exercise-card'>
                    <span class='steam-tag physics'>Desafio 1: Fundamento Massa vs Peso</span>
                    <h4>⚡ O que acontece com um astronauta na Lua?</h4>
                    <p>Uma astronauta com massa de <strong>60 kg</strong> na Terra viaja em uma missão para a Lua. Ao chegar na superfície lunar, qual é a sua <strong>massa</strong>?</p>
                </div>
            """, unsafe_allow_html=True)
            
            q_mass = st.radio("Escolha a resposta correta:", ["10 kg (diminui 6 vezes)", "60 kg (a massa permanece exatamente a mesma!)", "360 kg (aumenta 6 vezes)", "0 kg (fica sem massa)"], key="phys_q_mass_l1")
            if st.button("Verificar Massa", key="btn_phys_mass"):
                if "permanece exatamente a mesma" in q_mass:
                    st.success("🎉 Exato! A massa é a quantidade de matéria do corpo e não muda nunca. O que muda na Lua é o PESO (a força da gravidade)! (+20 XP)")
                    add_xp(user["id"], 20)
                else:
                    st.error("❌ Cuidado com a pegadinha! A massa é constante em qualquer lugar do universo.")
                    
        with st.container():
            st.markdown("""
                <div class='exercise-card' style='margin-top: 15px;'>
                    <span class='steam-tag physics'>Desafio 2: Aplicação do Peso Lunar</span>
                    <h4>🌕 Calculando o Peso na Lua</h4>
                    <p>Sabendo que a gravidade na Lua é $g_{\text{Lua}} \approx 1,6\text{ m/s}^2$, qual é a força peso ($P = m \cdot g$) dessa astronauta de <strong>60 kg</strong> na Lua?</p>
                </div>
            """, unsafe_allow_html=True)
            
            q_peso = st.radio("Selecione o valor do peso em Newtons:", ["60 N", "96 N ($60 \times 1,6$)", "588 N", "600 N"], key="phys_q_peso_l1")
            if st.button("Verificar Peso Lunar", key="btn_phys_peso"):
                if "96 N" in q_peso:
                    st.success("🎉 Perfeito! $P = 60\text{ kg} \times 1,6\text{ m/s}^2 = 96\text{ N}$. Na Terra ela pesava $\\approx 588\text{ N}$, ou seja, na Lua ela se sente 6 vezes mais leve! (+25 XP)")
                    add_xp(user["id"], 25)
                    unlock_badge(user["id"], "steam_phys_master")
                else:
                    st.error("❌ Multiplique a massa (60) pela gravidade da Lua (1,6).")

    # -------------------------------------------------------------------------
    # NÍVEL 2: FÍSICA
    # -------------------------------------------------------------------------
    elif "Nível 2" in level:
        st.markdown("""
            <div class='level-badge explorer'>🟡 NÍVEL 2 — EXPLORADOR (7º A 9º ANO)</div>
            <h3 style='color: #38bdf8;'>As 3 Leis de Newton e a Propulsão Espacial de Tsiolkovsky</h3>
        """, unsafe_allow_html=True)
        
        # ETAPA 1: FUNDAMENTOS
        st.markdown(r"""
            <div class='fundamento-box'>
                <h4 style='color: #ffd166; margin-top:0;'>🧱 ETAPA 1: O FUNDAMENTO BÁSICO (As 3 Leis do Movimento de Isaac Newton)</h4>
                <p>O cientista inglês Isaac Newton descobriu as 3 regras fundamentais que regem todo o movimento no Universo:</p>
                <ol>
                    <li><strong>1ª Lei (Lei da Inércia):</strong> Um corpo parado tende a ficar parado. Um corpo em movimento retilíneo uniforme tende a continuar se movendo em linha reta para sempre, a menos que uma força externa atue sobre ele (como o atrito do ar ou o chão).</li>
                    <li><strong>2ª Lei (Princípio Fundamental da Dinâmica):</strong>
                        $$F = m \cdot a$$
                        A força resultante ($F$) aplicada a um objeto gera uma aceleração ($a$) proporcional à sua massa ($m$). Quanto mais pesado um carro, maior a força necessária para acelerá-lo!
                    </li>
                    <li><strong>3ª Lei (Ação e Reação):</strong>
                        $$\vec{F}_{\text{ação}} = -\vec{F}_{\text{reação}}$$
                        Para toda força de ação que você aplica em um objeto, ele aplica de volta em você uma força de <strong>mesma intensidade, mesma direção e sentido contrário</strong>.<br>
                        <em>Exemplo na Terra:</em> Quando você pula de skate para frente (ação), o skate é empurrado para trás (reação)! Quando você nada, você empurra a água para trás e ela empurra você para frente.
                    </li>
                </ol>
            </div>
        """, unsafe_allow_html=True)
        
        # ETAPA 2: APLICAÇÃO NO ESPAÇO
        st.markdown(r"""
        ### 🚀 ETAPA 2: Como Foguetes se Movem no Vácuo sem Ter Onde se Apoiar?
        Muita gente pensa erroneamente que um foguete precisa "empurrar o ar" para subir. No vácuo do espaço, não há ar! Como ele acelera?
        - **Pela 3ª Lei de Newton pura!** O motor do foguete queima combustível e ejeta gases em altíssima velocidade para trás (ação). Pela reação imediata, a nave é empurrada para a frente com a mesma força!
        - **A Equação do Foguete de Tsiolkovsky:**
        $$\Delta v = v_e \cdot \ln\left(\frac{m_0}{m_f}\right)$$
        Onde $\Delta v$ é o ganho de velocidade da nave, $v_e$ é a velocidade de escape dos gases e $\frac{m_0}{m_f}$ é a razão entre a massa inicial (cheia de combustível) e a massa final (vazia).
        """)
        
        # ETAPA 3: SIMULADOR
        st.markdown("### 🧮 ETAPA 3: Simulador de Propulsão & Delta-V ($\Delta v$)")
        col_prop1, col_prop2 = st.columns(2)
        
        with col_prop1:
            fuel_pct = st.slider("Porcentagem de Combustível da Nave (%):", min_value=10, max_value=95, value=85, step=5)
            engine_type = st.selectbox(
                "Tipo de Propulsor:",
                ["Químico Tradicional (Metano/Oxigênio - $v_e = 3.500$ m/s)", "Motor Iônico Elétrico (Plasma de Xenônio - $v_e = 30.000$ m/s)"]
            )
            ve = 3500 if "Químico" in engine_type else 30000
            
        with col_prop2:
            m0 = 100.0 # base 100 toneladas
            mf = 100.0 - fuel_pct
            delta_v = ve * math.log(m0 / mf)
            
            st.metric("Velocidade Final Ganha ($\Delta v$)", f"{delta_v / 1000:.2f} km/s", f"{delta_v:.0f} m/s")
            if delta_v >= 11200:
                st.success("🚀 Velocidade suficiente para ESCAPAR da órbita da Terra e viajar pelo Sistema Solar! ($> 11,2$ km/s)")
            elif delta_v >= 7800:
                st.info("🛰️ Velocidade suficiente para entrar em ÓRBITA BAIXA da Terra ($7,8$ km/s)")
            else:
                st.warning("⚠️ Velocidade insuficiente para entrar em órbita. O foguete cairia de volta na Terra!")
                
        # ETAPA 4: TESTES
        st.markdown("### 📝 ETAPA 4: Testes de Fixação")
        with st.container():
            st.markdown("""
                <div class='exercise-card'>
                    <span class='steam-tag physics'>Desafio: A 3ª Lei de Newton no Espaço</span>
                    <h4>🚀 O Astronauta com o Extintor no Vácuo</h4>
                    <p>Um astronauta está flutuando em repouso no espaço fora da Estação Espacial. Ele aciona um extintor de gás para a sua DIREITA. O que acontece com o astronauta?</p>
                </div>
            """, unsafe_allow_html=True)
            
            q_newt = st.radio("Qual é a consequência física?", ["Ele fica parado porque não tem ar no vácuo", "Ele é empurrado para a ESQUERDA com força de mesma intensidade", "Ele é puxado para a DIREITA junto com o gás", "Ele começa a girar em círculos infinitos"], key="phys_q_newton")
            if st.button("Verificar 3ª Lei", key="btn_phys_newton"):
                if "para a ESQUERDA" in q_newt:
                    st.success("🎉 Perfeito! Pelo princípio da Ação e Reação, ao ejetar massa para a direita (ação), o corpo do astronauta recebe uma força igual e oposta para a esquerda (reação). (+25 XP)")
                    add_xp(user["id"], 25)
                else:
                    st.error("❌ Lembre-se: Ação e reação têm sentidos OPOSTOS!")

    # -------------------------------------------------------------------------
    # NÍVEL 3: FÍSICA
    # -------------------------------------------------------------------------
    else:
        st.markdown("""
            <div class='level-badge astrophysicist'>🔴 NÍVEL 3 — ASTROFÍSICO (AVANÇADO / ENSINO MÉDIO)</div>
            <h3 style='color: #c084fc;'>Relatividade de Einstein, Dilatação Temporal e Buracos Negros</h3>
        """, unsafe_allow_html=True)
        
        # ETAPA 1: FUNDAMENTOS
        st.markdown(r"""
            <div class='fundamento-box'>
                <h4 style='color: #ffd166; margin-top:0;'>🧱 ETAPA 1: O FUNDAMENTO BÁSICO (Referenciais e a Constância da Luz)</h4>
                <p>Em 1905 e 1915, Albert Einstein revolucionou a física ao mostrar que o tempo e o espaço não são absolutos:</p>
                <ul>
                    <li><strong>O Postulado da Velocidade da Luz:</strong> A velocidade da luz no vácuo ($c \approx 300.000\text{ km/s}$) é exatamente a mesma para <strong>qualquer observador</strong>, independentemente da velocidade com que você esteja se movendo!</li>
                    <li><strong>O Fator de Lorentz ($\gamma$):</strong> Quando um objeto viaja próximo à velocidade da luz, o tempo passa mais devagar para ele e o comprimento se contrai:
                        $$\gamma = \frac{1}{\sqrt{1 - \frac{v^2}{c^2}}}$$
                    </li>
                    <li><strong>Dilatação Temporal ($\Delta t'$):</strong>
                        $$\Delta t' = \gamma \cdot \Delta t_0 = \frac{\Delta t_0}{\sqrt{1 - \frac{v^2}{c^2}}}$$
                        Onde $\Delta t_0$ é o tempo medido por quem viaja na nave e $\Delta t'$ é o tempo transcorrido para quem ficou parado na Terra!
                    </li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
        # ETAPA 2: APLICAÇÃO NO ESPAÇO
        st.markdown(r"""
        ### 🚀 ETAPA 2: A Física do Filme *Interestelar* e os Buracos Negros
        1. **Dilatação Gravitacional do Tempo:** A gravidade extrema não atrai apenas matéria: ela curva a própria malha do **Espaço-Tempo**. Quanto mais perto você estiver de uma massa monstruosa (como o buraco negro *Gargantua*), mais devagar os seus segundos transcorrem em relação a quem está longe! No filme, 1 hora no planeta de Miller equivalia a 7 anos na Terra.
        2. **Raio de Schwarzschild ($R_s$ - O Horizonte de Eventos):** Se você comprimir qualquer massa $M$ abaixo do seu raio crítico, nem a luz consegue escapar da sua gravidade:
        $$R_s = \frac{2 \cdot G \cdot M}{c^2}$$
        *(Onde $G = 6,674 \times 10^{-11}\text{ N}\cdot\text{m}^2/\text{kg}^2$ e $c = 3 \times 10^8\text{ m/s}$)*.
        """)
        
        # ETAPA 3: SIMULADOR
        st.markdown("### 🧮 ETAPA 3: Simulador Relativístico de Dilatação Temporal")
        v_speed_pct = st.slider("Velocidade da sua espaçonave (% da velocidade da luz $c$):", min_value=0.0, max_value=99.9, value=90.0, step=0.5)
        
        beta = v_speed_pct / 100.0
        gamma = 1.0 / math.sqrt(max(1e-9, 1.0 - beta**2))
        
        st.metric("Fator de Dilatação ($\gamma$)", f"{gamma:.3f}x mais lento", f"Nave a {beta*300000:,.0f} km/s")
        
        col_rel1, col_rel2 = st.columns(2)
        with col_rel1:
            st.markdown("#### 🚀 Viagem de 1 Ano a Bordo:")
            st.write(f"- Para você dentro da nave: **1 ano** de vida e envelhecimento.")
            st.write(f"- Para quem ficou na Terra esperando: **{gamma:.2f} anos** já se passaram!")
        with col_rel2:
            st.markdown("#### 🕳️ Raio de Schwarzschild da Terra:")
            r_earth_blackhole = (2 * 6.674e-11 * 5.972e24) / ((3e8)**2)
            st.write(f"Se toda a massa da Terra fosse comprimida em um buraco negro, seu horizonte de eventos teria apenas **{r_earth_blackhole*1000:.1f} milímetros** (o tamanho de uma bola de gude!).")
            
        # ETAPA 4: TESTES
        st.markdown("### 📝 ETAPA 4: Testes de Astrofísica Relativística")
        with st.container():
            st.markdown("""
                <div class='exercise-card'>
                    <span class='steam-tag physics'>Desafio: Relatividade de Einstein</span>
                    <h4>🕳️ A Dilatação Temporal em Interestelar</h4>
                    <p>Por que os astronautas envelhecem mais devagar perto do buraco negro supermassivo do que as pessoas na Terra?</p>
                </div>
            """, unsafe_allow_html=True)
            
            q_ein = st.radio("Selecione o motivo físico correto:", [
                "Porque a gravidade extrema desacelera a passagem do tempo no tecido do espaço-tempo",
                "Porque o relógio quebrou devido à radiação",
                "Porque no espaço não existe dia e noite para contar as horas",
                "Porque a temperatura no vácuo congela o tempo"
            ], key="phys_q_einstein")
            if st.button("Verificar Relatividade", key="btn_phys_einstein"):
                if "desacelera a passagem do tempo" in q_ein:
                    st.success("🎉 Extraordinário! A Relatividade Geral de Einstein prevê que campos gravitacionais intensos curvam o espaço-tempo, fazendo com que o tempo flua mais lentamente. (+30 XP)")
                    add_xp(user["id"], 30)
                else:
                    st.error("❌ Revise a teoria: A curvatura do espaço-tempo pela gravidade é o que altera o ritmo do tempo!")


# ==============================================================================
# 🧪 3. TRILHA DE QUÍMICA
# ==============================================================================
def _render_chemistry_track(user: dict):
    st.markdown("## 🧪 Química: Fundamentos da Matéria & Astroquímica Estelar")
    st.write("Entenda a estrutura dos átomos e das reações químicas na Terra e viaje até a forja estelar e a atmosfera de outros mundos:")
    
    level = st.radio(
        "Selecione seu Nível de Treinamento:",
        [
            "🟢 Nível 1: Cadete (Fundamentos: Átomos, Elementos e a Forja Estelar / 6º Ano)",
            "🟡 Nível 2: Explorador (Fundamentos: Moléculas, Reações e Química em Marte / 7º-9º Ano)",
            "🔴 Nível 3: Astrofísico (Fundamentos: Espectro Eletromagnético e Bioassinaturas em Exoplanetas / Avançado)"
        ],
        key="chem_level_select"
    )
    
    st.markdown("---")
    
    # -------------------------------------------------------------------------
    # NÍVEL 1: QUÍMICA
    # -------------------------------------------------------------------------
    if "Nível 1" in level:
        st.markdown("""
            <div class='level-badge cadet'>🟢 NÍVEL 1 — CADETE (FUNDAMENTOS & 6º ANO)</div>
            <h3 style='color: #4ade80;'>Átomos, Elementos Químicos e a Forja Estelar</h3>
        """, unsafe_allow_html=True)
        
        # ETAPA 1: FUNDAMENTOS
        st.markdown(r"""
            <div class='fundamento-box'>
                <h4 style='color: #ffd166; margin-top:0;'>🧱 ETAPA 1: O FUNDAMENTO BÁSICO (O que é a Matéria e o Átomo?)</h4>
                <p>Tudo o que você pode tocar, cheirar ou ver — a água, seu cachorro, o ar e as estrelas — é feito de <strong>Átomos</strong>:</p>
                <ul>
                    <li><strong>Estrutura do Átomo:</strong>
                        <ul>
                            <li><strong>Núcleo Central:</strong> Contém <strong>Prótons</strong> (com carga elétrica positiva $+$) e <strong>Nêutrons</strong> (neutros, sem carga).</li>
                            <li><strong>Eletrosfera:</strong> Uma nuvem de <strong>Elétrons</strong> (carga negativa $-$) que giram em altíssima velocidade ao redor do núcleo.</li>
                        </ul>
                    </li>
                    <li><strong>O que define um Elemento Químico?</strong> É o <strong>Número Atômico ($Z$)</strong>, que é simplesmente a quantidade de prótons no núcleo!
                        <ul>
                            <li>$Z = 1$ (1 próton): <strong>Hidrogênio (H)</strong> — o elemento mais leve e abundante.</li>
                            <li>$Z = 2$ (2 prótons): <strong>Hélio (He)</strong> — o gás dos balões de festa.</li>
                            <li>$Z = 6$ (6 prótons): <strong>Carbono (C)</strong> — a base de toda a vida orgânica na Terra.</li>
                            <li>$Z = 8$ (8 prótons): <strong>Oxigênio (O)</strong> — o gás que respiramos.</li>
                            <li>$Z = 26$ (26 prótons): <strong>Ferro (Fe)</strong> — metal resistente presente no sangue e nas rochas.</li>
                        </ul>
                    </li>
                    <li><strong>Os 4 Estados da Matéria:</strong> Sólido (gelo), Líquido (água), Gasoso (vapor) e <strong>Plasma</strong> (gás tão quente que os elétrons se soltam dos núcleos — é o estado das estrelas e do Sol!).</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
        # ETAPA 2: APLICAÇÃO NO ESPAÇO
        st.markdown(r"""
        ### 🚀 ETAPA 2: A Forja Estelar — De Onde Vieram os Átomos do seu Corpo?
        Quando o Universo começou no Big Bang, só existiam basicamente Hidrogênio e Hélio. Onde foram criados o oxigênio que você respira, o carbono dos seus músculos, o cálcio dos seus dentes e o ferro do seu sangue?
        - **No coração das Estrelas!**
        - Sob temperaturas de dezenas de milhões de graus, os núcleos de hidrogênio colidem e se fundem (**Fusão Nuclear**), criando hélio:
        $$4 \text{ } ^1\text{H} \longrightarrow \text{ } ^4\text{He} + \text{Energia}$$
        - Quando estrelas gigantes morrem em explosões colossais chamadas **Supernovas**, elas espalham todos esses elementos pelo espaço. Por isso, como dizia o astrônomo Carl Sagan: *"Nós somos poeira de estrelas!"*
        """)
        
        # ETAPA 3: SIMULADOR
        st.markdown("### 🧮 ETAPA 3: Simulador do Reator de Fusão Estelar")
        st.write("Aumente a temperatura no núcleo da estrela e veja que elementos químicos ela consegue fabricar:")
        
        core_temp = st.slider("Temperatura no Núcleo Estelar (em Milhões de Graus Celsius):", min_value=1, max_value=3000, value=15, step=5)
        
        if core_temp < 10:
            st.info("❄️ Temperatura baixa: A estrela ainda não acendeu a fusão nuclear. É uma Protoestrela ou Anã Marrom.")
        elif core_temp < 100:
            st.success(f"☀️ **Temperatura de {core_temp} Milhões de °C:** Fusão ativa de **Hidrogênio em Hélio ($H \\rightarrow He$)**! É a fase atual do nosso Sol.")
        elif core_temp < 600:
            st.warning(f"🔴 **Temperatura de {core_temp} Milhões de °C (Gigante Vermelha):** Fusão de **Hélio em Carbono e Oxigênio ($He \\rightarrow C + O$)**!")
        elif core_temp < 2000:
            st.error(f"🔥 **Temperatura de {core_temp} Milhões de °C (Supergigante):** Fusão de elementos pesados: **Neônio, Magnésio, Silício até FERRO ($Fe$)**!")
        else:
            st.markdown(f"""
                <div style='background: rgba(247,37,133,0.2); border: 1px solid #f72585; padding: 15px; border-radius: 10px;'>
                    💥 <strong>SUPERNOVA / KILONOVA ({core_temp} Milhões de °C):</strong> A estrela explode! A energia descomunal forja elementos como <strong>Ouro ($Au$), Platina ($Pt$) e Urânio ($U$)</strong> e os espalha pela galáxia!
                </div>
            """, unsafe_allow_html=True)
            
        # ETAPA 4: TESTES
        st.markdown("### 📝 ETAPA 4: Testes de Fixação")
        with st.container():
            st.markdown("""
                <div class='exercise-card'>
                    <span class='steam-tag chem'>Desafio 1: Fundamento da Estrutura Atômica</span>
                    <h4>🧪 O que define qual é o elemento químico?</h4>
                    <p>Se um átomo possui exatamente <strong>6 prótons</strong> em seu núcleo, qual elemento químico ele é na Tabela Periódica?</p>
                </div>
            """, unsafe_allow_html=True)
            
            q_elem = st.radio("Escolha o elemento:", ["Hidrogênio ($Z=1$)", "Carbono ($Z=6$)", "Oxigênio ($Z=8$)", "Ferro ($Z=26$)"], key="chem_q_elem_l1")
            if st.button("Verificar Elemento", key="btn_chem_elem"):
                if "Carbono" in q_elem:
                    st.success("🎉 Correto! O número de prótons ($Z$) define a identidade do elemento. $Z=6$ é sempre o Carbono, a base da vida! (+20 XP)")
                    add_xp(user["id"], 20)
                else:
                    st.error("❌ Verifique a lista acima: $Z=6$ corresponde ao Carbono.")
                    
        with st.container():
            st.markdown("""
                <div class='exercise-card' style='margin-top: 15px;'>
                    <span class='steam-tag chem'>Desafio 2: Aplicação na Forja Estelar</span>
                    <h4>⭐ Onde foram forjados o ouro e a platina do universo?</h4>
                    <p>Os elementos mais pesados que o ferro, como o <strong>ouro</strong> das joias e a <strong>platina</strong> dos satélites, foram criados em qual processo cósmico?</p>
                </div>
            """, unsafe_allow_html=True)
            
            q_gold = st.radio("Escolha a origem cósmica:", [
                "No núcleo de planetas rochosos como a Terra",
                "Em explosões violentas de Supernovas e colisão de Estrelas de Nêutrons (Kilonovas)",
                "No vácuo frio do espaço entre as galáxias",
                "Na queima de fogo com madeira na Terra"
            ], key="chem_q_gold_l1")
            if st.button("Verificar Origem do Ouro", key="btn_chem_gold"):
                if "Supernovas" in q_gold:
                    st.success("🎉 Extraordinário! O ouro das alianças e circuitos eletrônicos só pôde nascer na explosão cataclísmica de estrelas gigantes! (+25 XP)")
                    add_xp(user["id"], 25)
                    unlock_badge(user["id"], "steam_chem_master")
                else:
                    st.error("❌ Revise o simulador de fusão: elementos além do ferro precisam de explosões de supernovas!")

    # -------------------------------------------------------------------------
    # NÍVEL 2: QUÍMICA
    # -------------------------------------------------------------------------
    elif "Nível 2" in level:
        st.markdown("""
            <div class='level-badge explorer'>🟡 NÍVEL 2 — EXPLORADOR (7º A 9º ANO)</div>
            <h3 style='color: #38bdf8;'>Moléculas, Reações Químicas e Sobrevivência em Marte (*Perdido em Marte*)</h3>
        """, unsafe_allow_html=True)
        
        # ETAPA 1: FUNDAMENTOS
        st.markdown(r"""
            <div class='fundamento-box'>
                <h4 style='color: #ffd166; margin-top:0;'>🧱 ETAPA 1: O FUNDAMENTO BÁSICO (Moléculas e a Lei da Conservação da Massa)</h4>
                <p>Quando átomos se juntam, eles formam <strong>Moléculas</strong> por meio de ligações químicas:</p>
                <ul>
                    <li><strong>Moléculas Importantes:</strong>
                        <ul>
                            <li>$\text{H}_2\text{O}$: Água (2 átomos de Hidrogênio + 1 de Oxigênio).</li>
                            <li>$\text{CO}_2$: Dióxido de Carbono (1 Carbono + 2 Oxigênios) — gás presente no ar e abundante na atmosfera de Marte.</li>
                            <li>$\text{O}_2$: Gás Oxigênio respirável (2 átomos de Oxigênio).</li>
                            <li>$\text{CH}_4$: Metano (1 Carbono + 4 Hidrogênios) — gás combustível poderoso!</li>
                        </ul>
                    </li>
                    <li><strong>Lei de Lavoisier (Conservação das Massas):</strong>
                        <blockquote><em>"Na natureza nada se cria, nada se perde, tudo se transforma."</em></blockquote>
                        Em qualquer reação química, o número total de átomos dos <strong>Reagentes</strong> (à esquerda da seta) tem que ser rigorosamente igual ao número de átomos dos <strong>Produtos</strong> (à direita da seta).
                    </li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
        # ETAPA 2: APLICAÇÃO NO ESPAÇO
        st.markdown(r"""
        ### 🚀 ETAPA 2: Como Gerar Oxigênio e Combustível em Marte?
        No livro e filme *Perdido em Marte* (e nas missões reais da NASA com o experimento MOXIE do rover Perseverance), os astronautas usam reações químicas reais para não morrerem sufocados:
        
        1. **Reação de Sabatier (Produz Água e Metano a partir do $\text{CO}_2$ marciano):**
        $$\text{CO}_2 + 4\text{H}_2 \longrightarrow \text{CH}_4 + 2\text{H}_2\text{O}$$
        2. **Eletrólise da Água (Divide a água em Oxigênio para respirar e Hidrogênio):**
        $$2\text{H}_2\text{O} \xrightarrow{\text{Eletricidade}} 2\text{H}_2 + \text{O}_2$$
        """)
        
        # ETAPA 3: SIMULADOR
        st.markdown("### 🧮 ETAPA 3: Simulador de Suporte de Vida do Habitat Marciano")
        st.write("Ajuste a quantidade de $\text{CO}_2$ capturado da atmosfera de Marte para alimentar os colonizadores:")
        
        co2_kg = st.slider("Dióxido de Carbono ($\text{CO}_2$) capturado (kg/dia):", min_value=1.0, max_value=50.0, value=10.0, step=1.0)
        
        # Estequiometria:
        # CO2 (44g/mol) + 4 H2 (8g/mol) -> CH4 (16g/mol) + 2 H2O (36g/mol)
        water_produced_kg = (co2_kg / 44.0) * 36.0
        methane_produced_kg = (co2_kg / 44.0) * 16.0
        # Eletrólise da água: 2 H2O (36g) -> 2 H2 (4g) + O2 (32g)
        o2_produced_kg = (water_produced_kg / 36.0) * 32.0
        
        c_m1, c_m2, c_m3 = st.columns(3)
        c_m1.metric("💧 Água Gerada ($\text{H}_2\text{O}$)", f"{water_produced_kg:.2f} kg/dia", "Reação de Sabatier")
        c_m2.metric("🫁 Oxigênio Puro ($\text{O}_2$)", f"{o2_produced_kg:.2f} kg/dia", f"Suporta {o2_produced_kg / 0.84:.1f} astronautas")
        c_m3.metric("🔥 Metano ($\text{CH}_4$)", f"{methane_produced_kg:.2f} kg/dia", "Combustível de Foguete")
        
        st.caption("ℹ️ Um ser humano adulto consome em média $\\approx 0,84\\text{ kg}$ de $\\text{O}_2$ puro por dia para respirar.")
        
        # ETAPA 4: TESTES
        st.markdown("### 📝 ETAPA 4: Testes de Fixação")
        with st.container():
            st.markdown("""
                <div class='exercise-card'>
                    <span class='steam-tag chem'>Desafio: Balanceamento Químico</span>
                    <h4>🧪 Balanceando a Eletrólise da Água</h4>
                    <p>Na reação de eletrólise $2\text{H}_2\text{O} \rightarrow 2\text{H}_2 + \text{X}$, qual molécula é representada por <strong>$\text{X}$</strong> para manter o equilíbrio de átomos de Lavoisier?</p>
                </div>
            """, unsafe_allow_html=True)
            
            q_elet = st.radio("Selecione a molécula que completa a equação:", ["$\text{CO}_2$", "$\text{O}_2$ (Gás Oxigênio)", "$\text{N}_2$ (Nitrogênio)", "$\text{O}_3$ (Ozônio)"], key="chem_q_eletrolise")
            if st.button("Verificar Balanceamento", key="btn_chem_elet"):
                if "\\text{O}_2" in q_elet:
                    st.success("🎉 Excelente! Temos 4 Hidrogênios e 2 Oxigênios nos reagentes ($2\\text{H}_2\\text{O}$). Nos produtos temos $2\\text{H}_2$ (4 hidrogênios), logo sobram 2 oxigênios formando uma molécula de $\\text{O}_2$. (+25 XP)")
                    add_xp(user["id"], 25)
                else:
                    st.error("❌ Conte os átomos: $2\\text{H}_2\\text{O}$ tem 2 átomos de Oxigênio. Como eles se combinam nos produtos?")

    # -------------------------------------------------------------------------
    # NÍVEL 3: QUÍMICA
    # -------------------------------------------------------------------------
    else:
        st.markdown("""
            <div class='level-badge astrophysicist'>🔴 NÍVEL 3 — ASTROFÍSICO (AVANÇADO / ENSINO MÉDIO)</div>
            <h3 style='color: #c084fc;'>Espectroscopia de Fraunhofer e Bioassinaturas em Exoplanetas</h3>
        """, unsafe_allow_html=True)
        
        # ETAPA 1: FUNDAMENTOS
        st.markdown(r"""
            <div class='fundamento-box'>
                <h4 style='color: #ffd166; margin-top:0;'>🧱 ETAPA 1: O FUNDAMENTO BÁSICO (Ondas de Luz e Níveis Quânticos de Energia)</h4>
                <p>Como os astrônomos sabem do que uma estrela ou um planeta distante a trilhões de quilômetros é feito sem nunca terem ido lá?</p>
                <ul>
                    <li><strong>A Luz como Onda e Partícula:</strong> A luz branca do Sol contém todas as cores do arco-íris, cada uma com seu <strong>comprimento de onda ($\lambda$)</strong> e energia:
                        $$E = h \cdot f = \frac{h \cdot c}{\lambda}$$
                    </li>
                    <li><strong>A "Impressão Digital" dos Átomos:</strong> No modelo atômico de Bohr, os elétrons giram em camadas com energias fixas. Quando um elétron é atingido por luz, ele só consegue absorver fótons que tenham <strong>exatamente a quantidade de energia necessária</strong> para ele pular de camada.</li>
                    <li><strong>Linhas de Absorção:</strong> Quando a luz passa por um gás (como a atmosfera de um planeta), certos comprimentos de onda específicos são absorvidos, deixando "linhas pretas" no arco-íris contínuo. Cada elemento e molécula tem um conjunto único de linhas — é o seu **código de barras químico**!</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
        # ETAPA 2: APLICAÇÃO NO ESPAÇO
        st.markdown(r"""
        ### 🚀 ETAPA 2: Como o Telescópio James Webb Procura Vida em Exoplanetas?
        Quando um exoplaneta passa na frente da sua estrela (trânsito planetário), a luz da estrela atravessa a atmosfera desse planeta antes de chegar aos nossos telescópios.
        - Analisando o espectro de absorção, podemos identificar **Bioassinaturas** (moléculas que indicam a presença de água líquida e processos biológicos):
          - Vapor de Água ($\text{H}_2\text{O}$)
          - Metano ($\text{CH}_4$) + Oxigênio ($\text{O}_2$) ou Ozônio ($\text{O}_3$) em desequilíbrio termodinâmico!
        """)
        
        # ETAPA 3: SIMULADOR
        st.markdown("### 🧮 ETAPA 3: Espectrômetro de Absorção Cósmica")
        st.write("Selecione um exoplaneta analisado pelo telescópio espacial para decodificar sua atmosfera:")
        
        target_exo = st.selectbox(
            "Selecione o Exoplaneta Alvo:",
            [
                "🪐 Exoplaneta Kepler-452b (Zona Habitável)",
                "🔥 Exoplaneta WASP-76b (Júpiter Ultrarquente)",
                "❄️ Exoplaneta TRAPPIST-1e (Mundo Rochoso Temperado)"
            ]
        )
        
        if "Kepler-452b" in target_exo:
            st.markdown("""
                **Linhas Espectrais Detectadas:**
                - 💧 **Forte banda em 1,4 µm e 1,9 µm:** Vapor de Água ($\text{H}_2\text{O}$).
                - 🌿 **Linha em 7,6 µm:** Metano ($\text{CH}_4$) e Ozônio ($\text{O}_3$).
                - 📋 **Veredito Astroquímico:** 🌟 **Candidato de Altíssimo Potencial Biológico!** Atmosfera com água líquida e bioassinaturas em equilíbrio sustentável.
            """)
        elif "WASP-76b" in target_exo:
            st.markdown("""
                **Linhas Espectrais Detectadas:**
                - ⚔️ **Linhas atômicas intensas em 372 nm e 589 nm:** Vapor de Ferro Gasoso ($\text{Fe}$) e Sódio ($\text{Na}$).
                - 📋 **Veredito Astroquímico:** 🔥 **Mundo Infernal!** Temperatura acima de 2.400 °C onde o ferro evapora de dia e chove ferro líquido à noite.
            """)
        else:
            st.markdown("""
                **Linhas Espectrais Detectadas:**
                - 🌫️ **Banda em 4,3 µm:** Dióxido de Carbono ($\text{CO}_2$) e Nitrogênio ($\text{N}_2$).
                - 💧 **Pequenos traços em 1,4 µm:** Vapor de Água ($\text{H}_2\text{O}$).
                - 📋 **Veredito Astroquímico:** 🌍 **Mundo Rochoso com Atmosfera Densa**, semelhante à Terra primitiva ou Marte antigo!
            """)
            
        # ETAPA 4: TESTES
        st.markdown("### 📝 ETAPA 4: Testes de Espectroscopia")
        with st.container():
            st.markdown("""
                <div class='exercise-card'>
                    <span class='steam-tag chem'>Desafio de Vanguarda: Astroquímica</span>
                    <h4>🔭 Como a Espectroscopia Identifica Gases?</h4>
                    <p>Por que cada molécula ou elemento gera um padrão diferente de linhas pretas no espectro da luz?</p>
                </div>
            """, unsafe_allow_html=True)
            
            q_esp = st.radio("Selecione a explicação científica:", [
                "Porque cada átomo tem níveis únicos de energia eletrônica e absorve comprimentos de onda específicos",
                "Porque a cor do vidro do telescópio muda para cada planeta",
                "Porque os planetas pintam a luz com cores diferentes ao refletir o sol",
                "Porque a velocidade da luz diminui dependendo do planeta"
            ], key="chem_q_espectro")
            if st.button("Verificar Espectroscopia", key="btn_chem_esp"):
                if "níveis únicos de energia eletrônica" in q_esp:
                    st.success("🎉 Perfeito! Os saltos quânticos dos elétrons entre orbitais criam um 'código de barras' luminoso único e inconfundível para cada elemento da tabela periódica. (+30 XP)")
                    add_xp(user["id"], 30)
                else:
                    st.error("❌ Revise a Etapa 1: A estrutura eletrônica e os níveis quânticos de energia de cada elemento são a chave!")


# ==============================================================================
# 💻 4. TRILHA DE TECNOLOGIA & COMPUTAÇÃO
# ==============================================================================
def _render_tech_track(user: dict):
    st.markdown("## 💻 Tecnologia & Computação: Fundamentos dos Algoritmos & IA Espacial")
    st.write("Descubra como os computadores pensam (lógica, loops e binário) e como usamos inteligência artificial para explorar o Cosmos:")
    
    level = st.radio(
        "Selecione seu Nível de Treinamento:",
        [
            "🟢 Nível 1: Cadete (Fundamentos: Algoritmos, Sequência e Loops do Rover / 6º Ano)",
            "🟡 Nível 2: Explorador (Fundamentos: Sistema Binário, Bytes e Telemetria de Sondas / 7º-9º Ano)",
            "🔴 Nível 3: Astrofísico (Fundamentos: Inteligência Artificial e Detecção de Trânsito / Avançado)"
        ],
        key="tech_level_select"
    )
    
    st.markdown("---")
    
    # -------------------------------------------------------------------------
    # NÍVEL 1: COMPUTAÇÃO
    # -------------------------------------------------------------------------
    if "Nível 1" in level:
        st.markdown("""
            <div class='level-badge cadet'>🟢 NÍVEL 1 — CADETE (FUNDAMENTOS & 6º ANO)</div>
            <h3 style='color: #4ade80;'>Algoritmos, Pensamento Computacional e Loops</h3>
        """, unsafe_allow_html=True)
        
        # ETAPA 1: FUNDAMENTOS
        st.markdown(r"""
            <div class='fundamento-box'>
                <h4 style='color: #ffd166; margin-top:0;'>🧱 ETAPA 1: O FUNDAMENTO BÁSICO (O que é um Algoritmo?)</h4>
                <p>Computadores e robôs não têm sentimentos e nem adivinham coisas: eles seguem instruções lógicas estritas chamadas <strong>Algoritmos</strong>:</p>
                <ul>
                    <li><strong>Definição de Algoritmo:</strong> É uma sequência finita, lógica e ordenada de passos para resolver um problema ou realizar uma tarefa.
                        <ul>
                            <li><em>Exemplo na Terra:</em> Uma receita de brigadeiro (1. Pegue a panela, 2. Coloque o leite condensado e manteiga, 3. Mexa até desgrudar, 4. Deixe esfriar e enrole). Se você trocar a ordem dos passos, o bolo desanda!</li>
                        </ul>
                    </li>
                    <li><strong>Os 3 Pilares da Lógica de Programação:</strong>
                        <ol>
                            <li><strong>Sequência:</strong> Executar comandos um após o outro de cima para baixo.</li>
                            <li><strong>Condicional (`SE / SENÃO`):</strong> Tomar decisões com base em sensores. Ex: `SE houver obstáculo ENTÃO desvie SENÃO siga em frente`.</li>
                            <li><strong>Laço de Repetição (`LOOP / REPITA`):</strong> Repetir uma ação várias vezes sem precisar escrever o mesmo código de novo. Ex: `REPITA 4 VEZES: avance 1 metro`.</li>
                        </ol>
                    </li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
        # ETAPA 2: APLICAÇÃO NO ESPAÇO
        st.markdown(r"""
        ### 🚀 ETAPA 2: Como a NASA Programa os Robôs em Marte (*Curiosity & Perseverance*)?
        Como vimos na trilha de matemática, um sinal de rádio demora de 5 a 20 minutos para ir da Terra a Marte. Se o robô estivesse indo em direção a um penhasco, não daria tempo de um humano na Terra freá-lo com controle remoto!
        - **Piloto Automático Autônomo:** Os engenheiros enviam um **algoritmo de rota** pela manhã com loops e decisões autônomas. Os sensores a laser (LiDAR e câmeras estéreo) analisam o terreno e decidem o melhor caminho sozinhos!
        """)
        
        # ETAPA 3: SIMULADOR
        st.markdown("### 🧮 ETAPA 3: Painel de Controle de Rota do Rover Marciano")
        st.write("Monte o algoritmo de blocos de comando para conduzir o rover até o laboratório de rochas sem cair em crateras:")
        
        col_cmd1, col_cmd2 = st.columns(2)
        with col_cmd1:
            cmd1 = st.selectbox("Comando 1 (Início):", ["Avançar 10 metros", "Girar 90° para a Direita", "Girar 90° para a Esquerda"], index=0, key="rover_c1")
            cmd2 = st.selectbox("Comando 2 (Decisão do Sensor):", ["SE sensor ver rocha ENTÃO coletar amostra", "SE sensor ver cratera ENTÃO frear e desviar 45°", "Ignorar sensores e acelerar"], index=1, key="rover_c2")
            loop_times = st.slider("Comando 3 (Loop de Repetição - vezes):", min_value=1, max_value=5, value=3, key="rover_c3")
            
        with col_cmd2:
            st.markdown("#### 📜 Código Gerado no Computador de Bordo:")
            st.code(f"""# Programa de Navegação do Rover
1: {cmd1}
2: {cmd2}
3: FOR passo IN RANGE({loop_times}):
4:     avancar_um_metro_com_cuidado()
5:     analisar_terreno()
6: emitir_telemetria_para_terra("Missao Concluida com Sucesso")
""", language="python")
            
            if "desviar 45°" in cmd2:
                st.success(f"🤖 **Missão Bem-Sucedida!** O robô desviou dos perigos e avançou {10 + loop_times} metros no solo marciano com segurança!")
            else:
                st.warning("⚠️ Cuidado: Sem o sensor de desvio de crateras ativado, o rover corre perigo no terreno acidentado!")

        st.markdown("""
            <div style='background: linear-gradient(135deg, rgba(255,107,107,0.15), rgba(78,205,196,0.15)); border: 1px solid #ff6b6b; border-radius: 10px; padding: 14px; margin: 15px 0;'>
                <h4 style='color: #ff6b6b; margin: 0 0 5px 0;'>🚀 Quer pilotar o Rover em 2D com Grid Interativo em Tempo Real?</h4>
                <p style='color: #e2e8f0; font-size: 0.95rem; margin: 0 0 10px 0;'>
                    Experimente o <strong>Simulador Visual Completo do Rover</strong> no Laboratório STEAM: veja o robô se movimentar no mapa marciano passo a passo, desviar de crateras, disparar o laser SuperCam e coletar amostras com 4 níveis de desafios!
                </p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("🎮 Abrir Simulador Visual 2D do Rover", key="btn_jump_rover_sim"):
            st.session_state.redirect_target = {
                "area": "🔬 Laboratório STEAM",
                "module_key": "nav_steam_lab",
                "module_val": "🔬 Laboratório STEAM"
            }
            st.rerun()
                
        # ETAPA 4: TESTES
        st.markdown("### 📝 ETAPA 4: Testes de Fixação")
        with st.container():
            st.markdown("""
                <div class='exercise-card'>
                    <span class='steam-tag tech'>Desafio: Lógica e Loops</span>
                    <h4>💻 Otimizando o Código do Rover</h4>
                    <p>Para fazer um robô desenhar um <strong>quadrado perfeito</strong> no solo de Marte, qual bloco de código é mais eficiente e elegante?</p>
                </div>
            """, unsafe_allow_html=True)
            
            q_loop = st.radio("Escolha a melhor estrutura:", [
                "Escrever 'Avançar 5m e Virar 90°' 4 vezes seguidas sem repetição",
                "LOOP: REPITA 4 VEZES { Avançar 5m; Virar 90° }",
                "Avançar 20 metros em linha reta",
                "Virar 360° no mesmo lugar"
            ], key="tech_q_loop_l1")
            if st.button("Verificar Algoritmo", key="btn_tech_loop"):
                if "REPITA 4 VEZES" in q_loop:
                    st.success("🎉 Perfeito! Os laços de repetição (loops) evitam repetição de código e tornam os algoritmos compactos e rápidos! (+20 XP)")
                    add_xp(user["id"], 20)
                    unlock_badge(user["id"], "steam_tech_master")
                else:
                    st.error("❌ Use o conceito de Laço de Repetição (Loop) para repetir 4 vezes os lados do quadrado.")

    # -------------------------------------------------------------------------
    # NÍVEL 2: COMPUTAÇÃO
    # -------------------------------------------------------------------------
    elif "Nível 2" in level:
        st.markdown("""
            <div class='level-badge explorer'>🟡 NÍVEL 2 — EXPLORADOR (7º A 9º ANO)</div>
            <h3 style='color: #38bdf8;'>Sistema Binário, Bytes e Telemetria de Sondas Espaciais</h3>
        """, unsafe_allow_html=True)
        
        # ETAPA 1: FUNDAMENTOS
        st.markdown(r"""
            <div class='fundamento-box'>
                <h4 style='color: #ffd166; margin-top:0;'>🧱 ETAPA 1: O FUNDAMENTO BÁSICO (Como Computadores Contam em Binário?)</h4>
                <p>Nós usamos o <strong>Sistema Decimal (Base 10)</strong> porque temos 10 dedos nas mãos ($0, 1, 2, 3, 4, 5, 6, 7, 8, 9$). Mas dentro de um chip eletrônico, só existem transistores que deixam ou não passar eletricidade (como interruptores de luz: <strong>LIGADO</strong> ou <strong>DESLIGADO</strong>):</p>
                <ul>
                    <li><strong>Bit (Binary Digit):</strong> A menor unidade de informação: vale apenas <strong>0</strong> (desligado) ou <strong>1</strong> (ligado).</li>
                    <li><strong>Byte:</strong> Um agrupamento de <strong>8 bits</strong> ($1\text{ Byte} = 8\text{ bits}$). Com 8 bits podemos formar $2^8 = 256$ combinações diferentes (de 0 a 255).</li>
                    <li><strong>Tabela de Pesos das Potências de 2:</strong>
                        <table style='width: 100%; text-align: center; border-collapse: collapse; margin-top: 8px;'>
                            <tr style='background: rgba(0,212,255,0.2);'>
                                <th>Bit 7</th><th>Bit 6</th><th>Bit 5</th><th>Bit 4</th><th>Bit 3</th><th>Bit 2</th><th>Bit 1</th><th>Bit 0</th>
                            </tr>
                            <tr>
                                <td>$128$</td><td>$64$</td><td>$32$</td><td>$16$</td><td>$8$</td><td>$4$</td><td>$2$</td><td>$1$</td>
                            </tr>
                        </table>
                    </li>
                    <li><strong>Exemplo Terrestre Resolvido:</strong> Qual é o número decimal para o byte binário <code>00001101</code>?<br>
                    $\text{Soma} = 0\cdot 128 + 0\cdot 64 + 0\cdot 32 + 0\cdot 16 + 1\cdot 8 + 1\cdot 4 + 0\cdot 2 + 1\cdot 1 = 8 + 4 + 1 = \mathbf{13}$!</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
        # ETAPA 2: APLICAÇÃO NO ESPAÇO
        st.markdown(r"""
        ### 🚀 ETAPA 2: Telemetria da Sonda Voyager a 24 Bilhões de km de Distância
        A sonda *Voyager 1* está fora do Sistema Solar. Para nos enviar as fotos dos planetas e as leituras de radiação interestelar, ela transforma cada dado em pulsos de ondas de rádio binárias (zeros e uns). Na Terra, as antenas gigantes da NASA recebem esses bits e remontam as imagens pixel por pixel!
        """)
        
        # ETAPA 3: SIMULADOR
        st.markdown("### 🧮 ETAPA 3: Tradutor Interativo Binário $\\longleftrightarrow$ Decimal")
        st.write("Ligue e desligue os 8 bits abaixo para ver a formação do número decimal em tempo real:")
        
        b_cols = st.columns(8)
        bit_vals = []
        powers = [128, 64, 32, 16, 8, 4, 2, 1]
        
        for idx, (col, p) in enumerate(zip(b_cols, powers)):
            with col:
                val = st.checkbox(f"{p} (Bit {7-idx})", value=(idx in [4, 7]), key=f"bin_b_{idx}")
                bit_vals.append(1 if val else 0)
                
        bin_str = "".join(str(b) for b in bit_vals)
        decimal_val = sum(b * p for b, p in zip(bit_vals, powers))
        hex_val = hex(decimal_val).upper().replace("0X", "0x")
        
        c_res1, c_res2, c_res3 = st.columns(3)
        c_res1.metric("Byte Binário", bin_str, "Base 2")
        c_res2.metric("Valor Decimal", str(decimal_val), "Base 10")
        c_res3.metric("Código Hexadecimal", hex_val, "Base 16 (Usado na NASA)")
        
        # ETAPA 4: TESTES
        st.markdown("### 📝 ETAPA 4: Testes de Fixação")
        with st.container():
            st.markdown("""
                <div class='exercise-card'>
                    <span class='steam-tag tech'>Desafio: Conversão de Telemetria</span>
                    <h4>📡 Decodificando o Sensor da Voyager</h4>
                    <p>A antena da NASA recebeu o seguinte byte de telemetria do sensor de temperatura da sonda: <strong><code>00100010</code></strong>. Qual é o valor decimal desse número?</p>
                </div>
            """, unsafe_allow_html=True)
            
            q_bin = st.radio("Escolha o valor decimal correspondente:", ["18", "34 ($32 + 2$)", "66", "130"], key="tech_q_bin_test")
            if st.button("Verificar Byte", key="btn_tech_bin"):
                if "34" in q_bin:
                    st.success("🎉 Perfeito! Os bits ligados estão nas posições de peso 32 e peso 2 ($32 + 2 = 34$). A temperatura decodificada é de 34 Kelvin! (+25 XP)")
                    add_xp(user["id"], 25)
                else:
                    st.error("❌ Some apenas os pesos onde o bit vale 1: posição 32 e posição 2.")

    # -------------------------------------------------------------------------
    # NÍVEL 3: COMPUTAÇÃO
    # -------------------------------------------------------------------------
    else:
        st.markdown("""
            <div class='level-badge astrophysicist'>🔴 NÍVEL 3 — ASTROFÍSICO (AVANÇADO / ENSINO MÉDIO)</div>
            <h3 style='color: #c084fc;'>Inteligência Artificial & Redes Neurais para Detecção de Exoplanetas</h3>
        """, unsafe_allow_html=True)
        
        # ETAPA 1: FUNDAMENTOS
        st.markdown(r"""
            <div class='fundamento-box'>
                <h4 style='color: #ffd166; margin-top:0;'>🧱 ETAPA 1: O FUNDAMENTO BÁSICO (O que é Aprendizado de Máquina & Redes Neurais?)</h4>
                <p>Na programação tradicional, você escreve regras manuais. Mas quando há milhões de dados complexos (como fotos ou séries temporais de brilho estelar), usamos <strong>Machine Learning (Aprendizado de Máquina)</strong>:</p>
                <ul>
                    <li><strong>Redes Neurais Artificiais:</strong> Inspiradas nos neurônios do cérebro biológico. Elas recebem sinais de entrada ($x_i$), multiplicam por pesos numéricos ($w_i$), somam tudo e passam por uma função de ativação matemática:
                        $$y = f\left(\sum_{i} w_i x_i + b\right)$$
                    </li>
                    <li><strong>Como a IA Aprende?</strong> Ela analisa milhares de exemplos rotulados (ex: "isto é um planeta", "isto é um falso positivo") e ajusta seus pesos matemáticos até conseguir classificar novos dados sozinha com mais de $99\%$ de precisão!</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
        # ETAPA 2: APLICAÇÃO NO ESPAÇO
        st.markdown(r"""
        ### 🚀 ETAPA 2: Como a IA do Google e NASA Descobriu Novos Sistemas Planetários?
        O telescópio espacial Kepler monitorou mais de $200.000$ estrelas durante anos, gerando bilhões de pontos de luz. É humanamente impossível astrônomos olharem todos os gráficos a olho nu!
        - Astrônomos treinaram uma **Rede Neural Convolucional (CNN)** para identificar a minúscula queda de brilho periódica em forma de "U" na curva de luz (chamada de **Curva de Trânsito**), descobrindo exoplanetas que haviam passado despercebidos pelos cientistas humanos!
        """)
        
        # ETAPA 3: SIMULADOR
        st.markdown("### 🧮 ETAPA 3: Simulador de IA Classificadora de Curvas de Luz")
        st.write("Ajuste os limiares de sensibilidade da Rede Neural para classificar uma curva de luz real:")
        
        noise_level = st.slider("Nível de Ruído Estelar nos Dados (%):", min_value=1, max_value=50, value=15, step=1)
        dip_depth = st.slider("Queda de Brilho do Trânsito (%):", min_value=0.1, max_value=5.0, value=1.5, step=0.1)
        
        snr = dip_depth / (noise_level / 10.0) # Razão Sinal-Ruído
        confidence = min(99.9, max(5.0, (snr / 2.0) * 100))
        
        c_ai1, c_ai2 = st.columns(2)
        c_ai1.metric("Razão Sinal/Ruído (SNR)", f"{snr:.2f}", "Qualidade do Sinal")
        c_ai2.metric("Confiança da Rede Neural", f"{confidence:.1f}%", "Probabilidade de Exoplaneta Real")
        
        if confidence >= 80:
            st.success("🟢 **Exoplaneta Confirmado pela IA!** O padrão em 'U' é inequívoco e foi validado estatisticamente.")
        elif confidence >= 50:
            st.warning("🟡 **Candidato Suspeito:** Sinal ruidoso. Recomendada nova observação com o Telescópio James Webb.")
        else:
            st.error("🔴 **Falso Positivo:** Ruído estelar (manchas solares ou pulsação) mascarando os dados.")
            
        # ETAPA 4: TESTES
        st.markdown("### 📝 ETAPA 4: Testes de IA Astronômica")
        with st.container():
            st.markdown("""
                <div class='exercise-card'>
                    <span class='steam-tag tech'>Desafio de Vanguarda: IA Espacial</span>
                    <h4>🤖 Como a IA Reconhece um Trânsito Planetário?</h4>
                    <p>Qual é a característica visual de uma curva de luz que a Rede Neural procura para identificar a passagem de um planeta na frente de sua estrela?</p>
                </div>
            """, unsafe_allow_html=True)
            
            q_ai = st.radio("Selecione o padrão de sinal correto:", [
                "Um aumento repentino no brilho da estrela",
                "Uma queda suave e periódica no brilho em formato de 'U' ou caixa",
                "A estrela muda permanentemente de cor de azul para vermelho",
                "O sinal de luz desaparece por 10 anos seguidos"
            ], key="tech_q_ai_transit")
            if st.button("Verificar IA", key="btn_tech_ai"):
                if "queda suave e periódica no brilho" in q_ai:
                    st.success("🎉 Extraordinário! Quando o planeta transita, ele bloqueia uma fração constante da luz estelar, gerando a clássica queda em formato de 'U' periódica que as Redes Neurais identificam. (+30 XP)")
                    add_xp(user["id"], 30)
                    unlock_badge(user["id"], "steam_polymath")
                else:
                    st.error("❌ Lembre-se: O planeta bloqueia luz da estrela ao passar na frente dela!")
