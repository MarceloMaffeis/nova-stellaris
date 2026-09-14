"""
Nova Stellaris - Plataforma Interativa de Aprendizado Espacial STEAM
Ponto de entrada principal com Autenticação (Alunos & Docentes),
Painel Administrativo, Portal de Boas-Vindas e Navegação Divisional.
"""

import sys
import os

# Garantir que o diretório raiz e subpastas estejam no caminho de busca do Python no Streamlit Cloud
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
MODULES_DIR = os.path.join(BASE_DIR, "modules")
if MODULES_DIR not in sys.path:
    sys.path.insert(0, MODULES_DIR)

import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Nova Stellaris — Universo STEAM",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar Banco de Dados
from database import (
    init_db, 
    get_user_by_id, 
    get_or_create_user, 
    update_user_profile, 
    get_user_badges, 
    get_user_stats
)
init_db()

# Carregar CSS
def load_css():
    css_path = os.path.join(os.path.dirname(__file__), "assets", "styles.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# Importar Módulos da Aplicação
from assets.badges import BADGES, get_rank_for_xp
from modules.auth import render_auth_page
from modules.student_portal import render_student_portal
from modules.admin_dashboard import render_admin_dashboard
from modules.steam_academy import render_steam_academy
from modules.observatory import render_observatory
from modules.sci_fi_missions import render_sci_fi_missions
from modules.steam_lab import render_steam_lab
from modules.arcade_hub import render_arcade_hub
from modules.cosmo_ai import render_cosmo_ai
from modules.quiz_game import render_quiz_game
from modules.knowledge_hub import render_knowledge_hub

# ----------------------------------------------------------------------
# CONTROLE DE SESSÃO & AUTENTICAÇÃO
# ----------------------------------------------------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None

if not st.session_state.authenticated or not st.session_state.current_user:
    render_auth_page()
else:
    # Recuperar dados atualizados do usuário autenticado
    current_user_id = st.session_state.current_user["id"]
    user = get_user_by_id(current_user_id)
    if not user:
        st.session_state.authenticated = False
        st.session_state.current_user = None
        st.rerun()

    is_teacher = user.get("role") == "docente"

    # ----------------------------------------------------------------------
    # BARRA LATERAL (SIDEBAR): PERFIL DO USUÁRIO & NAVEGAÇÃO
    # ----------------------------------------------------------------------
    with st.sidebar:
        st.markdown("""
            <div style='text-align: center; margin-bottom: 12px;'>
                <h1 style='color: #00d4ff; font-size: 1.8rem; margin: 0;'>NOVA STELLARIS</h1>
                <p style='color: #94a3b8; font-size: 0.85rem; margin: 0;'>Estação Científica STEAM</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Cartão de Perfil do Usuário
        rank_info = get_rank_for_xp(user["xp"])
        current_rank = rank_info["current"]
        next_rank = rank_info["next"]
        progress_pct = rank_info["progress_pct"]
        
        role_badge_html = "<span class='role-badge-teacher'>👑 Docente / Professor</span>" if is_teacher else f"<span class='role-badge-student'>👩‍🚀 {user.get('class_name', 'Aluno')}</span>"
        
        st.markdown(f"""
            <div class='xp-container'>
                <div style='display: flex; align-items: center; gap: 12px;'>
                    <span style='font-size: 2.3rem;'>{user['avatar']}</span>
                    <div>
                        <h3 style='margin: 0; color: #f1f5f9; font-size: 1.1rem;'>{user['name']}</h3>
                        <div style='margin-top: 3px;'>{role_badge_html}</div>
                    </div>
                </div>
                <div style='margin-top: 10px; display: flex; justify-content: space-between; font-size: 0.8rem; color: #94a3b8;'>
                    <span>Pontos: <strong style='color: #ffd166;'>{user['xp']} XP</strong></span>
                    <span>{f"{current_rank['icon']} {current_rank['title']}"}</span>
                </div>
                <div class='xp-bar-bg'>
                    <div class='xp-bar-fill' style='width: {progress_pct}%;'></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Edição de Perfil
        with st.expander("⚙️ Editar Meu Perfil", expanded=False):
            new_name = st.text_input("Seu Nome:", value=user["name"])
            avatar_options = ["👩‍🚀", "👨‍🚀", "🚀", "🤖", "👾", "🌟", "🪐", "🔬", "🔭"]
            new_avatar = st.selectbox("Seu Avatar:", avatar_options, index=avatar_options.index(user["avatar"]) if user["avatar"] in avatar_options else 0)
            
            if st.button("Salvar Alterações"):
                if new_name.strip():
                    update_user_profile(user["id"], new_name.strip(), new_avatar)
                    st.session_state.current_user["name"] = new_name.strip()
                    st.session_state.current_user["avatar"] = new_avatar
                    st.session_state.current_username = new_name.strip()
                    st.session_state.current_avatar = new_avatar
                    st.success("Perfil atualizado!")
                    st.rerun()
                    
        # Botão de Logout
        if st.button("🚪 Sair / Trocar de Conta", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.current_user = None
            st.rerun()
            
        st.markdown("---")
        
        # ------------------------------------------------------------------
        # MENU DE NAVEGAÇÃO DIVIDIDO POR ÁREAS
        # ------------------------------------------------------------------
        st.markdown("### 🧭 Divisões & Módulos")
        
        area_options = [
            "🌟 INÍCIO (Portal do Aluno)" if not is_teacher else "👑 PAINEL DO DOCENTE (Admin & Turmas)",
            "🎓 1. ACADEMIA NOVA STELLARIS (Fundamentos & Trilhas)",
            "🔭 2. EXPLORAÇÃO & CIÊNCIA",
            "🕹️ 3. ARCADE CÓSMICO & JOGOS",
            "🤖 4. MENTORIA IA & CONQUISTAS"
        ]
        
        area_choice = st.selectbox(
            "Selecione a Área da Estação:",
            area_options,
            key="nav_area_selector"
        )
        
        if "INÍCIO" in area_choice:
            nav_option = "🌟 Portal do Aluno (Início)"
        elif "PAINEL DO DOCENTE" in area_choice:
            nav_option = "👑 Painel do Docente (Admin)"
        elif "1. ACADEMIA" in area_choice:
            nav_option = st.radio(
                "Módulo de Aprendizado:",
                [
                    "🎓 Academia Nova Stellaris (Fundamentos & Trilhas)",
                    "🧪 Laboratório Prático de Experimentos"
                ],
                key="nav_mod_academy"
            )
        elif "2. EXPLORAÇÃO" in area_choice:
            nav_option = st.radio(
                "Módulo Científico:",
                [
                    "🌌 Observatório do Cosmos",
                    "🚀 Missões Sci-Fi Interativas"
                ],
                key="nav_mod_exploration"
            )
        elif "3. ARCADE" in area_choice:
            nav_option = st.radio(
                "Módulo de Jogos:",
                [
                    "🕹️ Arcade Cósmico (3 Jogos Sci-Fi)",
                    "🎮 AstroQuiz & Desafios"
                ],
                key="nav_mod_arcade"
            )
        else:
            nav_option = st.radio(
                "Módulo de Apoio & Perfil:",
                [
                    "🤖 CosmoAI (Mentor Espacial)",
                    "📚 Hub de Conhecimento",
                    "🏆 Minhas Insígnias & Conquistas"
                ],
                key="nav_mod_mentor"
            )
        
        st.markdown("---")
        st.markdown("""
            <div style='text-align: center; color: #64748b; font-size: 0.8rem;'>
                <p>⭐ Desenvolvido para jovens cientistas curiosos</p>
                <p><a href='https://github.com/MarceloMaffeis/nova-stellaris' target='_blank' style='color: #00d4ff; text-decoration: none;'>GitHub: MarceloMaffeis/nova-stellaris</a></p>
            </div>
        """, unsafe_allow_html=True)

    # ----------------------------------------------------------------------
    # ÁREA PRINCIPAL: ROTEAMENTO DE MÓDULOS
    # ----------------------------------------------------------------------
    if nav_option == "🌟 Portal do Aluno (Início)":
        render_student_portal(user)
    elif nav_option == "👑 Painel do Docente (Admin)":
        render_admin_dashboard(user)
    elif nav_option == "🎓 Academia Nova Stellaris (Fundamentos & Trilhas)":
        render_steam_academy(user)
    elif nav_option == "🌌 Observatório do Cosmos":
        render_observatory(user)
    elif nav_option == "🚀 Missões Sci-Fi Interativas":
        render_sci_fi_missions(user)
    elif nav_option == "🧪 Laboratório Prático de Experimentos":
        render_steam_lab(user)
    elif nav_option == "🕹️ Arcade Cósmico (3 Jogos Sci-Fi)":
        render_arcade_hub(user)
    elif nav_option == "🤖 CosmoAI (Mentor Espacial)":
        render_cosmo_ai(user)
    elif nav_option == "🎮 AstroQuiz & Desafios":
        render_quiz_game(user)
    elif nav_option == "📚 Hub de Conhecimento":
        render_knowledge_hub(user)
    elif nav_option == "🏆 Minhas Insígnias & Conquistas":
        st.markdown("""
            <div class='cosmic-hero' style='background: linear-gradient(135deg, rgba(30,16,60,0.95), rgba(16,20,47,0.95)); border: 1px solid #ffd166;'>
                <h1 style='color: #ffd166; margin-bottom: 5px;'>🏆 Galeria de Insígnias Cósmicas</h1>
                <p style='color: #cbd5e1; font-size: 1.1rem; margin: 0;'>
                    Colecione todas as medalhas completando missões, experimentos no laboratório e acertando desafios no quiz!
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        unlocked_badge_ids = set(get_user_badges(user["id"]))
        
        col_b1, col_b2, col_b3 = st.columns(3)
        
        for i, (badge_id, badge) in enumerate(BADGES.items()):
            is_unlocked = badge_id in unlocked_badge_ids
            target_col = [col_b1, col_b2, col_b3][i % 3]
            
            with target_col:
                st.markdown(f"""
                    <div class='badge-item {'unlocked' if is_unlocked else 'locked'}' style='margin-bottom: 15px;'>
                        <span style='font-size: 2.5rem;'>{badge['icon']}</span>
                        <h4 style='color: {badge['color'] if is_unlocked else '#94a3b8'}; margin: 5px 0;'>{badge['title']}</h4>
                        <span class='steam-tag' style='background: rgba(255,255,255,0.08); font-size: 0.75rem;'>{badge['category']}</span>
                        <p style='color: #cbd5e1; font-size: 0.85rem; margin-top: 8px;'>{badge['description']}</p>
                        <p style='color: #ffd166; font-size: 0.8rem; font-weight: 700; margin: 0;'>
                            {'✅ Desbloqueada (+ ' + str(badge['xp_reward']) + ' XP)' if is_unlocked else '🔒 Bloqueada (+ ' + str(badge['xp_reward']) + ' XP)'}
                        </p>
                    </div>
                """, unsafe_allow_html=True)

