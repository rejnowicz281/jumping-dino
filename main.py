import pygame
from sys import exit

pygame.init()

screen = pygame.display.set_mode((800, 400))

start_time = 0


def display_score():
    current_time = int(pygame.time.get_ticks() / 100) - start_time
    score_surf = test_font.render(str(current_time), False, (64, 64, 64))
    score_rect = score_surf.get_rect(midtop=(400, 50))
    screen.blit(score_surf, score_rect)


pygame.display.set_caption("Jumping Dino")
test_font = pygame.font.Font('font/dogicapixelbold.ttf', 30)

background_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surface.get_rect(midbottom=(600, 300))

player_surface = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
player_rect = player_surface.get_rect(midbottom=(80, 300))
player_gravity = 0

clock = pygame.time.Clock()
game_active = True
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN and player_rect.bottom == 300:
                if player_rect.collidepoint(event.pos):
                    player_gravity = -20
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom == 300:
                    player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                snail_rect.centerx = 600
                start_time = int(pygame.time.get_ticks() / 100)
                game_active = True

    if game_active:
        screen.blit(background_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        display_score()

        # Snail
        screen.blit(snail_surface, snail_rect)
        snail_rect.x -= 7
        if snail_rect.right < 0:
            snail_rect.left = 800

        # Player
        screen.blit(player_surface, player_rect)
        player_gravity += 1
        player_rect.y += player_gravity

        if player_rect.bottom > 300:
            player_rect.bottom = 300

        # Collision
        if snail_rect.colliderect(player_rect):
            game_active = False
    else:
        screen.fill("red")

    pygame.display.update()
    clock.tick(60)
