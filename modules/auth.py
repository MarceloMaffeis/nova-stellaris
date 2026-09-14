"""
Nova Stellaris - Módulo de Autenticação & Cadastro
Permite login seguro para Alunos e Docentes, além de cadastro de novos usuários.
"""

import streamlit as st
from database import authenticate_user, register_user, get_all_classes

def render_auth_page():
    st.markdown("""
        <div class='cosmic-hero' style='background: linear-gradient(135deg, rgba(16,24,55,0.95), rgba(8,12,30,0.95)); border: 1px solid #00d4ff; max-width: 800px; margin: 10px auto 25px auto;'>
            <h1 style='color: #00d4ff; font-size: 2.2rem; margin-bottom: 5px;'>🚀 NOVA STELLARIS</h1>
            <p style='color: #cbd5e1; font-size: 1.15rem; margin: 0;'>
                Estação Espacial Educacional STEAM — Plataforma de Astronomia & Ciências Exatas
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col_main1, col_center, col_main2 = st.columns([1, 4, 1])
    
    with col_center:
        tab_login, tab_register = st.tabs([
            "🔑 Entrar na Estação (Login)",
            "✨ Cadastrar Novo Acesso (Aluno ou Docente)"
        ])
        
        # ----------------------------------------------------------------------
        # ABA 1: LOGIN
        # ----------------------------------------------------------------------
        with tab_login:
            st.markdown("""
                <div class='cosmic-card'>
                    <h3 style='color: #00d4ff; margin-top: 0;'>Acesso de Tripulantes</h3>
                    <p style='color: #94a3b8; font-size: 0.9rem;'>
                        Digite seu nome de usuário ou e-mail cadastrado e sua senha de acesso.
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            with st.form("login_form"):
                login_user = st.text_input("👤 Nome de Usuário ou E-mail:", placeholder="Ex: Cadete Estelar ou seu_email@escola.com")
                login_pwd = st.text_input("🔒 Senha de Acesso:", type="password", placeholder="Digite sua senha...")
                
                submitted_login = st.form_submit_button("🚀 Entrar na Estação", use_container_width=True)
                
                if submitted_login:
                    if not login_user or not login_pwd:
                        st.warning("⚠️ Por favor, preencha o usuário e a senha.")
                    else:
                        user = authenticate_user(login_user, login_pwd)
                        if user:
                            st.session_state.authenticated = True
                            st.session_state.current_user = user
                            st.session_state.current_username = user["name"]
                            st.session_state.current_avatar = user["avatar"]
                            st.session_state.user_role = user.get("role", "aluno")
                            st.success(f"🎉 Bem-vindo(a) a bordo, {user['name']}! Carregando sistemas...")
                            st.rerun()
                        else:
                            st.error("❌ Usuário ou senha incorretos. Verifique os dados ou crie uma conta na aba ao lado.")
                            
            st.markdown("---")
            st.markdown("#### ⚡ Acesso Rápido de Demonstração (1 Clique):")
            c_d1, c_d2 = st.columns(2)
            with c_d1:
                if st.button("👩‍🚀 Entrar como Aluno Demo", use_container_width=True):
                    user = authenticate_user("Cadete Estelar", "123456")
                    if user:
                        st.session_state.authenticated = True
                        st.session_state.current_user = user
                        st.session_state.current_username = user["name"]
                        st.session_state.current_avatar = user["avatar"]
                        st.session_state.user_role = user.get("role", "aluno")
                        st.rerun()
            with c_d2:
                if st.button("👨‍🏫 Entrar como Docente Demo", use_container_width=True):
                    user = authenticate_user("Prof. Isaac Newton", "admin123")
                    if user:
                        st.session_state.authenticated = True
                        st.session_state.current_user = user
                        st.session_state.current_username = user["name"]
                        st.session_state.current_avatar = user["avatar"]
                        st.session_state.user_role = user.get("role", "docente")
                        st.rerun()

        # ----------------------------------------------------------------------
        # ABA 2: CADASTRO
        # ----------------------------------------------------------------------
        with tab_register:
            st.markdown("""
                <div class='cosmic-card'>
                    <h3 style='color: #06d6a0; margin-top: 0;'>Criar Novo Acesso</h3>
                    <p style='color: #94a3b8; font-size: 0.9rem;'>
                        Cadastre-se como <strong>Aluno</strong> para aprender e ganhar insígnias, ou como <strong>Docente</strong> para gerenciar turmas e notas.
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            with st.form("register_form"):
                reg_name = st.text_input("👤 Nome Completo / Nome de Explorador(a):", placeholder="Ex: Maria Sophia Teles")
                reg_email = st.text_input("📧 E-mail (opcional):", placeholder="maria@escola.com")
                
                c_pwd1, c_pwd2 = st.columns(2)
                with c_pwd1:
                    reg_pwd = st.text_input("🔒 Senha:", type="password", placeholder="Mínimo 4 caracteres")
                with c_pwd2:
                    reg_pwd2 = st.text_input("🔒 Confirme a Senha:", type="password", placeholder="Repita a senha")
                    
                reg_role = st.selectbox(
                    "🎓 Tipo de Perfil:",
                    ["👩‍🚀 Aluno / Estudante", "👨‍🏫 Docente / Professor(a)"],
                    index=0
                )
                role_val = "docente" if "Docente" in reg_role else "aluno"
                
                existing_classes = get_all_classes()
                if role_val == "aluno":
                    reg_class = st.selectbox("🏫 Turma / Série:", existing_classes + ["Outra Turma (Digite abaixo)"])
                    if reg_class == "Outra Turma (Digite abaixo)":
                        reg_class = st.text_input("Digite o nome da sua Turma:", placeholder="Ex: 6º Ano B - Manhã")
                else:
                    reg_class = st.text_input("🏫 Departamento / Escola:", value="Docente de Ciências & Exatas")
                    
                avatar_options = ["👩‍🚀", "👨‍🚀", "🚀", "🤖", "👾", "🌟", "🪐", "🔬", "🔭"]
                reg_avatar = st.selectbox("🎨 Escolha seu Avatar Espacial:", avatar_options, index=0)
                
                submitted_reg = st.form_submit_button("✨ Concluir Cadastro & Embarcar", use_container_width=True)
                
                if submitted_reg:
                    if not reg_name.strip():
                        st.warning("⚠️ O nome não pode estar em branco.")
                    elif len(reg_pwd) < 4:
                        st.warning("⚠️ A senha deve ter pelo menos 4 caracteres.")
                    elif reg_pwd != reg_pwd2:
                        st.error("❌ As senhas não coincidem. Digite novamente.")
                    else:
                        success, msg, new_user = register_user(
                            name=reg_name,
                            password=reg_pwd,
                            role=role_val,
                            avatar=reg_avatar,
                            class_name=reg_class if reg_class else "6º Ano A",
                            email=reg_email
                        )
                        if success and new_user:
                            st.session_state.authenticated = True
                            st.session_state.current_user = new_user
                            st.session_state.current_username = new_user["name"]
                            st.session_state.current_avatar = new_user["avatar"]
                            st.session_state.user_role = new_user.get("role", "aluno")
                            st.balloons()
                            st.success(f"🎉 Conta criada com sucesso! Bem-vindo(a), {new_user['name']}!")
                            st.rerun()
                        else:
                            st.error(f"❌ {msg}")
