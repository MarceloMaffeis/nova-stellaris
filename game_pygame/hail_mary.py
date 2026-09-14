"""
Operação Hail Mary - Jogo Desktop 2D em Pygame
Pilote a nave Hail Mary ao lado de Rocky, colete Taumebas e salve Tau Ceti!
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

def run_hail_mary(user_name="Cadete Estelar"):
    pygame.init()
    pygame.font.init()
    audio.init_audio()
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Operação Hail Mary & Rocky — (Nova Stellaris)")
    clock = pygame.time.Clock()
    
    database.init_db()
    user = database.get_or_create_user(user_name, "🚀")
    
    font_hud = pygame.font.SysFont("Segoe UI", 16, bold=True)
    font_title = pygame.font.SysFont("Segoe UI", 28, bold=True)
    font_big = pygame.font.SysFont("Segoe UI", 36, bold=True)
    
    # Estado do Jogo
    game_state = "START" # START, PLAYING, WIN, GAMEOVER
    
    stars = [{"x": random.randint(0, WIDTH), "y": random.randint(0, HEIGHT), "speed": random.uniform(0.5, 2.5), "size": random.randint(1, 2)} for _ in range(90)]
    
    ship_x, ship_y = 150.0, 320.0
    ship_speed = 5.5
    ship_shields = 100.0
    
    rocky_x, rocky_y = 100.0, 360.0
    rocky_shield = 0
    
    taumoebas = []
    astrophages = []
    collected = 0
    score = 0
    
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
                        game_state = "PLAYING"
                        ship_x, ship_y = 150.0, 320.0
                        ship_shields = 100.0
                        taumoebas.clear()
                        astrophages.clear()
                        collected = 0
                        score = 0
                        audio.play_sound("new_sol")
                elif game_state == "PLAYING":
                    if event.key == pygame.K_SPACE:
                        if rocky_shield <= 0:
                            rocky_shield = 60
                            audio.play_sound("zap")
                elif game_state in ["WIN", "GAMEOVER"]:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN or event.key == pygame.K_r:
                        game_state = "PLAYING"
                        ship_x, ship_y = 150.0, 320.0
                        ship_shields = 100.0
                        taumoebas.clear()
                        astrophages.clear()
                        collected = 0
                        score = 0
                        audio.play_sound("new_sol")

        # ----------------------------------------------------
        # ATUALIZAÇÃO DO MUNDO
        # ----------------------------------------------------
        for s in stars:
            s["x"] -= s["speed"]
            if s["x"] < 0:
                s["x"] = WIDTH
                s["y"] = random.randint(0, HEIGHT)

        if game_state == "PLAYING":
            keys = pygame.key.get_pressed()
            if (keys[pygame.K_w] or keys[pygame.K_UP]) and ship_y > 40:
                ship_y -= ship_speed
            if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and ship_y < HEIGHT - 50:
                ship_y += ship_speed
            if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and ship_x > 50:
                ship_x -= ship_speed
            if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and ship_x < WIDTH - 80:
                ship_x += ship_speed

            # Rocky segue a nave
            rocky_x += (ship_x - 60 - rocky_x) * 0.08
            rocky_y += (ship_y + 35 - rocky_y) * 0.08
            if rocky_shield > 0:
                rocky_shield -= 1

            # Spawn de Taumebas e Astrofagos
            if random.random() < 0.035 and len(taumoebas) < 4:
                taumoebas.append({"x": WIDTH + 20, "y": random.randint(60, HEIGHT - 80), "speed": 3.0})
            if random.random() < 0.06 and len(astrophages) < 10:
                astrophages.append({"x": WIDTH + 30, "y": random.randint(50, HEIGHT - 70), "speed": random.uniform(4.0, 6.5), "size": random.randint(12, 22)})

            # Atualizar Taumebas
            for i in range(len(taumoebas) - 1, -1, -1):
                t = taumoebas[i]
                t["x"] -= t["speed"]
                if math.hypot(ship_x - t["x"], ship_y - t["y"]) < 32:
                    taumoebas.pop(i)
                    collected += 1
                    score += 150
                    audio.play_sound("harvest")
                    if collected >= 10:
                        game_state = "WIN"
                        audio.play_sound("new_sol")
                        database.add_xp(user["id"], 200)
                        database.unlock_badge(user["id"], "hail_mary_hero")
                        database.unlock_badge(user["id"], "rocky_friend")
                elif t["x"] < -30:
                    taumoebas.pop(i)

            # Atualizar Astrofagos
            for i in range(len(astrophages) - 1, -1, -1):
                a = astrophages[i]
                a["x"] -= a["speed"]
                # Destruído pelo escudo sônico de Rocky
                if rocky_shield > 0 and math.hypot(ship_x - a["x"], ship_y - a["y"]) < 110:
                    astrophages.pop(i)
                    score += 50
                    audio.play_sound("mine")
                    continue
                # Dano na nave
                if math.hypot(ship_x - a["x"], ship_y - a["y"]) < 28:
                    astrophages.pop(i)
                    ship_shields -= 20
                    audio.play_sound("mine")
                    if ship_shields <= 0:
                        game_state = "GAMEOVER"
                elif a["x"] < -40:
                    astrophages.pop(i)

            score += 1

        # ----------------------------------------------------
        # RENDERIZAÇÃO
        # ----------------------------------------------------
        screen.fill((5, 7, 20))
        
        # Estrelas
        for s in stars:
            pygame.draw.circle(screen, (255, 255, 255), (int(s["x"]), int(s["y"])), s["size"])

        if game_state == "PLAYING":
            # Escudo de Rocky
            if rocky_shield > 0:
                shield_alpha = int((rocky_shield / 60.0) * 120)
                shield_surf = pygame.Surface((220, 220), pygame.SRCALPHA)
                pygame.draw.circle(shield_surf, (255, 209, 102, shield_alpha), (110, 110), 100)
                pygame.draw.circle(shield_surf, (255, 209, 102, 220), (110, 110), 100, 3)
                screen.blit(shield_surf, (int(ship_x - 110), int(ship_y - 110)))

            # Nave de Rocky (Blip-A)
            pygame.draw.circle(screen, (100, 116, 139), (int(rocky_x), int(rocky_y)), 18)
            pygame.draw.circle(screen, (255, 209, 102), (int(rocky_x), int(rocky_y)), 18, 2)
            lbl_rocky = font_hud.render("Rocky 🤝", True, (253, 230, 138))
            screen.blit(lbl_rocky, (int(rocky_x - 22), int(rocky_y - 34)))

            # Nave Hail Mary
            pts_ship = [
                (ship_x + 30, ship_y),
                (ship_x - 24, ship_y - 16),
                (ship_x - 14, ship_y),
                (ship_x - 24, ship_y + 16)
            ]
            pygame.draw.polygon(screen, (241, 245, 249), pts_ship)
            pygame.draw.polygon(screen, (0, 212, 255), pts_ship, 2)
            # Propulsor
            pygame.draw.circle(screen, (249, 115, 22), (int(ship_x - 22), int(ship_y)), random.randint(4, 7))

            # Taumebas
            for t in taumoebas:
                pygame.draw.circle(screen, (74, 222, 128), (int(t["x"]), int(t["y"])), 14)
                pygame.draw.circle(screen, (255, 255, 255), (int(t["x"]), int(t["y"])), 14, 2)
                lbl_t = font_hud.render("🦠", True, (255, 255, 255))
                screen.blit(lbl_t, (int(t["x"] - 7), int(t["y"] - 11)))

            # Astrofagos
            for a in astrophages:
                pygame.draw.circle(screen, (239, 68, 68), (int(a["x"]), int(a["y"])), a["size"])
                pygame.draw.circle(screen, (252, 165, 165), (int(a["x"]), int(a["y"])), a["size"], 2)

            # HUD
            hud_bg = pygame.Rect(20, 15, WIDTH - 40, 45)
            pygame.draw.rect(screen, (15, 23, 42), hud_bg, border_radius=8)
            pygame.draw.rect(screen, (255, 209, 102), hud_bg, 2, border_radius=8)
            
            screen.blit(font_hud.render(f"🦠 Taumebas: {collected} / 10", True, (74, 222, 128)), (40, 28))
            screen.blit(font_hud.render(f"🛡️ Escudos: {int(ship_shields)}%", True, (56, 189, 248) if ship_shields > 30 else (248, 113, 113)), (260, 28))
            screen.blit(font_hud.render(f"⭐ Pontos: {score}", True, (253, 224, 71)), (500, 28))
            screen.blit(font_hud.render("🎶 [ESPAÇO] Escudo Sônico de Rocky", True, (255, 209, 102) if rocky_shield <= 0 else (74, 222, 128)), (680, 28))

        # TELA DE START
        elif game_state == "START":
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((5, 10, 25, 230))
            screen.blit(overlay, (0, 0))
            
            t_title = font_big.render("✨ OPERAÇÃO HAIL MARY: RESGATE DE TAU CETI", True, (255, 209, 102))
            screen.blit(t_title, ((WIDTH - t_title.get_width()) // 2, 140))
            
            txts = [
                "O Sol está morrendo devido aos Astrofagos que consomem sua radiação.",
                "Junto com o alienígena Rocky, pilote a Hail Mary e colete 10 Taumebas para salvar a Terra!",
                "",
                "🎮 [W, A, S, D] ou [Setas] para pilotar a nave",
                "🛡️ [ESPAÇO] para ativar o Escudo Sônico de Rocky e vaporizar Astrofagos",
                "",
                "Pressione [ESPAÇO] ou [ENTER] para Iniciar a Missão!"
            ]
            for idx, line in enumerate(txts):
                t_l = font_hud.render(line, True, (241, 245, 249) if idx < 5 else (74, 222, 128))
                screen.blit(t_l, ((WIDTH - t_l.get_width()) // 2, 230 + idx * 30))

        # TELA DE VITÓRIA
        elif game_state == "WIN":
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((10, 30, 20, 240))
            screen.blit(overlay, (0, 0))
            
            t_win = font_big.render("🎉 MISSÃO CUMPRIDA! TAU CETI E A TERRA SALVAS!", True, (74, 222, 128))
            screen.blit(t_win, ((WIDTH - t_win.get_width()) // 2, 160))
            
            t_rocky = font_title.render("Rocky comemora: 'Amigo bom! Fist my bump! 👊'", True, (255, 209, 102))
            screen.blit(t_rocky, ((WIDTH - t_rocky.get_width()) // 2, 240))
            
            t_sc = font_hud.render(f"Pontuação Final: {score} pontos (+200 XP salvos no perfil!)", True, (241, 245, 249))
            screen.blit(t_sc, ((WIDTH - t_sc.get_width()) // 2, 320))
            
            t_re = font_hud.render("Pressione [ESPAÇO] para Jogar Novamente ou [ESC] para Sair", True, (56, 189, 248))
            screen.blit(t_re, ((WIDTH - t_re.get_width()) // 2, 420))

        # TELA DE GAME OVER
        elif game_state == "GAMEOVER":
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((40, 10, 20, 240))
            screen.blit(overlay, (0, 0))
            
            t_over = font_big.render("💥 O CASCO DA HAIL MARY FOI SUPERAQUECIDO!", True, (244, 63, 94))
            screen.blit(t_over, ((WIDTH - t_over.get_width()) // 2, 180))
            
            t_sc = font_hud.render(f"Pontuação: {score} pontos", True, (241, 245, 249))
            screen.blit(t_sc, ((WIDTH - t_sc.get_width()) // 2, 270))
            
            t_re = font_hud.render("Pressione [ESPAÇO] para Reiniciar a Missão ou [ESC] para Sair", True, (255, 209, 102))
            screen.blit(t_re, ((WIDTH - t_re.get_width()) // 2, 360))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    run_hail_mary()
