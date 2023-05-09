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


class Player(pygame.sprite.Sprite):
    PLAYER_WALK = [pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha(),
                   pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()]
    PLAYER_JUMP = pygame.image.load('graphics/Player/jump.png').convert_alpha()

    def __init__(self, x=80, y=300):
        super().__init__()
        self.gravity = 0
        self.anim_index = 0
        self.image = self.PLAYER_WALK[self.anim_index]
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.1)

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom == 300:
            self.jump()

    def jump(self):
        self.gravity = -20
        self.jump_sound.play()

    def animation(self):
        if self.rect.bottom < 300:
            self.image = self.PLAYER_JUMP
        else:
            self.anim_index += 0.1
            if self.anim_index >= len(self.PLAYER_WALK):
                self.anim_index = 0
            self.image = self.PLAYER_WALK[int(self.anim_index)]

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity

        if self.rect.bottom > 300:
            self.rect.bottom = 300

    def update(self):
        self.input()
        self.apply_gravity()
        self.animation()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, frames):
        super().__init__()
        self.frames = frames
        self.anim_index = 0
        self.image = self.frames[self.anim_index]
        self.rect = self.image.get_rect(midbottom=(x, y))

    def animation(self):
        self.anim_index += 0.5
        if self.anim_index >= len(self.frames):
            self.anim_index = 0
        self.image = self.frames[int(self.anim_index)]

    def update(self):
        self.animation()
        self.rect.x -= 8
        if self.rect.right < 0: self.kill()


class Snail(Obstacle):
    SNAIL_FRAMES = [pygame.image.load('graphics/snail/snail1.png').convert_alpha(),
                    pygame.image.load('graphics/snail/snail2.png').convert_alpha()]

    def __init__(self, x=900, y=300):
        super().__init__(x, y, self.SNAIL_FRAMES)


class Fly(Obstacle):
    FLY_FRAMES = [pygame.image.load('graphics/Fly/Fly1.png').convert_alpha(),
                  pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()]

    def __init__(self, x=900, y=200):
        super().__init__(x, y, self.FLY_FRAMES)


class Game:
    SKY_SURFACE = pygame.image.load('graphics/Sky.png').convert()
    GROUND_SURFACE = pygame.image.load('graphics/ground.png').convert()

    def __init__(self):
        self.score = 0
        self.start_time = 0
        self.obstacles = pygame.sprite.Group()
        self.add_random_obstacle()
        self.player = pygame.sprite.GroupSingle(Player())
        self.active = True
        pygame.mixer.music.load('audio/music.wav')
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)

    def add_random_obstacle(self):
        x = random.randint(900, 1100)
        self.obstacles.add(random.choice([Fly(x), Snail(x), Snail(x), Snail(x)]))

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

    def collision_check(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.obstacles, False):
            self.active = False
            self.obstacles.empty()
            self.player.sprite.rect.bottom = 300


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

        game.obstacles.draw(screen)
        game.obstacles.update()

        game.player.draw(screen)
        game.player.update()

        game.collision_check()
    else:
        game.draw_intro_screen()

    pygame.display.update()
    clock.tick(60)
