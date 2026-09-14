"""
Nova Stellaris - Jogo Arcade: Operação Hail Mary (Devoradores de Estrelas)
Jogo 2D em HTML5 Canvas + JS com tela de Início, Fim, Mecânicas de Som e Taumebas.
"""

import streamlit as st
import streamlit.components.v1 as components
from database import add_xp, unlock_badge

def render_hail_mary_game(user: dict):
    st.markdown("""
        <div class='cosmic-hero' style='background: linear-gradient(135deg, rgba(40,30,10,0.95), rgba(16,20,47,0.95)); border: 1px solid #ffd166;'>
            <h1 style='color: #ffd166; margin-bottom: 5px;'>✨ Operação Hail Mary: Resgate de Tau Ceti</h1>
            <p style='color: #cbd5e1; font-size: 1.1rem; margin: 0;'>
                Pilote a nave <strong>Hail Mary</strong> ao lado de <strong>Rocky</strong>, capture Taumebas e salve o Sol da extinção!
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col_game, col_info = st.columns([3, 1])
    
    with col_info:
        st.markdown("""
            <div class='cosmic-card' style='border-left: 4px solid #ffd166;'>
                <h3 style='color: #ffd166; margin-top: 0;'>🎮 Instruções de Voo</h3>
                <p style='font-size: 0.9rem;'><strong>Movimento:</strong> <code>W, A, S, D</code> ou <code>Setas</code></p>
                <p style='font-size: 0.9rem;'><strong>Escudo Harmônico de Rocky:</strong> <code>Espaço</code> ou <code>Botão Ação</code></p>
                <hr style='border-color: rgba(255,209,102,0.2);'>
                <p style='font-size: 0.85rem; color: #cbd5e1;'>
                    🦠 <strong>Objetivo:</strong> Colete <strong>10 Taumebas</strong> (células verdes) para vencer!<br>
                    🔴 <strong>Perigo:</strong> Desvie dos Astrofagos vermelhos que devoram o escudo.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        with st.expander("🏆 Reivindicar XP da Missão", expanded=True):
            st.write("Após completar a missão ou atingir uma pontuação alta, salve seu XP:")
            game_score = st.number_input("Sua Pontuação no Jogo:", min_value=0, max_value=5000, value=0, step=100, key="hail_mary_score_input")
            mission_won = st.checkbox("Missão Cumprida (10 Taumebas)?", value=False, key="hail_mary_won_check")
            
            if st.button("🌟 Reivindicar Recompensas de Tau Ceti!", type="primary", key="hail_mary_claim_btn"):
                earned_xp = (game_score // 10) + (200 if mission_won else 20)
                add_xp(user["id"], earned_xp)
                if mission_won:
                    unlock_badge(user["id"], "hail_mary_hero")
                    unlock_badge(user["id"], "rocky_friend")
                st.balloons()
                st.success(f"🎉 **+{earned_xp} XP** adicionados ao seu perfil de explorador!")
                st.rerun()

    with col_game:
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
                font-family: 'Segoe UI', sans-serif;
                display: flex;
                flex-direction: column;
                align-items: center;
                padding: 5px;
            }
            #canvas-wrapper {
                position: relative;
                width: 640px;
                height: 380px;
                border: 2px solid #ffd166;
                border-radius: 12px;
                box-shadow: 0 0 25px rgba(255, 209, 102, 0.25);
                background: #030712;
                overflow: hidden;
            }
            canvas {
                display: block;
                outline: none;
                cursor: pointer;
            }
            .screen-overlay {
                position: absolute;
                top: 0; left: 0; width: 100%; height: 100%;
                background: rgba(3, 7, 18, 0.92);
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                text-align: center;
                padding: 25px;
            }
            .btn-start {
                background: linear-gradient(135deg, #ffd166, #f59e0b);
                color: #0f172a;
                font-size: 18px;
                font-weight: 800;
                padding: 12px 32px;
                border: none;
                border-radius: 30px;
                cursor: pointer;
                box-shadow: 0 0 20px rgba(255, 209, 102, 0.6);
                transition: transform 0.15s;
                margin-top: 20px;
            }
            .btn-start:hover { transform: scale(1.05); }

            /* PAINEL DE CONTROLES LUMINOSOS */
            #controls-panel {
                display: flex;
                justify-content: space-between;
                align-items: center;
                width: 640px;
                background: rgba(15, 23, 42, 0.9);
                border: 1px solid rgba(255, 209, 102, 0.3);
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
                border: 2px solid #ffd166;
                color: #ffd166;
                border-radius: 10px;
                font-size: 17px;
                font-weight: 800;
                cursor: pointer;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                box-shadow: 0 0 10px rgba(255, 209, 102, 0.25);
                transition: all 0.1s ease;
                touch-action: manipulation;
            }
            .btn-ctrl span.key-lbl {
                font-size: 10px;
                color: #94a3b8;
                margin-top: -2px;
            }
            .btn-ctrl:active, .btn-ctrl.active {
                background: #ffd166;
                color: #070913;
                box-shadow: 0 0 18px rgba(255, 209, 102, 0.8);
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
                background: linear-gradient(135deg, #d97706, #f59e0b);
                border: 3px solid #ffd166;
                color: #ffffff;
                font-size: 14px;
                font-weight: 800;
                cursor: pointer;
                box-shadow: 0 0 20px rgba(245, 158, 11, 0.45);
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                transition: all 0.1s ease;
                touch-action: manipulation;
            }
            .btn-action-big:active {
                background: #ffd166;
                color: #0f172a;
                box-shadow: 0 0 30px rgba(255, 209, 102, 0.9);
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
                border-left: 3px solid #ffd166;
            }
        </style>
        </head>
        <body>

        <div id="canvas-wrapper">
            <canvas id="gameCanvas" width="640" height="380" tabindex="1"></canvas>

            <!-- TELA DE INÍCIO -->
            <div id="start-screen" class="screen-overlay">
                <h1 style="color: #ffd166; font-size: 26px; margin-bottom: 8px;">✨ OPERAÇÃO HAIL MARY</h1>
                <p style="color: #94a3b8; font-size: 14px; max-width: 480px; line-height: 1.4;">
                    Os microrganismos <strong>Astrofagos</strong> estão drenando a energia do Sol. 
                    Junto com a nave alienígena de <strong>Rocky</strong>, colete <strong>10 Taumebas</strong> para restaurar o equilíbrio do sistema estelar!
                </p>
                <div style="margin-top: 15px; font-size: 13px; color: #cbd5e1;">
                    <span>🚀 Movimento: <strong>W,A,S,D</strong></span> | 
                    <span>🛡️ Escudo de Rocky: <strong>ESPAÇO</strong></span>
                </div>
                <button class="btn-start" onclick="startGame()">🚀 INICIAR MISSÃO</button>
            </div>

            <!-- TELA DE VITÓRIA -->
            <div id="win-screen" class="screen-overlay" style="display: none;">
                <h1 style="color: #4ade80; font-size: 28px; margin-bottom: 10px;">🎉 MISSÃO CUMPRIDA!</h1>
                <p style="color: #ffd166; font-size: 18px; font-weight: bold;">
                    Rocky comemora: "Amigo bom! Fist my bump! 👊"
                </p>
                <p style="color: #cbd5e1; font-size: 14px; margin-top: 10px;">
                    Você coletou as 10 Taumebas e salvou a Terra e o planeta 40 Eridani!
                </p>
                <h3 id="win-score-txt" style="color: #00d4ff; margin-top: 15px;">Pontuação: 1000</h3>
                <button class="btn-start" style="background:#4ade80;" onclick="startGame()">🔄 JOGAR NOVAMENTE</button>
            </div>

            <!-- TELA DE GAME OVER -->
            <div id="gameover-screen" class="screen-overlay" style="display: none;">
                <h1 style="color: #f43f5e; font-size: 28px; margin-bottom: 10px;">💥 ESCUDOS ESGOTADOS!</h1>
                <p style="color: #94a3b8; font-size: 14px;">
                    A nave Hail Mary sofreu dano crítico por colisão com nuvens de Astrofagos.
                </p>
                <h3 id="lose-score-txt" style="color: #ffd166; margin-top: 15px;">Pontuação: 0</h3>
                <button class="btn-start" style="background:#f43f5e; color:white;" onclick="startGame()">🔄 REINICIAR MISSÃO</button>
            </div>
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
                <div style="background:rgba(255, 209, 102, 0.1);border-radius:6px;display:flex;align-items:center;justify-content:center;font-size:10px;color:#ffd166;font-weight:bold;">ROCKY</div>
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
                <div>⌨️ <strong>W, A, S, D</strong> ou <strong>Setas</strong> = Mover Nave</div>
                <div>🎶 <strong>Espaço</strong> = Escudo Harmônico de Rocky</div>
                <div>💡 <em>Clique no jogo para focar o teclado</em></div>
            </div>

            <div class="action-container">
                <button class="btn-action-big" onclick="triggerRockyShield()">
                    🎶 ESCUDO
                    <span style="font-size: 11px; font-weight: normal; color: #fef08a;">(Espaço)</span>
                </button>
            </div>
        </div>

        <script>
            const canvas = document.getElementById('gameCanvas');
            const ctx = canvas.getContext('2d');
            
            canvas.addEventListener('click', () => { canvas.focus(); });
            
            let gameState = 'START'; // START, PLAYING, WIN, GAMEOVER
            const keys = { up: false, down: false, left: false, right: false };
            
            function startMove(dir) {
                keys[dir] = true;
                const btn = document.getElementById('btn-' + dir);
                if (btn) btn.classList.add('active');
            }
            function stopMove(dir) {
                keys[dir] = false;
                const btn = document.getElementById('btn-' + dir);
                if (btn) btn.classList.remove('active');
            }
            
            let ship = { x: 100, y: 190, speed: 4.5, shields: 100 };
            let rocky = { x: 60, y: 220, pulse: 0, shieldActive: 0 };
            let taumoebas = [];
            let astrophages = [];
            let stars = [];
            let collected = 0;
            let score = 0;
            
            for (let i = 0; i < 60; i++) {
                stars.push({ x: Math.random() * 640, y: Math.random() * 380, speed: 0.5 + Math.random() * 2, size: Math.random() * 2 });
            }

            window.addEventListener('keydown', (e) => {
                if (e.key === 'w' || e.key === 'W' || e.key === 'ArrowUp') { keys.up = true; document.getElementById('btn-up')?.classList.add('active'); }
                if (e.key === 's' || e.key === 'S' || e.key === 'ArrowDown') { keys.down = true; document.getElementById('btn-down')?.classList.add('active'); }
                if (e.key === 'a' || e.key === 'A' || e.key === 'ArrowLeft') { keys.left = true; document.getElementById('btn-left')?.classList.add('active'); }
                if (e.key === 'd' || e.key === 'D' || e.key === 'ArrowRight') { keys.right = true; document.getElementById('btn-right')?.classList.add('active'); }
                if (e.key === ' ') { e.preventDefault(); triggerRockyShield(); }
            });

            window.addEventListener('keyup', (e) => {
                if (e.key === 'w' || e.key === 'W' || e.key === 'ArrowUp') { keys.up = false; document.getElementById('btn-up')?.classList.remove('active'); }
                if (e.key === 's' || e.key === 'S' || e.key === 'ArrowDown') { keys.down = false; document.getElementById('btn-down')?.classList.remove('active'); }
                if (e.key === 'a' || e.key === 'A' || e.key === 'ArrowLeft') { keys.left = false; document.getElementById('btn-left')?.classList.remove('active'); }
                if (e.key === 'd' || e.key === 'D' || e.key === 'ArrowRight') { keys.right = false; document.getElementById('btn-right')?.classList.remove('active'); }
            });

            function triggerRockyShield() {
                if (gameState === 'PLAYING' && rocky.shieldActive <= 0) {
                    rocky.shieldActive = 60; // 1 segundo de escudo sonoro
                }
            }

            function startGame() {
                document.getElementById('start-screen').style.display = 'none';
                document.getElementById('win-screen').style.display = 'none';
                document.getElementById('gameover-screen').style.display = 'none';
                
                gameState = 'PLAYING';
                ship = { x: 100, y: 190, speed: 4.5, shields: 100 };
                rocky = { x: 60, y: 220, pulse: 0, shieldActive: 0 };
                taumoebas = [];
                astrophages = [];
                collected = 0;
                score = 0;
                canvas.focus();
            }

            function endGame(win) {
                gameState = win ? 'WIN' : 'GAMEOVER';
                if (win) {
                    document.getElementById('win-score-txt').innerText = `Pontuação Final: ${score} pts`;
                    document.getElementById('win-screen').style.display = 'flex';
                } else {
                    document.getElementById('lose-score-txt').innerText = `Pontuação: ${score} pts`;
                    document.getElementById('gameover-screen').style.display = 'flex';
                }
            }

            function spawnEntities() {
                if (Math.random() < 0.035 && taumoebas.length < 5) {
                    taumoebas.push({ x: 650, y: 40 + Math.random() * 340, speed: 2.2 });
                }
                if (Math.random() < 0.055 && astrophages.length < 9) {
                    astrophages.push({ x: 650, y: 30 + Math.random() * 360, speed: 3.2 + Math.random() * 2, size: 10 + Math.random() * 10 });
                }
            }

            function update() {
                if (gameState !== 'PLAYING') return;

                // Movimento da Nave
                if (keys.up && ship.y > 40) ship.y -= ship.speed;
                if (keys.down && ship.y < 380) ship.y += ship.speed;
                if (keys.left && ship.x > 50) ship.x -= ship.speed;
                if (keys.right && ship.x < 580) ship.x += ship.speed;

                // Rocky segue a nave com atraso elástico
                rocky.x += (ship.x - 45 - rocky.x) * 0.08;
                rocky.y += (ship.y + 25 - rocky.y) * 0.08;
                rocky.pulse += 0.1;
                if (rocky.shieldActive > 0) rocky.shieldActive--;

                // Estrelas de Fundo
                for (let s of stars) {
                    s.x -= s.speed;
                    if (s.x < 0) s.x = 640;
                }

                spawnEntities();

                // Atualizar Taumebas
                for (let i = taumoebas.length - 1; i >= 0; i--) {
                    let t = taumoebas[i];
                    t.x -= t.speed;

                    // Colisão com a nave
                    if (Math.hypot(ship.x - t.x, ship.y - t.y) < 26) {
                        taumoebas.splice(i, 1);
                        collected++;
                        score += 150;
                        if (collected >= 10) {
                            endGame(true);
                            return;
                        }
                    } else if (t.x < -20) {
                        taumoebas.splice(i, 1);
                    }
                }

                // Atualizar Astrofagos
                for (let i = astrophages.length - 1; i >= 0; i--) {
                    let a = astrophages[i];
                    a.x -= a.speed;

                    // Destruído pelo escudo de som de Rocky
                    if (rocky.shieldActive > 0 && Math.hypot(ship.x - a.x, ship.y - a.y) < 80) {
                        astrophages.splice(i, 1);
                        score += 50;
                        continue;
                    }

                    // Dano na nave
                    if (Math.hypot(ship.x - a.x, ship.y - a.y) < 22) {
                        astrophages.splice(i, 1);
                        ship.shields -= 20;
                        if (ship.shields <= 0) {
                            endGame(false);
                            return;
                        }
                    } else if (a.x < -30) {
                        astrophages.splice(i, 1);
                    }
                }

                score += 1;
            }

            function draw() {
                ctx.fillStyle = '#050714';
                ctx.fillRect(0, 0, canvas.width, canvas.height);

                // Estrelas
                ctx.fillStyle = '#ffffff';
                for (let s of stars) {
                    ctx.beginPath();
                    ctx.arc(s.x, s.y, s.size, 0, Math.PI * 2);
                    ctx.fill();
                }

                if (gameState === 'PLAYING') {
                    // Escudo Sônico de Rocky (Onda Harmônica Amarela)
                    if (rocky.shieldActive > 0) {
                        ctx.beginPath();
                        ctx.arc(ship.x, ship.y, 75, 0, Math.PI * 2);
                        ctx.strokeStyle = `rgba(255, 209, 102, ${rocky.shieldActive / 60})`;
                        ctx.lineWidth = 4;
                        ctx.stroke();
                        ctx.fillStyle = `rgba(255, 209, 102, 0.15)`;
                        ctx.fill();
                    }

                    // Nave Alienígena de Rocky (Blip-A)
                    ctx.fillStyle = '#64748b';
                    ctx.beginPath();
                    ctx.arc(rocky.x, rocky.y, 14, 0, Math.PI * 2);
                    ctx.fill();
                    ctx.strokeStyle = '#ffd166';
                    ctx.stroke();
                    ctx.font = '14px sans-serif';
                    ctx.fillText('🕷️', rocky.x - 7, rocky.y + 5);

                    // Nave Hail Mary
                    ctx.fillStyle = '#f8fafc';
                    ctx.beginPath();
                    ctx.moveTo(ship.x + 22, ship.y);
                    ctx.lineTo(ship.x - 18, ship.y - 12);
                    ctx.lineTo(ship.x - 10, ship.y);
                    ctx.lineTo(ship.x - 18, ship.y + 12);
                    ctx.closePath();
                    ctx.fill();
                    ctx.strokeStyle = '#00d4ff';
                    ctx.stroke();
                    // Fogo do motor
                    ctx.fillStyle = '#f97316';
                    ctx.beginPath();
                    ctx.moveTo(ship.x - 14, ship.y - 4);
                    ctx.lineTo(ship.x - 24 - Math.random() * 8, ship.y);
                    ctx.lineTo(ship.x - 14, ship.y + 4);
                    ctx.closePath();
                    ctx.fill();

                    // Taumebas (Células Verdes Brilhantes)
                    for (let t of taumoebas) {
                        ctx.fillStyle = '#4ade80';
                        ctx.beginPath();
                        ctx.arc(t.x, t.y, 10, 0, Math.PI * 2);
                        ctx.fill();
                        ctx.strokeStyle = '#ffffff';
                        ctx.lineWidth = 2;
                        ctx.stroke();
                        ctx.font = '12px sans-serif';
                        ctx.fillText('🦠', t.x - 7, t.y + 5);
                    }

                    // Astrofagos (Nuvens Vermelhas Incandescentes)
                    for (let a of astrophages) {
                        ctx.fillStyle = '#ef4444';
                        ctx.beginPath();
                        ctx.arc(a.x, a.y, a.size, 0, Math.PI * 2);
                        ctx.fill();
                        ctx.strokeStyle = '#f87171';
                        ctx.stroke();
                    }

                    // HUD Superior
                    ctx.fillStyle = 'rgba(15, 23, 42, 0.85)';
                    ctx.fillRect(0, 0, canvas.width, 36);
                    ctx.fillStyle = '#ffd166';
                    ctx.font = 'bold 13px sans-serif';
                    ctx.fillText(`🦠 Taumebas: ${collected} / 10`, 20, 23);
                    
                    ctx.fillStyle = ship.shields > 30 ? '#38bdf8' : '#ef4444';
                    ctx.fillText(`🛡️ Escudos: ${ship.shields}%`, 220, 23);
                    
                    ctx.fillStyle = '#f1f5f9';
                    ctx.fillText(`⭐ Pontos: ${score}`, 420, 23);

                    ctx.fillStyle = rocky.shieldActive > 0 ? '#4ade80' : '#94a3b8';
                    ctx.fillText(rocky.shieldActive > 0 ? `🎶 ESCUDO ATIVO!` : `🎶 [ESPAÇO] Escudo`, 520, 23);
                }
            }

            function loop() {
                update();
                draw();
                requestAnimationFrame(loop);
            }

            loop();
        </script>
        </body>
        </html>
        """
        components.html(game_html, height=690)

