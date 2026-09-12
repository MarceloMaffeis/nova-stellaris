"""
Nova Stellaris - AstroQuiz STEAM & Gamificação
Jogo de perguntas e respostas com XP, níveis e feedback pedagógico imediato.
"""

import streamlit as st
from database import get_quiz_questions, record_quiz_attempt, get_user_stats, unlock_badge, add_xp

def render_quiz_game(user: dict):
    st.markdown("""
        <div class='cosmic-hero' style='background: linear-gradient(135deg, rgba(30,16,60,0.95), rgba(16,20,47,0.95)); border: 1px solid #ffd166;'>
            <h1 style='color: #ffd166; margin-bottom: 5px;'>🎮 AstroQuiz STEAM</h1>
            <p style='color: #cbd5e1; font-size: 1.1rem; margin: 0;'>
                Teste seus conhecimentos em Física, Matemática, Química e Computação Espacial e ganhe XP para subir de nível!
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    stats = get_user_stats(user["id"])
    
    # Placar rápido
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"<div class='cosmic-card' style='text-align:center;'><h4>Total Jogadas</h4><h2 style='color:#00d4ff;'>{stats['quizzes_played']}</h2></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='cosmic-card' style='text-align:center;'><h4>Acertos</h4><h2 style='color:#06d6a0;'>{stats['quizzes_correct']}</h2></div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='cosmic-card' style='text-align:center;'><h4>Precisão</h4><h2 style='color:#ffd166;'>{stats['quiz_accuracy']}%</h2></div>", unsafe_allow_html=True)
    with c4:
        st.markdown(f"<div class='cosmic-card' style='text-align:center;'><h4>Conquistas</h4><h2 style='color:#f72585;'>{stats['badges_count']}</h2></div>", unsafe_allow_html=True)
        
    st.markdown("---")
    
    # Filtros de Quiz
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        pillar_filter = st.selectbox("Filtrar por Pilar STEAM:", ["Todos", "Física", "Matemática", "Química", "Computação"])
    with col_f2:
        diff_filter = st.selectbox("Filtrar por Dificuldade:", ["Todos", "Cadete", "Cientista", "Mestre"])
        
    if "current_question" not in st.session_state or st.button("🔄 Próxima Pergunta Aleatória"):
        questions = get_quiz_questions(pillar=pillar_filter, difficulty=diff_filter, limit=1)
        if questions:
            st.session_state.current_question = questions[0]
            st.session_state.quiz_answered = False
            st.session_state.selected_option = None
        else:
            st.session_state.current_question = None

    q = st.session_state.get("current_question")
    
    if not q:
        st.info("Nenhuma pergunta encontrada com esses filtros. Tente selecionar 'Todos'!")
        return
        
    pillar_class = {
        "Física": "physics",
        "Matemática": "math",
        "Química": "chemistry",
        "Computação": "tech"
    }.get(q["pillar"], "physics")
    
    st.markdown(f"""
        <div class='cosmic-card' style='border: 1px solid #00d4ff;'>
            <div>
                <span class='steam-tag {pillar_class}'>{q['pillar']}</span>
                <span class='steam-tag' style='background: rgba(255,209,102,0.2); color: #ffd166; border: 1px solid #ffd166;'>{q['difficulty']}</span>
                <span style='color: #94a3b8; font-size: 0.9rem;'>Categoria: {q['category']}</span>
            </div>
            <h3 style='color: #f1f5f9; margin-top: 15px;'>{q['question']}</h3>
        </div>
    """, unsafe_allow_html=True)
    
    # Opções
    options = q["options"]
    answered = st.session_state.get("quiz_answered", False)
    
    for i, opt in enumerate(options):
        btn_label = f"{['A', 'B', 'C', 'D'][i]}) {opt}"
        if not answered:
            if st.button(btn_label, key=f"opt_{i}"):
                st.session_state.quiz_answered = True
                st.session_state.selected_option = i
                
                is_correct = (i == q["correct_idx"])
                xp_gain = 20 if q["difficulty"] == "Cadete" else (35 if q["difficulty"] == "Cientista" else 50)
                earned = xp_gain if is_correct else 5
                
                record_quiz_attempt(user["id"], q["id"], is_correct, earned)
                
                # Checar badges
                new_stats = get_user_stats(user["id"])
                if new_stats["quizzes_correct"] >= 5:
                    if unlock_badge(user["id"], "quiz_cadet"):
                        add_xp(user["id"], 100)
                        st.balloons()
                        st.success("🎉 **Conquista Desbloqueada:** ⭐ Cadete da Sabedoria! (+100 XP)")
                        
                if new_stats["quizzes_correct"] >= 10:
                    if unlock_badge(user["id"], "quiz_master"):
                        add_xp(user["id"], 250)
                        st.balloons()
                        st.success("🎉 **Conquista Desbloqueada:** 👑 Mestre Astrofísico! (+250 XP)")
                        
                st.rerun()
                
    if answered:
        selected_idx = st.session_state.get("selected_option")
        is_correct = (selected_idx == q["correct_idx"])
        
        if is_correct:
            st.success(f"🎉 **RESPOSTA CORRETA!** Você ganhou XP e avançou rumo ao próximo nível!")
        else:
            st.error(f"❌ **Resposta incorreta.** A opção correta era: **{['A', 'B', 'C', 'D'][q['correct_idx']]}) {options[q['correct_idx']]}** (Você ganhou +5 XP por tentar!)")
            
        st.markdown(f"""
            <div class='cosmic-card' style='border-left: 4px solid #00d4ff;'>
                <h4 style='color: #00d4ff;'>💡 Explicação Científica:</h4>
                <p>{q['explanation']}</p>
                {f"<h4 style='color: #ffd166; margin-top: 15px;'>🎬 Conexão Sci-Fi:</h4><p>{q['sci_fi_fact']}</p>" if q.get('sci_fi_fact') else ""}
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("➡️ Próximo Desafio!", type="primary"):
            st.session_state.quiz_answered = False
            questions = get_quiz_questions(pillar=pillar_filter, difficulty=diff_filter, limit=1)
            if questions:
                st.session_state.current_question = questions[0]
            st.rerun()
