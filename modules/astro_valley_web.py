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
                <h3 style='color: #4ade80; margin-top: 0;'>🎮 Teclas de Atalho</h3>
                <p style='font-size: 0.9rem;'>⌨️ <strong>Teclado:</strong></p>
                <ul style='font-size: 0.85rem; color: #cbd5e1; padding-left: 20px; line-height: 1.6;'>
                    <li><code>W</code> ou <code>▲</code>: Mover para Cima</li>
                    <li><code>S</code> ou <code>▼</code>: Mover para Baixo</li>
                    <li><code>A</code> ou <code>◀</code>: Mover para Esquerda</li>
                    <li><code>D</code> ou <code>▶</code>: Mover para Direita</li>
                    <li><code>Espaço</code>: Realizar Ação</li>
                </ul>
                <hr style='border-color: rgba(74,222,128,0.2);'>
                <p style='font-size: 0.85rem; color: #cbd5e1;'>
                    📱 <strong>Touchscreen / Mouse:</strong> Use os botões luminosos abaixo da tela do jogo!
                </p>
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
            sync_sol = st.number_input("Sols Completados no Jogo:", min_value=1, max_value=100, value=1, step=1, key="astro_valley_sol")
            sync_harvest = st.number_input("Batatas Colhidas:", min_value=0, max_value=500, value=0, step=1, key="astro_valley_harvest")
            
            if st.button("🌟 Reivindicar XP da Colônia!", type="primary", key="astro_valley_claim_btn"):
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
        # Código HTML5 + Canvas + JS do Astro-Valley com Controles Aprimorados
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
                justify-content: flex-start;
                padding: 4px;
            }
            #game-container {
                position: relative;
                width: 640px;
                border: 2px solid #00d4ff;
                border-radius: 12px;
                box-shadow: 0 0 25px rgba(0, 212, 255, 0.3);
                background: #111827;
                overflow: hidden;
            }
            canvas {
                display: block;
                image-rendering: pixelated;
                cursor: pointer;
                outline: none;
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
            
            /* PAINEL DE CONTROLES LUMINOSOS */
            #controls-panel {
                display: flex;
                justify-content: space-between;
                align-items: center;
                width: 640px;
                background: rgba(15, 23, 42, 0.9);
                border: 1px solid rgba(0, 212, 255, 0.3);
                border-radius: 12px;
                margin-top: 8px;
                padding: 10px 18px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.4);
            }
            .dpad-container {
                display: grid;
                grid-template-columns: repeat(3, 52px);
                grid-template-rows: repeat(3, 48px);
                gap: 5px;
            }
            .btn-ctrl {
                background: linear-gradient(180deg, #1e293b, #0f172a);
                border: 2px solid #38bdf8;
                color: #38bdf8;
                border-radius: 10px;
                font-size: 17px;
                font-weight: 800;
                cursor: pointer;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                box-shadow: 0 0 10px rgba(56, 189, 248, 0.25);
                transition: all 0.1s ease;
                touch-action: manipulation;
            }
            .btn-ctrl span.key-lbl {
                font-size: 10px;
                color: #94a3b8;
                margin-top: -2px;
            }
            .btn-ctrl:active, .btn-ctrl.active {
                background: #38bdf8;
                color: #070913;
                box-shadow: 0 0 18px rgba(56, 189, 248, 0.8);
                transform: scale(0.93);
            }
            .btn-ctrl:active span.key-lbl { color: #070913; }
            
            .action-container {
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 5px;
            }
            .btn-action-big {
                width: 140px;
                height: 75px;
                border-radius: 16px;
                background: linear-gradient(135deg, #059669, #10b981);
                border: 3px solid #34d399;
                color: #ffffff;
                font-size: 15px;
                font-weight: 800;
                cursor: pointer;
                box-shadow: 0 0 20px rgba(52, 211, 153, 0.45);
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                transition: all 0.1s ease;
                touch-action: manipulation;
            }
            .btn-action-big:active {
                background: #34d399;
                color: #064e3b;
                box-shadow: 0 0 30px rgba(52, 211, 153, 0.9);
                transform: scale(0.95);
            }
            
            .keys-guide {
                display: flex;
                flex-direction: column;
                gap: 4px;
                font-size: 11px;
                color: #94a3b8;
                background: rgba(0,0,0,0.3);
                padding: 8px 12px;
                border-radius: 8px;
                border-left: 3px solid #00d4ff;
            }
            
            #message-banner {
                position: absolute;
                bottom: 12px;
                left: 50%;
                transform: translateX(-50%);
                background: rgba(15, 23, 42, 0.95);
                border: 1px solid #4ade80;
                color: #4ade80;
                padding: 6px 14px;
                border-radius: 20px;
                font-size: 12px;
                font-weight: bold;
                pointer-events: none;
                transition: opacity 0.3s;
                opacity: 0;
                box-shadow: 0 0 15px rgba(74, 222, 128, 0.3);
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
            <canvas id="gameCanvas" width="640" height="380" tabindex="1"></canvas>
            <div id="message-banner">Mensagem da Base</div>
        </div>

        <!-- PAINEL DE CONTROLES LUMINOSOS E VISÍVEIS -->
        <div id="controls-panel">
            <div class="dpad-container">
                <div></div>
                <button class="btn-ctrl" id="btn-up" onpointerdown="startMove('up')" onpointerup="stopMove('up')" onpointerleave="stopMove('up')">
                    ▲<span class="key-lbl">W</span>
                </button>
                <div></div>
                
                <button class="btn-ctrl" id="btn-left" onpointerdown="startMove('left')" onpointerup="stopMove('left')" onpointerleave="stopMove('left')">
                    ◀<span class="key-lbl">A</span>
                </button>
                <div style="background:rgba(0, 212, 255, 0.1);border-radius:6px;display:flex;align-items:center;justify-content:center;font-size:10px;color:#38bdf8;font-weight:bold;">PAD</div>
                <button class="btn-ctrl" id="btn-right" onpointerdown="startMove('right')" onpointerup="stopMove('right')" onpointerleave="stopMove('right')">
                    ▶<span class="key-lbl">D</span>
                </button>
                
                <div></div>
                <button class="btn-ctrl" id="btn-down" onpointerdown="startMove('down')" onpointerup="stopMove('down')" onpointerleave="stopMove('down')">
                    ▼<span class="key-lbl">S</span>
                </button>
                <div></div>
            </div>

            <div class="keys-guide">
                <div>⌨️ <strong>W, A, S, D</strong> ou <strong>Setas</strong> = Mover</div>
                <div>🌱 <strong>Espaço / E</strong> = Ação no Domo</div>
                <div>💡 <em>Clique no jogo para focar o teclado</em></div>
            </div>

            <div class="action-container">
                <button class="btn-action-big" onclick="performAction()">
                    🌱 AÇÃO
                    <span style="font-size: 11px; font-weight: normal; color: #d1fae5;">(Espaço)</span>
                </button>
            </div>
        </div>

        <script>
            const canvas = document.getElementById('gameCanvas');
            const ctx = canvas.getContext('2d');
            
            // Focar canvas no clique
            canvas.addEventListener('click', () => { canvas.focus(); });

            // Estado do Jogo
            const state = {
                player: { x: 300, y: 190, size: 24, speed: 3.8, dir: 'down', animFrame: 0 },
                keys: { up: false, down: false, left: false, right: false },
                sol: 1,
                timeOfDay: 0,
                energy: 100,
                water: 50,
                potatoes: 0,
                ores: 0,
                solarDust: 0,
                plots: [
                    { x: 120, y: 110, state: 'empty', progress: 0 },
                    { x: 170, y: 110, state: 'empty', progress: 0 },
                    { x: 220, y: 110, state: 'empty', progress: 0 },
                    { x: 120, y: 160, state: 'empty', progress: 0 },
                    { x: 170, y: 160, state: 'empty', progress: 0 },
                    { x: 220, y: 160, state: 'empty', progress: 0 },
                ],
                rover: { x: 350, y: 120, dir: 1 }
            };

            function showBanner(text) {
                const b = document.getElementById('message-banner');
                b.innerText = text;
                b.style.opacity = '1';
                setTimeout(() => { b.style.opacity = '0'; }, 2500);
            }

            // Captura de Teclado
            window.addEventListener('keydown', (e) => {
                if (['Space', 'ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'].includes(e.code)) {
                    e.preventDefault();
                }
                if (e.key === 'w' || e.key === 'W' || e.key === 'ArrowUp') { state.keys.up = true; updateBtnVisual('btn-up', true); }
                if (e.key === 's' || e.key === 'S' || e.key === 'ArrowDown') { state.keys.down = true; updateBtnVisual('btn-down', true); }
                if (e.key === 'a' || e.key === 'A' || e.key === 'ArrowLeft') { state.keys.left = true; updateBtnVisual('btn-left', true); }
                if (e.key === 'd' || e.key === 'D' || e.key === 'ArrowRight') { state.keys.right = true; updateBtnVisual('btn-right', true); }
                if (e.key === ' ' || e.key === 'e' || e.key === 'E' || e.key === 'Enter') {
                    performAction();
                }
            });

            window.addEventListener('keyup', (e) => {
                if (e.key === 'w' || e.key === 'W' || e.key === 'ArrowUp') { state.keys.up = false; updateBtnVisual('btn-up', false); }
                if (e.key === 's' || e.key === 'S' || e.key === 'ArrowDown') { state.keys.down = false; updateBtnVisual('btn-down', false); }
                if (e.key === 'a' || e.key === 'A' || e.key === 'ArrowLeft') { state.keys.left = false; updateBtnVisual('btn-left', false); }
                if (e.key === 'd' || e.key === 'D' || e.key === 'ArrowRight') { state.keys.right = false; updateBtnVisual('btn-right', false); }
            });

            function updateBtnVisual(id, active) {
                const el = document.getElementById(id);
                if (el) {
                    if (active) el.classList.add('active');
                    else el.classList.remove('active');
                }
            }

            function startMove(dir) { state.keys[dir] = true; }
            function stopMove(dir) { state.keys[dir] = false; }

            // Lógica de Ação no Domo
            function performAction() {
                const p = state.player;
                
                // 1. Canteiros
                for (let plot of state.plots) {
                    const dist = Math.hypot(p.x - (plot.x + 18), p.y - (plot.y + 18));
                    if (dist < 42) {
                        if (plot.state === 'empty') {
                            plot.state = 'tilled';
                            showBanner('🌱 Solo arado! Aperte AÇÃO para semear batatas.');
                        } else if (plot.state === 'tilled') {
                            plot.state = 'seeded';
                            plot.progress = 10;
                            showBanner('🥔 Batatas plantadas! Aperte AÇÃO para regar.');
                        } else if (plot.state === 'seeded') {
                            if (state.water >= 5) {
                                state.water -= 5;
                                plot.state = 'growing';
                                showBanner('💧 Canteiro irrigado! As batatas estão crescendo.');
                            } else {
                                showBanner('⚠️ Falta água! Vá ao reator químico no canto direito.');
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

                // 2. Painéis Solares (x: 480, y: 70)
                if (Math.hypot(p.x - 510, p.y - 95) < 60) {
                    if (state.solarDust > 10) {
                        state.solarDust = 0;
                        state.energy = Math.min(100, state.energy + 20);
                        showBanner('⚡ Painéis limpos! Eficiência solar restaurada a 100%!');
                    } else {
                        showBanner('⚡ Painéis solares fotovoltaicos limpos e operando a 100%.');
                    }
                    updateHud();
                    return;
                }

                // 3. Reator Químico de Água (x: 480, y: 260)
                if (Math.hypot(p.x - 510, p.y - 280) < 60) {
                    if (state.energy >= 15) {
                        state.energy -= 15;
                        state.water += 25;
                        showBanner('🧪 Reação 2H₂ + O₂ ➔ 2H₂O concluída! +25L de Água sintetizados!');
                    } else {
                        showBanner('⚠️ Energia insuficiente na rede para o reator!');
                    }
                    updateHud();
                    return;
                }

                // 4. Mina de Tubo de Lava (x: 80, y: 290)
                if (Math.hypot(p.x - 100, p.y - 305) < 60) {
                    if (state.energy >= 10) {
                        state.energy -= 10;
                        state.ores += 2;
                        showBanner('⛏️ Mineração concluída! +2 Minérios de Ferro e Xenonite extraídos!');
                    } else {
                        showBanner('⚠️ Traje sem energia para perfurar a rocha!');
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

            function update() {
                const p = state.player;
                let moved = false;

                if (state.keys.up && p.y > 45) { p.y -= p.speed; p.dir = 'up'; moved = true; }
                if (state.keys.down && p.y < canvas.height - 45) { p.y += p.speed; p.dir = 'down'; moved = true; }
                if (state.keys.left && p.x > 45) { p.x -= p.speed; p.dir = 'left'; moved = true; }
                if (state.keys.right && p.x < canvas.width - 45) { p.x += p.speed; p.dir = 'right'; moved = true; }

                if (moved) p.animFrame += 0.2;

                // Ciclo Dia/Noite (Sol)
                state.timeOfDay += 0.7;
                if (state.timeOfDay > 1000) {
                    state.timeOfDay = 0;
                    state.sol += 1;
                    state.solarDust = Math.min(80, state.solarDust + 15);
                    showBanner(`🌅 Sol ${state.sol} iniciado em Marte! Novo dia na colônia.`);
                }

                const isDay = state.timeOfDay < 700;
                if (isDay) {
                    const solarGain = 0.05 * (1 - state.solarDust / 100);
                    state.energy = Math.min(100, state.energy + solarGain);
                } else {
                    state.energy = Math.max(0, state.energy - 0.03);
                }

                for (let plot of state.plots) {
                    if (plot.state === 'growing') {
                        plot.progress += 0.15;
                        if (plot.progress >= 100) plot.state = 'ready';
                    }
                }

                state.rover.x += 0.8 * state.rover.dir;
                if (state.rover.x > 400) state.rover.dir = -1;
                if (state.rover.x < 300) state.rover.dir = 1;

                updateHud();
            }

            function draw() {
                ctx.fillStyle = '#993d26';
                ctx.fillRect(0, 0, canvas.width, canvas.height);

                // Domo Geodésico
                ctx.fillStyle = '#1e293b';
                ctx.beginPath();
                ctx.arc(320, 190, 260, 0, Math.PI * 2);
                ctx.fill();
                ctx.lineWidth = 4;
                ctx.strokeStyle = '#00d4ff';
                ctx.stroke();

                // Grelha do Piso
                ctx.strokeStyle = 'rgba(0, 212, 255, 0.08)';
                ctx.lineWidth = 1;
                for (let x = 70; x < 570; x += 30) {
                    ctx.beginPath(); ctx.moveTo(x, 30); ctx.lineTo(x, 350); ctx.stroke();
                }
                for (let y = 30; y < 350; y += 30) {
                    ctx.beginPath(); ctx.moveTo(70, y); ctx.lineTo(570, y); ctx.stroke();
                }

                // Canteiros
                for (let plot of state.plots) {
                    ctx.fillStyle = plot.state === 'empty' ? '#451a03' : (plot.state === 'growing' ? '#14532d' : '#78350f');
                    ctx.fillRect(plot.x, plot.y, 40, 40);
                    ctx.strokeStyle = '#22c55e';
                    ctx.strokeRect(plot.x, plot.y, 40, 40);

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
                ctx.fillText('Horta de Batatas', 130, 100);

                // Painéis Solares
                ctx.fillStyle = '#0284c7';
                ctx.fillRect(470, 70, 80, 50);
                ctx.strokeStyle = '#38bdf8';
                ctx.lineWidth = 2;
                ctx.strokeRect(470, 70, 80, 50);
                ctx.beginPath();
                ctx.moveTo(510, 70); ctx.lineTo(510, 120);
                ctx.moveTo(470, 95); ctx.lineTo(550, 95);
                ctx.stroke();
                if (state.solarDust > 0) {
                    ctx.fillStyle = `rgba(180, 83, 9, ${state.solarDust / 120})`;
                    ctx.fillRect(470, 70, 80, 50);
                }
                ctx.fillStyle = '#38bdf8';
                ctx.fillText('⚡ Painéis Solares', 470, 62);

                // Reator Químico
                ctx.fillStyle = '#0f766e';
                ctx.fillRect(470, 245, 75, 55);
                ctx.strokeStyle = '#14b8a6';
                ctx.strokeRect(470, 245, 75, 55);
                ctx.font = '22px sans-serif';
                ctx.fillText('🧪💧', 485, 283);
                ctx.fillStyle = '#14b8a6';
                ctx.font = '11px sans-serif';
                ctx.fillText('Reator 2H₂+O₂', 470, 238);

                // Mina
                ctx.fillStyle = '#1f2937';
                ctx.beginPath();
                ctx.arc(100, 295, 28, 0, Math.PI * 2);
                ctx.fill();
                ctx.strokeStyle = '#f59e0b';
                ctx.stroke();
                ctx.font = '18px sans-serif';
                ctx.fillText('⛏️', 90, 300);
                ctx.fillStyle = '#f59e0b';
                ctx.font = '11px sans-serif';
                ctx.fillText('Tubo de Lava', 70, 338);

                // Rover
                ctx.font = '20px sans-serif';
                ctx.fillText('🤖', state.rover.x, state.rover.y);

                // Astronauta
                const p = state.player;
                ctx.font = '26px sans-serif';
                ctx.fillText('👩‍🚀', p.x - 12, p.y + 10);

                // Noite Marciana
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
        
        components.html(game_html, height=690)

