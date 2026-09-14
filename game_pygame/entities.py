"""
Astro-Valley - Entidades e Objetos do Jogo
Classes do Astronauta, Canteiros de Plantas, Painéis Solares, Reator e Robô.
"""

import pygame
import math

class Player:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.size = 28
        self.speed = 4.0
        self.direction = "down" # up, down, left, right
        self.anim_timer = 0
        self.is_moving = False
        
        # Recursos
        self.energy = 100.0
        self.oxygen = 100.0
        self.water = 60.0
        self.potatoes = 0
        self.ores = 0
        self.seeds = 10
        self.xp = 0

    def update(self, keys, bounds):
        self.is_moving = False
        dx, dy = 0, 0
        
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= self.speed
            self.direction = "up"
            self.is_moving = True
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += self.speed
            self.direction = "down"
            self.is_moving = True
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= self.speed
            self.direction = "left"
            self.is_moving = True
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += self.speed
            self.direction = "right"
            self.is_moving = True
            
        # Normalizar diagonal
        if dx != 0 and dy != 0:
            dx *= 0.7071
            dy *= 0.7071
            
        # Aplicar com limites do domo
        min_x, max_x, min_y, max_y = bounds
        self.x = max(min_x, min(max_x, self.x + dx))
        self.y = max(min_y, min(max_y, self.y + dy))
        
        if self.is_moving:
            self.anim_timer += 0.2
            self.energy = max(0.0, self.energy - 0.015)
        else:
            self.anim_timer = 0

    def draw(self, surface):
        px, py = int(self.x), int(self.y)
        bob = int(math.sin(self.anim_timer) * 2) if self.is_moving else 0
        
        # Sombra sob os pés
        shadow_rect = pygame.Rect(px - 10, py + 12, 20, 6)
        pygame.draw.ellipse(surface, (10, 15, 25, 120), shadow_rect)
        
        # Mochila de Suporte de Vida (Oxigênio)
        backpack_rect = pygame.Rect(px - 12, py - 10 + bob, 6, 18)
        if self.direction == "left":
            backpack_rect.x = px + 6
        elif self.direction == "up":
            backpack_rect = pygame.Rect(px - 9, py - 8 + bob, 18, 14)
        pygame.draw.rect(surface, (148, 163, 184), backpack_rect, border_radius=3)
        pygame.draw.rect(surface, (56, 189, 248), pygame.Rect(backpack_rect.x + 1, backpack_rect.y + 2, backpack_rect.width - 2, 3))
        
        # Corpo do Traje Espacial (Branco/Cinza Claro)
        body_rect = pygame.Rect(px - 9, py - 4 + bob, 18, 16)
        pygame.draw.rect(surface, (241, 245, 249), body_rect, border_radius=4)
        
        # Faixa Dourada/Azul no Traje
        pygame.draw.rect(surface, (0, 212, 255), pygame.Rect(px - 9, py + 2 + bob, 18, 3))
        
        # Pernas / Botas
        leg_offset = int(math.sin(self.anim_timer * 2) * 3) if self.is_moving else 0
        pygame.draw.rect(surface, (203, 213, 225), pygame.Rect(px - 8, py + 12 + leg_offset, 6, 6), border_radius=2)
        pygame.draw.rect(surface, (203, 213, 225), pygame.Rect(px + 2, py + 12 - leg_offset, 6, 6), border_radius=2)
        
        # Capacete
        helmet_rect = pygame.Rect(px - 10, py - 18 + bob, 20, 16)
        pygame.draw.rect(surface, (248, 250, 252), helmet_rect, border_radius=7)
        
        # Viseira Espelhada (Dourada ou Ciano reflexivo)
        visor_color = (251, 191, 36) if self.direction != "up" else (71, 85, 105)
        if self.direction == "down":
            visor_rect = pygame.Rect(px - 7, py - 14 + bob, 14, 8)
        elif self.direction == "left":
            visor_rect = pygame.Rect(px - 9, py - 14 + bob, 10, 8)
        elif self.direction == "right":
            visor_rect = pygame.Rect(px - 1, py - 14 + bob, 10, 8)
        else: # up
            visor_rect = pygame.Rect(px - 6, py - 16 + bob, 12, 5)
            
        pygame.draw.rect(surface, visor_color, visor_rect, border_radius=3)
        # Brilho de reflexo na viseira
        if self.direction != "up":
            pygame.draw.line(surface, (255, 255, 255), (visor_rect.x + 2, visor_rect.y + 2), (visor_rect.x + 5, visor_rect.y + 2), 1)


