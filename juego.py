import pygame
import sys
import random
import time

# Inicialización de Pygame
pygame.init()

# Dimensiones de la ventana del juego
WIDTH, HEIGHT = 400, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird Clone")

# Colores
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Cargar música de fondo
pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.set_volume(0.2)

# Reloj para controlar la velocidad del juego
clock = pygame.time.Clock()

# Animación del jugador
player_img = pygame.image.load("player.png")
player_img = pygame.transform.scale(player_img, (40, 40))  # Cambia las dimensiones a un cuadrado pequeño
player_rect = player_img.get_rect()
player_rect.topleft = (50, HEIGHT // 2)
player_velocity = 0

# Imagen de la explosión
explosion_img = pygame.image.load("explosion.png")
explosion_rect = explosion_img.get_rect()

# Variables de los obstáculos
obstacle_width = 60
obstacle_height = random.randint(100, 400)
obstacle_x = WIDTH
obstacle_y = random.randint(0, HEIGHT - obstacle_height)
obstacle_speed = 4

# Puntuación
score = 0
font = pygame.font.Font(None, 36)

# Tiempo transcurrido
start_time = time.time()

def draw_obstacle(x, y, width, height):
    pygame.draw.rect(SCREEN, GREEN, (x, y, width, height))

def game_over():
    pygame.mixer.music.stop()  # Detener la música
    SCREEN.fill(BLACK)  # Cambiar el fondo a negro
    explosion_rect.center = player_rect.center
    SCREEN.blit(explosion_img, explosion_rect)
    game_over_text = font.render("Game Over", True, RED)
    SCREEN.blit(game_over_text, (150, HEIGHT // 2))
    pygame.display.update()
    pygame.time.delay(2000)
    pygame.quit()
    sys.exit()

def main():
    global player_rect, player_velocity, obstacle_x, obstacle_width, obstacle_height, obstacle_y, score

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player_velocity = -10

        # Actualizar la posición del jugador
        player_rect.y += player_velocity
        player_velocity += 0.5

        # Actualizar la posición del obstáculo
        obstacle_x -= obstacle_speed

        # Dibujar los elementos del juego
        SCREEN.fill(BLACK)  # Cambiar el fondo a negro
        SCREEN.blit(player_img, player_rect)
        draw_obstacle(obstacle_x, obstacle_y, obstacle_width, obstacle_height)

        # Comprobar colisiones
        if player_rect.top <= 0 or player_rect.bottom >= HEIGHT:
            game_over()
        
        if obstacle_x <= 0:
            obstacle_x = WIDTH
            obstacle_height = random.randint(100, 400)
            obstacle_y = random.randint(0, HEIGHT - obstacle_height)
            score += 1

        if player_rect.colliderect(pygame.Rect(obstacle_x, obstacle_y, obstacle_width, obstacle_height)):
            game_over()

        # Mostrar la puntuación
        score_text = font.render(f"Score: {score}", True, WHITE)
        SCREEN.blit(score_text, (10, 10))

        # Mostrar el tiempo transcurrido
        current_time = int(time.time() - start_time)
        time_text = font.render(f"Time: {current_time} seconds", True, WHITE)
        SCREEN.blit(time_text, (10, 50))

        pygame.display.update()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    pygame.mixer.music.play(-1)  # Iniciar la música
    main()
