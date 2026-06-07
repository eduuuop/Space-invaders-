import pygame
from pygame.locals import *
import random

#aqui defino o fps
clock = pygame.time.Clock() #Esse objeto serve para:medir tempocontrolar velocidade do loop limitar FPS É como um “relógio interno” do jogo.
fps = 60 #definimos que os frames irão ate 60 quadros p/ segundo.


screen_widht= 600 #variaveis da tela
screen_height = 800

screen = pygame.display.set_mode((screen_widht,screen_height))
pygame.display.set_caption('Space Invaders')


#criando variáveis do jogo
rows = 5 #linhas
cols = 5 #colunas

alien_cooldown = 1000 #milisegundos
last_alien_shot = pygame.time.get_ticks()

#define colours
red = (255, 0, 0)
green = (0,255, 0)


#load image
bg = pygame.image.load("123.jpg")             #bg=background em ingleis = fundo

def draw_bg():
    screen.blit(bg, (0,0))

#criar a espaçonavedo moço
class Spaceship(pygame.sprite.Sprite):#isso é meio confuso....
    def __init__(self,x,y,health):
        pygame.sprite.Sprite.__init__(self)
        self.image= pygame.image.load("img/spaceship.png") #imagem da espaçonavedomoço0
        self.rect = self.image.get_rect() #hitbox retangular da nave
        self.rect.center = [x, y]#dizendo para estar no centro
        self.health_start = health
        self.health_remaining = health/2
        self.last_shoot = pygame.time.get_ticks()

    def update(self):

        #velocidade do movimento da nave
        speed = 8

        #tempo de recoil 
        cooldown = 300 #milisegundos

        #get key press
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
             self.rect.x -= speed 
        if key[pygame.K_RIGHT] and self.rect.right < screen_widht:
             self.rect.x += speed

        #recoil dos tiros
        time_now = pygame.time.get_ticks()

            #tiro
        if key[pygame.K_SPACE] and time_now - self.last_shoot > cooldown:
            bullet = Bullets(self.rect.centerx, self.rect.top)
            bullet_group.add(bullet)
            self.last_shoot = time_now


        #draw health bar
        pygame.draw.rect(screen, red,(self.rect.x, (self.rect.bottom + 10), self.rect.width, 15))
        if self.health_remaining > 0:
            pygame.draw.rect(screen, green,(self.rect.x,(self.rect.bottom + 10), int(self.rect.width * (self.health_remaining / self.health_start)), 15))
        
#criar o tiro do moço
class Bullets(pygame.sprite.Sprite):#isso eé meio confuso....
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/bullet.png") #imagem da espaçonavedomoço0
        self.rect = self.image.get_rect() #hitbox retangular da nave
        self.rect.center = [x, y]#dizendo para estar no centro


    def update(self):
        self.rect.y -= 6
        if self.rect.bottom < 1:
            self.kill() 

        if pygame.sprite.spritecollide(self, alien_group, True):
            self.kill()

#criando os inimigos
class Aliens(pygame.sprite.Sprite):#isso eé meio confuso....
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/alien" +str(random.randint(1,5))+".png") 
        self.rect = self.image.get_rect() 
        self.rect.center = [x, y]
        self.move_counter = 0
        self.move_direction = 1
    
    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 75:
            self.move_direction *= -1
            self.move_counter *= self.move_direction
        
#criar o tiro do moinimigo
class Alien_Bullets(pygame.sprite.Sprite):#isso eé meio confuso....
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/alien_bullet.png") #imagem da espaçonavedomoço0
        self.rect = self.image.get_rect() #hitbox retangular da nave
        self.rect.center = [x, y]#dizendo para estar no centro


    def update(self):
        self.rect.y += 2
        if self.rect.top > screen_height:
            self.kill()     





#criando sprites groups, um grupo de sprites
spaceship_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
alien_group = pygame.sprite.Group()
alien_bullet_group = pygame.sprite.Group()

def create_aliens():
    #gerar aliens
    for row in range(rows):
        for item in range(cols):
            alien = Aliens(100 + item * 100,   100 + row * 70)
                        #margem + #parametro do X  &  #parametro do Y
            alien_group.add(alien)#adicionando todo inimigo criado ao grupo inimigo/alien

create_aliens()


#criando o jogador
spaceship = Spaceship(int(screen_widht / 2), screen_height - 100, 3)
spaceship_group.add(spaceship)



run = True #enquanto querer jogar esse jogo isso sera true, ao sair isso sera false
while run:
    
    clock.tick(fps) #colocamos dentro do jogo aqui.
    
    #draw background
    draw_bg()
    
    #criar balas alieniginas aleatorias
    #registrar o horario
    time_now = pygame.time.get_ticks()
    #tiro
    if time_now - last_alien_shot > alien_cooldown and len(alien_bullet_group) < 5 and len(alien_group) > 0:
        attacking_alien = random.choice(alien_group.sprites())
        alien_bullet = Alien_Bullets(attacking_alien.rect.centerx, attacking_alien.rect.bottom)
        alien_bullet_group.add(alien_bullet)
        last_alien_shot = time_now


    #draw sprite groups
    spaceship_group.draw(screen)
    bullet_group.draw(screen)
    alien_group.draw(screen)
    alien_bullet_group.draw(screen)

    #UPDATE SPACESHIP
    spaceship.update() 

    #atualizar grupos de sprites
    bullet_group.update()
    alien_group.update()
    alien_bullet_group.update()
    pygame.display.update()
   


    #event handlers
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.quit()
