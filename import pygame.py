import pygame
import random
import os
from pygame import sprite
import sys



from pygame.constants import K_SPACE
FPS=60
white=(255,255,255)
green=(0,255,0)
red=(255,0,0)
yellow=(255,255,0)
black=(0,0,0) 
width=500
play_color=(222,222,222)
height=650
pygame.init()
pygame.mixer.init() #music init
screen=pygame.display.set_mode((width,height))
pygame.display.set_caption("Craft Shooting")
clock =pygame.time.Clock()




#import image
background_img=pygame.image.load(os.path.join("img","ground.png")).convert()
player_img=pygame.image.load(os.path.join("img","player.png")).convert()
bullet_img=pygame.image.load(os.path.join("img","bullet.png")).convert()


#rock_img=pygame.image.load(os.path.join("img","rock.png")).convert()
rock_img=[]
for i in range(4):
    r=pygame.image.load(os.path.join("img","rock_"+str(i)+".png")).convert()
    t=pygame.transform.scale(r,(30,30))
    rock_img.append(t)


#import music 


pygame.mixer.music.load(os.path.join("sound","buru.mp3"))
##exploration
expl_anim={}
expl_anim['lg']=[]
expl_anim['sm']=[]
for i in range(9):
    expl_img= pygame.image.load(os.path.join("img",f"exp{i}.png")).convert()
  #  expl_img.set_colorkey(black)
    expl_anim['lg'].append(pygame.transform.scale(expl_img,(40,40)))
    expl_anim['sm'].append(pygame.transform.scale(expl_img,(30,30)))


score = 0 

font_name=pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font =pygame.font.Font(font_name,size)
    text_surface=font.render(text, True,white)
    text_rect=text_surface.get_rect()
    text_rect.centerx=x
    text_rect.top=y
    surf.blit(text_surface,text_rect)


def new_rock():
    r=Rock()
    all_sprites.add(r)
    rocks.add(r) 

def draw_health(surf,hp,x,y):
    if hp <0:
        hp=0 
    bar_length=100
    bar_height=10
    fill=(hp/100)*bar_length
    outline_rect=pygame.Rect(x,y,bar_length,bar_height)
    fill_rect=pygame.Rect(x,y,fill,bar_height)
    pygame.draw.rect(surf, green,fill_rect)
    pygame.draw.rect(surf,white, outline_rect,2)


#define button 
def BUTTON(screen, position, text):
	bwidth = 250
	bheight = 50
	left, top = position
	pygame.draw.line(screen, (150, 150, 150), (left, top), (left+bwidth, top), 5)
	pygame.draw.line(screen, (150, 150, 150), (left, top-2), (left, top+bheight), 5)
	pygame.draw.line(screen, (50, 50, 50), (left, top+bheight), (left+bwidth, top+bheight), 5)
	pygame.draw.line(screen, (50, 50, 50), (left+bwidth, top+bheight), [left+bwidth, top], 5)
	pygame.draw.rect(screen, (100, 100, 100), (left, top, bwidth, bheight))
	font = pygame.font.Font(font_name,18)
	text_render = font.render(text, 1, red)
	return screen.blit(text_render, (left+20, top+10))

#quit game 
def end_interface(screen):
	clock = pygame.time.Clock()
	while True:
		button_1 = BUTTON(screen, (width/3, height/2), 'Yang, Wenjun: restart and be a man')
		button_2 = BUTTON(screen, (width/3, height/2-60), 'Fan, Jiayan: quit and f**k your gf')#now these two buttons overlap
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if button_1.collidepoint(pygame.mouse.get_pos()):
					return
				elif button_2.collidepoint(pygame.mouse.get_pos()):
					pygame.quit()
					sys.exit()
		clock.tick(60)
		pygame.display.update() 


#sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #self.image=pygame.Surface((50,40))
        #self.image.fill(green)
        self.image=pygame.transform.scale(player_img,(50,50))
        self.image.set_colorkey(white)
        self.rect=self.image.get_rect()
        self.radius=self.rect.width*0.85/2
        #pygame.draw.circle(self.image,red, self.rect.center, self.radius)
        
        self.rect.centerx=width/2
        self.rect.bottom=height-10
        #self.rect.center=(width/2,height/2) center
        self.speedx=8
        self.speedy=5
        self.health=100
    

    #craft 
    def update(self):
        key_pressed=pygame.key.get_pressed()
        if key_pressed[pygame.K_d]:
            self.rect.x+=self.speedx
        if key_pressed[pygame.K_a]:
            self.rect.x-=self.speedx
        #self.rect.x+=2
        if self.rect.right > width:
            self.rect.right=width
        if self.rect.left < 0:
            self.rect.left=0
        if key_pressed[pygame.K_s]:
            self.rect.y+=self.speedy
        if key_pressed[pygame.K_w]:
            self.rect.y-=self.speedy
        #if self.rect.top > height:
        #    self.rect.top=height 
        #if self.rect.bottom < 0:
        #    self.rect.bottom =0 
          
    
    def shoot(self):
        bullet=Bullet(self.rect.centerx,self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)


