import streamlit as st
from gemini_service import ask_cosmo, generate_enigma, is_gemini_configured
from database import save_chat_message, get_chat_history, clear_chat_history, add_xp

def render_cosmo_ai(user: dict):
    st.markdown("""
        <div class='cosmic-hero' style='background: linear-gradient(135deg, rgba(30,16,60,0.95), rgba(16,20,47,0.95)); border: 1px solid #9d4edd;'>
            <h1 style='color: #00d4ff; margin-bottom: 5px;'>🤖 CosmoAI — Seu Mentor Espacial STEAM</h1>
            <p style='color: #cbd5e1; font-size: 1.1rem; margin: 0;'>
                Tire dúvidas sobre Astronomia, Física, Matemática, Química, Computação e seus filmes de ficção científica favoritos!
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col_chat, col_tools = st.columns([2, 1])
    
    # ----------------------------------------------------
    # COLUNA DA DIREITA: FERRAMENTAS & CONFIGURAÇÃO
    # ----------------------------------------------------
    with col_tools:
        # Status da Conexão
        online = is_gemini_configured()
        if online:
            st.markdown("""
                <div style='background: rgba(6,214,160,0.15); border: 1px solid #06d6a0; border-radius: 8px; padding: 8px 12px; margin-bottom: 12px;'>
                    <span style='color: #06d6a0; font-size: 0.85rem; font-weight: bold;'>🟢 Google Gemini Ativado (Online)</span>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div style='background: rgba(0,212,255,0.12); border: 1px solid #00d4ff; border-radius: 8px; padding: 8px 12px; margin-bottom: 12px;'>
                    <span style='color: #00d4ff; font-size: 0.85rem; font-weight: bold;'>⚡ Motor de Conhecimento STEAM (Local)</span>
                </div>
            """, unsafe_allow_html=True)
            
        with st.expander("🔑 Chave Gemini API (Opcional)", expanded=False):
            st.caption("Insira sua chave gratuita do Google AI Studio se desejar respostas 100% livres e generativas na nuvem:")
            custom_key = st.text_input("Chave de API do Gemini:", type="password", value=st.session_state.get("custom_gemini_api_key", ""), key="input_custom_gemini_key")
            if st.button("Salvar Chave", key="btn_save_gemini_key"):
                st.session_state["custom_gemini_api_key"] = custom_key
                st.success("Chave salva na sessão!")
                st.rerun()

        st.markdown("""
            <div class='cosmic-card'>
                <h3 style='color: #ffd166; margin-top: 0;'>⚡ Perguntas Rápidas</h3>
                <p style='font-size: 0.85rem; color: #94a3b8;'>Clique em um tópico para perguntar direto:</p>
            </div>
        """, unsafe_allow_html=True)
        
        quick_prompts = [
            "🧪 Quais componentes químicos formam o corpo humano?",
            "🕳️ Como funciona a dilatação do tempo em Interestelar?",
            "🥔 Como Mark Watney fez água em Perdido em Marte?",
            "✨ O que são os Astrofagos em Devoradores de Estrelas?",
            "🚀 Como um foguete voa no vácuo do espaço?",
            "💻 Por que os computadores espaciais usam código binário?"
        ]
        
        for q in quick_prompts:
            if st.button(q, key=f"quick_{q}"):
                st.session_state["user_question_input"] = q
                st.rerun()
                
        st.markdown("---")
        st.markdown("### 🎲 Gerador de Enigmas")
        enigma_pillar = st.selectbox("Escolha a área do enigma:", ["Física", "Matemática", "Química", "Computação", "Geral"])
        
        if st.button("Gerar Novo Desafio Espacial! 🧠"):
            with st.spinner("Cosmo está preparando um enigma cósmico..."):
                enigma_data = generate_enigma(enigma_pillar)
                st.session_state["current_enigma"] = enigma_data["text"]
                add_xp(user["id"], 20)
                
        if "current_enigma" in st.session_state:
            st.markdown(f"""
                <div class='cosmic-card' style='border: 1px solid #06d6a0;'>
                    <h4 style='color: #06d6a0;'>🎯 Desafio do Cosmo:</h4>
                    {st.session_state['current_enigma']}
                </div>
            """, unsafe_allow_html=True)

    # ----------------------------------------------------
    # COLUNA PRINCIPAL: CHAT STREAMLIT
    # ----------------------------------------------------
    with col_chat:
        c_head1, c_head2 = st.columns([3, 1])
        with c_head1:
            st.subheader("💬 Diálogo com o Cosmo")
        with c_head2:
            if st.button("🗑️ Limpar Chat", use_container_width=True, key="btn_clear_chat"):
                clear_chat_history(user["id"])
                st.rerun()
        
        # Carregar histórico do banco de dados
        history = get_chat_history(user["id"], limit=30)
        
        # Exibir mensagens
        chat_container = st.container()
        with chat_container:
            if not history:
                st.markdown("""
                    <div class='chat-cosmo'>
                        <strong>🤖 Cosmo:</strong> Olá, jovem explorador(a)! Eu sou o Cosmo, seu guia nesta viagem pelas maravilhas do universo. 
                        O que você quer descobrir hoje? Podemos falar sobre buracos negros, robôs marcianos, a química do seu corpo ou como fazer cálculos de foguetes! 🚀
                    </div>
                """, unsafe_allow_html=True)
            else:
                for msg in history:
                    role = msg.get("role", msg.get("sender", "user"))
                    content = msg.get("content", msg.get("message", ""))
                    if role == "user":
                        st.markdown(f"<div class='chat-user'><strong>Você:</strong> {content}</div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<div class='chat-cosmo'><strong>🤖 Cosmo:</strong> {content}</div>", unsafe_allow_html=True)
                        
        # Caixa de entrada
        prefill_text = st.session_state.pop("user_question_input", "")
        
        user_input = st.chat_input("Digite sua pergunta ou teoria espacial aqui...")
        if not user_input and prefill_text:
            user_input = prefill_text
            
        if user_input:
            # Salvar mensagem do usuário
            save_chat_message(user["id"], "user", user_input)
            
            with st.spinner("🤖 Cosmo está consultando os bancos de dados estelares..."):
                reply = ask_cosmo(user_input, history)
                save_chat_message(user["id"], "cosmo", reply)
                add_xp(user["id"], 15)
                
            st.rerun()
