import random
import math
import pygame

# Jogo autoral para a atividade de Linguagem de Programação Aplicada.
# Tema: Estação Orbital — sobreviva aos drones até o resgate chegar.

pygame.init()
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Estacao Orbital")
clock = pygame.time.Clock()

FONT = pygame.font.SysFont("arial", 24)
SMALL = pygame.font.SysFont("arial", 18)
TITLE = pygame.font.SysFont("arial", 52, bold=True)
BIG = pygame.font.SysFont("arial", 36, bold=True)

BG = (10, 16, 35)
WHITE = (240, 245, 255)
CYAN = (70, 220, 245)
BLUE = (50, 105, 220)
RED = (245, 75, 90)
YELLOW = (255, 220, 80)
GREEN = (85, 230, 145)
GRAY = (115, 130, 160)

# Estrelas decorativas criadas pelo próprio código (sem assets externos).
stars = [(random.randrange(WIDTH), random.randrange(HEIGHT),
          random.choice([1, 1, 2])) for _ in range(100)]

def draw_background():
    screen.fill(BG)
    for x, y, radius in stars:
        pygame.draw.circle(screen, (100, 125, 175), (x, y), radius)
    pygame.draw.rect(screen, (19, 29, 58), (0, HEIGHT - 38, WIDTH, 38))

def draw_text(text, font, color, center):
    image = font.render(text, True, color)
    rect = image.get_rect(center=center)
    screen.blit(image, rect)

def draw_player(rect):
    # Nave triangular feita com formas geométricas.
    points = [(rect.centerx, rect.top), (rect.left, rect.bottom),
              (rect.centerx, rect.bottom - 10), (rect.right, rect.bottom)]
    pygame.draw.polygon(screen, CYAN, points)
    pygame.draw.polygon(screen, WHITE, points, 2)
    pygame.draw.circle(screen, YELLOW, (rect.centerx, rect.centery + 5), 5)

