"""
Astro-Valley - Jogo Desktop 2D em Pygame
Simulador do Domo Marciano com Ciência, Agricultura, Energia e Exploração.
"""

import pygame
import sys
import os
import math
import random

# Adicionar pasta raiz ao path para acessar database.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import database
from game_pygame.entities import Player, CropPlot, SolarArray, RoverBot
import game_pygame.audio as audio

WIDTH, HEIGHT = 960, 640
FPS = 60

# Cores Cósmicas
COLOR_BG = (153, 61, 38)        # Poeira Vermelha de Marte
COLOR_DOME = (30, 41, 59)       # Piso Interno do Domo
COLOR_CYAN = (0, 212, 255)      # Estrutura de Vidro Geodésico
COLOR_PANEL = (15, 23, 42, 220) # HUD Transparente

def run_game(user_name="Cadete Estelar"):
    pygame.init()
    pygame.font.init()
    audio.init_audio()
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Astro-Valley — Simulador do Domo Marciano (Nova Stellaris)")
    clock = pygame.time.Clock()
    
    # Inicializar Banco de Dados
    database.init_db()
    user = database.get_or_create_user(user_name, "👩‍🚀")
    
    # Fontes
    font_hud = pygame.font.SysFont("Segoe UI", 16, bold=True)
    font_title = pygame.font.SysFont("Segoe UI", 22, bold=True)
    font_msg = pygame.font.SysFont("Segoe UI", 15, bold=True)
    
    # Estrelas no Céu de Marte
    stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT), random.choice([1, 2])) for _ in range(70)]
    
    # Entidades
    player = Player(480, 320)
    
    # 6 Canteiros de Plantio
    plots = [
        CropPlot(200, 200), CropPlot(260, 200), CropPlot(320, 200),
        CropPlot(200, 270), CropPlot(260, 270), CropPlot(320, 270)
    ]
    
    solar_array = SolarArray(700, 140, 140, 80)
    chem_lab_rect = pygame.Rect(700, 420, 130, 90)
    mine_rect = pygame.Rect(120, 450, 100, 100)
    science_terminal_rect = pygame.Rect(450, 140, 80, 60)
    rover = RoverBot(450, 280)
    
    # Estado da Simulação
    sol = 1
    time_of_day = 0.0 # 0 a 1000
    message_text = "Bem-vindo a Marte, Comandante! Use W,A,S,D para mover e ESPAÇO para interagir."
    message_timer = 300
    
    # Overlay de Pergunta Científica
    current_quiz = None
    quiz_feedback = ""
    quiz_feedback_timer = 0
    
    running = True
    while running:
        dt = clock.tick(FPS)
        
        # ----------------------------------------------------
        # 1. EVENTOS
        # ----------------------------------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if current_quiz:
                        current_quiz = None
                    else:
                        running = False
                        
                # Resposta de Quiz Científico (1, 2, 3, 4)
                if current_quiz:
                    if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                        chosen_idx = event.key - pygame.K_1
                        if chosen_idx == current_quiz["correct_idx"]:
                            audio.play_sound("harvest")
                            player.water = min(100.0, player.water + 30.0)
                            player.energy = min(100.0, player.energy + 30.0)
                            player.xp += 40
                            database.add_xp(user["id"], 40)
                            quiz_feedback = "✅ RESPOSTA CORRETA! +30L Água, +30% Energia, +40 XP!"
                        else:
                            audio.play_sound("mine")
                            player.xp += 10
                            database.add_xp(user["id"], 10)
                            quiz_feedback = "❌ Incorreta, mas você ganhou +10 XP pelo esforço!"
                        quiz_feedback_timer = 180
                        current_quiz = None
                    continue
                    
                # Ações de Teclado no Mundo
                if event.key == pygame.K_SPACE or event.key == pygame.K_e:
                    # Ação 1: Canteiros
                    action_done = False
                    for plot in plots:
                        if plot.rect.inflate(25, 25).collidepoint(player.x, player.y):
                            if plot.state == "empty":
                                plot.state = "tilled"
                                audio.play_sound("plant")
                                message_text = "🌱 Solo arado! Pressione ESPAÇO para semear batatas."
                            elif plot.state == "tilled":
                                if player.seeds > 0:
                                    player.seeds -= 1
                                    plot.state = "seeded"
                                    audio.play_sound("plant")
                                    message_text = "🥔 Sementes plantadas! Pressione ESPAÇO para irrigar com água."
                                else:
                                    message_text = "⚠️ Sem sementes! Colha plantas prontas para obter mais."
                            elif plot.state == "seeded":
                                if player.water >= 5.0:
                                    player.water -= 5.0
                                    plot.state = "growing"
                                    plot.is_watered = True
                                    audio.play_sound("water")
                                    message_text = "💧 Canteiro irrigado! As batatas começaram a crescer."
                                else:
                                    message_text = "⚠️ Falta água! Vá até o Reator Químico sintetizar mais."
                            elif plot.state == "ready":
                                plot.state = "empty"
                                plot.is_watered = False
                                plot.growth_progress = 0
                                player.potatoes += 3
                                player.seeds += 2
                                player.xp += 30
                                database.add_xp(user["id"], 30)
                                audio.play_sound("harvest")
                                message_text = "🎉 Colheita realizada com sucesso! +3 Batatas (+300 kcal), +30 XP!"
                                if player.potatoes >= 10:
                                    database.unlock_badge(user["id"], "astro_farmer")
                            action_done = True
                            message_timer = 200
                            break
                            
                    if action_done:
                        continue
                        
                    # Ação 2: Painel Solar
                    if solar_array.rect.inflate(30, 30).collidepoint(player.x, player.y):
                        if solar_array.dust > 10.0:
                            solar_array.dust = 0.0
                            player.energy = min(100.0, player.energy + 25.0)
                            player.xp += 25
                            database.add_xp(user["id"], 25)
                            audio.play_sound("zap")
                            message_text = "⚡ Poeira marciana limpa! Painéis operando com 100% de eficiência!"
                            database.unlock_badge(user["id"], "energy_pioneer")
                        else:
                            audio.play_sound("zap")
                            message_text = "⚡ Painéis solares fotovoltaicos limpos e gerando energia limpa."
                        message_timer = 200
                        continue
                        
                    # Ação 3: Reator Químico de Água (2H2 + O2)
                    if chem_lab_rect.inflate(30, 30).collidepoint(player.x, player.y):
                        if player.energy >= 15.0:
                            player.energy -= 15.0
                            player.water = min(100.0, player.water + 35.0)
                            player.xp += 25
                            database.add_xp(user["id"], 25)
                            audio.play_sound("water")
                            message_text = "🧪 Reação 2H₂ + O₂ ➔ 2H₂O concluída! +35 Litros de água sintetizados!"
                        else:
                            message_text = "⚠️ Energia insuficiente na rede para iniciar a eletrólise/combustão!"
                        message_timer = 200
                        continue
                        
                    # Ação 4: Mineração de Tubo de Lava
                    if mine_rect.inflate(30, 30).collidepoint(player.x, player.y):
                        if player.energy >= 12.0:
                            player.energy -= 12.0
                            player.ores += 2
                            player.xp += 30
                            database.add_xp(user["id"], 30)
                            audio.play_sound("mine")
                            message_text = "⛏️ Minérios de Ferro e Xenonite extraídos da caverna vulcânica! (+30 XP)"
                        else:
                            message_text = "⚠️ Traje sem energia para perfurar o basalto marciano!"
                        message_timer = 200
                        continue
                        
                    # Ação 5: Terminal Científico
                    if science_terminal_rect.inflate(30, 30).collidepoint(player.x, player.y):
                        q_list = database.get_quiz_questions(limit=1)
                        if q_list:
                            current_quiz = q_list[0]
                            audio.play_sound("zap")
                        continue

        # ----------------------------------------------------
        # 2. ATUALIZAÇÕES DO MUNDO
        # ----------------------------------------------------
        if not current_quiz:
            keys = pygame.key.get_pressed()
            player.update(keys, (160, 800, 120, 520))
            
            # Ciclo do Sol (Dia/Noite Marciano)
            time_of_day += 0.5
            if time_of_day >= 1000.0:
                time_of_day = 0.0
                sol += 1
                audio.play_sound("new_sol")
                message_text = f"🌅 Sol {sol} amanheceu em Marte! +50 XP pela sobrevivência."
                message_timer = 250
                player.xp += 50
                database.add_xp(user["id"], 50)
                if sol >= 10:
                    database.unlock_badge(user["id"], "sol_survivor")
                    
            # Geração Solar vs Consumo
            is_day = time_of_day < 700.0
            if is_day:
                solar_gain = 0.06 * (1.0 - solar_array.dust / 100.0)
                player.energy = min(100.0, player.energy + solar_gain)
            else:
                player.energy = max(0.0, player.energy - 0.02)
                
            solar_array.update()
            rover.update()
            
            for plot in plots:
                plot.update()
                
            if message_timer > 0:
                message_timer -= 1
            if quiz_feedback_timer > 0:
                quiz_feedback_timer -= 1

        # ----------------------------------------------------
        # 3. RENDERIZAÇÃO GRÁFICA
        # ----------------------------------------------------
        screen.fill(COLOR_BG)
        
        # Estrelas no Céu
        for sx, sy, sz in stars:
            pygame.draw.circle(screen, (255, 255, 255), (sx, sy), sz)
            
        # Grande Cúpula Geodésica do Domo
        dome_center = (480, 320)
        dome_radius = 360
        
        # Sombra externa
        pygame.draw.circle(screen, (20, 10, 15), dome_center, dome_radius + 6)
        # Piso interno
        pygame.draw.circle(screen, COLOR_DOME, dome_center, dome_radius)
        # Borda de vidro ciano iluminado
        pygame.draw.circle(screen, COLOR_CYAN, dome_center, dome_radius, 4)
        
        # Linhas de grade interna (vidro geodésico)
        for r in [120, 240]:
            pygame.draw.circle(screen, (0, 212, 255, 30), dome_center, r, 1)
            
        # Desenhar Canteiros
        for plot in plots:
            plot.draw(screen)
            
        # Desenhar Painel Solar
        solar_array.draw(screen)
        
        # Desenhar Reator Químico
        pygame.draw.rect(screen, (15, 118, 110), chem_lab_rect, border_radius=8)
        pygame.draw.rect(screen, (20, 184, 166), chem_lab_rect, 2, border_radius=8)
        label_chem = font_hud.render("Reator 2H₂+O₂", True, (204, 251, 241))
        screen.blit(label_chem, (chem_lab_rect.x + 8, chem_lab_rect.y + 10))
        # Frasco Químico desenhado
        pygame.draw.circle(screen, (45, 212, 191), (chem_lab_rect.centerx, chem_lab_rect.y + 55), 18)
        pygame.draw.rect(screen, (45, 212, 191), pygame.Rect(chem_lab_rect.centerx - 6, chem_lab_rect.y + 30, 12, 16))
        
        # Desenhar Mina de Tubo de Lava
        pygame.draw.circle(screen, (31, 41, 55), mine_rect.center, 45)
        pygame.draw.circle(screen, (245, 158, 11), mine_rect.center, 45, 3)
        pygame.draw.circle(screen, (10, 15, 25), mine_rect.center, 26)
        label_mine = font_hud.render("Tubo de Lava ⛏️", True, (253, 230, 138))
        screen.blit(label_mine, (mine_rect.x - 10, mine_rect.bottom + 5))
        
        # Desenhar Terminal Científico
        pygame.draw.rect(screen, (30, 27, 75), science_terminal_rect, border_radius=6)
        pygame.draw.rect(screen, (168, 85, 247), science_terminal_rect, 2, border_radius=6)
        label_term = font_hud.render("Terminal 🧠", True, (216, 180, 254))
        screen.blit(label_term, (science_terminal_rect.x - 4, science_terminal_rect.y - 20))
        # Tela piscante do terminal
        pygame.draw.rect(screen, (147, 51, 234), pygame.Rect(science_terminal_rect.x + 8, science_terminal_rect.y + 8, science_terminal_rect.width - 16, 24), border_radius=3)
        
        # Desenhar Robô Auxiliar
        rover.draw(screen)
        
        # Desenhar Jogador
        player.draw(screen)
        
        # Efeito de Noite Marciana (Tint Escuro Suave)
        if time_of_day >= 700.0:
            dark_alpha = int(((time_of_day - 700.0) / 300.0) * 150)
            night_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            night_surf.fill((10, 15, 35, dark_alpha))
            screen.blit(night_surf, (0, 0))
            
        # ----------------------------------------------------
        # 4. HUD E PAINEL SUPERIOR
        # ----------------------------------------------------
        hud_rect = pygame.Rect(20, 15, WIDTH - 40, 50)
        pygame.draw.rect(screen, (15, 23, 42), hud_rect, border_radius=10)
        pygame.draw.rect(screen, (0, 212, 255), hud_rect, 2, border_radius=10)
        
        txt_sol = font_hud.render(f"🪐 Sol: {sol}", True, (241, 245, 249))
        txt_nrg = font_hud.render(f"⚡ Energia: {int(player.energy)}%", True, (56, 189, 248) if player.energy > 20 else (248, 113, 113))
        txt_wat = font_hud.render(f"💧 Água: {int(player.water)}L", True, (34, 197, 94))
        txt_pot = font_hud.render(f"🥔 Batatas: {player.potatoes}", True, (251, 191, 36))
        txt_ore = font_hud.render(f"⛏️ Minérios: {player.ores}", True, (244, 114, 182))
        txt_xp = font_hud.render(f"⭐ XP: {player.xp}", True, (253, 224, 71))
        
        screen.blit(txt_sol, (40, 30))
        screen.blit(txt_nrg, (170, 30))
        screen.blit(txt_wat, (340, 30))
        screen.blit(txt_pot, (500, 30))
        screen.blit(txt_ore, (660, 30))
        screen.blit(txt_xp, (820, 30))
        
        # Banner de Notificação
        if message_timer > 0:
            msg_surf = font_msg.render(message_text, True, (241, 245, 249))
            msg_bg = pygame.Rect((WIDTH - msg_surf.get_width()) // 2 - 16, HEIGHT - 60, msg_surf.get_width() + 32, 34)
            pygame.draw.rect(screen, (15, 23, 42), msg_bg, border_radius=17)
            pygame.draw.rect(screen, (34, 197, 94), msg_bg, 2, border_radius=17)
            screen.blit(msg_surf, ((WIDTH - msg_surf.get_width()) // 2, HEIGHT - 53))
            
        if quiz_feedback_timer > 0:
            f_surf = font_title.render(quiz_feedback, True, (253, 224, 71))
            screen.blit(f_surf, ((WIDTH - f_surf.get_width()) // 2, HEIGHT // 2 - 80))
            
        # Overlay do Quiz Científico
        if current_quiz:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((5, 10, 20, 230))
            screen.blit(overlay, (0, 0))
            
            box = pygame.Rect(120, 100, WIDTH - 240, HEIGHT - 200)
            pygame.draw.rect(screen, (15, 23, 42), box, border_radius=16)
            pygame.draw.rect(screen, (168, 85, 247), box, 3, border_radius=16)
            
            q_title = font_title.render(f"🧠 Desafio Científico: {current_quiz['pillar']} ({current_quiz['category']})", True, (168, 85, 247))
            screen.blit(q_title, (box.x + 30, box.y + 25))
            
            # Enunciado da Pergunta
            q_txt = font_msg.render(current_quiz['question'][:85], True, (241, 245, 249))
            screen.blit(q_txt, (box.x + 30, box.y + 70))
            if len(current_quiz['question']) > 85:
                q_txt2 = font_msg.render(current_quiz['question'][85:170], True, (241, 245, 249))
                screen.blit(q_txt2, (box.x + 30, box.y + 95))
                
            # Opções (1, 2, 3, 4)
            for i, opt in enumerate(current_quiz['options']):
                opt_txt = font_hud.render(f"[{i+1}] {opt[:70]}", True, (253, 230, 138))
                screen.blit(opt_txt, (box.x + 40, box.y + 140 + (i * 45)))
                
            info_esc = font_hud.render("Pressione [1, 2, 3, 4] no teclado para responder ou [ESC] para fechar", True, (148, 163, 184))
            screen.blit(info_esc, (box.x + 30, box.bottom - 40))
            
        pygame.display.flip()
        
    pygame.quit()

if __name__ == "__main__":
    run_game()
