"""
Interestelar: Manobra em Gargantua - Jogo Desktop 2D em Pygame
Resgate balizas de dados nas ondas gigantes e realize o estilingue gravitacional em Gargantua!
"""

import pygame
import sys
import os
import random
import math

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import database
import game_pygame.audio as audio

WIDTH, HEIGHT = 960, 640
FPS = 60

def run_interstellar(user_name="Cadete Estelar"):
    pygame.init()
    pygame.font.init()
    audio.init_audio()
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Interestelar: Manobra em Gargantua — (Nova Stellaris)")
    clock = pygame.time.Clock()
    
    database.init_db()
    user = database.get_or_create_user(user_name, "🚀")
    
    font_hud = pygame.font.SysFont("Segoe UI", 16, bold=True)
    font_title = pygame.font.SysFont("Segoe UI", 28, bold=True)
    font_big = pygame.font.SysFont("Segoe UI", 36, bold=True)
    
    game_state = "START" # START, PHASE1_WAVES, PHASE2_BLACKHOLE, WIN, GAMEOVER
    
    ship_x, ship_y = 150.0, 320.0
    ship_speed = 5.0
    ship_hull = 100.0
    ship_fuel = 100.0
    boost_timer = 0
    
    beacons = []
    waves = []
    collected_beacons = 0
    earth_years = 0.0
    score = 0
    
    # Parâmetros de Gargantua
    bh_x, bh_y = 700.0, 320.0
    bh_radius = 65.0
    orbit_progress = 0.0
    
    running = True
    while running:
        dt = clock.tick(FPS)
        
        # ----------------------------------------------------
        # EVENTOS
        # ----------------------------------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if game_state == "START":
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        game_state = "PHASE1_WAVES"
                        ship_x, ship_y = 150.0, 320.0
                        ship_hull = 100.0
                        ship_fuel = 100.0
                        beacons.clear()
                        waves.clear()
                        collected_beacons = 0
                        earth_years = 0.0
                        orbit_progress = 0.0
                        score = 0
                        audio.play_sound("new_sol")
                elif game_state in ["PHASE1_WAVES", "PHASE2_BLACKHOLE"]:
                    if event.key == pygame.K_SPACE:
                        if ship_fuel >= 15.0 and boost_timer <= 0:
                            ship_fuel -= 15.0
                            boost_timer = 30
                            audio.play_sound("zap")
                elif game_state in ["WIN", "GAMEOVER"]:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN or event.key == pygame.K_r:
                        game_state = "PHASE1_WAVES"
                        ship_x, ship_y = 150.0, 320.0
                        ship_hull = 100.0
                        ship_fuel = 100.0
                        beacons.clear()
                        waves.clear()
                        collected_beacons = 0
                        earth_years = 0.0
                        orbit_progress = 0.0
                        score = 0
                        audio.play_sound("new_sol")

        # ----------------------------------------------------
        # ATUALIZAÇÃO DO MUNDO
        # ----------------------------------------------------
        if game_state in ["PHASE1_WAVES", "PHASE2_BLACKHOLE"]:
            earth_years += 0.03
            score += 1
            
            # Movimentação
            current_spd = ship_speed * 1.7 if boost_timer > 0 else ship_speed
            if boost_timer > 0: boost_timer -= 1
            ship_fuel = min(100.0, ship_fuel + 0.08)
            
            keys = pygame.key.get_pressed()
            if (keys[pygame.K_w] or keys[pygame.K_UP]) and ship_y > 40:
                ship_y -= current_spd
            if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and ship_y < HEIGHT - 50:
                ship_y += current_spd
            if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and ship_x > 50:
                ship_x -= current_spd
            if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and ship_x < WIDTH - 80:
                ship_x += current_spd

            # FASE 1: ONDAS DE MILLER
            if game_state == "PHASE1_WAVES":
                if random.random() < 0.035 and len(beacons) < 3:
                    beacons.append({"x": WIDTH + 20, "y": random.randint(70, HEIGHT - 90), "speed": 3.0})
                if random.random() < 0.045 and len(waves) < 4:
                    waves.append({"x": WIDTH + 40, "y": random.randint(60, HEIGHT - 80), "width": 45, "height": 160, "speed": 5.0})

                for i in range(len(beacons) - 1, -1, -1):
                    b = beacons[i]
                    b["x"] -= b["speed"]
                    if math.hypot(ship_x - b["x"], ship_y - b["y"]) < 32:
                        beacons.pop(i)
                        collected_beacons += 1
                        score += 200
                        audio.play_sound("harvest")
                        if collected_beacons >= 5:
                            game_state = "PHASE2_BLACKHOLE"
                            ship_x, ship_y = 120.0, 320.0
                            audio.play_sound("new_sol")
                    elif b["x"] < -30:
                        beacons.pop(i)

                for i in range(len(waves) - 1, -1, -1):
                    w = waves[i]
                    w["x"] -= w["speed"]
                    if ship_x > w["x"] - 20 and ship_x < w["x"] + w["width"] and ship_y > w["y"] - w["height"]//2 and ship_y < w["y"] + w["height"]//2:
                        waves.pop(i)
                        ship_hull -= 35
                        audio.play_sound("mine")
                        if ship_hull <= 0:
                            game_state = "GAMEOVER"
                    elif w["x"] < -80:
                        waves.pop(i)

            # FASE 2: GARGANTUA SLINGSHOT
            elif game_state == "PHASE2_BLACKHOLE":
                dx = bh_x - ship_x
                dy = bh_y - ship_y
                dist = math.hypot(dx, dy)
                
                if dist < bh_radius + 15:
                    game_state = "GAMEOVER"
                    audio.play_sound("mine")
                else:
                    # Puxão gravitacional F = G * M / r^2
                    grav = min(4.0, (1800.0 / (dist + 60)))
                    ship_x += (dx / dist) * grav
                    ship_y += (dy / dist) * grav
                    
                    # Zona de Órbita de Slingshot
                    if 120 < dist < 300:
                        orbit_progress += 0.35
                        score += 2
                        if orbit_progress >= 100.0:
                            game_state = "WIN"
                            audio.play_sound("new_sol")
                            database.add_xp(user["id"], 200)
                            database.unlock_badge(user["id"], "gargantua_slingshot")
                            database.unlock_badge(user["id"], "time_traveler")

        # ----------------------------------------------------
        # RENDERIZAÇÃO
        # ----------------------------------------------------
        if game_state == "PHASE1_WAVES":
            # Oceano de Miller
            screen.fill((15, 43, 72))
            for y in range(40, HEIGHT, 50):
                pygame.draw.line(screen, (56, 189, 248, 40), (0, y), (WIDTH, y), 2)
            for b in beacons:
                pygame.draw.rect(screen, (245, 158, 11), pygame.Rect(b["x"] - 14, b["y"] - 14, 28, 28), border_radius=5)
                lbl_b = font_hud.render("💾", True, (255, 255, 255))
                screen.blit(lbl_b, (int(b["x"] - 7), int(b["y"] - 11)))
            for w in waves:
                wave_surf = pygame.Surface((w["width"] * 2, w["height"]), pygame.SRCALPHA)
                pygame.draw.ellipse(wave_surf, (14, 116, 144, 220), pygame.Rect(0, 0, w["width"] * 2, w["height"]))
                pygame.draw.ellipse(wave_surf, (56, 189, 248), pygame.Rect(0, 0, w["width"] * 2, w["height"]), 3)
                screen.blit(wave_surf, (int(w["x"]), int(w["y"] - w["height"]//2)))

        elif game_state == "PHASE2_BLACKHOLE":
            # Espaço Profundo de Gargantua
            screen.fill((5, 7, 20))
            # Disco de Acreção Dourado
            pygame.draw.ellipse(screen, (251, 191, 36), pygame.Rect(bh_x - 220, bh_y - 65, 440, 130), 24)
            # Sombra do Buraco Negro
            pygame.draw.circle(screen, (0, 0, 0), (int(bh_x), int(bh_y)), int(bh_radius))
            pygame.draw.circle(screen, (255, 209, 102), (int(bh_x), int(bh_y)), int(bh_radius), 3)
            # Órbita Segura Pontilhada
            pygame.draw.circle(screen, (0, 212, 255), (int(bh_x), int(bh_y)), 190, 1)

        if game_state in ["PHASE1_WAVES", "PHASE2_BLACKHOLE"]:
            # Nave Ranger
            pts_ship = [
                (ship_x + 28, ship_y),
                (ship_x - 22, ship_y - 14),
                (ship_x - 12, ship_y),
                (ship_x - 22, ship_y + 14)
            ]
            pygame.draw.polygon(screen, (226, 232, 240), pts_ship)
            pygame.draw.polygon(screen, (192, 132, 252), pts_ship, 2)
            if boost_timer > 0:
                pygame.draw.circle(screen, (56, 189, 248), (int(ship_x - 24), int(ship_y)), random.randint(5, 8))

            # HUD
            hud_bg = pygame.Rect(20, 15, WIDTH - 40, 45)
            pygame.draw.rect(screen, (15, 23, 42), hud_bg, border_radius=8)
            pygame.draw.rect(screen, (192, 132, 252), hud_bg, 2, border_radius=8)
            
            if game_state == "PHASE1_WAVES":
                screen.blit(font_hud.render(f"💾 Balizas: {collected_beacons} / 5", True, (192, 132, 252)), (40, 28))
            else:
                screen.blit(font_hud.render(f"🕳️ Slingshot: {int(orbit_progress)}%", True, (192, 132, 252)), (40, 28))
            screen.blit(font_hud.render(f"⏳ Terra: {earth_years:.1f} Anos", True, (251, 191, 36)), (260, 28))
            screen.blit(font_hud.render(f"🛡️ Ranger: {int(ship_hull)}%", True, (56, 189, 248) if ship_hull > 30 else (248, 113, 113)), (480, 28))
            screen.blit(font_hud.render(f"⚡ Fuel: {int(ship_fuel)}%", True, (74, 222, 128)), (680, 28))

        # TELA DE START
        elif game_state == "START":
            screen.fill((5, 7, 20))
            t_title = font_big.render("⏳ INTERESTELAR: MANOBRA EM GARGANTUA", True, (192, 132, 252))
            screen.blit(t_title, ((WIDTH - t_title.get_width()) // 2, 140))
            
            txts = [
                "Resgate 5 balizas de dados nas ondas gigantes do Planeta Miller.",
                "Depois, realize a manobra de estilingue gravitacional em Gargantua sem cair na singularidade!",
                "",
                "🎮 [W, A, S, D] ou [Setas] para pilotar a nave Ranger",
                "⚡ [ESPAÇO] para acionar os Propulsores de Impulso",
                "",
                "Pressione [ESPAÇO] ou [ENTER] para Iniciar a Missão!"
            ]
            for idx, line in enumerate(txts):
                t_l = font_hud.render(line, True, (241, 245, 249) if idx < 5 else (192, 132, 252))
                screen.blit(t_l, ((WIDTH - t_l.get_width()) // 2, 230 + idx * 30))

        # TELA DE VITÓRIA
        elif game_state == "WIN":
            screen.fill((10, 25, 20))
            t_win = font_big.render("🎉 WORMHOLE ATINGIDO! DADOS QUÂNTICOS TRANSMITIDOS!", True, (74, 222, 128))
            screen.blit(t_win, ((WIDTH - t_win.get_width()) // 2, 160))
            
            t_tars = font_title.render("TARS: 'Manobra concluída com sucesso. A Terra está salva!'", True, (192, 132, 252))
            screen.blit(t_tars, ((WIDTH - t_tars.get_width()) // 2, 240))
            
            t_sc = font_hud.render(f"Pontuação: {score} pts | Anos transcorridos na Terra: {earth_years:.1f} anos (+200 XP salvos!)", True, (241, 245, 249))
            screen.blit(t_sc, ((WIDTH - t_sc.get_width()) // 2, 320))
            
            t_re = font_hud.render("Pressione [ESPAÇO] para Rejogar ou [ESC] para Sair", True, (56, 189, 248))
            screen.blit(t_re, ((WIDTH - t_re.get_width()) // 2, 420))

        # TELA DE GAME OVER
        elif game_state == "GAMEOVER":
            screen.fill((30, 10, 20))
            t_over = font_big.render("💥 A NAVE RANGER FOI DESTRUÍDA NA MISSÃO!", True, (244, 63, 94))
            screen.blit(t_over, ((WIDTH - t_over.get_width()) // 2, 180))
            
            t_sc = font_hud.render(f"Pontuação: {score} pts | Anos na Terra: {earth_years:.1f}", True, (241, 245, 249))
            screen.blit(t_sc, ((WIDTH - t_sc.get_width()) // 2, 270))
            
            t_re = font_hud.render("Pressione [ESPAÇO] para Tentar Novamente ou [ESC] para Sair", True, (192, 132, 252))
            screen.blit(t_re, ((WIDTH - t_re.get_width()) // 2, 360))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    run_interstellar()
