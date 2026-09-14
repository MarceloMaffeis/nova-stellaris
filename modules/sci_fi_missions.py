"""
Nova Stellaris - Módulo de Missões de Ficção Científica Interativas
Simuladores baseados em "Perdido em Marte", "Devoradores de Estrelas" e "Interestelar".
"""

import os
import streamlit as st
import numpy as np
import plotly.graph_objects as go
from database import add_xp, unlock_badge, save_mission_progress, get_mission_progress

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_DIR = os.path.join(BASE_DIR, "assets", "images")

def get_img(filename: str) -> str:
    local_p = os.path.join(IMG_DIR, filename)
    if os.path.exists(local_p):
        return local_p
    return filename

def render_sci_fi_missions(user: dict):
    st.markdown("""
        <div class='cosmic-hero' style='background: linear-gradient(135deg, rgba(30,16,60,0.95), rgba(16,20,47,0.95)); border: 1px solid #f72585;'>
            <h1 style='color: #ffd166; margin-bottom: 5px;'>🚀 Simulador de Missões Sci-Fi</h1>
            <p style='color: #cbd5e1; font-size: 1.1rem; margin: 0;'>
                Assuma o controle de missões lendárias do cinema e da literatura, usando Física, Matemática, Química e Computação para vencer!
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    mission_choice = st.radio(
        "Selecione sua Operação Espacial:",
        [
            "🔴 Missão 1: Perdido em Marte (The Martian)",
            "✨ Missão 2: Devoradores de Estrelas (Project Hail Mary)",
            "⏳ Missão 3: Gargantua & Planeta Miller (Interestelar)"
        ],
        horizontal=True
    )
    
    if "Perdido em Marte" in mission_choice:
        render_the_martian_mission(user)
    elif "Devoradores de Estrelas" in mission_choice:
        render_hail_mary_mission(user)
    else:
        render_interstellar_mission(user)

# ----------------------------------------------------------------------
# MISSÃO 1: PERDIDO EM MARTE
# ----------------------------------------------------------------------
def render_the_martian_mission(user: dict):
    st.image(get_img("perseverance.jpg"), caption="🔴 Superfície de Marte - Habitat da Missão Ares III", use_container_width=True)
    st.markdown("""
        <div class='cosmic-card' style='border-left: 5px solid #ff6b6b;'>
            <h2 style='color: #ff6b6b;'>🔴 Operação Acidalia: Sobrevivência Marciana</h2>
            <p>
                <strong>Situação:</strong> Uma tempestade de areia separou você da tripulação da Ares III. 
                O Habitat está intacto, mas seus suprimentos duram apenas 60 dias. O resgate só chegará no <strong>Sol 500</strong>!
                Você precisa usar química, botânica e computação para sobreviver.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    stage = st.tabs(["🧪 Fase 1: Fábrica de Água", "🥔 Fase 2: Dieta de Batatas", "💻 Fase 3: Decodificador Pathfinder"])
    
    # FASE 1: ÁGUA
    with stage[0]:
        st.subheader("🧪 Fase 1: Síntese Química de Água ($2H_2 + O_2 \\to 2H_2O$)")
        st.markdown("""
            Você encontrou tanques de combustível de hidrazina ($N_2H_4$) que podem ser decompostos em gás Hidrogênio ($H_2$).
            Para formar água líquida ($H_2O$), você precisa queimar **2 partes de Hidrogênio** para cada **1 parte de Oxigênio**.
        """)
        
        c1, c2 = st.columns(2)
        with c1:
            h2_liters = st.slider("Quantidade de Hidrogênio ($H_2$) liberada (litros):", 50, 500, 200, step=10)
        with c2:
            o2_liters = st.slider("Quantidade de Oxigênio ($O_2$) injetada (litros):", 50, 500, 100, step=10)
            
        ratio = h2_liters / o2_liters if o2_liters > 0 else 0
        
        st.markdown(f"**Proporção Atual ($H_2 : O_2$):** `{ratio:.2f} : 1`")
        
        if abs(ratio - 2.0) < 0.05:
            produced_water = o2_liters * 2
            st.success(f"🎉 **Reação Perfeita!** Você produziu com segurança **{produced_water} litros de água pura** sem explodir o Habitat!")
            if st.button("Salvar Progresso da Água 💧"):
                save_mission_progress(user["id"], "the_martian", 1, False, 100)
                add_xp(user["id"], 50)
                st.success("+50 XP adicionados!")
        elif ratio > 2.05:
            st.error("⚠️ **Excesso de Hidrogênio!** Há muito gás inflamável acumulado no teto do Habitat. Risco de explosão! Reduza o $H_2$ ou aumente o $O_2$.")
        else:
            st.warning("⚠️ **Oxigênio em excesso!** A reação está incompleta e você está gastando seu precioso oxigênio de respiração. Aumente o $H_2$ para a proporção 2:1.")

    # FASE 2: BATATAS
    with stage[1]:
        st.subheader("🥔 Fase 2: Otimização Matemática de Calorias")
        st.markdown("""
            Você tem 126 m² de área dentro do Habitat para plantar batatas no solo marciano enriquecido.
            • 1 batata média fornece **100 calorias** (kcal).
            • O astronauta precisa de pelo menos **1.500 calorias por Sol** para não definhar.
            • Cada metro quadrado de solo produz **15 batatas por colheita**.
        """)
        
        area_used = st.slider("Área cultivada de batatas (m²):", 10, 126, 100)
        days_to_survive = st.number_input("Sols necessários até o resgate:", value=400, step=50)
        
        total_potatoes = area_used * 15
        total_calories = total_potatoes * 100
        calories_per_sol = total_calories / days_to_survive
        
        st.markdown(f"""
            <div class='cosmic-card'>
                <h4>📊 Balanço Nutricional da Missão:</h4>
                <p>🥔 <strong>Total de batatas produzidas:</strong> {total_potatoes:,} batatas</p>
                <p>🔥 <strong>Total de energia calórica:</strong> {total_calories:,} kcal</p>
                <p>📈 <strong>Calorias diárias disponíveis:</strong> <span style='font-size: 1.3rem; color: {'#06d6a0' if calories_per_sol >= 1500 else '#f72585'};'>{calories_per_sol:.0f} kcal / Sol</span></p>
            </div>
        """, unsafe_allow_html=True)
        
        if calories_per_sol >= 1500:
            st.success("✅ **Dieta Sustentável!** Mark Watney tem calorias suficientes para sobreviver com energia até a chegada da nave Hermes!")
            if unlock_badge(user["id"], "martian_botanist"):
                add_xp(user["id"], 150)
                st.balloons()
                st.success("🎉 **Conquista Desbloqueada:** 🥔 Botânico de Marte! (+150 XP)")
        else:
            st.error(f"❌ **Déficit Calórico!** {calories_per_sol:.0f} kcal/Sol é insuficiente (mínimo 1.500 kcal). Você precisa aumentar a área de cultivo para não passar fome!")

    # FASE 3: PATHFINDER HEX
    with stage[2]:
        st.subheader("💻 Fase 3: Decodificador Hexadecimal da Sonda Pathfinder")
        st.markdown("""
            Para conversar com a NASA, Mark Watney desenterrou a antiga sonda **Pathfinder**.
            A câmera gira 360° apontando para cartas com dígitos hexadecimais (**0 a 9** e **A a F**).
            Cada letra do alfabeto na tabela ASCII é formada por 2 dígitos Hexadecimais!
        """)
        
        st.info("📖 **Tabela ASCII de Referência Rápida:**\n\n`H = 48` | `E = 45` | `L = 4C` | `P = 50` | `S = 53` | `O = 4F` | `N = 4E` | `A = 41`")
        
        st.markdown("### 📡 Mensagem recebida da Terra via câmera:")
        st.code("4E 41 53 41", language="text")
        
        user_decode = st.text_input("Digite a palavra decodificada em letras maiúsculas:", placeholder="Ex: CASA").strip().upper()
        
        if user_decode == "NASA":
            st.success("🎉 **TRANSMISSÃO DECODIFICADA COM SUCESSO!** A NASA respondeu: 'Watney, nós estamos vendo você!'")
            save_mission_progress(user["id"], "the_martian", 3, True, 300)
            if unlock_badge(user["id"], "pathfinder_hacker"):
                add_xp(user["id"], 150)
                st.balloons()
                st.success("🎉 **Conquista Desbloqueada:** 💾 Hacker da Pathfinder! (+150 XP)")
        elif user_decode:
            st.error("❌ Palavra incorreta. Dica: 4E='N', 41='A', 53='S', 41='A'!")

# ----------------------------------------------------------------------
# MISSÃO 2: DEVORADORES DE ESTRELAS (PROJECT HAIL MARY)
# ----------------------------------------------------------------------
def render_hail_mary_mission(user: dict):
    st.image(get_img("pillars.jpg"), caption="✨ Espaço Profundo - Viagem Interestelar até Tau Ceti", use_container_width=True)
    st.markdown("""
        <div class='cosmic-card' style='border-left: 5px solid #ffd166;'>
            <h2 style='color: #ffd166;'>✨ Operação Hail Mary: O Encontro com Rocky</h2>
            <p>
                <strong>Situação:</strong> O astronauta Ryland Grace está na estrela Tau Ceti para salvar a Terra dos Astrofagos.
                Ele encontra o alienígena engenheiro <strong>Rocky</strong>, uma criatura inteligente de 5 patas que vive sob 29 atmosferas de pressão!
            </p>
        </div>
    """, unsafe_allow_html=True)

    stage = st.tabs(["🌀 Fase 1: Gravidade por Rotação", "🎶 Fase 2: Tradutor Musical do Rocky"])
    
    # FASE 1: GRAVIDADE ARTIFICIAL
    with stage[0]:
        st.subheader("🌀 Fase 1: Física da Gravidade Artificial ($a_c = \\omega^2 \\cdot r$)")
        st.markdown("""
            No espaço profundo não há gravidade natural. Para não perder massa muscular e óssea, 
            a nave *Hail Mary* estende dois cabos com os módulos nas pontas e começa a girar.
            A aceleração centrípeta gerada no chão da cabine deve ser exatamente **$9,81 \\text{ m/s}^2$** ($1g$).
        """)
        
        c1, c2 = st.columns(2)
        with c1:
            radius = st.slider("Raio do cabo ($r$ em metros):", 10.0, 100.0, 45.0, step=1.0)
        with c2:
            rpm = st.slider("Velocidade de Rotação (RPM - rotações por minuto):", 1.0, 10.0, 4.45, step=0.05)
            
        # Converter RPM para rad/s: omega = (rpm * 2 * pi) / 60
        omega = (rpm * 2 * np.pi) / 60
        accel = (omega ** 2) * radius
        g_force = accel / 9.81
        
        st.markdown(f"""
            <div class='cosmic-card'>
                <h4>🛰️ Telemetria da Nave Hail Mary:</h4>
                <p>🔄 <strong>Velocidade Angular ($\\\omega$):</strong> {omega:.3f} rad/s</p>
                <p>⚖️ <strong>Aceleração Gerada ($a_c$):</strong> <span style='font-size: 1.4rem; color: #00d4ff;'>{accel:.2f} m/s²</span></p>
                <p>🌍 <strong>Força G Relativa:</strong> <span style='font-size: 1.4rem; color: {'#06d6a0' if abs(g_force - 1.0) <= 0.05 else '#f72585'};'>{g_force:.2f} g</span></p>
            </div>
        """, unsafe_allow_html=True)
        
        if abs(g_force - 1.0) <= 0.05:
            st.success("✅ **Gravidade Terrestre Perfeita ($1g$)!** Ryland Grace pode andar normalmente pelos corredores da nave!")
            if st.button("Confirmar Calibragem de Rotação 🚀"):
                add_xp(user["id"], 50)
                st.success("+50 XP concedidos!")
        elif g_force < 0.95:
            st.warning("⚠️ **Gravidade muito baixa!** Aumente a rotação (RPM) ou aumente o raio do cabo para atingir 1,00g.")
        else:
            st.error("⚠️ **Gravidade excessiva!** A tripulação está sendo esmagada contra o piso. Reduza os RPMs.")

    # FASE 2: ROCKY
    with stage[1]:
        st.subheader("🎶 Fase 2: Dicionário Harmônico de Frequências de Rocky")
        st.markdown("""
            Rocky não tem cordas vocais como humanos: ele se comunica combinando frequências e acordes musicais!
            Para criar amizade e salvar o sistema solar, você precisa traduzir os sons do sintetizador.
        """)
        
        st.markdown("### 🎼 Frase Alienígena transmitida:")
        st.markdown("""
            > 🎵 **Frequência 1 (440 Hz - Nota Lá):** 'Amigo / Humano'  
            > 🎵 **Frequência 2 (523 Hz - Nota Dó):** 'Bom / Sim'  
            > 🎵 **Frequência 3 (659 Hz - Nota Mi):** 'Toca aqui / Fist Bump! 👊'
        """)
        
        choice = st.radio(
            "Qual o significado do acorde triplo (Lá + Dó + Mi) emitido por Rocky?",
            [
                "Ele quer atacar a nave!",
                "Amigo bom, toca aqui! (Fist my bump! 👊)",
                "Ele está com fome de xenônio.",
                "Ele quer voltar para o planeta 40 Eridani."
            ]
        )
        
        if choice == "Amigo bom, toca aqui! (Fist my bump! 👊)":
            st.success("🤝 **FIST MY BUMP! 👊** Você compreendeu a linguagem de Rocky e formou a aliança mais fantástica da galáxia!")
            save_mission_progress(user["id"], "project_hail_mary", 2, True, 250)
            if unlock_badge(user["id"], "rocky_friend"):
                add_xp(user["id"], 150)
                st.balloons()
                st.success("🎉 **Conquista Desbloqueada:** 🤝 Amigo de Rocky! (+150 XP)")

# ----------------------------------------------------------------------
# MISSÃO 3: INTERESTELAR (GARGANTUA)
# ----------------------------------------------------------------------
def render_interstellar_mission(user: dict):
    st.image(get_img("blackhole.jpg"), caption="🕳️ Horizonte de Eventos do Buraco Negro Supermassivo Gargantua", use_container_width=True)
    st.markdown("""
        <div class='cosmic-card' style='border-left: 5px solid #7209b7;'>
            <h2 style='color: #7209b7;'>⏳ Operação Gargantua: A Gravidade que Dobra o Tempo</h2>
            <p>
                <strong>Situação:</strong> A nave <em>Endurance</em> atingiu o sistema do buraco negro supermassivo Gargantua.
                Você precisa pousar no <strong>Planeta de Miller</strong> para checar o sinal da primeira astronauta.
                Mas cuidado: cada minuto gasto na superfície custa anos preciosos na Terra!
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.subheader("⏳ Simulador de Dilatação Gravitacional do Tempo (Einstein)")
    st.markdown("""
        Devido à extrema proximidade de Gargantua:
        $$\\text{Fator de Dilatação} = 61.320 \\implies 1 \\text{ hora no Planeta Miller} = 7 \\text{ anos na Terra!}$$
    """)
    
    minutes_on_miller = st.slider("Tempo de permanência na superfície do Planeta Miller (em minutos):", 10, 300, 60, step=10)
    
    hours_on_miller = minutes_on_miller / 60.0
    earth_years = hours_on_miller * 7.0
    earth_days = earth_years * 365.25
    
    st.markdown(f"""
        <div class='cosmic-card' style='background: linear-gradient(135deg, rgba(16,20,47,0.9), rgba(40,10,60,0.9)); border: 1px solid #7209b7;'>
            <h3 style='color: #ffd166;'>⏱️ Relatório do Computador de Bordo TARS:</h3>
            <p>🌊 <strong>Tempo no Planeta Miller:</strong> {minutes_on_miller} minutos ({hours_on_miller:.2f} horas)</p>
            <hr style='border-color: rgba(255,255,255,0.1);'>
            <h2 style='color: #00d4ff;'>⏳ Tempo transcorrido na Terra para sua família:</h2>
            <h1 style='color: #f72585; font-size: 2.8rem;'>{earth_years:.1f} ANOS TERRESTRES</h1>
            <p style='color: #94a3b8;'>({earth_days:,.0f} dias se passaram enquanto você estava no planeta aquático!)</p>
        </div>
    """, unsafe_allow_html=True)
    
    if minutes_on_miller <= 120:
        st.info("💡 **Reflexão Científica:** Cooper e Brand gastaram cerca de 3 horas no planeta por causa das ondas gigantes, e quando voltaram à nave Endurance, seu amigo Romilly havia envelhecido 23 anos!")
        if unlock_badge(user["id"], "time_traveler"):
            add_xp(user["id"], 150)
            st.balloons()
            st.success("🎉 **Conquista Desbloqueada:** ⏳ Viajante do Tempo de Miller! (+150 XP)")

