"""
Nova Stellaris - Portal Inicial do Aluno (Dashboard de Boas-Vindas)
Mural de avisos do professor, botões de acesso rápido aos cursos e resumo de progresso.
"""

import streamlit as st
from database import get_announcements, add_xp
from assets.badges import get_rank_for_xp

def render_student_portal(user: dict):
    rank_info = get_rank_for_xp(user["xp"])
    rank = rank_info["current"]
    
    # Header de Boas-Vindas
    st.markdown(f"""
        <div class='cosmic-hero' style='background: linear-gradient(135deg, rgba(16,30,65,0.95), rgba(10,18,45,0.95)); border: 1px solid #00d4ff;'>
            <div style='display: flex; align-items: center; justify-content: center; gap: 15px;'>
                <span style='font-size: 3rem;'>{user['avatar']}</span>
                <div>
                    <h1 style='color: #00d4ff; margin: 0; font-size: 2rem;'>Olá, Cadete {user['name']}!</h1>
                    <p style='color: #cbd5e1; font-size: 1.1rem; margin: 4px 0 0 0;'>
                        Turma: <strong>{user.get('class_name', '6º Ano')}</strong> | Patente: <strong style='color: {rank['badge_color']};'>{rank['icon']} {rank['title']}</strong> | XP: <strong style='color: #ffd166;'>{user['xp']} pts</strong>
                    </p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # ----------------------------------------------------------------------
    # 1. MURAL DE AVISOS & MISSÕES DO PROFESSOR
    # ----------------------------------------------------------------------
    user_class = user.get("class_name", "6º Ano A")
    announcements = get_announcements(user_class)
    
    if announcements:
        st.markdown("### 📢 Missões & Avisos do Seu Professor:")
        for ann in announcements[:2]: # mostrar os 2 mais recentes
            st.markdown(f"""
                <div style='background: linear-gradient(135deg, rgba(25,35,70,0.85), rgba(19,23,43,0.85)); border: 1px solid #ffd166; border-left: 6px solid #ffd166; border-radius: 12px; padding: 16px 20px; margin-bottom: 15px;'>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <h4 style='color: #ffd166; margin: 0;'>{ann['title']}</h4>
                        <span class='steam-tag' style='background: rgba(255,209,102,0.2); color: #ffd166;'>🎁 +{ann['xp_reward']} XP</span>
                    </div>
                    <p style='color: #f1f5f9; font-size: 0.95rem; margin: 8px 0;'>{ann['content']}</p>
                    <span style='color: #94a3b8; font-size: 0.8rem;'>👨‍🏫 Postado por {ann['teacher_name']}</span>
                </div>
            """, unsafe_allow_html=True)
            
    # ----------------------------------------------------------------------
    # 2. GRADE DE BOTÕES DE ACESSO RÁPIDO AOS CURSOS
    # ----------------------------------------------------------------------
    st.markdown("## 🚀 Acesso Rápido às Estações de Aprendizado")
    st.write("Clique em qualquer estação abaixo para entrar diretamente no conteúdo:")
    
    col1, col2, col3 = st.columns(3)
    
    # Card 1: Matemática
    with col1:
        st.markdown("""
            <div class='course-card' style='border-top: 4px solid #f72585;'>
                <span style='font-size: 2.2rem;'>📐</span>
                <h3 style='color: #f72585; margin: 6px 0;'>Matemática Espacial</h3>
                <p style='color: #cbd5e1; font-size: 0.85rem;'>Proporções, escalas, notação científica, velocidade da luz e Leis de Kepler.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Entrar em Matemática 📐", use_container_width=True, key="btn_portal_math"):
            st.session_state.redirect_target = {
                "area": "🎓 1. ACADEMIA NOVA STELLARIS (Fundamentos & Trilhas)",
                "module_key": "nav_mod_academy",
                "module_val": "🎓 Academia Nova Stellaris (Fundamentos & Trilhas)"
            }
            st.rerun()
            
    # Card 2: Física
    with col2:
        st.markdown("""
            <div class='course-card' style='border-top: 4px solid #9d4edd;'>
                <span style='font-size: 2.2rem;'>⚡</span>
                <h3 style='color: #c77dff; margin: 6px 0;'>Física Cósmica</h3>
                <p style='color: #cbd5e1; font-size: 0.85rem;'>Massa vs Peso, 3 Leis de Newton, propulsão de foguetes e relatividade.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Entrar em Física ⚡", use_container_width=True, key="btn_portal_phys"):
            st.session_state.redirect_target = {
                "area": "🎓 1. ACADEMIA NOVA STELLARIS (Fundamentos & Trilhas)",
                "module_key": "nav_mod_academy",
                "module_val": "🎓 Academia Nova Stellaris (Fundamentos & Trilhas)"
            }
            st.rerun()

    # Card 3: Química
    with col3:
        st.markdown("""
            <div class='course-card' style='border-top: 4px solid #00f5d4;'>
                <span style='font-size: 2.2rem;'>🧪</span>
                <h3 style='color: #00f5d4; margin: 6px 0;'>Química Estelar</h3>
                <p style='color: #cbd5e1; font-size: 0.85rem;'>Átomos, fusão nuclear em estrelas, química em Marte e espectroscopia.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Entrar em Química 🧪", use_container_width=True, key="btn_portal_chem"):
            st.session_state.redirect_target = {
                "area": "🎓 1. ACADEMIA NOVA STELLARIS (Fundamentos & Trilhas)",
                "module_key": "nav_mod_academy",
                "module_val": "🎓 Academia Nova Stellaris (Fundamentos & Trilhas)"
            }
            st.rerun()

    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
    col4, col5, col6 = st.columns(3)

    # Card 4: Tecnologia
    with col4:
        st.markdown("""
            <div class='course-card' style='border-top: 4px solid #00d4ff;'>
                <span style='font-size: 2.2rem;'>💻</span>
                <h3 style='color: #00d4ff; margin: 6px 0;'>Tecnologia & IA</h3>
                <p style='color: #cbd5e1; font-size: 0.85rem;'>Algoritmos do rover marciano, código binário e redes neurais.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Entrar em Tecnologia 💻", use_container_width=True, key="btn_portal_tech"):
            st.session_state.redirect_target = {
                "area": "🎓 1. ACADEMIA NOVA STELLARIS (Fundamentos & Trilhas)",
                "module_key": "nav_mod_academy",
                "module_val": "🎓 Academia Nova Stellaris (Fundamentos & Trilhas)"
            }
            st.rerun()

    # Card 5: Observatório
    with col5:
        st.markdown("""
            <div class='course-card' style='border-top: 4px solid #ffd166;'>
                <span style='font-size: 2.2rem;'>🌌</span>
                <h3 style='color: #ffd166; margin: 6px 0;'>Observatório 3D</h3>
                <p style='color: #cbd5e1; font-size: 0.85rem;'>Atlas do Sistema Solar, fotos do James Webb e balança interplanetária.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Abrir Observatório 🌌", use_container_width=True, key="btn_portal_obs"):
            st.session_state.redirect_target = {
                "area": "🔭 2. EXPLORAÇÃO & CIÊNCIA",
                "module_key": "nav_mod_exploration",
                "module_val": "🌌 Observatório do Cosmos"
            }
            st.rerun()

    # Card 6: Missões Sci-Fi
    with col6:
        st.markdown("""
            <div class='course-card' style='border-top: 4px solid #ff6b6b;'>
                <span style='font-size: 2.2rem;'>🚀</span>
                <h3 style='color: #ff6b6b; margin: 6px 0;'>Missões Sci-Fi</h3>
                <p style='color: #cbd5e1; font-size: 0.85rem;'>Sobreviva em Marte, decodifique Rocky e explore o buraco negro Gargantua.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Iniciar Missões 🚀", use_container_width=True, key="btn_portal_scifi"):
            st.session_state.redirect_target = {
                "area": "🔭 2. EXPLORAÇÃO & CIÊNCIA",
                "module_key": "nav_mod_exploration",
                "module_val": "🚀 Missões Sci-Fi Interativas"
            }
            st.rerun()

    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
    col7, col8, col9 = st.columns(3)

    # Card 7: Arcade de Jogos
    with col7:
        st.markdown("""
            <div class='course-card' style='border-top: 4px solid #06d6a0;'>
                <span style='font-size: 2.2rem;'>🎮</span>
                <h3 style='color: #06d6a0; margin: 6px 0;'>Arcade Cósmico</h3>
                <p style='color: #cbd5e1; font-size: 0.85rem;'>3 Jogos retrô completos inspirados nos filmes com botões de start/fim.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Jogar no Arcade 🎮", use_container_width=True, key="btn_portal_arcade"):
            st.session_state.redirect_target = {
                "area": "🕹️ 3. ARCADE CÓSMICO & JOGOS",
                "module_key": "nav_mod_arcade",
                "module_val": "🕹️ Arcade Cósmico (3 Jogos Sci-Fi)"
            }
            st.rerun()

    # Card 8: Biblioteca Cósmica
    with col8:
        st.markdown("""
            <div class='course-card' style='border-top: 4px solid #38bdf8;'>
                <span style='font-size: 2.2rem;'>📚</span>
                <h3 style='color: #38bdf8; margin: 6px 0;'>Biblioteca & Busca</h3>
                <p style='color: #cbd5e1; font-size: 0.85rem;'>Enciclopédia de pesquisa, biografia dos cientistas e guia de estrelas.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Pesquisar na Biblioteca 📚", use_container_width=True, key="btn_portal_library"):
            st.session_state.redirect_target = {
                "area": "🤖 4. MENTORIA IA & CONQUISTAS",
                "module_key": "nav_mod_mentor",
                "module_val": "📚 Hub de Conhecimento"
            }
            st.rerun()

    # Card 9: CosmoAI
    with col9:
        st.markdown("""
            <div class='course-card' style='border-top: 4px solid #a855f7;'>
                <span style='font-size: 2.2rem;'>🤖</span>
                <h3 style='color: #c084fc; margin: 6px 0;'>CosmoAI Mentor</h3>
                <p style='color: #cbd5e1; font-size: 0.85rem;'>Tire dúvidas de matemática, física, química e astronomia com a IA.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Conversar com CosmoAI 🤖", use_container_width=True, key="btn_portal_ai"):
            st.session_state.redirect_target = {
                "area": "🤖 4. MENTORIA IA & CONQUISTAS",
                "module_key": "nav_mod_mentor",
                "module_val": "🤖 CosmoAI (Mentor Espacial)"
            }
            st.rerun()
