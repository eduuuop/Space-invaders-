import pygame
from pygame.locals import *

#aqui defino o fps
clock = pygame.time.Clock() #Esse objeto serve para:medir tempocontrolar velocidade do loop limitar FPS É como um “relógio interno” do jogo.
fps = 60 #definimos que os frames irão ate 60 quadros p/ segundo.


screen_widht= 600 #variaveis da tela
screen_height = 800

screen = pygame.display.set_mode((screen_widht,screen_height))
pygame.display.set_caption('Space Invaders')


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
        self.image = pygame.image.load("img/spaceship.png") #imagem da espaçonavedomoço0
        self.rect = self.image.get_rect() #hitbox retangular da nave
        self.rect.center = [x, y]#dizendo para estar no centro
        self.health_start = health
        self.health_remaining = health/2
        self.last_shoot = pygame.time.get_ticks()

    def update(self):
        #velocidade dos movimentos
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
    def __init__(self,x,y,):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/bullet.png") #imagem da espaçonavedomoço0
        self.rect = self.image.get_rect() #hitbox retangular da nave
        self.rect.center = [x, y]#dizendo para estar no centro


    def update(self):
        self.rect.y -= 6        


#criando sprites groups, um grupo de sprites
spaceship_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()

#criando o jogador
spaceship = Spaceship(int(screen_widht / 2), screen_height - 100, 3)
spaceship_group.add(spaceship)



run = True #enquanto querer jogar esse jogo isso sera true, ao sair isso sera false
while run:
    
    clock.tick(fps) #colocamos dentro do jogo aqui.
    
    #draw background
    draw_bg()
    


    #draw sprite groups
    spaceship_group.draw(screen)
    bullet_group.draw(screen)
    
    
    #UPDATE SPACESHIP
    spaceship.update() 

    #atualizar grupos de sprites
    bullet_group.update()
    
    pygame.display.update()
   


    #event handlers
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.quit()
