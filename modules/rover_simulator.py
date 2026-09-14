"""
Nova Stellaris - Simulador Visual de Programação do Rover Marciano (Perseverance / Curiosity)
Permite programar blocos visuais, executar trajetórias em grid 2D com animação e rastro,
desviar de crateras, coletar amostras e aprender pensamento computacional em 4 missões graduadas.
"""

import streamlit as st
import time
from database import add_xp, unlock_badge

ROVER_MISSIONS = {
    "missao_1": {
        "title": "🟢 Missão 1: Primeiro Contato em Jezero (Básico)",
        "subtitle": "Aprenda a sequência de comandos básicos (Avançar e Girar)",
        "grid_size": 5,
        "start": (0, 0),
        "target": (3, 2),
        "target_icon": "🪨 Rocha Basáltica",
        "target_action": "laser",
        "craters": [(1, 1), (2, 3)],
        "description": "Conduza o Rover do ponto de pouso (0, 0) até a Rocha de Basalto em (3, 2) e dispare o laser SuperCam para analisar os minerais. Cuidado com as crateras no caminho!",
        "xp": 50,
        "badge": "rover_cadet"
    },
    "missao_2": {
        "title": "🟡 Missão 2: O Labirinto de Crateras & Loops (Intermediário)",
        "subtitle": "Use Laços de Repetição (Loops) para economizar comandos e bateria",
        "grid_size": 6,
        "start": (0, 0),
        "target": (4, 4),
        "target_icon": "⛏️ Amostra de Sedimento",
        "target_action": "coleta",
        "craters": [(1, 0), (1, 2), (2, 2), (3, 2), (3, 4), (4, 2)],
        "description": "Um labirinto rochoso bloqueia o caminho. Utilize comandos de repetição (Loops) para avançar rapidamente pelos corredores e colete a amostra em (4, 4)!",
        "xp": 75,
        "badge": "rover_loop_master"
    },
    "missao_3": {
        "title": "🔴 Missão 3: Bioassinaturas no Delta do Rio Antigo (Avançado)",
        "subtitle": "Análise completa com Laser + Coleta no Tubo de Titânio",
        "grid_size": 7,
        "start": (0, 0),
        "target": (5, 5),
        "target_icon": "🧬 Fóssil Microbiano em Tubo",
        "target_action": "ambos",
        "craters": [(0, 2), (1, 4), (2, 1), (2, 5), (3, 3), (4, 1), (4, 5), (5, 3)],
        "description": "Navegue pelo delta do antigo rio marciano, desvie dos campos de dunas e crateras, chegue em (5, 5), dispare o laser SuperCam e em seguida recolha a amostra no tubo de titânio!",
        "xp": 100,
        "badge": "rover_commander"
    },
    "missao_4": {
        "title": "🟣 Missão 4: Tempestade de Poeira no Monte Olimpo (Mestre)",
        "subtitle": "Planejamento de Rota Otimizada com Limite de Bateria",
        "grid_size": 8,
        "start": (1, 1),
        "target": (6, 6),
        "target_icon": "🏔️ Cume do Vulcão",
        "target_action": "ambos",
        "craters": [(2, 2), (2, 4), (3, 6), (4, 2), (4, 4), (5, 1), (5, 5), (6, 3)],
        "description": "Uma tempestade de poeira se aproxima. Encontre a rota mais curta e segura até o topo da colina em (6, 6) antes que a bateria solar se esgote!",
        "xp": 150,
        "badge": "steam_tech_master"
    }
}

DIRECTIONS = ["➡️ Leste (X+)", "⬇️ Sul (Y-)", "⬅️ Oeste (X-)", "⬆️ Norte (Y+)"]
DIR_DELTAS = [(1, 0), (0, -1), (-1, 0), (0, 1)]

