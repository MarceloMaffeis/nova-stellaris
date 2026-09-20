"""
Nova Stellaris - Arcade Cósmico & Jogos Sci-Fi
Hub unificado com os 3 jogos dos filmes: Astro-Valley, Hail Mary e Interestelar.
"""

import streamlit as st
from modules.astro_valley_web import render_astro_valley
from modules.hail_mary_game import render_hail_mary_game
from modules.interstellar_game import render_interstellar_game

def render_arcade_hub(user: dict, default_game: str = None, *args, **kwargs):
    if not default_game:
        default_game = st.session_state.get("arcade_game_default")
    st.markdown("""
        <div class='cosmic-hero' style='background: linear-gradient(135deg, rgba(30,16,60,0.95), rgba(16,20,47,0.95)); border: 1px solid #ffd166;'>
            <h1 style='color: #ffd166; margin-bottom: 5px;'>🎮 Arcade Cósmico STEAM — Trilogia Sci-Fi</h1>
            <p style='color: #cbd5e1; font-size: 1.1rem; margin: 0;'>
                Três jogos completos com <strong>Telas de Início (Start)</strong>, <strong>Física/Ciência em tempo real</strong> e <strong>Telas de Fim (Vitória & Recompensas)</strong>!
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    game_options = [
        "🌾 1. Astro-Valley (Perdido em Marte)",
        "✨ 2. Operação Hail Mary (Devoradores de Estrelas)",
        "⏳ 3. Manobra em Gargantua (Interestelar)"
    ]
    
    default_idx = 0
    if default_game:
        for i, opt in enumerate(game_options):
            if default_game.lower() in opt.lower():
                default_idx = i
                break
    elif "arcade_game_idx" in st.session_state:
        default_idx = st.session_state.arcade_game_idx

    active_game = st.radio(
        "Selecione o Jogo:",
        game_options,
        index=default_idx,
        horizontal=True,
        label_visibility="collapsed",
        key="arcade_game_selector"
    )
    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    
    if active_game == game_options[0]:
        render_astro_valley(user)
    elif active_game == game_options[1]:
        render_hail_mary_game(user)
    else:
        render_interstellar_game(user)
