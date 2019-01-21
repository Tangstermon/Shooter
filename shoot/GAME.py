#import pygame_sdl2
#pygame_sdl2.import_as_pygame()
import pygame
import cProfile
from os import path
import random
import os


img_dir = path.join(path.dirname(__file__), "img")
sound_dir = path.join(path.dirname(__file__), "sound")

WINDOW_WIDTH = 1080
WINDOW_HEIGHT = 720
FPS = 60

WIDTH_THIRD = WINDOW_WIDTH /3
WIDTH_HALF = WINDOW_WIDTH/2
WIDTH_UPQUARTER = (WINDOW_WIDTH/4)*3
WIDTH_LOWQUARTER = WINDOW_WIDTH/4
WIDTH_EIGTH = WINDOW_WIDTH/8

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

MAX_ROCKS = 50
MAX_BOSS = 1
SHOOT_DELAY = 300

def draw_text(surf, text, size, x, y):
    font_name = pygame.font.match_font("arial")
    font = pygame.font.Font(font_name, size)
    text_surface =font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def highScore(file, curr_score, high_score):
    array = []
    if not os.path.isfile(file):
        f = open(file, 'w')
        f.write(str(0))
        f.close()
    else:    
        with open(file, 'r+') as ins: 
            for line in ins:
                array.append(line)
            if array:
                high_score = array[0]
        
            if curr_score >= int(high_score):
                high_score = curr_score
                ins.seek(0)
                ins.write(str(curr_score))
                ins.flush()
    return high_score

def start_again():
    all_sprites = pygame.sprite.Group()
    rockGroup_sprites = pygame.sprite.Group()
    bullet_sprites = pygame.sprite.Group()
    boss_group = pygame.sprite.Group()
    
    player = Player()
    for i in range(MAX_ROCKS):
        rock = Rock()
        rockGroup_sprites.add(rock)

    all_sprites.add(player)
    player.high_score = highScore("high_score.txt", player.score, player.high_score)
    player.score = 0
    player.health = 100

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(shipSprite, (70,50))
        #pygame.transform.rotate(self.image, 180)
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
                bullet1 = Bullet(self.rect.centerx -20, self.rect.top +10)
                bullet2 = Bullet(self.rect.centerx +20, self.rect.top+10)
                bullet_sprites.add(bullet1)
                bullet_sprites.add(bullet2)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
       
        if self.rect.right > WINDOW_WIDTH:
            self.rect.right = WINDOW_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom  > WINDOW_HEIGHT:
            self.rect.bottom =WINDOW_HEIGHT

   
class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #self.scale = random.uniform(0.6,1.5)
        self.image = random.choice(rock_list)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width /2)
        self.rect.centerx = random.randint(WIDTH_EIGTH,WIDTH_UPQUARTER + 100)
        self.rect.bottom = random.randint(-200,-40)
        self.speedy = random.randint(1,6)
        self.speedx = random.randint(-1,1)
        self.health = 3
        self.max_health = 0
        if self.image == rockSprite_sm:
            self.health = 1
            self.max_health = 1
        if self.image == rockSprite_m:
            self.health = 2
            self.max_health = 2
        if self.image == rockSprite_lg:
            self.health = 3
            self.max_health = 2

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx

        if self.rect.left > WINDOW_WIDTH:
            self.kill()
        if self.rect.right < 0:
            self.kill()
        if self.rect.top > WINDOW_HEIGHT:
            self.kill()
        

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.rotozoom(bulletSprite, 90, 0.1)
        self.image.set_colorkey(BLACK)
        
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = 6

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

