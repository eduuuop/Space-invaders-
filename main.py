import pygame
from pygame import mixer
from pygame.locals import *
import random


pygame.mixer.pre_init(44100 , -16, 2, 512)
mixer.init()
pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_widht= 600
screen_height = 800

screen = pygame.display.set_mode((screen_widht,screen_height))
pygame.display.set_caption('Space Invaders')

font30 = pygame.font.SysFont('Constantia', 30)
font40 = pygame.font.SysFont('Constantia', 40)

Explosion_fx = pygame.mixer.Sound("img/explosion.wav")
Explosion_fx.set_volume(0.25)

Explosion2_fx = pygame.mixer.Sound("img/explosion.wav") 
Explosion2_fx.set_volume(0.25)

laser_fx = pygame.mixer.Sound("img/laser.wav")
laser_fx.set_volume(0.25)

rows = 5
cols = 5

alien_cooldown = 1000
last_alien_shot = pygame.time.get_ticks()
countdown = 3
last_count = pygame.time.get_ticks()
game_over = 0

red = (255, 0, 0)
green = (0,255, 0)
white = ( 255 , 255 , 255 )

bg = pygame.image.load("123.jpg")

def draw_bg():
    screen.blit(bg, (0,0))

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))


class Spaceship(pygame.sprite.Sprite):
    def __init__(self,x,y,health):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/spaceship.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.health_start = health
        self.health_remaining = health
        self.last_shoot = pygame.time.get_ticks()

    def update(self):
        speed = 4
        cooldown = 676

        result = 0

        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
             self.rect.x -= speed 
        if key[pygame.K_RIGHT] and self.rect.right < screen_widht:
             self.rect.x += speed

        time_now = pygame.time.get_ticks()

        if key[pygame.K_SPACE] and time_now - self.last_shoot > cooldown:
            laser_fx.play()
            bullet = Bullets(self.rect.centerx, self.rect.top)
            bullet_group.add(bullet)
            self.last_shoot = time_now

        self.mask = pygame.mask.from_surface(self.image)

        pygame.draw.rect(screen, red,(self.rect.x, (self.rect.bottom + 10), self.rect.width, 15))
        if self.health_remaining > 0:
            pygame.draw.rect(screen, green,(self.rect.x,(self.rect.bottom + 10), int(self.rect.width * (self.health_remaining / self.health_start)), 15))
        elif self.health_remaining <= 0:
            explosion = Explosion(self.rect.centerx, self.rect.centery, 3)
            Explosion_group.add(explosion)
            self.kill()
            result = -1

        return result


class Bullets(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y -= 6
        if self.rect.bottom < 1:
            self.kill() 

        if pygame.sprite.spritecollide(self, alien_group, True):
            self.kill()
            Explosion_fx.play()
            explosion = Explosion(self.rect.centerx, self.rect.centery, 2)
            Explosion_group.add(explosion)


class Aliens(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/alien" + str(random.randint(1,5)) + ".png") 
        self.rect = self.image.get_rect() 
        self.rect.center = [x, y]
        self.move_counter = 0 #armazena quanto andou
        self.move_direction = 1 #direção
    
    def update(self):
        self.rect.x += self.move_direction #mova X pixel para direção atual
        self.move_counter += 1
        if abs(self.move_counter) > 75:
            self.move_direction *= -1 #sempre inverte a direção --> (+1) * (-1) = (-1)*(-1) = +1 
            self.move_counter *= self.move_direction
                    #não importa a ordem nesse caso.

class Alien_Bullets(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/alien_bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y += 5 #velocidade do tiro
        if self.rect.top > screen_height:#se não houve contato kill.
            self.kill()  
        if pygame.sprite.spritecollide(self, spaceship_group, False, pygame.sprite.collide_mask):  
             self.kill()
             Explosion2_fx.play()
             spaceship.health_remaining -= 1
             explosion = Explosion(self.rect.centerx, self.rect.centery, 1)
             Explosion_group.add(explosion)


class Explosion(pygame.sprite.Sprite):
    def __init__(self,x,y, size):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1,6):
            img = pygame.image.load(f"img/exp{num}.png")
            if size == 1:
                img = pygame.transform.scale(img,(20,20))#explosão no player
            if size == 2:
                img = pygame.transform.scale(img,(40,40))#explosão no inimigo
            if size == 3:
                img = pygame.transform.scale(img,(160,160))#explosão game over do player
            self.images.append(img)
        self.index = 0            
        self.image = self.images[self.index]
        self.rect = self.image.get_rect() 
        self.rect.center = [x, y]
        self.counter = 0

    def update(self):
        Explosion_speed = 3
        self.counter += 1 

        if self.counter >= Explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        if self.index >= len(self.images) - 1 and self.counter >= Explosion_speed:
            self.kill()


spaceship_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
alien_group = pygame.sprite.Group()
alien_bullet_group = pygame.sprite.Group()
Explosion_group = pygame.sprite.Group()

def create_aliens():
    for row in range(rows):
        for item in range(cols):
            alien = Aliens(100 + item * 100, 100 + row * 70)
            alien_group.add(alien)

create_aliens()

spaceship = Spaceship(int(screen_widht / 2), screen_height - 100, 10)
spaceship_group.add(spaceship)


countdown_timer = pygame.time.get_ticks()

run = True
while run:
    
    clock.tick(fps)
    
    draw_bg()
    
    if countdown > 0:
        draw_text('!PREPARE-SE!', font40, white, int(screen_widht/2 - 110), int(screen_height / 2 + 50))
        draw_text(str(countdown), font40, white, int(screen_widht/2 - 10), int(screen_height / 2 + 100))
        countdown_timer = pygame.time.get_ticks()
        if countdown_timer - last_count > 1000:
            countdown -= 1
            last_count = countdown_timer #CRONOMETRO

    if countdown == 0:#Quando o temporizador chegar a zero
        time_now = pygame.time.get_ticks()
        if time_now - last_alien_shot > alien_cooldown and len(alien_bullet_group) < 5 and len(alien_group) > 0:
            attacking_alien = random.choice(alien_group.sprites())
            alien_bullet = Alien_Bullets(attacking_alien.rect.centerx, attacking_alien.rect.bottom)
            alien_bullet_group.add(alien_bullet)
            last_alien_shot = time_now

    if countdown == 0 and len(alien_group) == 0:
        game_over = 1

    if game_over == 0:
        if len(spaceship_group) == 0:
            game_over = -1
        elif countdown == 0:#Se o player perder toda a vida
            result = spaceship.update()
            bullet_group.update()
            alien_group.update()
            alien_bullet_group.update()
            
            
            if result == -1:
                game_over = -1

       
    else:
        if game_over == -1:
            draw_text('GAME OVER!', font40, white, int(screen_widht/2 - 100), int(screen_height / 2 + 50))
        if game_over == 1:
            draw_text('!VITÓRIA!', font40, white, int(screen_widht/2 - 100), int(screen_height / 2 + 50))

    Explosion_group.update()

    spaceship_group.draw(screen)
    bullet_group.draw(screen)
    alien_group.draw(screen)
    alien_bullet_group.draw(screen)
    Explosion_group.draw(screen)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.quit()
