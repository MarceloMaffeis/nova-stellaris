"""
Nova Stellaris - Arcade Cósmico & Jogos Sci-Fi
Hub unificado com os 3 jogos dos filmes: Astro-Valley, Hail Mary e Interestelar.
"""

import streamlit as st
from modules.astro_valley_web import render_astro_valley
from modules.hail_mary_game import render_hail_mary_game
from modules.interstellar_game import render_interstellar_game

def render_arcade_hub(user: dict, default_game: str = None, *args, **kwargs):
    tab1, tab2, tab3 = st.tabs([
        "🌾 1. Astro-Valley (Perdido em Marte)",
        "✨ 2. Operação Hail Mary (Devoradores de Estrelas)",
        "⏳ 3. Manobra em Gargantua (Interestelar)"
    ])
    with tab1:
        render_astro_valley(user)
    with tab2:
        render_hail_mary_game(user)
    with tab3:
        render_interstellar_game(user)
