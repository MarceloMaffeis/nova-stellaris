"""
Nova Stellaris - Painel Administrativo do Docente / Professor
Gestão de turmas, atribuição de XP bônus, publicação de tarefas e relatórios CSV.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from database import (
    get_all_students, 
    get_all_classes, 
    get_class_stats, 
    award_bonus_xp, 
    create_announcement, 
    get_announcements, 
    delete_announcement,
    reset_user_password,
    delete_user
)
from assets.badges import BADGES, get_rank_for_xp

def render_admin_dashboard(user: dict):
    st.markdown("""
        <div class='cosmic-hero' style='background: linear-gradient(135deg, rgba(35,20,65,0.95), rgba(16,24,55,0.95)); border: 1px solid #ffd166;'>
            <h1 style='color: #ffd166; margin-bottom: 5px;'>👑 Painel de Controle do Docente & Gestão Escolar</h1>
            <p style='color: #cbd5e1; font-size: 1.1rem; margin: 0;'>
                Acompanhe o engajamento dos seus alunos, publique desafios de aula, conceda recompensas de XP e exporte relatórios pedagógicos!
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    classes = ["Todas as Turmas"] + get_all_classes()
    selected_class = st.selectbox("🎯 Filtrar por Turma / Série:", classes, index=0)
    
    tab_overview, tab_students, tab_announcements, tab_reports = st.tabs([
        "📊 Visão Geral & Métricas",
        "👥 Gestão de Alunos & XP Bônus",
        "📢 Mural de Missões & Avisos",
        "📥 Relatório & Exportação CSV"
    ])
    
    # ----------------------------------------------------------------------
    # TAB 1: VISÃO GERAL
    # ----------------------------------------------------------------------
    with tab_overview:
        stats = get_class_stats(selected_class)
        students = get_all_students(selected_class)
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("👥 Total de Alunos", str(stats["total_students"]), "Cadastrados na Turma")
        c2.metric("⭐ Média de XP", f"{stats['avg_xp']:.0f} XP", "Por Estudante")
        c3.metric("🏆 Insígnias Conquistadas", str(stats["total_badges"]), "Medalhas Coletivas")
        c4.metric("👑 Aluno Destaque", stats["top_student"], "Líder de Pontuação")
        
        st.markdown("---")
        
        if students:
            st.markdown("### 📈 Distribuição de XP e Níveis da Turma")
            df_students = pd.DataFrame([
                {
                    "Aluno": s["name"],
                    "XP": s["xp"],
                    "Turma": s.get("class_name", "Geral"),
                    "Insígnias": s["badges_count"],
                    "Quizzes Feitos": s["quiz_attempts_count"]
                }
                for s in students
            ])
            
            fig_xp = px.bar(
                df_students,
                x="Aluno",
                y="XP",
                color="XP",
                color_continuous_scale="Viridis",
                title="Ranking de XP dos Alunos",
                text="XP"
            )
            fig_xp.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(19, 23, 43, 0.6)",
                font=dict(color="#cbd5e1")
            )
            st.plotly_chart(fig_xp, use_container_width=True)
        else:
            st.info("Nenhum aluno encontrado para a turma selecionada.")

    # ----------------------------------------------------------------------
    # TAB 2: GESTÃO DE ALUNOS & XP BÔNUS
    # ----------------------------------------------------------------------
    with tab_students:
        st.subheader("👥 Gestão Individual de Alunos")
        st.write("Conceda XP de participação em aula, redefina senhas ou edite turmas:")
        
        students = get_all_students(selected_class)
        
        if not students:
            st.info("Nenhum aluno cadastrado nesta turma ainda.")
        else:
            for s in students:
                rank_info = get_rank_for_xp(s["xp"])
                rank = rank_info["current"]
                
                with st.expander(f"{s['avatar']} {s['name']} — Turma: {s.get('class_name', 'Geral')} | {s['xp']} XP ({rank['title']})"):
                    col_info, col_actions = st.columns([1.2, 1])
                    
                    with col_info:
                        st.markdown(f"""
                            <div style='background: rgba(19, 23, 43, 0.7); border: 1px solid rgba(0,212,255,0.2); border-radius: 10px; padding: 12px;'>
                                <p style='margin: 0;'><strong>👤 Nome:</strong> {s['name']}</p>
                                <p style='margin: 0;'><strong>📧 E-mail:</strong> {s.get('email', 'Não informado')}</p>
                                <p style='margin: 0;'><strong>🏫 Turma:</strong> {s.get('class_name', 'Não definida')}</p>
                                <p style='margin: 0;'><strong>⭐ XP Total:</strong> <span style='color: #ffd166; font-weight: bold;'>{s['xp']} XP</span></p>
                                <p style='margin: 0;'><strong>🎖️ Patente:</strong> {rank['icon']} {rank['title']}</p>
                                <p style='margin: 0;'><strong>🏆 Insígnias:</strong> {s['badges_count']} conquistadas</p>
                                <p style='margin: 0;'><strong>📅 Cadastrado em:</strong> {s.get('created_at', 'N/A')}</p>
                            </div>
                        """, unsafe_allow_html=True)
                        
                    with col_actions:
                        st.markdown("#### ⭐ Conceder XP Bônus de Aula")
                        bonus_amount = st.number_input(f"Pontos XP para {s['name']}:", min_value=10, max_value=500, value=50, step=10, key=f"bonus_xp_{s['id']}")
                        bonus_reason = st.selectbox(
                            "Motivo do Bônus:",
                            ["Excelente Participação em Aula", "Tarefa de Casa Concluída", "Ajudou um Colega", "Desafio Extra Resolvido", "Feira de Ciências"],
                            key=f"reason_{s['id']}"
                        )
                        if st.button(f"🎁 Atribuir +{bonus_amount} XP", key=f"btn_bonus_{s['id']}"):
                            if award_bonus_xp(s["id"], bonus_amount, bonus_reason):
                                st.success(f"+{bonus_amount} XP atribuídos com sucesso para {s['name']}!")
                                st.rerun()
                                
                        st.markdown("---")
                        with st.popover(f"⚙️ Opções Avançadas ({s['name']})"):
                            st.write("Redefinir Senha do Aluno:")
                            new_p = st.text_input("Nova Senha:", value="123456", key=f"reset_p_{s['id']}")
                            if st.button("Salvar Nova Senha", key=f"btn_reset_{s['id']}"):
                                reset_user_password(s["id"], new_p)
                                st.success("Senha redefinida com sucesso para '123456'!")
                                
                            st.write("Excluir Aluno:")
                            if st.button("🗑️ Excluir Cadastro", key=f"btn_del_{s['id']}", type="primary"):
                                delete_user(s["id"])
                                st.warning("Aluno removido.")
                                st.rerun()

    # ----------------------------------------------------------------------
    # TAB 3: MURAL DE AVISOS & MISSÕES
    # ----------------------------------------------------------------------
    with tab_announcements:
        st.subheader("📢 Publicar Avisos & Tarefas para os Alunos")
        st.write("As mensagens criadas aqui aparecem no Portal Inicial de todos os alunos da turma selecionada:")
        
        with st.form("new_announcement_form"):
            ann_title = st.text_input("📌 Título da Missão / Comunicado:", placeholder="Ex: Desafio da Semana: Calcular a Órbita de Marte")
            ann_class = st.selectbox("Turma Destino:", ["Todas as Turmas"] + get_all_classes())
            ann_content = st.text_area("📝 Conteúdo da Mensagem / Instruções:", placeholder="Descreva o que os alunos devem fazer no laboratório ou trilhas...")
            ann_xp = st.number_input("🎁 Recompensa de XP ao Concluir:", min_value=0, max_value=500, value=50, step=10)
            
            submit_ann = st.form_submit_button("🚀 Publicar no Mural dos Alunos", use_container_width=True)
            
            if submit_ann:
                if not ann_title.strip() or not ann_content.strip():
                    st.warning("⚠️ Preencha o título e o conteúdo da mensagem.")
                else:
                    create_announcement(
                        teacher_id=user["id"],
                        teacher_name=user["name"],
                        title=ann_title,
                        content=ann_content,
                        class_name=ann_class,
                        xp_reward=ann_xp
                    )
                    st.success("🎉 Mensagem publicada com sucesso no mural dos alunos!")
                    st.rerun()
                    
        st.markdown("---")
        st.markdown("### 📋 Avisos Publicados Ativos:")
        all_anns = get_announcements(selected_class)
        if not all_anns:
            st.info("Nenhum aviso ativo no momento.")
        else:
            for a in all_anns:
                with st.container():
                    st.markdown(f"""
                        <div style='background: rgba(19, 23, 43, 0.75); border-left: 4px solid #ffd166; padding: 14px 18px; border-radius: 8px; margin-bottom: 12px;'>
                            <div style='display: flex; justify-content: space-between;'>
                                <h4 style='color: #ffd166; margin: 0;'>{a['title']}</h4>
                                <span class='steam-tag' style='background: rgba(255,209,102,0.15); color: #ffd166;'>🎯 {a['class_name']} (+{a['xp_reward']} XP)</span>
                            </div>
                            <p style='color: #e2e8f0; font-size: 0.95rem; margin: 8px 0;'>{a['content']}</p>
                            <span style='color: #94a3b8; font-size: 0.8rem;'>Publicado por {a['teacher_name']} em {a['created_at']}</span>
                        </div>
                    """, unsafe_allow_html=True)
                    if st.button("🗑️ Remover Aviso", key=f"del_ann_{a['id']}"):
                        delete_announcement(a["id"])
                        st.rerun()

    # ----------------------------------------------------------------------
    # TAB 4: RELATÓRIOS & EXPORTAÇÃO CSV
    # ----------------------------------------------------------------------
    with tab_reports:
        st.subheader("📥 Exportação de Relatório de Notas & Desempenho")
        st.write("Baixe a planilha completa com o progresso de todos os alunos da turma para seus registros escolares:")
        
        students = get_all_students(selected_class)
        if students:
            df_export = pd.DataFrame([
                {
                    "ID": s["id"],
                    "Nome do Aluno": s["name"],
                    "E-mail": s.get("email", ""),
                    "Turma": s.get("class_name", ""),
                    "XP Acumulado": s["xp"],
                    "Patente": get_rank_for_xp(s["xp"])["current"]["title"],
                    "Insígnias Desbloqueadas": s["badges_count"],
                    "Quizzes Realizados": s["quiz_attempts_count"],
                    "Data de Cadastro": s.get("created_at", "")
                }
                for s in students
            ])
            
            st.dataframe(df_export, use_container_width=True)
            
            csv_data = df_export.to_csv(index=False, encoding="utf-8-sig")
            st.download_button(
                label="📥 Baixar Planilha da Turma em CSV (Excel)",
                data=csv_data,
                file_name=f"relatorio_nova_stellaris_{selected_class.replace(' ', '_')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        else:
            st.info("Sem dados disponíveis para exportação.")
