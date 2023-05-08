import pygame
from sys import exit

import pygame.time

pygame.init()

screen = pygame.display.set_mode((800, 400))

pygame.display.set_caption("Jumping Dino")
test_font = pygame.font.Font('font/dogicapixelbold.ttf', 30)

background_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()
text_surface = test_font.render("Hey", False, 'Black')

snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_x = 600

clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(background_surface, (0, 0))
    screen.blit(ground_surface, (0, 300))
    screen.blit(text_surface, (300, 50))
    snail_x -= 5
    if snail_x < -100:
        snail_x = 800
    screen.blit(snail_surface, (snail_x, 265))

    pygame.display.update()
    clock.tick(60)
