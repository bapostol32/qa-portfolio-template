import pygame
import sys
import time

pygame.init()
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
screen1 = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
pygame.display.set_caption("Turn-based RPG - Window Test")
time_clock1 = pygame.time.Clock()
running = True

while running:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                            running = False
        screen1.fill(BLACK) # draws screen with a full black screen
        player_zone = pygame.draw.rect(screen1, RED, (50, 100, 200, 300), 2)
        enemy_zone = pygame.draw.rect(screen1, BLUE, (950, 100, 200, 300), 2)
        health_bars = pygame.draw.rect(screen1, GREEN, (650, 50, 150, 300), 2)
        pygame.display.flip() # produces draw on screen
        time_clock1.tick(60) # sets fps


pygame.quit()
sys.exit()