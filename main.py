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
text_rect = text_surface.get_rect(midtop=(400, 20))

snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surface.get_rect(midbottom=(600, 300))

player_surface = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
player_rect = player_surface.get_rect(midbottom=(80, 300))

clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(background_surface, (0, 0))
    screen.blit(ground_surface, (0, 300))
    screen.blit(text_surface, text_rect)
    screen.blit(snail_surface, snail_rect)
    snail_rect.x -= 7
    if snail_rect.right < 0:
        snail_rect.left = 800
    screen.blit(player_surface, player_rect)

    if snail_rect.colliderect(player_rect):
        print("bop")

    pygame.display.update()
    clock.tick(60)
