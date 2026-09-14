"""
Nova Stellaris - Módulo Astro-Valley (Simulador Web do Domo Marciano)
Jogo 2D interativo estilo Stardew Valley Espacial em HTML5 Canvas + JS + Streamlit.
"""

import streamlit as st
import streamlit.components.v1 as components
from database import add_xp, unlock_badge

def render_astro_valley(user: dict):
    st.markdown("""
        <div class='cosmic-hero' style='background: linear-gradient(135deg, rgba(20,40,30,0.95), rgba(16,20,47,0.95)); border: 1px solid #4ade80;'>
            <h1 style='color: #4ade80; margin-bottom: 5px;'>🌾 Astro-Valley: Simulador do Domo Marciano</h1>
            <p style='color: #cbd5e1; font-size: 1.1rem; margin: 0;'>
                Gerencie sua colônia científica em Marte: cultive batatas espaciais, limpe painéis solares, sintetize água e minere nos tubos de lava!
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col_game, col_info = st.columns([3, 1])
    
    with col_info:
        st.markdown("""
            <div class='cosmic-card' style='border-left: 4px solid #4ade80;'>
                <h3 style='color: #4ade80; margin-top: 0;'>🎮 Como Jogar</h3>
                <p style='font-size: 0.9rem;'><strong>Movimento:</strong> Teclas <code>W, A, S, D</code> ou <code>Setas</code> (ou use o D-Pad na tela).</p>
                <p style='font-size: 0.9rem;'><strong>Ação Principal (Espaço / Botão A):</strong></p>
                <ul style='font-size: 0.85rem; color: #cbd5e1; padding-left: 20px;'>
                    <li>🌱 Nos canteiros: Arar ➔ Plantar ➔ Regar ➔ Colher</li>
                    <li>⚡ Nos painéis solares: Limpar poeira</li>
                    <li>🧪 No reator: Fabricar água</li>
                    <li>⛏️ Na mina: Extrair minérios</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🏆 Conquistas do Astro-Valley")
        st.markdown("""
            - 🌾 **Agricultor Marciano:** Colha 10 safras de batatas (+150 XP)
            - ⚡ **Pioneiro da Energia:** Gere 100 kWh de energia (+150 XP)
            - 🪐 **Sobrevivente dos Sols:** Sobreviva a 10 Sols (+200 XP)
        """)
        
        with st.expander("🎁 Sincronizar Recompensas do Jogo", expanded=True):
            st.write("Conforme você colhe, gera energia e sobrevive a novos Sols, reivindique seu XP no botão abaixo:")
            sync_sol = st.number_input("Sols Completados no Jogo:", min_value=1, max_value=100, value=1, step=1)
            sync_harvest = st.number_input("Batatas Colhidas:", min_value=0, max_value=500, value=0, step=1)
            
            if st.button("🌟 Reivindicar XP da Colônia!", type="primary"):
                earned_xp = (sync_sol * 25) + (sync_harvest * 15)
                add_xp(user["id"], earned_xp)
                
                if sync_harvest >= 10:
                    unlock_badge(user["id"], "astro_farmer")
                if sync_sol >= 10:
                    unlock_badge(user["id"], "sol_survivor")
                    
                st.balloons()
                st.success(f"🎉 Parabéns! Você ganhou **+{earned_xp} XP** para o seu perfil cósmico!")
                st.rerun()

    with col_game:
        # Código HTML5 + Canvas + JS do Astro-Valley
        game_html = """
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
        <meta charset="UTF-8">
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; }
            body {
                background: #070913;
                color: #f1f5f9;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                padding: 10px;
            }
            #game-container {
                position: relative;
                border: 2px solid #00d4ff;
                border-radius: 12px;
                box-shadow: 0 0 25px rgba(0, 212, 255, 0.3);
                background: #111827;
                overflow: hidden;
            }
            canvas {
                display: block;
                image-rendering: pixelated;
            }
            #hud {
                display: flex;
                justify-content: space-between;
                align-items: center;
                background: rgba(15, 23, 42, 0.95);
                border-bottom: 2px solid #38bdf8;
                padding: 8px 16px;
                font-size: 13px;
                font-weight: bold;
                width: 100%;
            }
            .hud-item {
                display: flex;
                align-items: center;
                gap: 5px;
            }
            .val { color: #38bdf8; font-size: 15px; }
            #touch-controls {
                display: flex;
                justify-content: space-between;
                width: 100%;
                max-width: 640px;
                margin-top: 10px;
                padding: 0 10px;
            }
            .dpad {
                display: grid;
                grid-template-columns: repeat(3, 45px);
                grid-template-rows: repeat(3, 45px);
                gap: 5px;
            }
            .btn-ctrl {
                background: #1e293b;
                border: 2px solid #475569;
                color: #38bdf8;
                border-radius: 8px;
                font-size: 18px;
                font-weight: bold;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                transition: 0.1s;
            }
            .btn-ctrl:active { background: #38bdf8; color: #0f172a; transform: scale(0.95); }
            .btn-action {
                width: 80px;
                height: 80px;
                border-radius: 50%;
                background: #059669;
                border: 3px solid #34d399;
                color: white;
                font-size: 16px;
                font-weight: bold;
                align-self: center;
                cursor: pointer;
                box-shadow: 0 0 15px rgba(52, 211, 153, 0.4);
            }
            .btn-action:active { background: #34d399; transform: scale(0.95); }
            #message-banner {
                position: absolute;
                bottom: 12px;
                left: 50%;
                transform: translateX(-50%);
                background: rgba(15, 23, 42, 0.9);
                border: 1px solid #4ade80;
                color: #4ade80;
                padding: 6px 14px;
                border-radius: 20px;
                font-size: 12px;
                pointer-events: none;
                transition: opacity 0.3s;
                opacity: 0;
            }
        </style>
        </head>
        <body>

        <div id="game-container">
            <div id="hud">
                <div class="hud-item">🪐 Sol: <span id="sol-val" class="val">1</span></div>
                <div class="hud-item">⚡ Energia: <span id="energy-val" class="val">100%</span></div>
                <div class="hud-item">💧 Água: <span id="water-val" class="val">50L</span></div>
                <div class="hud-item">🥔 Batatas: <span id="potato-val" class="val">0</span></div>
                <div class="hud-item">⛏️ Minério: <span id="ore-val" class="val">0</span></div>
            </div>
            <canvas id="gameCanvas" width="640" height="400"></canvas>
            <div id="message-banner">Mensagem da Base</div>
        </div>

        <div id="touch-controls">
            <div class="dpad">
                <div></div>
                <button class="btn-ctrl" onpointerdown="startMove('up')" onpointerup="stopMove('up')">▲</button>
                <div></div>
                <button class="btn-ctrl" onpointerdown="startMove('left')" onpointerup="stopMove('left')">◀</button>
                <div style="background:rgba(255,255,255,0.05);border-radius:6px;"></div>
                <button class="btn-ctrl" onpointerdown="startMove('right')" onpointerup="stopMove('right')">▶</button>
                <div></div>
                <button class="btn-ctrl" onpointerdown="startMove('down')" onpointerup="stopMove('down')">▼</button>
                <div></div>
            </div>
            <button class="btn-action" onclick="performAction()">AÇÃO<br>(Espaço)</button>
        </div>

        <script>
            const canvas = document.getElementById('gameCanvas');
            const ctx = canvas.getContext('2d');
            
            // Estado do Jogo
            const state = {
                player: { x: 300, y: 200, size: 24, speed: 3.5, dir: 'down', animFrame: 0 },
                keys: { up: false, down: false, left: false, right: false },
                sol: 1,
                timeOfDay: 0, // 0 a 1000 (0-700 dia, 700-1000 noite)
                energy: 100,
                water: 50,
                potatoes: 0,
                ores: 0,
                solarDust: 0, // 0 a 100% de poeira nos painéis
                plots: [
                    { x: 120, y: 120, state: 'empty', progress: 0 },
                    { x: 170, y: 120, state: 'empty', progress: 0 },
                    { x: 220, y: 120, state: 'empty', progress: 0 },
                    { x: 120, y: 170, state: 'empty', progress: 0 },
                    { x: 170, y: 170, state: 'empty', progress: 0 },
                    { x: 220, y: 170, state: 'empty', progress: 0 },
                ],
                rover: { x: 350, y: 130, dir: 1, targetPlot: 0 }
            };

            function showBanner(text) {
                const b = document.getElementById('message-banner');
                b.innerText = text;
                b.style.opacity = '1';
                setTimeout(() => { b.style.opacity = '0'; }, 2500);
            }

            // Controles de Teclado
            window.addEventListener('keydown', (e) => {
                if (e.key === 'w' || e.key === 'ArrowUp') state.keys.up = true;
                if (e.key === 's' || e.key === 'ArrowDown') state.keys.down = true;
                if (e.key === 'a' || e.key === 'ArrowLeft') state.keys.left = true;
                if (e.key === 'd' || e.key === 'ArrowRight') state.keys.right = true;
                if (e.key === ' ' || e.key === 'e' || e.key === 'Enter') {
                    e.preventDefault();
                    performAction();
                }
            });

            window.addEventListener('keyup', (e) => {
                if (e.key === 'w' || e.key === 'ArrowUp') state.keys.up = false;
                if (e.key === 's' || e.key === 'ArrowDown') state.keys.down = false;
                if (e.key === 'a' || e.key === 'ArrowLeft') state.keys.left = false;
                if (e.key === 'd' || e.key === 'ArrowRight') state.keys.right = false;
            });

            function startMove(dir) { state.keys[dir] = true; }
            function stopMove(dir) { state.keys[dir] = false; }

            // Lógica de Ação
            function performAction() {
                const p = state.player;
                
                // 1. Checar Canteiros de Plantas
                for (let plot of state.plots) {
                    const dist = Math.hypot(p.x - (plot.x + 18), p.y - (plot.y + 18));
                    if (dist < 40) {
                        if (plot.state === 'empty') {
                            plot.state = 'tilled';
                            showBanner('🌱 Solo arado! Aperte ação para plantar batatas marcianas.');
                        } else if (plot.state === 'tilled') {
                            plot.state = 'seeded';
                            plot.progress = 10;
                            showBanner('🥔 Batatas plantadas! Aperte ação para regar.');
                        } else if (plot.state === 'seeded') {
                            if (state.water >= 5) {
                                state.water -= 5;
                                plot.state = 'growing';
                                showBanner('💧 Canteiro irrigado com sucesso! As batatas estão crescendo.');
                            } else {
                                showBanner('⚠️ Falta água! Vá ao reator químico no canto.');
                            }
                        } else if (plot.state === 'ready') {
                            plot.state = 'empty';
                            plot.progress = 0;
                            state.potatoes += 3;
                            showBanner('🎉 Colheita realizada! +3 Batatas (+300 kcal)!');
                        }
                        updateHud();
                        return;
                    }
                }

                // 2. Checar Painéis Solares (x: 480, y: 80)
                if (Math.hypot(p.x - 510, p.y - 110) < 55) {
                    if (state.solarDust > 10) {
                        state.solarDust = 0;
                        state.energy = Math.min(100, state.energy + 20);
                        showBanner('⚡ Painéis limpos! Eficiência solar restaurada a 100%!');
                    } else {
                        showBanner('⚡ Painéis solares fotovoltaicos limpos e operando perfeitamente.');
                    }
                    updateHud();
                    return;
                }

                // 3. Checar Reator Químico de Água (x: 480, y: 280)
                if (Math.hypot(p.x - 510, p.y - 300) < 55) {
                    if (state.energy >= 15) {
                        state.energy -= 15;
                        state.water += 25;
                        showBanner('🧪 Reação 2H₂ + O₂ ➔ 2H₂O concluída! +25 Litros de Água sintetizados!');
                    } else {
                        showBanner('⚠️ Energia insuficiente para operar o reator químico!');
                    }
                    updateHud();
                    return;
                }

                // 4. Checar Mina de Tubo de Lava (x: 80, y: 310)
                if (Math.hypot(p.x - 100, p.y - 330) < 55) {
                    if (state.energy >= 10) {
                        state.energy -= 10;
                        state.ores += 2;
                        showBanner('⛏️ Mineração subterrânea! +2 Minérios de Ferro e Xenonite extraídos!');
                    } else {
                        showBanner('⚠️ Sem energia no traje para perfurar a rocha!');
                    }
                    updateHud();
                    return;
                }
            }

            function updateHud() {
                document.getElementById('sol-val').innerText = state.sol;
                document.getElementById('energy-val').innerText = Math.round(state.energy) + '%';
                document.getElementById('water-val').innerText = state.water + 'L';
                document.getElementById('potato-val').innerText = state.potatoes;
                document.getElementById('ore-val').innerText = state.ores;
            }

            // Loop Principal
            function update() {
                const p = state.player;
                let moved = false;

                if (state.keys.up && p.y > 50) { p.y -= p.speed; p.dir = 'up'; moved = true; }
                if (state.keys.down && p.y < canvas.height - 50) { p.y += p.speed; p.dir = 'down'; moved = true; }
                if (state.keys.left && p.x > 50) { p.x -= p.speed; p.dir = 'left'; moved = true; }
                if (state.keys.right && p.x < canvas.width - 50) { p.x += p.speed; p.dir = 'right'; moved = true; }

                if (moved) p.animFrame += 0.2;

                // Ciclo Dia/Noite (Sol)
                state.timeOfDay += 0.8;
                if (state.timeOfDay > 1000) {
                    state.timeOfDay = 0;
                    state.sol += 1;
                    state.solarDust = Math.min(80, state.solarDust + 15);
                    showBanner(`🌅 Sol ${state.sol} iniciado em Marte! Novo dia na colônia.`);
                }

                // Geração Solar de Dia vs Consumo de Noite
                const isDay = state.timeOfDay < 700;
                if (isDay) {
                    const solarGain = 0.05 * (1 - state.solarDust / 100);
                    state.energy = Math.min(100, state.energy + solarGain);
                } else {
                    state.energy = Math.max(0, state.energy - 0.03); // Consumo das lâmpadas e suporte
                }

                // Crescimento das Plantas
                for (let plot of state.plots) {
                    if (plot.state === 'growing') {
                        plot.progress += 0.15;
                        if (plot.progress >= 100) {
                            plot.state = 'ready';
                        }
                    }
                }

                // Movimento autônomo do Rover
                state.rover.x += 0.8 * state.rover.dir;
                if (state.rover.x > 400) state.rover.dir = -1;
                if (state.rover.x < 300) state.rover.dir = 1;

                updateHud();
            }

            function draw() {
                // Fundo Marciano com Cúpula
                ctx.fillStyle = '#993d26'; // Solo vermelho de Marte
                ctx.fillRect(0, 0, canvas.width, canvas.height);

                // Área Interna do Domo Geodésico
                ctx.fillStyle = '#1e293b';
                ctx.beginPath();
                ctx.arc(320, 200, 270, 0, Math.PI * 2);
                ctx.fill();
                ctx.lineWidth = 4;
                ctx.strokeStyle = '#00d4ff';
                ctx.stroke();

                // Chão do Domo (Grelha Tecnológica)
                ctx.strokeStyle = 'rgba(0, 212, 255, 0.08)';
                ctx.lineWidth = 1;
                for (let x = 70; x < 570; x += 30) {
                    ctx.beginPath(); ctx.moveTo(x, 40); ctx.lineTo(x, 360); ctx.stroke();
                }
                for (let y = 40; y < 360; y += 30) {
                    ctx.beginPath(); ctx.moveTo(70, y); ctx.lineTo(570, y); ctx.stroke();
                }

                // 1. Canteiros de Plantas (Horta do Domo)
                for (let plot of state.plots) {
                    ctx.fillStyle = plot.state === 'empty' ? '#451a03' : (plot.state === 'growing' ? '#14532d' : '#78350f');
                    ctx.fillRect(plot.x, plot.y, 40, 40);
                    ctx.strokeStyle = '#22c55e';
                    ctx.strokeRect(plot.x, plot.y, 40, 40);

                    // Desenho da Plantação
                    if (plot.state === 'tilled') {
                        ctx.fillStyle = '#b45309';
                        ctx.fillRect(plot.x + 8, plot.y + 18, 24, 4);
                    } else if (plot.state === 'seeded') {
                        ctx.fillStyle = '#fde047';
                        ctx.beginPath(); ctx.arc(plot.x + 20, plot.y + 20, 4, 0, Math.PI * 2); ctx.fill();
                    } else if (plot.state === 'growing') {
                        ctx.fillStyle = '#4ade80';
                        const h = (plot.progress / 100) * 16;
                        ctx.fillRect(plot.x + 16, plot.y + 30 - h, 8, h);
                    } else if (plot.state === 'ready') {
                        ctx.font = '20px sans-serif';
                        ctx.fillText('🥔', plot.x + 10, plot.y + 28);
                    }
                }
                ctx.fillStyle = '#4ade80';
                ctx.font = '11px sans-serif';
                ctx.fillText('Horta de Batatas', 130, 110);

                // 2. Painéis Solares
                ctx.fillStyle = '#0284c7';
                ctx.fillRect(470, 80, 80, 50);
                ctx.strokeStyle = '#38bdf8';
                ctx.lineWidth = 2;
                ctx.strokeRect(470, 80, 80, 50);
                // Grades do painel
                ctx.beginPath();
                ctx.moveTo(510, 80); ctx.lineTo(510, 130);
                ctx.moveTo(470, 105); ctx.lineTo(550, 105);
                ctx.stroke();
                // Poeira solar
                if (state.solarDust > 0) {
                    ctx.fillStyle = `rgba(180, 83, 9, ${state.solarDust / 120})`;
                    ctx.fillRect(470, 80, 80, 50);
                }
                ctx.fillStyle = '#38bdf8';
                ctx.fillText('⚡ Painéis Solares', 470, 72);

                // 3. Reator Químico de Água
                ctx.fillStyle = '#0f766e';
                ctx.fillRect(470, 260, 75, 55);
                ctx.strokeStyle = '#14b8a6';
                ctx.strokeRect(470, 260, 75, 55);
                ctx.font = '22px sans-serif';
                ctx.fillText('🧪💧', 485, 298);
                ctx.fillStyle = '#14b8a6';
                ctx.font = '11px sans-serif';
                ctx.fillText('Reator 2H₂+O₂', 470, 252);

                // 4. Mina de Tubo de Lava
                ctx.fillStyle = '#1f2937';
                ctx.beginPath();
                ctx.arc(100, 320, 30, 0, Math.PI * 2);
                ctx.fill();
                ctx.strokeStyle = '#f59e0b';
                ctx.stroke();
                ctx.font = '18px sans-serif';
                ctx.fillText('⛏️', 90, 325);
                ctx.fillStyle = '#f59e0b';
                ctx.font = '11px sans-serif';
                ctx.fillText('Tubo de Lava', 70, 365);

                // 5. Robô Auxiliar
                ctx.font = '20px sans-serif';
                ctx.fillText('🤖', state.rover.x, state.rover.y);

                // 6. Astronauta (Jogador)
                const p = state.player;
                ctx.font = '26px sans-serif';
                ctx.fillText('👩‍🚀', p.x - 12, p.y + 10);

                // Efeito Dia/Noite sobre o Domo
                if (state.timeOfDay >= 700) {
                    const darkness = ((state.timeOfDay - 700) / 300) * 0.55;
                    ctx.fillStyle = `rgba(15, 23, 42, ${darkness})`;
                    ctx.fillRect(0, 0, canvas.width, canvas.height);
                }
            }

            function gameLoop() {
                update();
                draw();
                requestAnimationFrame(gameLoop);
            }

            gameLoop();
        </script>
        </body>
        </html>
        """
        
        components.html(game_html, height=560)

