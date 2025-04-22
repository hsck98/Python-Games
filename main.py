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
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown = 400

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if (current_time - self.laser_shoot_time >= self.cooldown):
                self.can_shoot = True

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt

        #check event for space and shoot laser/ set delay of 3sec
        recent_keys = pygame.key.get_just_pressed()
        if (recent_keys[pygame.K_SPACE] and self.can_shoot):
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()
            Laser(groups = (all_sprites, laser_sprites), surf = laser_surf, pos = player.rect.midtop)
            laser_audio.play()

        self.laser_timer()

class Star(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center=(random.randint(0, SCREEN_WIDTH),random.randint(0, SCREEN_HEIGHT)))

class Meteor(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.original_surf = surf
        self.image = self.original_surf
        self.rect = self.image.get_frect(center=(random.randint(0, SCREEN_WIDTH), -10))
        self.direction = pygame.Vector2(random.uniform(-0.5, 0.5),1)
        self.speed = random.randint(300, 400)
        self.rotation = 0
        self.rotation_speed = random.randint(-360, 360)
        self.scale = random.uniform(0.5, 1.5)

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        
        if self.rect.top > SCREEN_HEIGHT or self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

        self.rotation += self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(self.original_surf, self.rotation, self.scale)
        self.rect = self.image.get_frect(center = self.rect.center)

class Laser(pygame.sprite.Sprite):
    def __init__(self, groups, surf, pos):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom=pos)

    def update(self, dt):
        self.rect.centery += -400 * dt
        if self.rect.bottom < 0:
            self.kill()

class AnimatedExplosion(pygame.sprite.Sprite):
    def __init__(self, frames, pos, groups):
        super().__init__(groups)
        self.frames = frames
        self.frame_index = 0
        self.image = frames[self.frame_index]
        self.rect = self.image.get_frect(center=pos)

    def update(self, dt):
        self.frame_index += 20 * dt
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)]
        else:
            self.kill()
        
def collisions():
    global running

    if pygame.sprite.spritecollide(player, meteor_sprites, True, pygame.sprite.collide_mask):
        running = False

    for laser in laser_sprites:
        collision_points = pygame.sprite.spritecollide(laser, meteor_sprites, True)
        if (collision_points):
            laser.kill()
            AnimatedExplosion(explosion_frames, laser.rect.midtop, all_sprites)
            explosion_audio.play()

def display_score():
    current_time = int(pygame.time.get_ticks()/100)
    score_surf = font.render(str(current_time), True, (240,240,240))
    score_rect =  score_surf.get_frect(center=(SCREEN_WIDTH / 2, 100))
    screen.blit(score_surf, score_rect)

    pygame.draw.rect(screen, (240,240,240), score_rect.inflate(30,20).move(0, -7), 1, 10)

meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)

#import
meteor_surf = pygame.image.load(join('images', 'meteor.png')).convert_alpha()
laser_surf = pygame.image.load(join('images', 'laser.png')).convert_alpha()
star_surf = pygame.image.load(join('images','star.png')).convert_alpha()
font = pygame.font.Font(join('images', 'Oxanium-Bold.ttf'), 40)
explosion_frames = [pygame.image.load(join('images', 'explosion', f'{n}.png')).convert_alpha() for n in range(21)]

laser_audio = pygame.mixer.Sound(join('audio', 'laser.wav'))
explosion_audio = pygame.mixer.Sound(join('audio', 'explosion.wav'))
game_music_audio = pygame.mixer.Sound(join('audio', 'game_music.wav'))
game_music_audio.play(loops = -1)

laser_audio.set_volume(0.01)
explosion_audio.set_volume(0.01)
game_music_audio.set_volume(0.01)

#create sprite group
all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()

#get star positions
for x in range(20):
    Star(groups = all_sprites, surf = star_surf)

#create player
player = Player(speed = 500, groups = all_sprites)

#event loop
while running:
    dt = clock.tick() / 1000
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == meteor_event:
            Meteor(groups = (all_sprites, meteor_sprites), surf = meteor_surf)


    all_sprites.update(dt)
    collisions()

    screen.fill('#3a2e3f')
    all_sprites.draw(screen)
    display_score()
    pygame.display.update()

pygame.quit()

#testing Git
