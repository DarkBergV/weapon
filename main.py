import pygame
import sys
from sprites import Body, Player, Enemy, GunEnemy
from tilemap import Tilemap
from utils import load_image, load_images, Animation


WINDTH = 640

LENGTH = 480

RENDER_SCALE = 2.0


COYOTE_JUMP_EVENT = pygame.USEREVENT + 1
ATTACK_EVENT = pygame.USEREVENT + 2
INVINCIBILITY_EVENT = pygame.USEREVENT + 3




class Main():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('weapon game')
        self.screen = pygame.display.set_mode((WINDTH, LENGTH))
        self.display_screen = pygame.surface.Surface((WINDTH // 2 , LENGTH // 2))
        self.movement = [0,0,0,0]
        self.scroll = [0,0]
        self.running = True
        self.clock = pygame.time.Clock()
        self.bullets = []
        self.player_died = 0
        
       
        self.tilemap = Tilemap(self, 32)
        self.scene = []
        self.assets = {'ground/ground': load_images('tiles/ground'),
                       'player/ceiling': Animation(load_images('player/ceiling')),
                       'player/attack':Animation(load_images('player/attack')),
                       'player/iddle':Animation(load_images('player/iddle')),
                       'player/run':Animation(load_images('player/run')),
                       'player/fall_attack':Animation(load_images('player/fall_attack')),
                       'enemy/iddle': Animation(load_images('enemy/iddle')),
                       'enemy/run': Animation(load_images('enemy/run')),
                       'gun_enemy/iddle': Animation(load_images('gun_enemy/iddle')),
                       'gun_enemy/run': Animation(load_images('gun_enemy/run')),
                       'spawners': load_images('tiles/spawner'),
                       'gun':load_image("gun.png"),
                       'bullet':load_image("bullet.png")}
        
        
        
        self.player = Player(self, [200,100], [26,26], (255,0,0), 'player')
        
        self.load_level()

        
    def load_level(self):
        self.tilemap.load('map.json')
        self.enemies = []
        self.scene = []
        self.bullets = []
        for ground in self.tilemap.extract([('ground/ground', 0)], keep = True):
            self.scene.append(pygame.Rect(ground['pos'][0], ground['pos'][1],32.0,32.0))
     

        for spawner in self.tilemap.extract([('spawners',0),('spawners',1), ('spawners',2)]):
            
         
            if spawner['variant'] == 0:
                enemy = Enemy(self,spawner['pos'], [26,26], [15,20,70], "enemy")
                self.enemies.append(enemy)

            if spawner['variant'] == 1:
                gun_enemy = GunEnemy(self, spawner['pos'], [26,26], [70,15,20], 'gun_enemy')
                self.enemies.append(gun_enemy)

            if spawner['variant'] == 2:
                self.player.pos = spawner["pos"]
        self.player.hp = 5

        self.dead = 0
        

    def run(self):
        while self.running:
            
            self.display_screen.fill((100,25,50))
            if self.dead:
                self.dead +=1
                if self.dead > 40:
                    self.load_level()
            self.tilemap.render(self.display_screen, self.scroll)
            self.scroll[0] += (self.player.rect().centerx - self.display_screen.get_width() / 2 - self.scroll[0]) 
            self.scroll[1] += (self.player.rect().centery - self.display_screen.get_height() / 2 - self.scroll[1])


            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == COYOTE_JUMP_EVENT:
                   
                    self.player.was_on_floor = False
                    self.player.jumps -=1
                    pygame.time.set_timer(COYOTE_JUMP_EVENT,0)

                if event.type == ATTACK_EVENT:
                    self.player.is_attacking = False
                
                if event.type == INVINCIBILITY_EVENT:
                    self.player.invincibility = False
                    pygame.time.set_timer(INVINCIBILITY_EVENT,0)

                

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.player.dealing_damage = True
                       
                        self.player.attack(self.display_screen, self.scroll)
                       
                       
                        
                       
              

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        self.movement[0] = True
                        self.movement[1] = False
                        self.player.velocity[0] = min(5, self.player.velocity[0] + 1)
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                        self.movement[1] = True
                        self.player.velocity[0] = min(5, self.player.velocity[0] + 1) * -1
                    if event.key == pygame.K_w:
                        
                        self.player.jump()
                    if event.key == pygame.K_s:
                        self.movement[2] = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_d:
                        self.movement[0] = False
                        self.player.velocity[0] = 0
                    if event.key == pygame.K_a:
                        self.movement[1] = False 
                        self.player.velocity[0] = 0
                    if event.key == pygame.K_w:
                        self.player.release_jump()
                    if event.key == pygame.K_s:
                        self.movement[2] = False

           
            
            for enemy in self.enemies.copy():
                kill = enemy.update(self.tilemap, [0,0], [0,0])
                enemy.render(self.display_screen, render_scroll)
                
                if enemy.killed:
                    self.enemies.remove(enemy)

            if not self.dead:
                self.player.update(self.tilemap,[self.movement[0] - self.movement[1], self.movement[2] - self.movement[3]])
                self.player.render(self.display_screen, render_scroll)
            
            for bullet in self.bullets.copy():
                bullet[0][0] += bullet[1]
                bullet[2] += 1
                img = self.assets['bullet']
                self.display_screen.blit(img, (bullet[0][0] - img.get_width() / 2 - render_scroll[0], bullet[0][1] - img.get_height() / 2 - render_scroll[1]))
                
                for tilerect in self.tilemap.physics_rect_around(bullet[0]):
                    if tilerect.collidepoint(bullet[0]):
                        self.bullets.remove(bullet)
                if bullet[2] > 360:
                    self.bullets.remove(bullet)
                elif self.player.rect().collidepoint(bullet[0]):
                    self.player.hp -= 1
                    self.player.invincibility = True
                    self.bullets.remove(bullet)
            if self.player.hp <= 0 :
                
                self.player_died += 1 
                self.dead += 1 
            print(self.dead)



            self.screen.blit(pygame.transform.scale(self.display_screen, self.screen.get_size()), (0,0))
            pygame.display.update()
            self.clock.tick(60)
g = Main()

while g.running:
    g.run()

pygame.quit()
sys.exit()