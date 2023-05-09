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
    PLAYER_WALK = [pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha(),
                   pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()]
    PLAYER_JUMP = pygame.image.load('graphics/Player/jump.png').convert_alpha()

    def __init__(self, x=80, y=300):
        self.gravity = 0
        self.anim_index = 0
        self.current_anim = self.PLAYER_WALK[self.anim_index]
        self.rect = self.current_anim.get_rect(midbottom=(x, y))

    def animation(self):
        if self.rect.bottom < 300:
            self.current_anim = self.PLAYER_JUMP
        else:
            self.anim_index += 0.1
            if self.anim_index >= len(self.PLAYER_WALK):
                self.anim_index = 0
            self.current_anim = self.PLAYER_WALK[int(self.anim_index)]

    def draw(self):
        screen.blit(self.current_anim, self.rect)

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity

        if self.rect.bottom > 300:
            self.rect.bottom = 300


class Snail:
    SNAIL_FRAME = [pygame.image.load('graphics/snail/snail1.png').convert_alpha(),
                   pygame.image.load('graphics/snail/snail2.png').convert_alpha()]

    def __init__(self, x=900, y=300):
        self.anim_index = 0
        self.current_anim = self.SNAIL_FRAME[self.anim_index]
        self.rect = self.current_anim.get_rect(midbottom=(x, y))

    def draw(self):
        screen.blit(self.current_anim, self.rect)

    def animation(self):
        self.anim_index += 0.5
        if self.anim_index >= len(self.SNAIL_FRAME):
            self.anim_index = 0
        self.current_anim = self.SNAIL_FRAME[int(self.anim_index)]


class Fly:
    FLY_FRAME = [pygame.image.load('graphics/Fly/Fly1.png').convert_alpha(),
                 pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()]

    def __init__(self, x=900, y=200):
        self.anim_index = 0
        self.current_anim = self.FLY_FRAME[self.anim_index]
        self.rect = self.current_anim.get_rect(midbottom=(x, y))

    def draw(self):
        screen.blit(self.current_anim, self.rect)

    def animation(self):
        self.anim_index += 0.1
        if self.anim_index >= len(self.FLY_FRAME):
            self.anim_index = 0
        self.current_anim = self.FLY_FRAME[int(self.anim_index)]


class Game:
    SKY_SURFACE = pygame.image.load('graphics/Sky.png').convert()
    GROUND_SURFACE = pygame.image.load('graphics/ground.png').convert()

    def __init__(self):
        self.score = 0
        self.start_time = 0
        self.obstacles = []
        self.add_random_obstacle()
        self.player = Player()
        self.active = True

    def add_random_obstacle(self):
        x = random.randint(900, 1100)
        self.obstacles.append(random.choice([Fly(x), Snail(x), Snail(x), Snail(x)]))

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
        if game.obstacles:
            if self.obstacles[0].rect.right < 0: del self.obstacles[0]

            for obstacle in self.obstacles:
                obstacle.rect.x -= 8
                obstacle.animation()
                obstacle.draw()

                if obstacle.rect.colliderect(self.player.rect):
                    self.active = False
                    self.obstacles = []
                    self.player.rect.bottom = 300


obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1000)

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
                game.add_random_obstacle()
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game.start_time = int(pygame.time.get_ticks() / 100)
                game.active = True

    if game.active:
        game.draw_background()

        game.update_score()
        game.draw_score()

        game.player.animation()
        game.player.draw()

        game.player.apply_gravity()

        game.update_obstacles()
    else:
        game.draw_intro_screen()

    pygame.display.update()
    clock.tick(60)