class CropPlot:
    def __init__(self, x, y, size=46):
        self.rect = pygame.Rect(x, y, size, size)
        self.state = "empty" # empty, tilled, seeded, growing, ready
        self.crop_type = "potato" # potato, carrot
        self.growth_progress = 0.0 # 0 a 100
        self.is_watered = False

    def update(self):
        if self.state == "growing":
            growth_rate = 0.18 if self.is_watered else 0.05
            self.growth_progress += growth_rate
            if self.growth_progress >= 100.0:
                self.state = "ready"
                self.growth_progress = 100.0

    def draw(self, surface):
        # Base da Terra
        dirt_color = (69, 26, 3) if not self.is_watered else (45, 18, 5)
        if self.state != "empty":
            dirt_color = (120, 53, 15) if not self.is_watered else (78, 32, 7)
            
        pygame.draw.rect(surface, dirt_color, self.rect, border_radius=6)
        pygame.draw.rect(surface, (34, 197, 94) if self.state == "ready" else (30, 41, 59), self.rect, 2, border_radius=6)
        
        cx, cy = self.rect.centerx, self.rect.centery
        
        if self.state == "tilled":
            # Sulcos arados
            for offset in [-10, 0, 10]:
                pygame.draw.line(surface, (180, 83, 9), (cx - 14, cy + offset), (cx + 14, cy + offset), 2)
        elif self.state == "seeded":
            # Sementes brilhantes
            pygame.draw.circle(surface, (253, 224, 71), (cx, cy), 4)
        elif self.state == "growing":
            # Broto em crescimento proporcional
            h = int((self.growth_progress / 100.0) * 22)
            pygame.draw.rect(surface, (74, 222, 128), pygame.Rect(cx - 3, cy + 12 - h, 6, h), border_radius=2)
            pygame.draw.circle(surface, (34, 197, 94), (cx - 6, cy + 12 - h), 5)
            pygame.draw.circle(surface, (34, 197, 94), (cx + 6, cy + 12 - h), 5)
        elif self.state == "ready":
            # Batata madura com folhas verdes e brilho dourado
            pygame.draw.circle(surface, (234, 179, 8), (cx, cy + 2), 10)
            pygame.draw.circle(surface, (34, 197, 94), (cx - 7, cy - 8), 6)
            pygame.draw.circle(surface, (34, 197, 94), (cx + 7, cy - 8), 6)
            pygame.draw.circle(surface, (74, 222, 128), (cx, cy - 11), 7)


class SolarArray:
    def __init__(self, x, y, width=100, height=60):
        self.rect = pygame.Rect(x, y, width, height)
        self.dust = 0.0 # 0 a 100% de poeira

    def update(self):
        # Acúmulo lento de poeira marciana
        self.dust = min(100.0, self.dust + 0.01)

    def draw(self, surface):
        # Suporte metálico
        pygame.draw.rect(surface, (71, 85, 105), pygame.Rect(self.rect.x + 10, self.rect.y + self.rect.height, self.rect.width - 20, 8))
        
        # Painel Solar Azul Fotovoltaico
        pygame.draw.rect(surface, (2, 132, 199), self.rect, border_radius=4)
        pygame.draw.rect(surface, (56, 189, 248), self.rect, 2, border_radius=4)
        
        # Grade fotovoltaica
        for i in range(1, 4):
            gx = self.rect.x + (self.rect.width * i // 4)
            pygame.draw.line(surface, (56, 189, 248), (gx, self.rect.y), (gx, self.rect.bottom), 1)
        gy = self.rect.centery
        pygame.draw.line(surface, (56, 189, 248), (self.rect.x, gy), (self.rect.right, gy), 1)
        
        # Camada de Poeira Vermelha
        if self.dust > 5.0:
            dust_surf = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            alpha = int((self.dust / 100.0) * 160)
            dust_surf.fill((180, 83, 9, alpha))
            surface.blit(dust_surf, (self.rect.x, self.rect.y))


class RoverBot:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.dir = 1
        self.speed = 1.0

    def update(self):
        self.x += self.speed * self.dir
        if self.x > 450: self.dir = -1
        if self.x < 320: self.dir = 1

    def draw(self, surface):
        rx, ry = int(self.x), int(self.y)
        
        # Rodas do Rover
        pygame.draw.circle(surface, (30, 41, 59), (rx - 10, ry + 8), 5)
        pygame.draw.circle(surface, (30, 41, 59), (rx, ry + 8), 5)
        pygame.draw.circle(surface, (30, 41, 59), (rx + 10, ry + 8), 5)
        
        # Chassi do Rover
        pygame.draw.rect(surface, (226, 232, 240), pygame.Rect(rx - 12, ry - 4, 24, 10), border_radius=3)
        
        # Mastro e Câmera SuperCam
        pygame.draw.line(surface, (148, 163, 184), (rx + 4 * self.dir, ry - 4), (rx + 4 * self.dir, ry - 14), 2)
        pygame.draw.rect(surface, (6, 214, 160), pygame.Rect(rx + 2 * self.dir, ry - 17, 6, 5), border_radius=1)