def reset_game():
    player = pygame.Rect(WIDTH // 2 - 18, HEIGHT - 100, 36, 42)
    return {
        "player": player,
        "enemies": [],
        "shots": [],
        "score": 0,
        "health": 3,
        "spawn_timer": 0,
        "shot_timer": 0,
        "start_ticks": pygame.time.get_ticks(),
        "invulnerable": 0,
    }

def draw_button(text, rect, color):
    pygame.draw.rect(screen, color, rect, border_radius=10)
    pygame.draw.rect(screen, WHITE, rect, 2, border_radius=10)
    draw_text(text, FONT, WHITE, rect.center)

def draw_menu():
    draw_background()
    draw_text("ESTACAO ORBITAL", TITLE, CYAN, (WIDTH // 2, 115))
    draw_text("Proteja a nave ate a equipe de resgate chegar!", FONT, WHITE,
              (WIDTH // 2, 170))
    panel = pygame.Rect(205, 215, 490, 190)
    pygame.draw.rect(screen, (22, 36, 70), panel, border_radius=14)
    pygame.draw.rect(screen, BLUE, panel, 2, border_radius=14)
    draw_text("CONTROLES", BIG, YELLOW, (WIDTH // 2, 246))
    draw_text("A / D ou setas: mover a nave", FONT, WHITE, (WIDTH // 2, 286))
    draw_text("ESPACO: disparar", FONT, WHITE, (WIDTH // 2, 322))
    draw_text("Sobreviva por 45 segundos para vencer.", SMALL, GREEN,
              (WIDTH // 2, 365))
    draw_button("JOGAR", pygame.Rect(335, 435, 230, 58), (30, 125, 100))
    draw_text("ESC: sair", SMALL, GRAY, (WIDTH // 2, 525))

def draw_game(game, elapsed):
    draw_background()
    p = game["player"]
    draw_player(p)
    for item in game["enemies"]:
        enemy = item["rect"]
        pygame.draw.circle(screen, RED, enemy.center, enemy.width // 2)
        pygame.draw.circle(screen, (255, 170, 175), enemy.center, enemy.width // 2, 2)
        pygame.draw.line(screen, WHITE, (enemy.left + 7, enemy.centery),
                         (enemy.right - 7, enemy.centery), 2)
    for shot in game["shots"]:
        pygame.draw.rect(screen, YELLOW, shot, border_radius=3)
    pygame.draw.rect(screen, (24, 35, 65), (12, 12, 250, 78), border_radius=8)
    pygame.draw.rect(screen, BLUE, (12, 12, 250, 78), 2, border_radius=8)
    draw_text(f"VIDAS: {game['health']}", FONT, WHITE, (92, 38))
    draw_text(f"PONTOS: {game['score']}", SMALL, YELLOW, (100, 68))
    draw_text(f"RESGATE: {max(0, 45 - int(elapsed))} s", FONT, CYAN,
              (WIDTH - 125, 36))
    draw_text("Desvie dos drones e atire!", SMALL, WHITE, (WIDTH - 145, 68))

def end_screen(won, score):
    draw_background()
    title = "RESGATE CONCLUIDO!" if won else "NAVE DESTRUIDA"
    color = GREEN if won else RED
    draw_text(title, TITLE, color, (WIDTH // 2, 190))
    message = "Voce sobreviveu ate a chegada da equipe." if won else "Os drones venceram desta vez."
    draw_text(message, FONT, WHITE, (WIDTH // 2, 255))
    draw_text(f"Pontuacao final: {score}", BIG, YELLOW, (WIDTH // 2, 315))
    draw_button("JOGAR NOVAMENTE", pygame.Rect(280, 390, 340, 58), (30, 95, 145))
    draw_text("ENTER: jogar novamente  |  ESC: sair", SMALL, GRAY, (WIDTH // 2, 485))

MENU, PLAYING, END = "menu", "playing", "end"
state = MENU
game = None
won = False
running = True

while running:
    dt = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if state == MENU and event.key in (pygame.K_RETURN, pygame.K_SPACE):
                game = reset_game()
                state = PLAYING
            elif state == END and event.key == pygame.K_RETURN:
                game = reset_game()
                state = PLAYING
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if state == MENU and pygame.Rect(335, 435, 230, 58).collidepoint(event.pos):
                game = reset_game()
                state = PLAYING
            elif state == END and pygame.Rect(280, 390, 340, 58).collidepoint(event.pos):
                game = reset_game()
                state = PLAYING

    if state == MENU:
        draw_menu()
    elif state == PLAYING:
        keys = pygame.key.get_pressed()
        p = game["player"]
        speed = 330
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            p.x -= int(speed * dt)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            p.x += int(speed * dt)
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            p.y -= int(speed * dt)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            p.y += int(speed * dt)
        p.clamp_ip(pygame.Rect(12, 100, WIDTH - 24, HEIGHT - 145))

        game["shot_timer"] -= dt
        if keys[pygame.K_SPACE] and game["shot_timer"] <= 0:
            game["shots"].append(pygame.Rect(p.centerx - 3, p.top - 13, 6, 16))
            game["shot_timer"] = 0.22

        game["spawn_timer"] -= dt
        if game["spawn_timer"] <= 0:
            size = random.randint(25, 39)
            x = random.randint(20, WIDTH - size - 20)
            enemy = {"rect": pygame.Rect(x, -size, size, size),
                     "speed": random.randint(125, 225)}
            game["enemies"].append(enemy)
            game["spawn_timer"] = max(0.28, 0.8 - game["score"] * 0.008)

        for shot in game["shots"][:]:
            shot.y -= int(480 * dt)
            if shot.bottom < 0:
                game["shots"].remove(shot)

        for item in game["enemies"][:]:
            enemy = item["rect"]
            enemy.y += int(item["speed"] * dt)
            if enemy.top > HEIGHT:
                game["enemies"].remove(item)
                continue
            hit_shot = next((shot for shot in game["shots"] if enemy.colliderect(shot)), None)
            if hit_shot:
                if hit_shot in game["shots"]:
                    game["shots"].remove(hit_shot)
                if item in game["enemies"]:
                    game["enemies"].remove(item)
                game["score"] += 10
                continue
            if enemy.colliderect(p):
                game["enemies"].remove(item)
                if game["invulnerable"] <= 0:
                    game["health"] -= 1
                    game["invulnerable"] = 1.0

        game["invulnerable"] = max(0, game["invulnerable"] - dt)
        elapsed = (pygame.time.get_ticks() - game["start_ticks"]) / 1000
        draw_game(game, elapsed)
        if game["health"] <= 0:
            won = False
            state = END
        elif elapsed >= 45:
            won = True
            state = END
    else:
        draw_background()
        end_screen(won, game["score"])

    pygame.display.flip()

pygame.quit()