def render_rover_simulator(user: dict):
    st.markdown("""<div class='cosmic-hero' style='background: linear-gradient(135deg, rgba(40,15,20,0.95), rgba(16,20,45,0.95)); border: 1px solid #ff6b6b;'>
<h1 style='color: #ff6b6b; margin-bottom: 5px;'>🤖 Simulador Visual de Trajetória do Rover em Marte</h1>
<p style='color: #cbd5e1; font-size: 1.1rem; margin: 0;'>
Programe os algoritmos de navegação autônoma do <strong>Rover Perseverance</strong> na Cratera Jezero com blocos visuais e veja ele se movimentar pelo solo marciano!
</p>
</div>""", unsafe_allow_html=True)
    
    # ----------------------------------------------------------------------
    # SELEÇÃO DE MISSÃO / NÍVEL
    # ----------------------------------------------------------------------
    mission_id = st.selectbox(
        "🎯 Escolha o Nível do Desafio de Programação:",
        list(ROVER_MISSIONS.keys()),
        format_func=lambda k: ROVER_MISSIONS[k]["title"],
        key="rover_mission_selector"
    )
    mission = ROVER_MISSIONS[mission_id]
    
    st.markdown(f"""<div style='background: rgba(19, 23, 43, 0.75); border-left: 4px solid #ff6b6b; padding: 12px 18px; border-radius: 8px; margin: 12px 0;'>
<h4 style='color: #ff6b6b; margin: 0;'>{mission['title']}</h4>
<p style='color: #ffd166; font-size: 0.9rem; margin: 4px 0;'><strong>Objetivo:</strong> {mission['subtitle']}</p>
<p style='color: #e2e8f0; font-size: 0.9rem; margin: 0;'>{mission['description']}</p>
</div>""", unsafe_allow_html=True)
    
    # Inicializar Fila de Comandos na Session State
    if "rover_command_queue" not in st.session_state:
        st.session_state.rover_command_queue = []
        
    col_controls, col_map = st.columns([1.1, 1.4])
    
    # ----------------------------------------------------------------------
    # COLUNA 1: PAINEL DE CONTROLES VISUAIS (BLOCOS DE PROGRAMAÇÃO)
    # ----------------------------------------------------------------------
    with col_controls:
        st.markdown("### 🎛️ 1. Painel de Blocos de Comando")
        st.write("Clique nos botões abaixo para montar o algoritmo de navegação do Rover:")
        
        # Grupo de Movimentação
        st.markdown("##### 🚶 Movimentação Básica:")
        c_m1, c_m2, c_m3 = st.columns(3)
        with c_m1:
            if st.button("⬆️ Avançar 1m", use_container_width=True, key="cmd_fwd_1"):
                st.session_state.rover_command_queue.append({"cmd": "AVANCAR", "name": "⬆️ Avançar 1m", "val": 1})
                st.rerun()
        with c_m2:
            if st.button("⬅️ Girar 90° Esq", use_container_width=True, key="cmd_turn_l"):
                st.session_state.rover_command_queue.append({"cmd": "GIRAR_ESQ", "name": "⬅️ Girar 90° Esquerda", "val": 1})
                st.rerun()
        with c_m3:
            if st.button("➡️ Girar 90° Dir", use_container_width=True, key="cmd_turn_r"):
                st.session_state.rover_command_queue.append({"cmd": "GIRAR_DIR", "name": "➡️ Girar 90° Direita", "val": 1})
                st.rerun()
                
        # Grupo de Laços de Repetição (Loops)
        st.markdown("##### 🔁 Laços de Repetição (Loops):")
        c_l1, c_l2 = st.columns(2)
        with c_l1:
            if st.button("🔁 Loop: Avançar 2x", use_container_width=True, key="cmd_loop_2"):
                st.session_state.rover_command_queue.append({"cmd": "LOOP_AVANCAR", "name": "🔁 Repita 2x: Avançar", "val": 2})
                st.rerun()
        with c_l2:
            if st.button("🔁 Loop: Avançar 3x", use_container_width=True, key="cmd_loop_3"):
                st.session_state.rover_command_queue.append({"cmd": "LOOP_AVANCAR", "name": "🔁 Repita 3x: Avançar", "val": 3})
                st.rerun()
                
        # Grupo de Ações Científicas
        st.markdown("##### 🔬 Ações Científicas:")
        c_a1, c_a2 = st.columns(2)
        with c_a1:
            if st.button("🔬 Laser SuperCam", use_container_width=True, key="cmd_laser"):
                st.session_state.rover_command_queue.append({"cmd": "LASER", "name": "🔬 Disparar Laser", "val": 1})
                st.rerun()
        with c_a2:
            if st.button("⛏️ Coletar Amostra", use_container_width=True, key="cmd_coleta"):
                st.session_state.rover_command_queue.append({"cmd": "COLETA", "name": "⛏️ Coletar em Tubo", "val": 1})
                st.rerun()
                
        st.markdown("---")
        
        # Fila de Comandos Montada
        st.markdown("### 📜 2. Fila de Execução do Algoritmo:")
        
        if not st.session_state.rover_command_queue:
            st.info("💡 A fila de comandos está vazia. Clique nos blocos acima para adicionar passos!")
        else:
            for idx, c in enumerate(st.session_state.rover_command_queue):
                st.markdown(f"`Passo {idx+1:02d}:` **{c['name']}**")
                
            c_btn1, c_btn2 = st.columns(2)
            with c_btn1:
                if st.button("⏪ Remover Último Passo", use_container_width=True):
                    st.session_state.rover_command_queue.pop()
                    st.rerun()
            with c_btn2:
                if st.button("🗑️ Limpar Todos", use_container_width=True):
                    st.session_state.rover_command_queue = []
                    st.rerun()
                    
        # Código Python Equivalente
        with st.expander("💻 Ver Código Python Gerado", expanded=False):
            py_lines = ["# Código Autônomo de Navegação do Rover", "from mars_rover import Rover", "perseverance = Rover(pos=(0,0), dir='LESTE')"]
            for c in st.session_state.rover_command_queue:
                if c["cmd"] == "AVANCAR": py_lines.append("perseverance.avancar(metros=1)")
                elif c["cmd"] == "GIRAR_ESQ": py_lines.append("perseverance.girar_esquerda(90)")
                elif c["cmd"] == "GIRAR_DIR": py_lines.append("perseverance.girar_direita(90)")
                elif c["cmd"] == "LOOP_AVANCAR": py_lines.append(f"for i in range({c['val']}): perseverance.avancar(1)")
                elif c["cmd"] == "LASER": py_lines.append("perseverance.disparar_laser_supercam()")
                elif c["cmd"] == "COLETA": py_lines.append("perseverance.coletar_amostra_geologica()")
            st.code("\n".join(py_lines), language="python")

    # ----------------------------------------------------------------------
    # COLUNA 2: MAPA 2D DO SOLO MARCIANO & SIMULAÇÃO VISUAL
    # ----------------------------------------------------------------------
    with col_map:
        st.markdown("### 🗺️ 3. Mapa Tático da Superfície Marciana")
        
        # Calcular Trajetória do Rover
        g_size = mission["grid_size"]
        cur_x, cur_y = mission["start"]
        cur_dir = 0 # 0: Leste (X+), 1: Sul (Y-), 2: Oeste (X-), 3: Norte (Y+)
        
        path_history = [(cur_x, cur_y)]
        crashed = False
        crash_reason = ""
        used_laser = False
        collected_sample = False
        
        for c in st.session_state.rover_command_queue:
            cmd = c["cmd"]
            if cmd == "AVANCAR":
                dx, dy = DIR_DELTAS[cur_dir]
                cur_x += dx
                cur_y += dy
                path_history.append((cur_x, cur_y))
            elif cmd == "LOOP_AVANCAR":
                for _ in range(c["val"]):
                    dx, dy = DIR_DELTAS[cur_dir]
                    cur_x += dx
                    cur_y += dy
                    path_history.append((cur_x, cur_y))
                    if (cur_x, cur_y) in mission["craters"] or not (0 <= cur_x < g_size and 0 <= cur_y < g_size):
                        break
            elif cmd == "GIRAR_DIR":
                cur_dir = (cur_dir + 1) % 4
            elif cmd == "GIRAR_ESQ":
                cur_dir = (cur_dir - 1) % 4
            elif cmd == "LASER":
                if (cur_x, cur_y) == mission["target"]:
                    used_laser = True
            elif cmd == "COLETA":
                if (cur_x, cur_y) == mission["target"]:
                    collected_sample = True
                    
            # Verificar Limites do Mapa
            if not (0 <= cur_x < g_size and 0 <= cur_y < g_size):
                crashed = True
                crash_reason = f"O Rover saiu dos limites da área de exploração ({cur_x}, {cur_y}) e perdeu sinal com a Terra!"
                break
            # Verificar Colisão com Crateras
            if (cur_x, cur_y) in mission["craters"]:
                crashed = True
                crash_reason = f"💥 Alerta de Impacto! O Rover caiu na cratera em ({cur_x}, {cur_y}) e ficou atolado!"
                break

        # Renderizar Grid Visual em HTML/CSS
        # Eixo Y de cima para baixo (g_size-1 até 0)
        grid_html = f"<div style='display: grid; grid-template-columns: repeat({g_size}, 1fr); gap: 6px; background: rgba(30,12,12,0.85); border: 2px solid #ff6b6b; padding: 12px; border-radius: 12px; box-shadow: 0 8px 30px rgba(255,107,107,0.25);'>"
        
        path_set = set(path_history[:-1]) # posições anteriores percorridas
        
        for y in range(g_size - 1, -1, -1):
            for x in range(g_size):
                cell_content = ""
                cell_bg = "rgba(45, 20, 20, 0.7)"
                cell_border = "1px solid rgba(255, 107, 107, 0.3)"
                
                # Posição Atual do Rover
                if (x, y) == (cur_x, cur_y):
                    dir_icon = ["👉 🤖", "👇 🤖", "👈 🤖", "👆 🤖"][cur_dir]
                    cell_content = f"<div style='font-size: 1.3rem; text-shadow: 0 0 10px #00d4ff;'>{dir_icon}</div><span style='font-size:0.65rem; color:#00d4ff; font-weight:bold;'>ROVER</span>"
                    cell_bg = "rgba(0, 212, 255, 0.25)"
                    cell_border = "2px solid #00d4ff"
                # Ponto de Destino / Alvo
                elif (x, y) == mission["target"]:
                    cell_content = f"<div style='font-size: 1.3rem;'>{mission['target_icon'].split()[0]}</div><span style='font-size:0.65rem; color:#ffd166; font-weight:bold;'>ALVO</span>"
                    cell_bg = "rgba(255, 209, 102, 0.2)"
                    cell_border = "2px solid #ffd166"
                # Ponto de Partida Inicial
                elif (x, y) == mission["start"]:
                    cell_content = "<div style='font-size: 1.2rem;'>🚀</div><span style='font-size:0.65rem; color:#4ade80;'>INÍCIO</span>"
                # Crateras / Perigos
                elif (x, y) in mission["craters"]:
                    cell_content = "<div style='font-size: 1.2rem;'>🌋</div><span style='font-size:0.65rem; color:#f87171;'>PERIGO</span>"
                    cell_bg = "rgba(239, 68, 68, 0.2)"
                # Rastro de Caminho Percorrido
                elif (x, y) in path_set:
                    cell_content = "<div style='font-size: 1.1rem; color:#00d4ff;'>•</div>"
                    cell_bg = "rgba(0, 212, 255, 0.1)"
                else:
                    cell_content = f"<span style='font-size:0.65rem; color:#78350f;'>({x},{y})</span>"
                    
                grid_html += f"<div style='background: {cell_bg}; border: {cell_border}; min-height: 55px; border-radius: 8px; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center;'>{cell_content}</div>"
        grid_html += "</div>"
        
        st.markdown(grid_html, unsafe_allow_html=True)
        
        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        
        # Telemetria da Posição Atual
        c_pos1, c_pos2, c_pos3 = st.columns(3)
        c_pos1.metric("📍 Coordenada", f"X={cur_x}, Y={cur_y}", f"Alvo em {mission['target']}")
        c_pos2.metric("🧭 Direção da Antena", DIRECTIONS[cur_dir].split()[0], DIRECTIONS[cur_dir].split()[1])
        c_pos3.metric("🔋 Passos Executados", str(len(path_history)-1), "Consumo de Bateria")
        
        st.markdown("---")
        
        # ----------------------------------------------------------------------
        # AVALIAÇÃO DO ALGORITMO & RESULTADO DA MISSÃO
        # ----------------------------------------------------------------------
        if st.button("🚀 Transmitir e Executar Rota em Marte", use_container_width=True, type="primary"):
            if not st.session_state.rover_command_queue:
                st.warning("⚠️ Adicione comandos à fila antes de transmitir.")
            elif crashed:
                st.error(crash_reason)
            else:
                reached_target = (cur_x, cur_y) == mission["target"]
                req_action = mission["target_action"]
                
                action_ok = True
                action_msg = ""
                
                if req_action == "laser" and not used_laser:
                    action_ok = False
                    action_msg = "Você chegou até a rocha, mas esqueceu de adicionar o comando `🔬 Disparar Laser SuperCam` na posição do alvo!"
                elif req_action == "coleta" and not collected_sample:
                    action_ok = False
                    action_msg = "Você chegou ao ponto, mas esqueceu de adicionar o comando `⛏️ Coletar Amostra`!"
                elif req_action == "ambos" and (not used_laser or not collected_sample):
                    action_ok = False
                    action_msg = "Missão incompleta! É necessário disparar o laser E coletar a amostra na posição do alvo!"
                    
                if reached_target and action_ok:
                    st.balloons()
                    st.success(f"""
                        🎉 **MISSÃO CUMPRIDA COM SUCESSO ABSOLUTO!**
                        
                        O Rover Perseverance executou com perfeição todos os {len(st.session_state.rover_command_queue)} passos do seu algoritmo, desviou das crateras e realizou as análises científicas no solo marciano!
                        
                        ⭐ **Recompensa Concedida:** +{mission['xp']} XP
                    """)
                    add_xp(user["id"], mission["xp"])
                    unlock_badge(user["id"], mission["badge"])
                elif reached_target and not action_ok:
                    st.warning(f"⚠️ {action_msg}")
                else:
                    st.error(f"❌ O Rover parou na posição ({cur_x}, {cur_y}), mas o objetivo estava na posição {mission['target']}. Ajuste seu algoritmo e tente de novo!")
