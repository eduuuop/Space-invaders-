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
        self.health_remaining = health
        self.last_shoot = pygame.time.get_ticks()

    def update(self):

        #velocidade do movimento da nave
        speed = 4

        #tempo de recoil 
        cooldown = 900 #milisegundos

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


        #alinhando a hitbox com a imagem da nave 
        self.mask = pygame.mask.from_surface(self.image)

        #desenhando a barra de vida
        pygame.draw.rect(screen, red,(self.rect.x, (self.rect.bottom + 10), self.rect.width, 15))
        if self.health_remaining > 0:
            pygame.draw.rect(screen, green,(self.rect.x,(self.rect.bottom + 10), int(self.rect.width * (self.health_remaining / self.health_start)), 15))
        elif self.health_remaining <= 0:
            explosion = Explosion(self.rect.centerx, self.rect.centery, 5)
            Explosion_group.add(explosion)
            self.kill()




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
            explosion = Explosion(self.rect.centerx, self.rect.centery, 2)
#1-parâmetro = x, self.rect.centerx = a imagem acontecera no seu centroX, dentro de sua largura
# 2-parâmetro = a imagem estara no centro deste objeto no centro de sua altura. 
            Explosion_group.add(explosion)




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
        
#criar o tiro do inimigo
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
        if pygame.sprite.spritecollide(self, spaceship_group, False,pygame.sprite.collide_mask ):  
             self.kill()
             #dano da nave espacial
             spaceship.health_remaining -= 1
             explosion = Explosion(self.rect.centerx, self.rect.centery, 1)
             Explosion_group.add(explosion)

#criando explosão
class Explosion(pygame.sprite.Sprite):
    def __init__(self,x,y, size):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1,6):
            img = pygame.image.load(f"img/exp{num}.png")
            if size == 1:
                img = pygame.transform.scale(img,(20,20))
            if size == 2:
                img = pygame.transform.scale(img,(40,40))
            if size == 3:
                img = pygame.transform.scale(img,(160,160))
            #adicionar a imagem a lista
            self.images.append(img)
        self.index = 0            
        self.image = self.images[self.index]
        self.rect = self.image.get_rect() 
        self.rect.center = [x, y]
        self.counter = 0


    def update(self):
        Explosion_speed = 3
        #atualização das imagens, fps
        self.counter += 1 

        if self.counter >= Explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image= self.images[self.index] #a imagem sera aquela imagem pertencente a contagem da lista de frames. se imagem da posição 1 = frame de explosão 1

        if self.index >= len(self.images) - 1 and self.counter >= Explosion_speed:
            #se o índice de imagens for maior         |E| se meu contador for maior ou 
            #ou igual a quantidade de imagens menos 1 | |igual a minha v. de ex.
            self.kill()






#criando sprites groups, um grupo de sprites
spaceship_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
alien_group = pygame.sprite.Group()
alien_bullet_group = pygame.sprite.Group()
Explosion_group = pygame.sprite.Group()

def create_aliens():
    #gerar aliens
    for row in range(rows):
        for item in range(cols):
            alien = Aliens(100 + item * 100,   100 + row * 70)
                        #margem + #parametro do X  &  #parametro do Y
            alien_group.add(alien)#adicionando todo inimigo criado ao grupo inimigo/alien

create_aliens()


#criando o jogador
spaceship = Spaceship(int(screen_widht / 2), screen_height - 100, 10)
spaceship_group.add(spaceship)



run = True #enquanto querer jogar esse jogo isso sera true, ao sair isso sera false
while run:
    
    clock.tick(fps) #colocamos dentro do jogo aqui.
    
    #draw background
    draw_bg()
    
     #UPDATE SPACESHIP
    spaceship.update() 

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
    Explosion_group.draw(screen)

   

    #atualizar grupos de sprites
    bullet_group.update()
    alien_group.update()
    alien_bullet_group.update()
    pygame.display.update()
    Explosion_group.update()





    #event handlers
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.quit()
