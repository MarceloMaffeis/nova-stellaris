"""
Nova Stellaris - Plataforma Interativa de Aprendizado Espacial STEAM
Ponto de entrada principal com Centro de Comando em Tela Cheia,
Acesso Direto a todos os Aplicativos, Botão Universal de Retorno e Perfis.
"""

import sys
import os

# Garantir que o diretório raiz e subpastas estejam no caminho de busca do Python
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
MODULES_DIR = os.path.join(BASE_DIR, "modules")
if MODULES_DIR not in sys.path:
    sys.path.insert(0, MODULES_DIR)

import streamlit as st
import streamlit.components.v1 as components

# Configuração da página
st.set_page_config(
    page_title="Nova Stellaris — Centro de Comando STEAM",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Injetar meta tags Open Graph diretamente no index.html do Streamlit para crawlers de redes sociais (WhatsApp, etc.)
def patch_index_html():
    try:
        streamlit_path = os.path.dirname(st.__file__)
        index_path = os.path.join(streamlit_path, "static", "index.html")
        if os.path.exists(index_path):
            with open(index_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            og_meta_tags = """
    <!-- Open Graph / Rich Social Preview (WhatsApp, Classroom, Discord, Redes Sociais) -->
    <meta property="og:type" content="website" />
    <meta property="og:site_name" content="Nova Stellaris" />
    <meta property="og:title" content="🚀 Nova Stellaris — Centro de Comando Espacial STEAM" />
    <meta property="og:description" content="Plataforma interativa de astronomia, física, matemática e ciências espaciais para jovens e estudantes. Explore planetas, simule missões cósmicas e aprenda com CosmoAI!" />
    <meta property="og:image" content="https://raw.githubusercontent.com/MarceloMaffeis/nova-stellaris/main/assets/images/earth.jpg" />
    <meta property="og:image:secure_url" content="https://raw.githubusercontent.com/MarceloMaffeis/nova-stellaris/main/assets/images/earth.jpg" />
    <meta property="og:image:type" content="image/jpeg" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:url" content="https://nova-stellaris.streamlit.app" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="🚀 Nova Stellaris — Centro de Comando Espacial STEAM" />
    <meta name="twitter:description" content="Plataforma interativa de astronomia, física, matemática e ciências espaciais para jovens e estudantes." />
    <meta name="twitter:image" content="https://raw.githubusercontent.com/MarceloMaffeis/nova-stellaris/main/assets/images/earth.jpg" />
            """
            if "og:title" not in content and "<head>" in content:
                content = content.replace("<head>", f"<head>{og_meta_tags}")
                with open(index_path, "w", encoding="utf-8") as f:
                    f.write(content)
    except Exception:
        pass

patch_index_html()

def inject_seo_tags():
    """Injeta meta tags Open Graph no cabeçalho da janela principal para navegadores e compartilhamento."""
    components.html(
        """
        <script>
            try {
                const head = window.parent.document.head;
                const metaTags = [
                    { property: 'og:title', content: '🚀 Nova Stellaris — Centro de Comando Espacial STEAM' },
                    { property: 'og:description', content: 'Plataforma interativa de astronomia, física, matemática e ciências espaciais para jovens e estudantes. Explore planetas, simule missões cósmicas e aprenda com CosmoAI!' },
                    { property: 'og:image', content: 'https://raw.githubusercontent.com/MarceloMaffeis/nova-stellaris/main/assets/images/earth.jpg' },
                    { property: 'og:type', content: 'website' },
                    { property: 'og:url', content: 'https://nova-stellaris.streamlit.app' },
                    { name: 'twitter:card', content: 'summary_large_image' },
                    { name: 'twitter:title', content: '🚀 Nova Stellaris — Centro de Comando Espacial STEAM' },
                    { name: 'twitter:description', content: 'Plataforma interativa de astronomia e ciências espaciais.' },
                    { name: 'twitter:image', content: 'https://raw.githubusercontent.com/MarceloMaffeis/nova-stellaris/main/assets/images/earth.jpg' }
                ];
                metaTags.forEach(m => {
                    let selector = m.property ? `meta[property='${m.property}']` : `meta[name='${m.name}']`;
                    let el = head.querySelector(selector);
                    if (!el) {
                        el = window.parent.document.createElement('meta');
                        if (m.property) el.setAttribute('property', m.property);
                        if (m.name) el.setAttribute('name', m.name);
                        head.appendChild(el);
                    }
                    el.setAttribute('content', m.content);
                });
            } catch(e) {}
        </script>
        """,
        height=0,
        width=0,
    )

def scroll_to_top():
    """Garante que a visualização role instantaneamente para o topo ao carregar ou trocar de tela."""
    components.html(
        """
        <script>
            function forceScrollTop() {
                try {
                    const doc = window.parent.document;
                    const targets = [
                        doc.querySelector('section.main'),
                        doc.querySelector('[data-testid="stMain"]'),
                        doc.querySelector('[data-testid="stAppViewContainer"]'),
                        doc.querySelector('.main'),
                        window.parent,
                        window
                    ];
                    targets.forEach(t => {
                        if (t && typeof t.scrollTo === 'function') {
                            t.scrollTo({ top: 0, left: 0, behavior: 'instant' });
                        }
                        if (t && t.scrollTop !== undefined) {
                            t.scrollTop = 0;
                        }
                    });
                } catch(e) {}
            }
            forceScrollTop();
            setTimeout(forceScrollTop, 30);
            setTimeout(forceScrollTop, 120);
            setTimeout(forceScrollTop, 300);
        </script>
        """,
        height=0,
        width=0,
    )

# Inicializar Banco de Dados
from database import (
    init_db, 
    get_user_by_id, 
    update_user_profile, 
    get_user_badges, 
    get_user_stats,
    get_announcements
)
init_db()

# Carregar CSS
def load_css():
    css_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "styles.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()
inject_seo_tags()

# Importar Módulos da Aplicação com Recarregamento Dinâmico (Evita cache antigo no Streamlit Cloud)
import importlib
from assets.badges import BADGES, get_rank_for_xp
from modules.auth import render_auth_page
from modules.admin_dashboard import render_admin_dashboard

import modules.observatory
importlib.reload(modules.observatory)
from modules.observatory import render_observatory

import modules.knowledge_hub
importlib.reload(modules.knowledge_hub)
from modules.knowledge_hub import render_knowledge_hub

import modules.steam_lab
importlib.reload(modules.steam_lab)
from modules.steam_lab import render_steam_lab

import modules.steam_academy
importlib.reload(modules.steam_academy)
from modules.steam_academy import render_steam_academy

import modules.sci_fi_missions
importlib.reload(modules.sci_fi_missions)
from modules.sci_fi_missions import render_sci_fi_missions

import modules.arcade_hub
importlib.reload(modules.arcade_hub)
from modules.arcade_hub import render_arcade_hub

from modules.cosmo_ai import render_cosmo_ai
from modules.quiz_game import render_quiz_game

def safe_call(render_fn, user_data, **kwargs):
    """Executa a função de renderização de forma segura contra divergências de versão em cache."""
    try:
        render_fn(user_data, **kwargs)
    except TypeError:
        render_fn(user_data)


# ----------------------------------------------------------------------
# CONTROLE DE SESSÃO & AUTENTICAÇÃO
# ----------------------------------------------------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "current_page" not in st.session_state:
    st.session_state.current_page = "home"

# Redirecionamento legado para compatibilidade
if "redirect_target" in st.session_state and st.session_state.redirect_target:
    st.session_state.current_page = "home"
    st.session_state.redirect_target = None

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
    rank_info = get_rank_for_xp(user["xp"])
    current_rank = rank_info["current"]
    next_rank = rank_info["next"]
    progress_pct = rank_info["progress_pct"]
    unlocked_badges = set(get_user_badges(user["id"]))

    # ----------------------------------------------------------------------
    # BARRA LATERAL (SIDEBAR): PERFIL DO USUÁRIO & NAVEGAÇÃO DE APOIO
    # ----------------------------------------------------------------------
    with st.sidebar:
        st.markdown("""
            <div style='text-align: center; margin-bottom: 12px;'>
                <h1 style='color: #00d4ff; font-size: 1.7rem; margin: 0;'>NOVA STELLARIS</h1>
                <p style='color: #94a3b8; font-size: 0.85rem; margin: 0;'>Estação Científica STEAM</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Cartão de Perfil do Usuário
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
                <div style='margin-top: 8px; text-align: center; font-size: 0.75rem; color: #cbd5e1;'>
                    🏅 <strong>{len(unlocked_badges)} de {len(BADGES)}</strong> medalhas conquistadas
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Botão direto para o Menu Principal
        is_at_home = st.session_state.current_page == "home"
        if st.button("🏠 Menu Principal (Início)", use_container_width=True, type="primary" if is_at_home else "secondary"):
            st.session_state.current_page = "home"
            st.rerun()

        # Botão de Acesso ao Painel do Docente
        if is_teacher:
            if st.button("👑 Painel do Docente (Admin)", use_container_width=True):
                st.session_state.current_page = "admin_dashboard"
                st.rerun()

        st.markdown("---")

        # Atalhos rápidos para navegar sem voltar (caso queira)
        with st.expander("🧭 Acesso Rápido aos Módulos", expanded=False):
            st.caption("Salte diretamente para qualquer aplicativo:")
            if st.button("🪐 Atlas dos Mundos", use_container_width=True, key="sb_atlas"):
                st.session_state.current_page = "obs_atlas"
                st.rerun()
            if st.button("⚖️ Balança Planetária", use_container_width=True, key="sb_balance"):
                st.session_state.current_page = "obs_balance"
                st.rerun()
            if st.button("🧪 Laboratório STEAM", use_container_width=True, key="sb_steam_lab"):
                st.session_state.current_page = "steam_chem"
                st.rerun()
            if st.button("💻 Terminal do Rover", use_container_width=True, key="sb_rover"):
                st.session_state.current_page = "steam_rover"
                st.rerun()
            if st.button("🚀 Missões Sci-Fi", use_container_width=True, key="sb_scifi"):
                st.session_state.current_page = "scifi_martian"
                st.rerun()
            if st.button("🎮 Arcade Cósmico", use_container_width=True, key="sb_arcade"):
                st.session_state.current_page = "arcade_hub"
                st.rerun()
            if st.button("📚 Biblioteca Cósmica", use_container_width=True, key="sb_library"):
                st.session_state.current_page = "lib_encyclopedia"
                st.rerun()
            if st.button("🤖 CosmoAI Mentor", use_container_width=True, key="sb_cosmo"):
                st.session_state.current_page = "cosmo_ai"
                st.rerun()
            if st.button("🎮 AstroQuiz STEAM", use_container_width=True, key="sb_quiz"):
                st.session_state.current_page = "quiz_game"
                st.rerun()
            if st.button("🏆 Minhas Insígnias", use_container_width=True, key="sb_badges"):
                st.session_state.current_page = "badges_gallery"
                st.rerun()

        # Edição de Perfil
        with st.expander("⚙️ Editar Meu Perfil", expanded=False):
            new_name = st.text_input("Seu Nome:", value=user["name"])
            avatar_options = ["👩‍🚀", "👨‍🚀", "🚀", "🤖", "👾", "🌟", "🪐", "🔬", "🔭"]
            new_avatar = st.selectbox("Seu Avatar:", avatar_options, index=avatar_options.index(user["avatar"]) if user["avatar"] in avatar_options else 0)
            
            if st.button("Salvar Alterações", key="btn_save_profile"):
                if new_name.strip():
                    update_user_profile(user["id"], new_name.strip(), new_avatar)
                    st.session_state.current_user["name"] = new_name.strip()
                    st.session_state.current_user["avatar"] = new_avatar
                    st.session_state.current_username = new_name.strip()
                    st.session_state.current_avatar = new_avatar
                    st.success("Perfil atualizado!")
                    st.rerun()
                    
        # Botão de Logout
        if st.button("🚪 Sair / Trocar de Conta", use_container_width=True, key="btn_logout"):
            st.session_state.authenticated = False
            st.session_state.current_user = None
            st.session_state.current_page = "home"
            st.rerun()
            
        st.markdown("---")
        st.markdown("""
            <div style='text-align: center; color: #64748b; font-size: 0.8rem;'>
                <p>⭐ Desenvolvido para jovens cientistas curiosos</p>
                <p><a href='https://github.com/MarceloMaffeis/nova-stellaris' target='_blank' style='color: #00d4ff; text-decoration: none;'>GitHub: MarceloMaffeis/nova-stellaris</a></p>
            </div>
        """, unsafe_allow_html=True)

    # ----------------------------------------------------------------------
    # FUNÇÃO: RENDERIZAR GALERIA DE INSÍGNIAS
    # ----------------------------------------------------------------------
    def render_badges_page():
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

    # ----------------------------------------------------------------------
    # FUNÇÃO: RENDERIZAR O CENTRO DE COMANDO (TELA CHEIA PRINCIPAL)
    # ----------------------------------------------------------------------
    def render_command_center():
        # Hero Banner de Boas-Vindas
        st.markdown(f"""
            <div class='cosmic-hero' style='background: linear-gradient(135deg, rgba(16,30,65,0.95), rgba(10,18,45,0.95)); border: 1px solid #00d4ff;'>
                <div style='display: flex; align-items: center; justify-content: center; gap: 16px; flex-wrap: wrap;'>
                    <span style='font-size: 3.2rem;'>{user['avatar']}</span>
                    <div style='text-align: left;'>
                        <h1 style='color: #00d4ff; margin: 0; font-size: 2rem;'>Centro de Comando — Cadete {user['name']}</h1>
                        <p style='color: #cbd5e1; font-size: 1.05rem; margin: 4px 0 0 0;'>
                            Turma: <strong>{user.get('class_name', '6º Ano')}</strong> &nbsp;|&nbsp; Patente: <strong style='color: {current_rank['badge_color']};'>{current_rank['icon']} {current_rank['title']}</strong> &nbsp;|&nbsp; XP: <strong style='color: #ffd166;'>{user['xp']} pts</strong>
                        </p>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Se for professor, banner especial de acesso ao painel do docente
        if is_teacher:
            st.markdown("""
                <div style='background: linear-gradient(135deg, rgba(35,25,60,0.9), rgba(20,15,40,0.9)); border: 1px solid #ffd166; border-radius: 12px; padding: 14px 20px; margin-bottom: 20px; display: flex; align-items: center; justify-content: space-between;'>
                    <div>
                        <h4 style='color: #ffd166; margin: 0;'>👑 Modo Docente Ativo</h4>
                        <p style='color: #cbd5e1; font-size: 0.85rem; margin: 2px 0 0 0;'>Gerencie turmas, crie missões para seus alunos e acompanhe o desempenho da classe.</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            if st.button("👑 Acessar Painel do Docente (Gerenciar Alunos & Turmas)", use_container_width=True, key="btn_hero_teacher"):
                st.session_state.current_page = "admin_dashboard"
                st.rerun()

        # Mural de Missões e Avisos do Professor
        user_class = user.get("class_name", "6º Ano A")
        announcements = get_announcements(user_class)
        if announcements:
            st.markdown("### 📢 Mensagens & Missões do Professor:")
            for ann in announcements[:2]:
                st.markdown(f"""
                    <div style='background: linear-gradient(135deg, rgba(25,35,70,0.85), rgba(19,23,43,0.85)); border: 1px solid #ffd166; border-left: 6px solid #ffd166; border-radius: 12px; padding: 14px 18px; margin-bottom: 12px;'>
                        <div style='display: flex; justify-content: space-between; align-items: center;'>
                            <h4 style='color: #ffd166; margin: 0;'>{ann['title']}</h4>
                            <span class='steam-tag' style='background: rgba(255,209,102,0.2); color: #ffd166;'>🎁 +{ann['xp_reward']} XP</span>
                        </div>
                        <p style='color: #f1f5f9; font-size: 0.92rem; margin: 6px 0;'>{ann['content']}</p>
                        <span style='color: #94a3b8; font-size: 0.78rem;'>👨‍🏫 Postado por {ann['teacher_name']}</span>
                    </div>
                """, unsafe_allow_html=True)

        st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 1rem; margin: 15px 0 25px 0;'>✨ <strong>Clique em qualquer aplicativo abaixo</strong> para abrir diretamente a ferramenta desejada:</p>", unsafe_allow_html=True)

        # ======================================================================
        # SETOR 1: 🔭 OBSERVATÓRIO DO COSMOS
        # ======================================================================
        st.markdown("""
            <div class='sector-header'>
                <span style='font-size: 1.8rem;'>🔭</span>
                <div>
                    <h2 style='color: #ffd166;'>Setor 1 — Observatório do Cosmos</h2>
                    <p class='sector-desc'>Explore planetas reais, calcule pesos gravitacionais, viagens e fotos do James Webb</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

        c1, c2, c3, c4, c5 = st.columns(5)
        
        with c1:
            st.markdown("""
                <div class='hub-card sector-obs'>
                    <div class='hub-card-icon'>🪐</div>
                    <h3 class='hub-card-title'>Atlas Planetário</h3>
                    <p class='hub-card-desc'>Dados físicos, raios, temperaturas e fotos reais dos mundos.</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Abrir Atlas 🪐", use_container_width=True, key="btn_c_atlas"):
                st.session_state.current_page = "obs_atlas"
                st.rerun()

        with c2:
            st.markdown("""
                <div class='hub-card sector-obs'>
                    <div class='hub-card-icon'>⚖️</div>
                    <h3 class='hub-card-title'>Balança Cósmica</h3>
                    <p class='hub-card-desc'>Descubra seu peso e o salto em Marte, Júpiter e na Lua.</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Pesar Agora ⚖️", use_container_width=True, key="btn_c_balance"):
                st.session_state.current_page = "obs_balance"
                st.rerun()

        with c3:
            st.markdown("""
                <div class='hub-card sector-obs'>
                    <div class='hub-card-icon'>🚀</div>
                    <h3 class='hub-card-title'>Calculadora Cósmica</h3>
                    <p class='hub-card-desc'>Tempo de viagem na velocidade da luz, foguetes e sondas.</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Calcular Viagem 🚀", use_container_width=True, key="btn_c_calc"):
                st.session_state.current_page = "obs_calc"
                st.rerun()

        with c4:
            st.markdown("""
                <div class='hub-card sector-obs'>
                    <div class='hub-card-icon'>📸</div>
                    <h3 class='hub-card-title'>Galeria James Webb</h3>
                    <p class='hub-card-desc'>Fotos em altíssima definição de nebulosas e buracos negros.</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Ver Galeria 📸", use_container_width=True, key="btn_c_gallery"):
                st.session_state.current_page = "obs_gallery"
                st.rerun()

        with c5:
            st.markdown("""
                <div class='hub-card sector-obs'>
                    <div class='hub-card-icon'>🌠</div>
                    <h3 class='hub-card-title'>Foto do Dia (APOD)</h3>
                    <p class='hub-card-desc'>A imagem astronômica diária oficial da NASA explicada.</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Ver Foto NASA 🌠", use_container_width=True, key="btn_c_apod"):
                st.session_state.current_page = "obs_apod"
                st.rerun()

        # ======================================================================
        # SETOR 2: 🧪 LABORATÓRIOS STEAM (MÃO NA MASSA)
        # ======================================================================
        st.markdown("""
            <div class='sector-header'>
                <span style='font-size: 1.8rem;'>🧪</span>
                <div>
                    <h2 style='color: #00f5d4;'>Setor 2 — Laboratórios STEAM & Experimentos</h2>
                    <p class='sector-desc'>Química nas estrelas, órbitas de Kepler, código do Rover e trilhas explicadas</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

        s1, s2, s3, s4, s5 = st.columns(5)

        with s1:
            st.markdown("""
                <div class='hub-card sector-steam'>
                    <div class='hub-card-icon'>🧪</div>
                    <h3 class='hub-card-title'>Química das Estrelas</h3>
                    <p class='hub-card-desc'>A forja dos átomos no cosmos e reator de foguetes.</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Laboratório Químico 🧪", use_container_width=True, key="btn_c_chem"):
                st.session_state.current_page = "steam_chem"
                st.rerun()

        with s2:
            st.markdown("""
                <div class='hub-card sector-steam'>
                    <div class='hub-card-icon'>💻</div>
                    <h3 class='hub-card-title'>Terminal do Rover</h3>
                    <p class='hub-card-desc'>Programe o robô Perseverance para desviar de crateras.</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Programar Rover 💻", use_container_width=True, key="btn_c_rover"):
                st.session_state.current_page = "steam_rover"
                st.rerun()

        with s3:
            st.markdown("""
                <div class='hub-card sector-steam'>
                    <div class='hub-card-icon'>🧮</div>
                    <h3 class='hub-card-title'>Matemática Espacial</h3>
                    <p class='hub-card-desc'>Mago da notação científica, potências de 10 e volumes.</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Abrir Matemática 🧮", use_container_width=True, key="btn_c_math"):
                st.session_state.current_page = "steam_math"
                st.rerun()

        with s4:
            st.markdown("""
                <div class='hub-card sector-steam'>
                    <div class='hub-card-icon'>⚡</div>
                    <h3 class='hub-card-title'>Física & Órbitas</h3>
                    <p class='hub-card-desc'>As 3 Leis de Kepler, velocidade orbital e gravidade.</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Abrir Física ⚡", use_container_width=True, key="btn_c_phys"):
                st.session_state.current_page = "steam_physics"
                st.rerun()

        with s5:
            st.markdown("""
                <div class='hub-card sector-steam'>
                    <div class='hub-card-icon'>🎓</div>
                    <h3 class='hub-card-title'>Trilhas da Academia</h3>
                    <p class='hub-card-desc'>Lições completas do 6º ano ao Ensino Médio com exercícios.</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Aulas da Academia 🎓", use_container_width=True, key="btn_c_acad"):
                st.session_state.current_page = "steam_academy"
                st.rerun()

        # ======================================================================
        # SETOR 3: 🚀 MISSÕES & JOGOS SCI-FI
        # ======================================================================
        st.markdown("""
            <div class='sector-header'>
                <span style='font-size: 1.8rem;'>🚀</span>
                <div>
                    <h2 style='color: #f72585;'>Setor 3 — Missões & Jogos Sci-Fi</h2>
                    <p class='sector-desc'>Do cinema à ciência real: viva as missões de Perdido em Marte, Hail Mary e Interestelar</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

        m1, m2, m3, m4 = st.columns(4)

        with m1:
            st.markdown("""
                <div class='hub-card sector-scifi'>
                    <div class='hub-card-icon'>🔴</div>
                    <h3 class='hub-card-title'>Perdido em Marte</h3>
                    <p class='hub-card-desc'>Produza água, cultive batatas e decodifique Pathfinder em Hex.</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Missão Marte 🔴", use_container_width=True, key="btn_c_martian"):
                st.session_state.current_page = "scifi_martian"
                st.rerun()

        with m2:
            st.markdown("""
                <div class='hub-card sector-scifi'>
                    <div class='hub-card-icon'>✨</div>
                    <h3 class='hub-card-title'>Devoradores de Estrelas</h3>
                    <p class='hub-card-desc'>Gere 1g por rotação na Hail Mary e converse com Rocky por acordes.</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Missão Hail Mary ✨", use_container_width=True, key="btn_c_hailmary"):
                st.session_state.current_page = "scifi_hailmary"
                st.rerun()

        with m3:
            st.markdown("""
                <div class='hub-card sector-scifi'>
                    <div class='hub-card-icon'>⏳</div>
                    <h3 class='hub-card-title'>Interestelar (Gargantua)</h3>
                    <p class='hub-card-desc'>Dilatação do tempo no Planeta Miller e órbita no buraco negro.</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Missão Interestelar ⏳", use_container_width=True, key="btn_c_interstellar"):
                st.session_state.current_page = "scifi_interstellar"
                st.rerun()

        with m4:
            st.markdown("""
                <div class='hub-card sector-scifi'>
                    <div class='hub-card-icon'>🎮</div>
                    <h3 class='hub-card-title'>Arcade Cósmico (3 Jogos)</h3>
                    <p class='hub-card-desc'>Jogue Astro-Valley, Operação Hail Mary e Gargantua no navegador.</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Entrar no Arcade 🎮", use_container_width=True, key="btn_c_arcade"):
                st.session_state.current_page = "arcade_hub"
                st.rerun()

        # ======================================================================
        # SETOR 4: 📚 BIBLIOTECA CÓSMICA & PESQUISA
        # ======================================================================
        st.markdown("""
            <div class='sector-header'>
                <span style='font-size: 1.8rem;'>📚</span>
                <div>
                    <h2 style='color: #38bdf8;'>Setor 4 — Biblioteca Cósmica & Exploração do Céu</h2>
                    <p class='sector-desc'>Enciclopédia de termos, fotos dos grandes cientistas, telescópios e guia das estrelas</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

        b1, b2, b3, b4, b5 = st.columns(5)

        with b1:
            st.markdown("""
                <div class='hub-card sector-library'>
                    <div class='hub-card-icon'>🔍</div>
                    <h3 class='hub-card-title'>Enciclopédia & Glossário</h3>
                    <p class='hub-card-desc'>Busque mais de 20 conceitos astronômicos explicados.</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Pesquisar Termos 🔍", use_container_width=True, key="btn_c_enc"):
                st.session_state.current_page = "lib_encyclopedia"
                st.rerun()

        with b2:
            st.markdown("""
                <div class='hub-card sector-library'>
                    <div class='hub-card-icon'>👩‍🔬</div>
                    <h3 class='hub-card-title'>Grandes Cientistas</h3>
                    <p class='hub-card-desc'>Fotos, biografias e frases de Marie Curie, Sagan, Einstein e mais.</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Ver Cientistas 👩‍🔬", use_container_width=True, key="btn_c_sci"):
                st.session_state.current_page = "lib_scientists"
                st.rerun()

        with b3:
            st.markdown("""
                <div class='hub-card sector-library'>
                    <div class='hub-card-icon'>🛰️</div>
                    <h3 class='hub-card-title'>Missões & Telescópios</h3>
                    <p class='hub-card-desc'>James Webb, Hubble, Perseverance, Voyager e ISS com fotos.</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Ver Missões 🛰️", use_container_width=True, key="btn_c_miss"):
                st.session_state.current_page = "lib_missions"
                st.rerun()

        with b4:
            st.markdown("""
                <div class='hub-card sector-library'>
                    <div class='hub-card-icon'>🔭</div>
                    <h3 class='hub-card-title'>Guia do Céu Noturno</h3>
                    <p class='hub-card-desc'>Como achar o Cruzeiro do Sul, fases da Lua e meteoros.</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Aprender a Olhar o Céu 🔭", use_container_width=True, key="btn_c_sky"):
                st.session_state.current_page = "lib_sky"
                st.rerun()

        with b5:
            st.markdown("""
                <div class='hub-card sector-library'>
                    <div class='hub-card-icon'>🌐</div>
                    <h3 class='hub-card-title'>Simuladores 3D & Canais</h3>
                    <p class='hub-card-desc'>NASA Eyes, Stellarium 3D e canais educativos do YouTube.</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Ver Links Úteis 🌐", use_container_width=True, key="btn_c_links"):
                st.session_state.current_page = "lib_links"
                st.rerun()

        # ======================================================================
        # SETOR 5: 🤖 MENTORIA IA & CONQUISTAS
        # ======================================================================
        st.markdown("""
            <div class='sector-header'>
                <span style='font-size: 1.8rem;'>🤖</span>
                <div>
                    <h2 style='color: #a855f7;'>Setor 5 — Mentoria IA, Quiz & Conquistas</h2>
                    <p class='sector-desc'>Converse com o astrofísico de IA, dispute pontos no quiz e desbloqueie insígnias</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

        a1, a2, a3 = st.columns(3)

        with a1:
            st.markdown("""
                <div class='hub-card sector-ai'>
                    <div class='hub-card-icon'>🤖</div>
                    <h3 class='hub-card-title'>CosmoAI (Mentor Espacial)</h3>
                    <p class='hub-card-desc'>Tire qualquer dúvida de ciências e peça desafios inteligentes com Google Gemini IA.</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Conversar com CosmoAI 🤖", use_container_width=True, key="btn_c_cosmo"):
                st.session_state.current_page = "cosmo_ai"
                st.rerun()

        with a2:
            st.markdown("""
                <div class='hub-card sector-ai'>
                    <div class='hub-card-icon'>🎮</div>
                    <h3 class='hub-card-title'>AstroQuiz STEAM</h3>
                    <p class='hub-card-desc'>Desafios categorizados por nível e matéria com ganho de XP e ranking.</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Jogar AstroQuiz 🎮", use_container_width=True, key="btn_c_quiz"):
                st.session_state.current_page = "quiz_game"
                st.rerun()

        with a3:
            st.markdown("""
                <div class='hub-card sector-ai'>
                    <div class='hub-card-icon'>🏆</div>
                    <h3 class='hub-card-title'>Mural de Insígnias Cósmicas</h3>
                    <p class='hub-card-desc'>Veja suas medalhas desbloqueadas, patentes e recompensas de XP.</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Ver Minhas Medalhas 🏆", use_container_width=True, key="btn_c_badges"):
                st.session_state.current_page = "badges_gallery"
                st.rerun()

        st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)

    # ----------------------------------------------------------------------
    # BARRA UNIVERSAL DE NAVEGAÇÃO & RETORNO PARA TELAS INTERNAS
    # ----------------------------------------------------------------------
    page_configs = {
        "obs_atlas": {"title": "Atlas Planetário", "icon": "🪐", "sector": "Observatório"},
        "obs_balance": {"title": "Balança Interplanetária", "icon": "⚖️", "sector": "Observatório"},
        "obs_calc": {"title": "Calculadora Cósmica", "icon": "🚀", "sector": "Observatório"},
        "obs_gallery": {"title": "Galeria James Webb & Hubble", "icon": "📸", "sector": "Observatório"},
        "obs_apod": {"title": "Foto Astronômica do Dia (NASA)", "icon": "🌠", "sector": "Observatório"},
        "steam_chem": {"title": "Química Cósmica & Reator", "icon": "🧪", "sector": "Laboratório STEAM"},
        "steam_rover": {"title": "Terminal do Rover Perseverance", "icon": "💻", "sector": "Laboratório STEAM"},
        "steam_math": {"title": "Matemática Espacial & Volume", "icon": "🧮", "sector": "Laboratório STEAM"},
        "steam_physics": {"title": "Física & Leis de Kepler", "icon": "⚡", "sector": "Laboratório STEAM"},
        "steam_academy": {"title": "Academia Nova Stellaris", "icon": "🎓", "sector": "Fundamentos STEAM"},
        "scifi_martian": {"title": "Missão: Perdido em Marte", "icon": "🔴", "sector": "Missões Sci-Fi"},
        "scifi_hailmary": {"title": "Missão: Devoradores de Estrelas", "icon": "✨", "sector": "Missões Sci-Fi"},
        "scifi_interstellar": {"title": "Missão: Interestelar (Gargantua)", "icon": "⏳", "sector": "Missões Sci-Fi"},
        "arcade_hub": {"title": "Arcade Cósmico — Trilogia Sci-Fi", "icon": "🎮", "sector": "Jogos"},
        "lib_encyclopedia": {"title": "Enciclopédia de Termos Cósmicos", "icon": "🔍", "sector": "Biblioteca Cósmica"},
        "lib_scientists": {"title": "Galeria dos Grandes Cientistas", "icon": "👩‍🔬", "sector": "Biblioteca Cósmica"},
        "lib_missions": {"title": "Grandes Missões & Telescópios", "icon": "🛰️", "sector": "Biblioteca Cósmica"},
        "lib_sky": {"title": "Guia de Observação do Céu Noturno", "icon": "🔭", "sector": "Biblioteca Cósmica"},
        "lib_links": {"title": "Simuladores 3D & Canais de Ciência", "icon": "🌐", "sector": "Biblioteca Cósmica"},
        "cosmo_ai": {"title": "CosmoAI — Mentor Espacial", "icon": "🤖", "sector": "Mentoria com IA"},
        "quiz_game": {"title": "AstroQuiz STEAM", "icon": "🎮", "sector": "Desafios & XP"},
        "badges_gallery": {"title": "Mural de Insígnias Cósmicas", "icon": "🏆", "sector": "Conquistas"},
        "admin_dashboard": {"title": "Painel de Controle do Docente", "icon": "👑", "sector": "Área do Professor"}
    }

    current_page = st.session_state.current_page
    scroll_to_top()

    # RENDERIZAÇÃO DA PÁGINA ESCOLHIDA
    if current_page == "home":
        render_command_center()
    else:
        cfg = page_configs.get(current_page, {"title": "Estação Espacial", "icon": "🚀", "sector": "Nova Stellaris"})
        
        # Barra de Topo com Botão Voltar
        col_btn_back, col_nav_info = st.columns([1.2, 3.8])
        with col_btn_back:
            if st.button("⬅️ Voltar ao Menu Principal", key="btn_top_back", use_container_width=True, type="primary"):
                st.session_state.current_page = "home"
                st.rerun()
        with col_nav_info:
            st.markdown(f"""
                <div class='top-nav-bar' style='margin: 0; padding: 10px 18px;'>
                    <span class='top-nav-title'>{cfg['icon']} {cfg['title']}</span>
                    <span class='top-nav-breadcrumb'>Setor: {cfg['sector']}</span>
                </div>
            """, unsafe_allow_html=True)
            
        st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

        # Roteamento dos Módulos Específicos com Blindagem contra Erros de Cache
        if current_page == "obs_atlas":
            st.session_state.observatory_tool_default = "Atlas"
            safe_call(render_observatory, user, default_tool="Atlas")
        elif current_page == "obs_balance":
            st.session_state.observatory_tool_default = "Balança"
            safe_call(render_observatory, user, default_tool="Balança")
        elif current_page == "obs_calc":
            st.session_state.observatory_tool_default = "Calculadora"
            safe_call(render_observatory, user, default_tool="Calculadora")
        elif current_page == "obs_gallery":
            st.session_state.observatory_tool_default = "Galeria"
            safe_call(render_observatory, user, default_tool="Galeria")
        elif current_page == "obs_apod":
            st.session_state.observatory_tool_default = "APOD"
            safe_call(render_observatory, user, default_tool="APOD")
        elif current_page == "steam_chem":
            st.session_state.steam_lab_default = "Química"
            safe_call(render_steam_lab, user, default_lab="Química")
        elif current_page == "steam_rover":
            st.session_state.steam_lab_default = "Computação"
            safe_call(render_steam_lab, user, default_lab="Computação")
        elif current_page == "steam_math":
            st.session_state.steam_lab_default = "Matemática"
            safe_call(render_steam_lab, user, default_lab="Matemática")
        elif current_page == "steam_physics":
            st.session_state.steam_lab_default = "Física"
            safe_call(render_steam_lab, user, default_lab="Física")
        elif current_page == "steam_academy":
            safe_call(render_steam_academy, user)
        elif current_page == "scifi_martian":
            st.session_state.scifi_mission_default = "Perdido em Marte"
            safe_call(render_sci_fi_missions, user, default_mission="Perdido em Marte")
        elif current_page == "scifi_hailmary":
            st.session_state.scifi_mission_default = "Devoradores de Estrelas"
            safe_call(render_sci_fi_missions, user, default_mission="Devoradores de Estrelas")
        elif current_page == "scifi_interstellar":
            st.session_state.scifi_mission_default = "Interestelar"
            safe_call(render_sci_fi_missions, user, default_mission="Interestelar")
        elif current_page == "arcade_hub":
            safe_call(render_arcade_hub, user)
        elif current_page == "lib_encyclopedia":
            st.session_state.knowledge_subtab_default = "Enciclopédia"
            safe_call(render_knowledge_hub, user, default_subtab="Enciclopédia")
        elif current_page == "lib_scientists":
            st.session_state.knowledge_subtab_default = "Cientistas"
            safe_call(render_knowledge_hub, user, default_subtab="Cientistas")
        elif current_page == "lib_missions":
            st.session_state.knowledge_subtab_default = "Missões"
            safe_call(render_knowledge_hub, user, default_subtab="Missões")
        elif current_page == "lib_sky":
            st.session_state.knowledge_subtab_default = "Guia"
            safe_call(render_knowledge_hub, user, default_subtab="Guia")
        elif current_page == "lib_links":
            st.session_state.knowledge_subtab_default = "Simuladores"
            safe_call(render_knowledge_hub, user, default_subtab="Simuladores")
        elif current_page == "cosmo_ai":
            safe_call(render_cosmo_ai, user)
        elif current_page == "quiz_game":
            safe_call(render_quiz_game, user)
        elif current_page == "badges_gallery":
            render_badges_page()
        elif current_page == "admin_dashboard":
            safe_call(render_admin_dashboard, user)

        # Botão de retorno no rodapé para comodidade do aluno
        st.markdown("---")
        if st.button("⬅️ Voltar ao Menu Principal", key="btn_bottom_back", use_container_width=True):
            st.session_state.current_page = "home"
            st.rerun()
