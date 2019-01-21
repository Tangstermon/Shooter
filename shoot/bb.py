import pygame
from os import path 

img_dir = path.join(path.dirname(__file__), "img")

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
FPS = 60

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

pygame.init()
mainClock = pygame.time.Clock()
surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Game")

explosion_anim = []

for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    explosion_anim.append(img)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(shipSprite, (70,50))
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 /2)
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = (WINDOW_WIDTH/2)
        self.rect.bottom = WINDOW_HEIGHT - 20
        self.speed = 5
        self.shot = pygame.time.get_ticks()
        self.health = 100
        self.score = 0
        self.high_score = 0
    
    def update(self):
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.rect.x -= self.speed 
        if keystate[pygame.K_RIGHT]:
            self.rect.x += self.speed 
        if keystate[pygame.K_UP]:
            self.rect.y -= self.speed
        if keystate[pygame.K_DOWN]:
            self.rect.y += self.speed
        if keystate[pygame.K_SPACE]:
            now = pygame.time.get_ticks()
            if  now - self.shot > SHOOT_DELAY:
                laser_sound.play()
                self.shot = now
                bullet = Bullet(self.rect.centerx, self.rect.top +10)
                bullet_sprites.add(bullet)
                all_sprites.add(bullet)
       
        if self.rect.right > WINDOW_WIDTH:
            self.rect.right = WINDOW_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom  > WINDOW_HEIGHT:
            self.rect.bottom =WINDOW_HEIGHT

   

class Explosion(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = explosion_anim[0]
        self.rect = self.image.get_rect()
        #self.rect.center = center
        self.rect.centerx = 100
        self.rect.bottom = 400
        #self.image.set_colorkey(BLACK)
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 60
        self.speed = 3

    def update(self):
    
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim):
                self.kill()
            else:
                #center = self.rect.center
                self.image = explosion_anim[self.frame]
                self.rect = self.image.get_rect()
                #self.rect.center = center

all_sprites = pygame.sprite.Group()
shipSprite = pygame.image.load(path.join(img_dir, "space_ship.png")).convert()
player = Player()
all_sprites.add(player)


while True:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

    all_sprites.update()
    explosion = Explosion()
    all_sprites.add(explosion)
    surface.fill(BLACK)
    all_sprites.update() 
    all_sprites.draw(surface)
    pygame.display.update()
    surface.fill(BLACK)
