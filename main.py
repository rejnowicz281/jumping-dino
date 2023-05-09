import pygame
from sys import exit
import random

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
main_font = pygame.font.Font('font/dogicapixelbold.ttf', 30)
pygame.display.set_caption("Jumping Dino")


def draw_text(text, x, y, font=main_font, surface=screen):
    content = font.render(str(text), False, (64, 64, 64))
    content_rect = content.get_rect(center=(x, y))
    surface.blit(content, content_rect)


class Player:
    PLAYER_SURFACE = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()

    def __init__(self, x=80, y=300):
        self.gravity = 0
        self.rect = self.PLAYER_SURFACE.get_rect(midbottom=(x, y))

    def draw(self):
        screen.blit(self.PLAYER_SURFACE, self.rect)

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity

        if self.rect.bottom > 300:
            self.rect.bottom = 300


class Snail:
    SNAIL_SURFACE = pygame.image.load('graphics/snail/snail1.png').convert_alpha()

    def __init__(self, x=1000, y=300):
        self.rect = self.SNAIL_SURFACE.get_rect(midbottom=(x, y))

    def draw(self):
        screen.blit(self.SNAIL_SURFACE, self.rect)


class Fly:
    FLY_SURFACE = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()

    def __init__(self, x=1000, y=150):
        self.rect = self.FLY_SURFACE.get_rect(midbottom=(x, y))

    def draw(self):
        screen.blit(self.FLY_SURFACE, self.rect)


class Game:
    SKY_SURFACE = pygame.image.load('graphics/Sky.png').convert()
    GROUND_SURFACE = pygame.image.load('graphics/ground.png').convert()

    def __init__(self):
        self.score = 0
        self.start_time = 0
        self.obstacles = [Fly(), Snail(1300), Fly(1500), Fly(1700), Snail(2000)]
        self.player = Player()
        self.active = True

    def draw_intro_screen(self):
        screen.fill((100, 160, 192))

        top_text = "Jumping Dino" if self.score == 0 else f"Score: {self.score}"
        draw_text(top_text, SCREEN_WIDTH / 2, 50)

        player_stand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
        player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
        player_stand_rect = player_stand.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

        screen.blit(player_stand, player_stand_rect)

        draw_text("Press 'space' to JUMP", SCREEN_WIDTH / 2, 330)

    def draw_background(self):
        screen.blit(self.SKY_SURFACE, (0, 0))
        screen.blit(self.GROUND_SURFACE, (0, 300))

    def update_score(self):
        self.score = int(pygame.time.get_ticks() / 100) - self.start_time

    def draw_score(self):
        draw_text(str(self.score), 400, 50)

    def update_obstacles(self):
        for obstacle in self.obstacles:
            obstacle.rect.x -= 5
            obstacle.draw()

            if obstacle.rect.colliderect(self.player.rect):
                self.active = False


obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1700)

clock = pygame.time.Clock()
game = Game()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game.active:
            if event.type == pygame.MOUSEBUTTONDOWN and game.player.rect.bottom == 300:
                if game.player.rect.collidepoint(event.pos):
                    game.player.gravity = -20
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game.player.rect.bottom == 300:
                    game.player.gravity = -20
            if event.type == obstacle_timer:
                pass
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game.start_time = int(pygame.time.get_ticks() / 100)
                game.active = True

    if game.active:
        game.draw_background()

        game.update_score()
        game.draw_score()

        game.player.draw()

        game.player.apply_gravity()

        game.update_obstacles()
    else:
        game.draw_intro_screen()

    pygame.display.update()
    clock.tick(60)