class Boss(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bossSprite, (300,300))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width /2)
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WINDOW_WIDTH /2
        self.rect.bottom = -100
        #self.radius = int(self.rect.width /2)
        self.direction = random.randint(0,1)
        self.speedy = 3
        self.speedx = 4
        
        self.health = 15
        self.max_health = 15
        
        self.downleft = True
        self.downright = False
        self.upleft = False
        self.upright = False
        self.left = False
        self.right = False
        
    def update(self):
        
        if self.downleft:
            self.rect.y += self.speedy
            self.rect.x -= self.speedx
            
        if self.downright:
            self.rect.y += self.speedy
            self.rect.x += self.speedx
            
        if self.upleft:
            self.rect.y -= self.speedy
            self.rect.x -= self.speedx
            
            
        if self.upright:
            self.rect.y -= self.speedy
            self.rect.x += self.speedx
            
        if self.rect.top < 0:
            if self.upright:
                self.downright = True
                self.upright = False
            if self.upleft:
                self.downleft = True
                self.upleft = False
                
        if self.rect.bottom > WINDOW_HEIGHT:
            if self.downright:
                self.upright = True
                self.downright = False
            if self.downleft:
                self.upleft = True
                self.downleft = False
            
        if self.rect.right > WINDOW_WIDTH:
            if self.downright:
                self.downleft = True
                self.downright = False
            if self.upright:
                self.upleft = True
                self.upright = False
            
        if self.rect.left < 0:
            if self.downleft:
                self.downright = True
                self.downleft = False
            if self.upleft:
                self.upright = True
                self.upleft = False
           
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = explosion_anim[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.image.set_colorkey(BLACK)
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

class Power(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(healthSprite, (40,40))
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width /2)
        self.rect.center = center
        self.speed = 2

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > WINDOW_WIDTH:
            self.kill()


#set up
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
pygame.mixer.init()
mainClock = pygame.time.Clock()
surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Game")

#load sprites
shipSprite = pygame.image.load(path.join(img_dir, "space_ship.png")).convert()
rockSprite_m = pygame.image.load(path.join(img_dir, "Meteor.gif")).convert()
rockSprite_sm = pygame.image.load(path.join(img_dir, "Meteor_sm.gif")).convert()
rockSprite_lg = pygame.image.load(path.join(img_dir, "Meteor_lg.gif")).convert()
bulletSprite = pygame.image.load(path.join(img_dir, "redLaserRay.png")).convert()
bossSprite = pygame.image.load(path.join(img_dir, "boss.png")).convert_alpha()
healthSprite = pygame.image.load(path.join(img_dir, "health.png")).convert_alpha()
 
bgI = pygame.transform.scale(
pygame.image.load(path.join(img_dir, "bg.png")).convert(),
                            (WINDOW_WIDTH, WINDOW_HEIGHT))
bg_rect = bgI.get_rect()
x =0
y = 0
x1 = 0
y1 = -WINDOW_HEIGHT

explosion_anim = []

for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert_alpha()
    imgTr = pygame.transform.scale(img, (80,80))
    explosion_anim.append(imgTr)


#load sounds
laser_sound = pygame.mixer.Sound(path.join(sound_dir,"Laser_Shoot.wav"))
expl = pygame.mixer.Sound(path.join(sound_dir,"Explosion10.wav"))
music1 = pygame.mixer.music.load(path.join(sound_dir,"Desperate Strike.mp3"))

rock_list = [rockSprite_m, rockSprite_sm, rockSprite_lg]
counter  =0
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play()
loop = True
#pow_group = pygame.sprite.Group
while True:
    if loop:
        all_sprites = pygame.sprite.Group()
        rockGroup_sprites = pygame.sprite.Group()
        bullet_sprites = pygame.sprite.Group()
        boss_group = pygame.sprite.Group()
        pow_group = pygame.sprite.Group()
        
        player = Player()
        boss = Boss()
        
        for i in range(MAX_ROCKS):
            rock = Rock()
            rockGroup_sprites.add(rock)

        all_sprites.add(player)
       
        player.score = 0
        player.health = 100
        player.high_score = highScore("high_score.txt", player.score, player.high_score)
        loop = False
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    pygame.display.update()
   
    if len(rockGroup_sprites) < MAX_ROCKS:
        rockGroup_sprites.add(Rock())
       
    
    #Update
    all_sprites.update()
    rockGroup_sprites.update()

    if player.score > int(player.high_score):
        player.high_score = player.score

    rand = random.randint(1,500)
    if player.score >= 1000 and rand == 10 and len(boss_group) < MAX_BOSS:
        
        boss = Boss()
        boss_group.add(boss)
        all_sprites.add(boss)
   

    #power collide player
    pow_hits = pygame.sprite.spritecollide(player, pow_group, True)

    for p in pow_hits:
        player.health += 20
        if player.health > 100:
            player.health = 100
    
            
    #bullets hit rock
    bu_hits = pygame.sprite.groupcollide(rockGroup_sprites ,
                                      bullet_sprites, False, True)
    for hit in bu_hits:
        hit.health -= 1
        expl.play()
        player.score += 20 * hit.max_health
        if hit.health <= 0:
            explosion = Explosion(hit.rect.center) 
            all_sprites.add(explosion)
            hit.kill()
            player.score += 50
            if(random.randint(0,100) < 5):
                power = Power(hit.rect.center)
                all_sprites.add(power)
                pow_group.add(power)
            
            

    #player crashes into rock       
    pl_hits = pygame.sprite.spritecollide(player, rockGroup_sprites , True,
                                       pygame.sprite.collide_circle)
    for hit in pl_hits:
        player.health -= (hit.health *10)
        if player.health <=0:
            player.rect.top = -500
            highScore("high_score.txt", player.score, player.high_score)
            loop = True
    
    #bullets hit boss
    b1_hits = pygame.sprite.groupcollide(boss_group, bullet_sprites,False,
                                       True)
    for hit in b1_hits:
        hit.health -= 1
        expl.play()
        player.score += 20 * hit.max_health
        if hit.health <= 0:
            boss.kill()
            player.score += 50

    #player crashes into boss    
    p2_hits = pygame.sprite.spritecollide(player, boss_group , False,
                                       pygame.sprite.collide_circle)
    if p2_hits:
        player.health -= 1
        if player.health <=0:
            player.rect.top = -500
            highScore("high_score.txt", player.score, player.high_score)
            loop = True
       
    mainClock.tick(FPS)
    
    #Draw
    surface.fill(BLACK)
    
    y +=3
    y1 +=3
    surface.blit(bgI, (x,y))
    surface.blit(bgI, (x1,y1))
    
    if y > WINDOW_HEIGHT:
        y = -WINDOW_HEIGHT
    if y1 > WINDOW_HEIGHT:
        y1 = -WINDOW_HEIGHT
    
    all_sprites.draw(surface)
    rockGroup_sprites.draw(surface)   
    
    draw_text(surface, str(mainClock.get_fps()), 18, 550, 100)
    draw_text(surface, str(player.health), 18, 100, 100)
    draw_text(surface, str(player.score), 18, 300, 100)     
    draw_text(surface, str(player.high_score), 18, 300, 50)
   
    #flip
    pygame.display.update()

highScore("high_score.txt", player.score, player.high_score)
pygame.quit()
