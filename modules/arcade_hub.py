"""
Nova Stellaris - Arcade Cósmico & Jogos Sci-Fi
Hub unificado com os 3 jogos dos filmes: Astro-Valley, Hail Mary e Interestelar.
"""

import streamlit as st
from modules.astro_valley_web import render_astro_valley
from modules.hail_mary_game import render_hail_mary_game
from modules.interstellar_game import render_interstellar_game

def render_arcade_hub(user: dict):
    st.markdown("""
        <div class='cosmic-hero' style='background: linear-gradient(135deg, rgba(30,16,60,0.95), rgba(16,20,47,0.95)); border: 1px solid #ffd166;'>
            <h1 style='color: #ffd166; margin-bottom: 5px;'>🎮 Arcade Cósmico STEAM — Trilogia Sci-Fi</h1>
            <p style='color: #cbd5e1; font-size: 1.1rem; margin: 0;'>
                Três jogos completos com <strong>Telas de Início (Start)</strong>, <strong>Física/Ciência em tempo real</strong> e <strong>Telas de Fim (Vitória & Recompensas)</strong>!
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    game_tab1, game_tab2, game_tab3 = st.tabs([
        "🌾 1. Astro-Valley (Perdido em Marte)",
        "✨ 2. Operação Hail Mary (Devoradores de Estrelas)",
        "⏳ 3. Manobra em Gargantua (Interestelar)"
    ])
    
    with game_tab1:
        render_astro_valley(user)
        
    with game_tab2:
        render_hail_mary_game(user)
        
    with game_tab3:
        render_interstellar_game(user)
