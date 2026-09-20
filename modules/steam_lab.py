"""
Nova Stellaris - Laboratório Integrado STEAM
Física, Matemática, Química Cósmica e Computação / Algoritmos do Rover.
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from database import add_xp, unlock_badge

def render_steam_lab(user: dict, default_lab: str = None, *args, **kwargs):
    if not default_lab:
        default_lab = st.session_state.get("steam_lab_default", "Química")
    
    l = str(default_lab).lower()
    
    # ----------------------------------------------------
    # 1. QUÍMICA ESPACIAL
    # ----------------------------------------------------
    if "quím" in l or "chem" in l:
        st.subheader("🧪 A Tabela Periódica Forjada nas Estrelas")
        st.markdown("""
            Você sabia que **todos os elementos do seu corpo foram fabricados dentro de estrelas**?
            O astrônomo Carl Sagan dizia: *"Nós somos poeira de estrelas pensando sobre as estrelas"*.
        """)
        
        c_elem1, c_elem2 = st.columns([1, 1])
        
        elements_origins = {
            "Hidrogênio (H)": {"origem": "Big Bang (O início do universo)", "onde_esta": "Na água dos seus oceanos e no seu DNA", "cor": "#38bdf8"},
            "Carbono (C)": {"origem": "Coração de Estrelas Gigantes Vermelhas", "onde_esta": "A base de toda a vida orgânica na Terra", "cor": "#4ade80"},
            "Oxigênio (O)": {"origem": "Fusão em Estrelas Massivas", "onde_esta": "No ar que você respira a cada segundo", "cor": "#00f5d4"},
            "Ferro (Fe)": {"origem": "Explosões Cataclísmicas de Supernovas", "onde_esta": "Na hemoglobina do seu sangue que transporta oxigênio", "cor": "#f87171"},
            "Cálcio (Ca)": {"origem": "Morte de Estrelas Massivas", "onde_esta": "Na estrutura sólida dos seus ossos e dentes", "cor": "#fbbf24"},
            "Ouro (Au) & Platina": {"origem": "Fusão de Estrelas de Nêutrons (Kilonovas)", "onde_esta": "Em joias e nos circuitos dos computadores espaciais", "cor": "#ffd700"}
        }
        
        with c_elem1:
            selected_elem = st.selectbox("Escolha um elemento para ver sua certidão de nascimento cósmica:", list(elements_origins.keys()))
            elem_info = elements_origins[selected_elem]
            st.markdown(f"""
                <div class='cosmic-card' style='border-left: 5px solid {elem_info['cor']};'>
                    <h3 style='color: {elem_info['cor']};'>{selected_elem}</h3>
                    <p>🌟 <strong>Origem Cósmica:</strong> {elem_info['origem']}</p>
                    <p>🧬 <strong>Onde está em você:</strong> {elem_info['onde_esta']}</p>
                </div>
            """, unsafe_allow_html=True)
            
        with c_elem2:
            st.markdown("""
                <div class='cosmic-card'>
                    <h4 style='color: #00d4ff;'>🚀 Reator Químico de Propelentes de Foguete</h4>
                    <p>Escolha a mistura de combustível do motor do seu foguete:</p>
            """, unsafe_allow_html=True)
            fuel = st.radio("Combustível:", ["Hidrogênio Líquido + Oxigênio (LH2/LOX)", "Metano + Oxigênio (Methalox - Starship)", "Hidrazina Monopropelente"])
            if "LH2" in fuel:
                st.success("💧 **Resultado:** Motor super eficiente! Subproduto: **100% Vapor de Água pura!** ($2H_2 + O_2 \\to 2H_2O$)")
            elif "Metano" in fuel:
                st.info("🪐 **Resultado:** Excelente para Marte porque podemos produzir metano na atmosfera marciana ($CO_2 + 4H_2 \\to CH_4 + 2H_2O$)!")
            else:
                st.warning("⚠️ **Resultado:** Altamente tóxico, mas perfeito para manobras de satélites no vácuo.")
            st.markdown("</div>", unsafe_allow_html=True)
            
        if unlock_badge(user["id"], "stellar_chemist"):
            add_xp(user["id"], 120)
            st.balloons()
            st.success("🎉 **Conquista Desbloqueada:** 🧪 Alquimista das Estrelas! (+120 XP)")

    # ----------------------------------------------------
    # 2. COMPUTAÇÃO: TERMINAL DO ROVER VISUAL
    # ----------------------------------------------------
    elif "comp" in l or "rover" in l:
        from modules.rover_simulator import render_rover_simulator
        render_rover_simulator(user)

    # ----------------------------------------------------
    # 3. MATEMÁTICA: POTÊNCIAS DE 10 & NOTAÇÃO CIENTÍFICA
    # ----------------------------------------------------
    elif "mat" in l or "math" in l:
        st.subheader("🧮 O Mago da Notação Científica & Potências de 10")
        st.markdown("""
            No espaço, os números são gigantescos (milhões de anos-luz) ou minúsculos (átomos).
            A **Notação Científica** é a forma elegante que a matemática inventou para escrever qualquer número como:
            $$a \\times 10^b \\quad (\\text{onde } 1 \\le a < 10)$$
        """)
        
        c_m1, c_m2 = st.columns(2)
        with c_m1:
            st.markdown("#### 🔢 Experimente converter números grandes:")
            test_number = st.number_input("Digite um número grande (ex: 150000000):", value=150000000, step=1000000)
            
            formatted_sci = f"{test_number:.2e}".replace("e+0", " × 10^").replace("e+", " × 10^")
            st.markdown(f"""
                <div class='cosmic-card'>
                    <p>Número normal: <strong>{test_number:,}</strong></p>
                    <h2 style='color: #f72585;'>Notação: {formatted_sci}</h2>
                    <p style='color: #94a3b8; font-size: 0.9rem;'>
                        Contamos quantas casas a vírgula 'andou' para a esquerda até sobrar apenas 1 dígito antes dela!
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
        with c_m2:
            st.markdown("#### 🪐 Quantas Terras cabem dentro de outros mundos? ($V = \\frac{4}{3}\\pi r^3$)")
            target_planet = st.selectbox("Compare a Terra com:", ["Júpiter", "Sol", "Saturno"])
            if target_planet == "Júpiter":
                st.info("🪐 **Júpiter:** Cabem cerca de **1.321 planetas Terra** dentro do volume de Júpiter!")
            elif target_planet == "Sol":
                st.info("☀️ **Sol:** Cabem impressionantes **1.300.000 planetas Terra** dentro da nossa estrela!")
            else:
                st.info("🪐 **Saturno:** Cabem cerca de **764 planetas Terra** dentro de Saturno!")
                
        if unlock_badge(user["id"], "scientific_notation_wizard"):
            add_xp(user["id"], 120)
            st.balloons()
            st.success("🎉 **Conquista Desbloqueada:** 🧮 Mago das Potências de 10! (+120 XP)")

    # ----------------------------------------------------
    # 4. FÍSICA: LEIS DE KEPLER & VELOCIDADE ORBITAL
    # ----------------------------------------------------
    else:
        st.subheader("🌌 Leis de Johannes Kepler: A Dança dos Planetas")
        st.markdown("""
            Johannes Kepler descobriu que quanto **mais perto do Sol** um planeta está, **mais rápido** ele se move no espaço!
        """)
        
        kepler_data = pd.DataFrame([
            {"Planeta": "Mercúrio", "Distancia_UA": 0.39, "Velocidade_kms": 47.4, "Ano_dias": 88},
            {"Planeta": "Vênus", "Distancia_UA": 0.72, "Velocidade_kms": 35.0, "Ano_dias": 225},
            {"Planeta": "Terra", "Distancia_UA": 1.00, "Velocidade_kms": 29.8, "Ano_dias": 365},
            {"Planeta": "Marte", "Distancia_UA": 1.52, "Velocidade_kms": 24.1, "Ano_dias": 687},
            {"Planeta": "Júpiter", "Distancia_UA": 5.20, "Velocidade_kms": 13.1, "Ano_dias": 4333},
            {"Planeta": "Saturno", "Distancia_UA": 9.58, "Velocidade_kms": 9.7, "Ano_dias": 10759},
            {"Planeta": "Urano", "Distancia_UA": 19.22, "Velocidade_kms": 6.8, "Ano_dias": 30685},
            {"Planeta": "Netuno", "Distancia_UA": 30.05, "Velocidade_kms": 5.4, "Ano_dias": 60189}
        ])
        
        fig_kepler = px.scatter(
            kepler_data,
            x="Distancia_UA",
            y="Velocidade_kms",
            size="Velocidade_kms",
            color="Planeta",
            text="Planeta",
            title="Velocidade Orbital vs Distância do Sol (3ª Lei de Kepler)",
            labels={"Distancia_UA": "Distância do Sol (Unidades Astronômicas)", "Velocidade_kms": "Velocidade Orbital (km/s)"}
        )
        fig_kepler.update_traces(textposition="top center")
        fig_kepler.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(19, 23, 43, 0.6)",
            font=dict(color="#f1f5f9")
        )
        st.plotly_chart(fig_kepler, use_container_width=True)
        
        st.markdown("""
            <div class='cosmic-card'>
                <h4>💡 Conclusão da Física:</h4>
                <p>
                    Mercúrio corre a velozes <strong>47,4 km/s</strong> para a gravidade do Sol não engoli-lo, 
                    enquanto o distante Netuno vaga tranquilamente a apenas <strong>5,4 km/s</strong>!
                </p>
            </div>
        """, unsafe_allow_html=True)
