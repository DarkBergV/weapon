import pygame

COYOTE_JUMP_EVENT = pygame.USEREVENT + 1
ATTACK_EVENT = pygame.USEREVENT + 2


class Body(pygame.sprite.Sprite):
    def __init__(self, game, pos, size, color, type):
        self.game = game
        self.pos = pos
        self.size = size 
        self.color = color
        
        
        self.velocity = [0,0]
        self.type = type
        self.collisions = {'up':False, 'down': False, 'left': False, 'right':False}
        self.was_on_floor = False
        self.is_on_ceiling = False
        self.is_jumping = False
        self.is_attacking = False
        

        #animation 
        self.action = ''
        self.anim_offset = (-3, -3)
        self.flip = False
        

    def set_action(self,action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.type + '/' + self.action].copy()
        

    def update(self,tilemap, movement, offset=[0,0]):
        self.collisions = {'up':False, 'down': False, 'left': False, 'right':False}
        self.apply_gravity()

        framemove = (self.velocity[0] + movement[0], self.velocity[1] + movement[1])
     
        self.pos[0]+= framemove[0] * 1.5
        body_rect = self.rect()
        for rect in tilemap.physics_rect_around(self.pos):
            if body_rect.colliderect(rect):
                if framemove[0] < 0:
                    self.collisions['left'] = True
                    body_rect.left = rect.right 

                if framemove[0] > 0:
                    self.collisions['right'] = True
                    body_rect.right = rect.left 
                    
                
                self.pos[0] = body_rect.x

     
        self.pos[1]+= framemove[1]
        body_rect = self.rect()
        


        for rect in tilemap.physics_rect_around(self.pos):
            if body_rect.colliderect(rect):
                if framemove[1] < 0: #check if is on the ceiling
                    self.collisions['top'] = True
                    body_rect.top = rect.bottom
                    

                if framemove[1] > 0: #checks if is on the ground
                    self.collisions['down'] = True
                    body_rect.bottom = rect.top
                    if self.type == 'player':
                        self.jumps = self.jump_value
                        self.was_on_floor = True
                    
                
                self.pos[1] = body_rect.y

        if movement[0] > 0:
            self.flip = False

        if movement[0] < 0:
            self.flip = True
       

    def rect(self):
        return pygame.rect.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    def render(self, surf, offset = (0,0)):
      
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), 
                  (
                      self.pos[0] - offset[0] + self.anim_offset[0],
                      self.pos[1] - offset[1] + self.anim_offset[1],
                  ))
        
    
    def apply_gravity(self):
        self.velocity[1] = min(2, self.velocity[1] + 0.1)
        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0
            




class Player(Body):
    def __init__(self, game, pos, size, color, type):

        super().__init__(game, pos, size, color, type)
        self.jump_value = 1
        self.jumps = self.jump_value
        self.jump_force = 0
        self.coyote = False
        self.display =pygame.surface.Surface((50,50))
        self.display.fill((255,0,0))
        self.is_attacking = False
        self.set_action('iddle')
        self.dealing_damage = False
        
       
       



    def update(self, tilemap, movement):
        
        self.can_coyote()
        
        player_rect = self.rect()
      

        if self.collisions['down'] and  movement[0] == 0 and not self.is_attacking:
           
            self.set_action('iddle')
        
        if self.collisions['down'] and  movement[0] == 0 and self.is_attacking:
            self.set_action('attack')
           
            
            
          

        if self.collisions['down'] and  movement[0] != 0 and not self.is_attacking:
            self.set_action('run')

        if self.collisions['down'] and movement[0] != 0 and self.is_attacking:
            self.set_action('attack')

        if not self.collisions['down'] and self.is_jumping and self.is_attacking:
            self.set_action('fall_attack')

        if not self.collisions['down'] and self.is_jumping and self.collisions['up']:
            self.set_action('ceiling')
        self.enemy_detection()#check to see how it handles multiple boxes
        self.animation.update()
        if self.animation.done:#when the animation ends is_attacking becomes false
            self.is_attacking = False

        
        return super().update(tilemap, movement = movement)

    
    def player_states(self):
        pass
    def jump(self):
        if self.jumps > 0 :
            
            self.velocity[1] -= max(7, self.velocity[1] + 0.2)
            self.jumps -=1
            self.is_jumping = True

   
    def release_jump(self):
        pass

    def can_coyote(self):
        if not self.collisions['down'] and self.was_on_floor and self.velocity[1] >= 0:
            pygame.time.set_timer(COYOTE_JUMP_EVENT, 500)
            

        if not self.collisions['down']:
            self.was_on_floor = False

    def flip_image(self):
        self.flip = not self.flip

    def attack(self, surf, offset = [0,0]): #attack function thats called when the left,mouse button is pressed
                                            #is attacking becomes true

        self.is_attacking = True
        

        rect = self.hitbox()
        
        if not self.flip:

            surf.blit(self.display, 
                    (rect[0] + 40  - offset[0], rect[1] - offset[1]))
        
        if self.flip:
            surf.blit(self.display, 
                    (rect[0] - 40 - offset[0], rect[1] - offset[1]))
    
    def render(self, surf, offset=(0, 0)):
        rect = self.hitbox()
        
        if not self.flip:

            surf.blit(self.display, 
                    (rect[0]  - offset[0], rect[1] - offset[1]))
        
        if self.flip:
            surf.blit(self.display, 
                    (rect[0] - offset[0], rect[1] - offset[1]))
    
        return super().render(surf, offset)

    def hitbox(self):
        if not self.flip:
            return pygame.rect.Rect(self.pos[0]+ 32, self.pos[1], 50, 50)
        if self.flip:
            return pygame.rect.Rect(self.pos[0] - 23, self.pos[1], 50, 50)
    
    
        
        
    def enemy_detection(self):
        enemies = [enemy for enemy in self.game.enemies]
        hitbox = self.hitbox()
        if self.dealing_damage:
            print(self.dealing_damage)
      
        

        for enemy in enemies:
            if hitbox.colliderect(enemy.rect())  and self.is_attacking and self.dealing_damage:
                enemy.lose_hp()
                enemy.losing_hp = True
                self.dealing_damage = False
class Enemy(Body):
    def __init__(self, game, pos, size, color, type):
            
        super().__init__(game, pos, size, color, type)
        self.display = pygame.Surface(self.size)
        self.display.fill(color)
        self.hp = 3
        self.losing_hp = False



    def update(self, tilemap, movement, offset=[0, 0]):
        print(self.hp)
        return super().update(tilemap, movement, offset)
        
    def render(self, surf, offset=(0, 0)):
        rect = self.rect()
        surf.blit(self.display, (
            rect[0] - offset[0], rect[1] - offset[1]
        ))

    def lose_hp(self):
        self.hp -=1
        if self.hp <= 0:
            print('asasas')
            return True
   