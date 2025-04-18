import pygame
import random
from os.path import join

SCREEN_WIDTH, SCREEN_HEIGHT = (1280, 720)

#initialize pygame and create display surface
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game")
running = True
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self, speed, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('images','player.png')).convert_alpha()
        self.rect = self.image.get_frect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        self.direction = pygame.Vector2(0,0)
        self.speed = speed

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt

        recent_keys = pygame.key.get_just_pressed()
        if (recent_keys[pygame.K_SPACE]):
            print("spacebar pressed")

class Star(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center=(random.randint(0, SCREEN_WIDTH),random.randint(0, SCREEN_HEIGHT)))

class Meteor(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center=(random.randint(0, SCREEN_WIDTH), -10))
        self.direction = pygame.Vector2(random.uniform(-1,1),1)
        self.speed = 100

    def update(self, dt):
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt

pygame.time.set_timer(pygame.USEREVENT, 1000)

#create sprite group
all_sprites = pygame.sprite.Group()

#create stars
star_surf = pygame.image.load(join('images','star.png')).convert_alpha()
for x in range(20):
    Star(all_sprites, star_surf)

#create meteors
meteor_surf = pygame.image.load(join('images', 'meteor.png')).convert_alpha()

#create player
player = Player(speed = 300, groups = all_sprites)

# laser_surf = pygame.image.load(join('5games','space shooter', 'images', 'laser.png')).convert_alpha()
# laser_rect = laser_surf.get_frect(bottomleft=(20, SCREEN_HEIGHT - 20))

#event loop
while running:
    dt = clock.tick() / 1000
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.USEREVENT:
            Meteor(all_sprites, meteor_surf)

    screen.fill("darkgray")

    all_sprites.draw(screen)
    all_sprites.update(dt)

    pygame.display.update()

pygame.quit()

#testing Git