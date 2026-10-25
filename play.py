import pygame
import sys
import random

pygame.init()

# Ventana
width, height = 700, 775
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ametralladora Espacial 🚀")

# Fuente
font = pygame.font.SysFont(None, 40)

# Cargar imagen del Jugador (Corazón)
player_image = pygame.image.load("C:/Users/GLEYDY/OneDrive/Documentos/DIBUJOS/corazon.png")
player_image = pygame.transform.scale(player_image, (35, 40))

# Jugador (Cuerpo principal de la máquina de guerra)
player_width, player_height = 70, 60
player_rect = pygame.Rect(width // 2 - player_width // 2, height - player_height - 10, player_width, player_height)
player_speed = 8

# Sistema de Ráfaga / Ametralladora
shoot_cooldown = 0
SHOOT_DELAY = 5  # Alta velocidad de disparo continuo

# Bolas de fuego (Balas)
bullets = []
bullet_speed = 15
bullet_radius = 6

# Enemigos (Bolitas grandes)
enemies = []
enemy_speed = 3
enemy_radius = 25

# Fondo Dinámico: Estrellas espaciales en movimiento
stars = []
for _ in range(60):
    stars.append({
        'x': random.randint(0, width),
        'y': random.randint(0, height),
        'speed': random.uniform(1, 3),
        'size': random.randint(1, 3)
    })

# Reloj
clock = pygame.time.Clock()

# Teclas
keys_pressed = {'left': False, 'right': False, 'space': False}

# Juego
score = 0
game_over = False

# Loop principal
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                keys_pressed['left'] = True
            elif event.key == pygame.K_RIGHT:
                keys_pressed['right'] = True
            elif event.key == pygame.K_SPACE:
                keys_pressed['space'] = True

            elif event.key == pygame.K_r and game_over:
                # Reiniciar
                bullets.clear()
                enemies.clear()
                score = 0
                game_over = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                keys_pressed['left'] = False
            elif event.key == pygame.K_RIGHT:
                keys_pressed['right'] = False
            elif event.key == pygame.K_SPACE:
                keys_pressed['space'] = False

    if not game_over:
        # Movimiento jugador
        if keys_pressed['left'] and player_rect.left > 0:
            player_rect.x -= player_speed

        if keys_pressed['right'] and player_rect.right < width:
            player_rect.x += player_speed

        # Actualizar estrellas del fondo (movimiento dinámico hacia abajo)
        for star in stars:
            star['y'] += star['speed']
            if star['y'] > height:
                star['y'] = 0
                star['x'] = random.randint(0, width)

        # Control del disparo continuo (Ametralladora)
        if shoot_cooldown > 0:
            shoot_cooldown -= 1

        if keys_pressed['space'] and shoot_cooldown == 0:
            bullet_rect = pygame.Rect(0, 0, bullet_radius * 2, bullet_radius * 2)
            
            # Desvío aleatorio en ráfaga
            offset_x = random.randint(-5, 5)
            bullet_rect.centerx = player_rect.centerx + offset_x
            bullet_rect.bottom = player_rect.top - 20
            
            bullets.append(bullet_rect)
            shoot_cooldown = SHOOT_DELAY

        # Movimiento de las balas de fuego
        for bullet in bullets[:]:
            bullet.y -= bullet_speed
            if bullet.bottom < 0:
                bullets.remove(bullet)

        # Crear enemigos (Bolitas grandes)
        if random.randint(1, 100) < 3:
            enemy_rect = pygame.Rect(0, 0, enemy_radius * 2, enemy_radius * 2)
            enemy_rect.x = random.randint(0, width - enemy_rect.width)
            enemy_rect.y = -enemy_rect.height
            enemies.append(enemy_rect)

        # Movimiento enemigos
        for enemy in enemies[:]:
            enemy.y += enemy_speed
            if enemy.top > height:
                enemies.remove(enemy)

        # Colisiones bala - enemigo
        for bullet in bullets[:]:
            for enemy in enemies[:]:
                if bullet.colliderect(enemy):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    score += 1
                    break

        # Colisión jugador con enemigos
        for enemy in enemies:
            if player_rect.colliderect(enemy):
                game_over = True

    # --- RENDERIZADO (DIBUJO) ---
    
    # 1. Fondo espacial oscuro (Azul noche muy profundo)
    screen.fill((10, 10, 25))

    # 2. Dibujar estrellas en movimiento (Efecto de velocidad)
    for star in stars:
        color = (200, 220, 255) if star['size'] > 1 else (100, 120, 160)
        pygame.draw.circle(screen, color, (int(star['x']), int(star['y'])), star['size'])

    # 3. Cañones dobles metálicos (Ametralladora militar)
    barrel_width = 8
    barrel_height = 25
    left_barrel = pygame.Rect(player_rect.centerx - 12, player_rect.top - barrel_height + 5, barrel_width, barrel_height)
    right_barrel = pygame.Rect(player_rect.centerx + 4, player_rect.top - barrel_height + 5, barrel_width, barrel_height)
    
    pygame.draw.rect(screen, (50, 50, 50), left_barrel)
    pygame.draw.rect(screen, (50, 50, 50), right_barrel)
    pygame.draw.rect(screen, (20, 20, 20), (left_barrel.x, left_barrel.y, barrel_width, 4))
    pygame.draw.rect(screen, (20, 20, 20), (right_barrel.x, right_barrel.y, barrel_width, 4))

    # 4. Oruga / Base del Tanque
    base_rect = pygame.Rect(player_rect.x, player_rect.bottom - 20, player_rect.width, 20)
    pygame.draw.rect(screen, (30, 30, 30), base_rect, border_radius=5)
    
    # 5. Torreta Blindada
    turret_rect = pygame.Rect(player_rect.x + 5, player_rect.y, player_rect.width - 10, player_rect.height - 10)
    pygame.draw.rect(screen, (60, 80, 50), turret_rect, border_radius=8)
    pygame.draw.rect(screen, (40, 60, 35), turret_rect, width=3, border_radius=8)

    # 6. Emblema del Corazón montado al centro
    screen.blit(player_image, (player_rect.centerx - 17, player_rect.centery - 18))

    # 7. Bolitas de fuego (Balas)
    for bullet in bullets:
        pygame.draw.circle(screen, (255, 140, 0), bullet.center, bullet_radius + 2)
        pygame.draw.circle(screen, (255, 69, 0), bullet.center, bullet_radius)
        pygame.draw.circle(screen, (255, 255, 0), bullet.center, bullet_radius // 2)

    # 8. Enemigos (Bolitas grandes)
    for enemy in enemies:
        pygame.draw.circle(screen, (70, 20, 20), enemy.center, enemy_radius + 2)
        pygame.draw.circle(screen, (160, 82, 45), enemy.center, enemy_radius)
        pygame.draw.circle(screen, (205, 133, 63), (enemy.centerx - 6, enemy.centery - 6), 6)

    # Puntaje
    score_text = font.render(f"Puntos: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Game Over
    if game_over:
        over_text = font.render("GAME OVER - Presiona R", True, (255, 0, 0))
        screen.blit(over_text, (width // 2 - 170, height // 2))

    pygame.display.flip()
    clock.tick(60)