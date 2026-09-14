"""
Nova Stellaris - Jogo Arcade: Interestelar (Manobra em Gargantua & Ondas de Miller)
Jogo 2D em HTML5 Canvas + JS com Ondas Gigantes, Buraco Negro, Start, Fim e Dilatação do Tempo.
"""

import streamlit as st
import streamlit.components.v1 as components
from database import add_xp, unlock_badge

def render_interstellar_game(user: dict):
    st.markdown("""
        <div class='cosmic-hero' style='background: linear-gradient(135deg, rgba(30,10,50,0.95), rgba(16,20,47,0.95)); border: 1px solid #c084fc;'>
            <h1 style='color: #c084fc; margin-bottom: 5px;'>⏳ Interestelar: Manobra em Gargantua</h1>
            <p style='color: #cbd5e1; font-size: 1.1rem; margin: 0;'>
                Pilote a nave <strong>Ranger</strong> pelas ondas colossais do Planeta Miller e faça o estilingue gravitacional em <strong>Gargantua</strong>!
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col_game, col_info = st.columns([3, 1])
    
    with col_info:
        st.markdown("""
            <div class='cosmic-card' style='border-left: 4px solid #c084fc;'>
                <h3 style='color: #c084fc; margin-top: 0;'>🎮 Instruções de Voo</h3>
                <p style='font-size: 0.9rem;'><strong>Controles:</strong> <code>W, A, S, D</code> ou <code>Setas</code></p>
                <p style='font-size: 0.9rem;'><strong>Propulsores de Manobra:</strong> <code>Espaço</code> (Impulso Rápido)</p>
                <hr style='border-color: rgba(192,132,252,0.2);'>
                <p style='font-size: 0.85rem; color: #cbd5e1;'>
                    💾 <strong>Fase 1:</strong> Colete <strong>5 Balizas de Dados</strong> desviando das montanhas de água!<br>
                    🕳️ <strong>Fase 2:</strong> Acelere ao redor do disco de acreção de <strong>Gargantua</strong> até cruzar o Wormhole sem cair na singularidade!
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        with st.expander("🏆 Reivindicar XP da Missão", expanded=True):
            st.write("Após realizar a manobra ou cruzar o Wormhole, reivindique seus pontos:")
            game_score = st.number_input("Sua Pontuação no Jogo:", min_value=0, max_value=5000, value=0, step=100, key="interstellar_score_input")
            mission_won = st.checkbox("Cruzou o Wormhole com Sucesso?", value=False, key="interstellar_won_check")
            
            if st.button("🌟 Reivindicar Recompensas Relativísticas!", type="primary", key="interstellar_claim_btn"):
                earned_xp = (game_score // 10) + (200 if mission_won else 25)
                add_xp(user["id"], earned_xp)
                if mission_won:
                    unlock_badge(user["id"], "gargantua_slingshot")
                    unlock_badge(user["id"], "time_traveler")
                st.balloons()
                st.success(f"🎉 **+{earned_xp} XP** adicionados ao seu perfil cósmico!")
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
                height: 420px;
                border: 2px solid #c084fc;
                border-radius: 12px;
                box-shadow: 0 0 25px rgba(192, 132, 252, 0.3);
                background: #030712;
                overflow: hidden;
            }
            canvas { display: block; }
            .screen-overlay {
                position: absolute;
                top: 0; left: 0; width: 100%; height: 100%;
                background: rgba(5, 7, 20, 0.93);
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                text-align: center;
                padding: 25px;
            }
            .btn-start {
                background: linear-gradient(135deg, #c084fc, #7e22ce);
                color: #ffffff;
                font-size: 18px;
                font-weight: 800;
                padding: 12px 32px;
                border: none;
                border-radius: 30px;
                cursor: pointer;
                box-shadow: 0 0 20px rgba(192, 132, 252, 0.6);
                transition: transform 0.15s;
                margin-top: 20px;
            }
            .btn-start:hover { transform: scale(1.05); }
            #touch-bar {
                display: flex;
                justify-content: space-between;
                width: 640px;
                margin-top: 8px;
            }
            .dpad {
                display: grid;
                grid-template-columns: repeat(3, 40px);
                grid-template-rows: repeat(3, 40px);
                gap: 4px;
            }
            .t-btn {
                background: #1e293b;
                border: 1px solid #475569;
                color: #c084fc;
                border-radius: 6px;
                font-size: 16px;
                font-weight: bold;
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
            }
            .t-btn:active { background: #c084fc; color: #000; }
            .t-action {
                width: 110px;
                height: 80px;
                background: #7e22ce;
                border: 2px solid #c084fc;
                color: white;
                font-weight: bold;
                border-radius: 12px;
                cursor: pointer;
                box-shadow: 0 0 15px rgba(126, 34, 206, 0.4);
            }
            .t-action:active { background: #c084fc; color: #000; }
        </style>
        </head>
        <body>

        <div id="canvas-wrapper">
            <canvas id="gameCanvas" width="640" height="420"></canvas>

            <!-- TELA DE INÍCIO -->
            <div id="start-screen" class="screen-overlay">
                <h1 style="color: #c084fc; font-size: 26px; margin-bottom: 8px;">⏳ OPERAÇÃO GARGANTUA</h1>
                <p style="color: #94a3b8; font-size: 14px; max-width: 490px; line-height: 1.4;">
                    Resgate os <strong>5 Gravadores de Dados</strong> nas ondas gigantes do Planeta Miller e escape da atração gravitacional do buraco negro <strong>Gargantua</strong> para salvar a humanidade!
                </p>
                <div style="margin-top: 15px; font-size: 13px; color: #cbd5e1;">
                    <span>🚀 Pilotar Ranger: <strong>W,A,S,D</strong></span> | 
                    <span>⚡ Impulso de Manobra: <strong>ESPAÇO</strong></span>
                </div>
                <button class="btn-start" onclick="startGame()">🚀 INICIAR MISSÃO</button>
            </div>

            <!-- TELA DE VITÓRIA -->
            <div id="win-screen" class="screen-overlay" style="display: none;">
                <h1 style="color: #4ade80; font-size: 28px; margin-bottom: 10px;">🎉 WORMHOLE ATINGIDO!</h1>
                <p style="color: #c084fc; font-size: 17px; font-weight: bold;">
                    TARS relata: "Dados da gravidade quântica transmitidos com sucesso!"
                </p>
                <p style="color: #cbd5e1; font-size: 14px; margin-top: 10px;">
                    Você completou o estilingue gravitacional e abriu o caminho para a sobrevivência da Terra!
                </p>
                <h3 id="win-score-txt" style="color: #ffd166; margin-top: 15px;">Pontuação: 1500</h3>
                <button class="btn-start" style="background:#4ade80; color:#0f172a;" onclick="startGame()">🔄 REPLAY DA MISSÃO</button>
            </div>

            <!-- TELA DE GAME OVER -->
            <div id="gameover-screen" class="screen-overlay" style="display: none;">
                <h1 style="color: #f43f5e; font-size: 28px; margin-bottom: 10px;">💥 FALHA NA MANOBRA!</h1>
                <p id="gameover-reason" style="color: #94a3b8; font-size: 14px;">
                    A nave Ranger ultrapassou o horizonte de eventos e caiu na singularidade!
                </p>
                <h3 id="lose-score-txt" style="color: #ffd166; margin-top: 15px;">Pontuação: 0</h3>
                <button class="btn-start" style="background:#f43f5e;" onclick="startGame()">🔄 TENTAR NOVAMENTE</button>
            </div>
        </div>

        <div id="touch-bar">
            <div class="dpad">
                <div></div>
                <button class="t-btn" onpointerdown="keys.up=true" onpointerup="keys.up=false">▲</button>
                <div></div>
                <button class="t-btn" onpointerdown="keys.left=true" onpointerup="keys.left=false">◀</button>
                <div style="background:rgba(255,255,255,0.05);border-radius:4px;"></div>
                <button class="t-btn" onpointerdown="keys.right=true" onpointerup="keys.right=false">▶</button>
                <div></div>
                <button class="t-btn" onpointerdown="keys.down=true" onpointerup="keys.down=false">▼</button>
                <div></div>
            </div>
            <button class="t-action" onclick="triggerBoost()">IMPULSO<br>DE MARCHA<br>(Espaço)</button>
        </div>

        <script>
            const canvas = document.getElementById('gameCanvas');
            const ctx = canvas.getContext('2d');
            
            let gameState = 'START'; // START, PHASE1_WAVES, PHASE2_BLACKHOLE, WIN, GAMEOVER
            const keys = { up: false, down: false, left: false, right: false };
            
            let ship = { x: 120, y: 210, speed: 4.5, hull: 100, fuel: 100, boostTimer: 0 };
            let beacons = [];
            let waves = [];
            let earthYears = 0;
            let collectedBeacons = 0;
            let blackHole = { x: 500, y: 210, radius: 45, pull: 0.08 };
            let orbitProgress = 0;
            let score = 0;

            window.addEventListener('keydown', (e) => {
                if (e.key === 'w' || e.key === 'ArrowUp') keys.up = true;
                if (e.key === 's' || e.key === 'ArrowDown') keys.down = true;
                if (e.key === 'a' || e.key === 'ArrowLeft') keys.left = true;
                if (e.key === 'd' || e.key === 'ArrowRight') keys.right = true;
                if (e.key === ' ') { e.preventDefault(); triggerBoost(); }
            });

            window.addEventListener('keyup', (e) => {
                if (e.key === 'w' || e.key === 'ArrowUp') keys.up = false;
                if (e.key === 's' || e.key === 'ArrowDown') keys.down = false;
                if (e.key === 'a' || e.key === 'ArrowLeft') keys.left = false;
                if (e.key === 'd' || e.key === 'ArrowRight') keys.right = false;
            });

            function triggerBoost() {
                if (ship.fuel >= 15 && ship.boostTimer <= 0) {
                    ship.fuel -= 15;
                    ship.boostTimer = 35;
                }
            }

            function startGame() {
                document.getElementById('start-screen').style.display = 'none';
                document.getElementById('win-screen').style.display = 'none';
                document.getElementById('gameover-screen').style.display = 'none';
                
                gameState = 'PHASE1_WAVES';
                ship = { x: 120, y: 210, speed: 4.5, hull: 100, fuel: 100, boostTimer: 0 };
                beacons = [];
                waves = [];
                earthYears = 0;
                collectedBeacons = 0;
                orbitProgress = 0;
                score = 0;
            }

            function endGame(win, reason = '') {
                gameState = win ? 'WIN' : 'GAMEOVER';
                if (win) {
                    document.getElementById('win-score-txt').innerText = `Pontuação Final: ${score} pts (Anos na Terra: ${earthYears.toFixed(1)})`;
                    document.getElementById('win-screen').style.display = 'flex';
                } else {
                    document.getElementById('gameover-reason').innerText = reason || 'A nave Ranger sofreu dano estrutural irreparável!';
                    document.getElementById('lose-score-txt').innerText = `Pontuação: ${score} pts`;
                    document.getElementById('gameover-screen').style.display = 'flex';
                }
            }

            function update() {
                if (gameState !== 'PHASE1_WAVES' && gameState !== 'PHASE2_BLACKHOLE') return;

                // Dilatação do Tempo na Terra
                earthYears += 0.04;
                score += 1;

                // Movimento com Boost
                const currentSpeed = ship.boostTimer > 0 ? ship.speed * 1.8 : ship.speed;
                if (ship.boostTimer > 0) ship.boostTimer--;

                if (keys.up && ship.y > 40) ship.y -= currentSpeed;
                if (keys.down && ship.y < 380) ship.y += currentSpeed;
                if (keys.left && ship.x > 40) ship.x -= currentSpeed;
                if (keys.right && ship.x < 600) ship.x += currentSpeed;

                // Regeneração lenta de combustível
                ship.fuel = Math.min(100, ship.fuel + 0.08);

                // --- FASE 1: ONDAS DE MILLER ---
                if (gameState === 'PHASE1_WAVES') {
                    // Spawn de Balizas
                    if (Math.random() < 0.03 && beacons.length < 3) {
                        beacons.push({ x: 650, y: 50 + Math.random() * 320, speed: 2.5 });
                    }
                    // Spawn de Ondas Gigantes
                    if (Math.random() < 0.04 && waves.length < 4) {
                        waves.push({ x: 650, y: 30 + Math.random() * 360, width: 35, height: 110, speed: 4.0 });
                    }

                    // Atualizar Balizas
                    for (let i = beacons.length - 1; i >= 0; i--) {
                        let b = beacons[i];
                        b.x -= b.speed;
                        if (Math.hypot(ship.x - b.x, ship.y - b.y) < 25) {
                            beacons.splice(i, 1);
                            collectedBeacons++;
                            score += 200;
                            if (collectedBeacons >= 5) {
                                gameState = 'PHASE2_BLACKHOLE';
                                ship.x = 100;
                                ship.y = 210;
                                return;
                            }
                        } else if (b.x < -30) {
                            beacons.splice(i, 1);
                        }
                    }

                    // Atualizar Ondas
                    for (let i = waves.length - 1; i >= 0; i--) {
                        let w = waves[i];
                        w.x -= w.speed;
                        if (ship.x > w.x - 15 && ship.x < w.x + w.width && ship.y > w.y - w.height/2 && ship.y < w.y + w.height/2) {
                            waves.splice(i, 1);
                            ship.hull -= 35;
                            if (ship.hull <= 0) {
                                endGame(false, 'A nave foi atingida em cheio por uma onda colossal de 1.000 metros!');
                                return;
                            }
                        } else if (w.x < -60) {
                            waves.splice(i, 1);
                        }
                    }
                }

                // --- FASE 2: GARGANTUA SLINGSHOT ---
                if (gameState === 'PHASE2_BLACKHOLE') {
                    // Puxão Gravitacional de Gargantua
                    const dx = blackHole.x - ship.x;
                    const dy = blackHole.y - ship.y;
                    const dist = Math.hypot(dx, dy);

                    if (dist < blackHole.radius + 10) {
                        endGame(false, 'A Ranger cruzou o Horizonte de Eventos e foi engolida por Gargantua!');
                        return;
                    }

                    // Força da gravidade F = G * M / r^2
                    const gravForce = Math.min(3.5, (1200 / (dist + 50)));
                    ship.x += (dx / dist) * gravForce;
                    ship.y += (dy / dist) * gravForce;

                    // Progresso do Slingshot na órbita externa
                    if (dist > 90 && dist < 220) {
                        orbitProgress += 0.35;
                        score += 3;
                        if (orbitProgress >= 100) {
                            endGame(true);
                            return;
                        }
                    }
                }
            }

            function draw() {
                // Fundo Cósmico
                ctx.fillStyle = '#060818';
                ctx.fillRect(0, 0, canvas.width, canvas.height);

                if (gameState === 'PHASE1_WAVES') {
                    // Oceano do Planeta Miller
                    ctx.fillStyle = '#0f2b48';
                    ctx.fillRect(0, 0, canvas.width, canvas.height);

                    // Efeito de ondulação da água
                    ctx.strokeStyle = 'rgba(56, 189, 248, 0.2)';
                    for (let y = 30; y < 420; y += 40) {
                        ctx.beginPath();
                        ctx.moveTo(0, y);
                        ctx.bezierCurveTo(200, y + 10, 400, y - 10, 640, y);
                        ctx.stroke();
                    }

                    // Balizas de Dados (Chips Dourados)
                    for (let b of beacons) {
                        ctx.fillStyle = '#f59e0b';
                        ctx.fillRect(b.x - 10, b.y - 10, 20, 20);
                        ctx.strokeStyle = '#ffd166';
                        ctx.strokeRect(b.x - 10, b.y - 10, 20, 20);
                        ctx.font = '12px sans-serif';
                        ctx.fillText('💾', b.x - 7, b.y + 5);
                    }

                    // Ondas Gigantes de 1000m (Paredões de Água)
                    for (let w of waves) {
                        ctx.fillStyle = 'rgba(14, 116, 144, 0.85)';
                        ctx.beginPath();
                        ctx.ellipse(w.x + 15, w.y, w.width, w.height, 0, 0, Math.PI * 2);
                        ctx.fill();
                        ctx.strokeStyle = '#38bdf8';
                        ctx.lineWidth = 3;
                        ctx.stroke();
                    }
                } else if (gameState === 'PHASE2_BLACKHOLE') {
                    // Disco de Acreção Brilhante de Gargantua
                    ctx.save();
                    ctx.translate(blackHole.x, blackHole.y);
                    
                    // Anel Dourado de Matéria Quente
                    ctx.beginPath();
                    ctx.ellipse(0, 0, 160, 50, -0.2, 0, Math.PI * 2);
                    ctx.strokeStyle = 'rgba(251, 191, 36, 0.75)';
                    ctx.lineWidth = 18;
                    ctx.stroke();
                    
                    // Sombra do Horizonte de Eventos (Negro Absoluto)
                    ctx.beginPath();
                    ctx.arc(0, 0, blackHole.radius, 0, Math.PI * 2);
                    ctx.fillStyle = '#000000';
                    ctx.fill();
                    ctx.strokeStyle = '#ffd166';
                    ctx.lineWidth = 3;
                    ctx.stroke();
                    
                    ctx.restore();

                    // Zona de Slingshot Segura (Anel Ciano Guia)
                    ctx.beginPath();
                    ctx.arc(blackHole.x, blackHole.y, 140, 0, Math.PI * 2);
                    ctx.strokeStyle = 'rgba(0, 212, 255, 0.35)';
                    ctx.setLineDash([8, 8]);
                    ctx.stroke();
                    ctx.setLineDash([]);
                }

                if (gameState === 'PHASE1_WAVES' || gameState === 'PHASE2_BLACKHOLE') {
                    // Nave Ranger
                    ctx.fillStyle = '#e2e8f0';
                    ctx.beginPath();
                    ctx.moveTo(ship.x + 20, ship.y);
                    ctx.lineTo(ship.x - 16, ship.y - 10);
                    ctx.lineTo(ship.x - 10, ship.y);
                    ctx.lineTo(ship.x - 16, ship.y + 10);
                    ctx.closePath();
                    ctx.fill();
                    ctx.strokeStyle = '#c084fc';
                    ctx.stroke();

                    // Rastro dos propulsores
                    if (ship.boostTimer > 0) {
                        ctx.fillStyle = '#38bdf8';
                        ctx.beginPath();
                        ctx.arc(ship.x - 18, ship.y, 6 + Math.random() * 4, 0, Math.PI * 2);
                        ctx.fill();
                    }

                    // HUD Superior
                    ctx.fillStyle = 'rgba(15, 23, 42, 0.9)';
                    ctx.fillRect(0, 0, canvas.width, 38);
                    
                    ctx.fillStyle = '#c084fc';
                    ctx.font = 'bold 12px sans-serif';
                    if (gameState === 'PHASE1_WAVES') {
                        ctx.fillText(`💾 Balizas: ${collectedBeacons} / 5`, 20, 24);
                    } else {
                        ctx.fillText(`🕳️ Slingshot Gargantua: ${Math.round(orbitProgress)}%`, 20, 24);
                    }

                    ctx.fillStyle = '#ffd166';
                    ctx.fillText(`⏳ Terra: ${earthYears.toFixed(1)} Anos`, 220, 24);

                    ctx.fillStyle = ship.hull > 40 ? '#38bdf8' : '#ef4444';
                    ctx.fillText(`🛡️ Ranger: ${ship.hull}%`, 380, 24);

                    ctx.fillStyle = '#4ade80';
                    ctx.fillText(`⚡ Fuel: ${Math.round(ship.fuel)}%`, 520, 24);
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
        components.html(game_html, height=550)