class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.image=pygame.Surface((30,40))
        #self.image.fill(red)
       # self.image=pygame.transform.scale(i in rock_img,(30,30))

       # self.image=random.choice(rock_img) 
        self.image_ori=random.choice(rock_img)
        self.image=self.image_ori.copy()
        self.rect=self.image.get_rect()
        self.radius=self.rect.width*0.85 /2
        #pygame.draw.circle(self.image,red, self.rect.center, self.radius)
        self.rect.x=random.randrange(0,width-self.rect.width)
        self.rect.y=random.randrange(-100,-40)
        #self.rect.center=(width/2,height/2) center
        self.speedy=random.randrange(2,10)
        self.speedx=random.randrange(-3,3)
        self.total_degree=0 
        self.rot_degree=random.randrange(-1,1)
        
    def rotate(self):
        self.total_degree+=self.rot_degree
        self.total_degree=self.total_degree % 360 
        self.image=pygame.transform.rotate(self.image_ori,self.total_degree)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center=center 
   
    def update(self):
       #self.rect.y+=self.speedy
       self.rotate()  
       self.rect.x+=self.speedx
       self.rect.y+=3   #this is wj speed n ot to fast 
       #self.rect.x+=3
       if self.rect.top > height or self.rect.left > width or self.rect.right < 0:
            self.rect.x=random.randrange(0,width-self.rect.width)
            self.rect.y=random.randrange(-100,-40)
            #self.rect.center=(width/2,height/2) center
            self.speedy=random.randrange(2,10)
            self.speedx=random.randrange(-3,3)   


class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        #self.image=pygame.Surface((10,15))
        #self.image.fill(yellow)
        self.image=bullet_img
        self.image.set_colorkey(white)
        self.rect=self.image.get_rect()
        self.rect.centerx=x
        self.rect.bottom=y
        #self.rect.center=(width/2,height/2) center
        self.speedy=-10
       
        

    #craft 
    def update(self):
        self.rect.y+=self.speedy
        if self.rect.bottom < 0: 
            self.kill()
    
class Explosion(pygame.sprite.Sprite):
    def __init__(self,center,size):
        pygame.sprite.Sprite.__init__(self)
        #self.image=pygame.Surface((10,15))
        #self.image.fill(yellow)
        self.size=size
        self.image=expl_anim[self.size][0]
        #self.image.set_colorkey(white)
        self.rect=self.image.get_rect()
        self.rect.center=center
        self.frame=0
        #self.rect.center=(width/2,height/2) center
        self.last_update =pygame.time.get_ticks()
        self.frame_rate=50
        

    
    def update(self):
        now=pygame.time.get_ticks()
        if now -self.last_update > self.frame_rate:
            self.last_update=now 
            self.frame+=1
            if self.frame == len(expl_anim[self.size]):
                self.kill()
            else:
                self.image = expl_anim[self.size][self.frame]
                # this will lead to a expl on the very top left corner 

            #    center=self.rect.center 
            #    self.rect=self.image.get_rect()
            #    self.rect_center=center
    



#group 
all_sprites=pygame.sprite.Group()
rocks=pygame.sprite.Group()
bullets=pygame.sprite.Group()
player=Player()
all_sprites.add(player)
for i in range(8):
    rock=Rock()
    all_sprites.add(rock)
    rocks.add(rock)

pygame.mixer.music.play(-1)

#game quit 
running = True 

while running:
    clock.tick(FPS)
    #input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False 
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE:
                player.shoot() 


    #update screen 
    all_sprites.update()
    hits=pygame.sprite.groupcollide(rocks,bullets,True, True)
    
    for hit in hits:
        score += round(hit.radius)
        expl=Explosion(hit.rect.center,'lg')
        all_sprites.add(expl)
        new_rock()
  
    
    hits=pygame.sprite.spritecollide(player,rocks, True,  pygame.sprite.collide_circle)
    for hit in hits :
        new_rock()
        player.health-=hit.radius
        expl=Explosion(hit.rect.center,'sm')
        all_sprites.add(expl)
        if player.health <=0: 
            running=False
    
    #current display

    screen.fill(black)
    screen.blit(background_img,(0,0))
    all_sprites.draw(screen)
    draw_text(screen, str(score),18,width/2,10)
    draw_health(screen,player.health,5,10)
    pygame.display.update()

end_interface(screen) 