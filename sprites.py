import pygame

COYOTE_JUMP_EVENT = pygame.USEREVENT + 1


class Body(pygame.sprite.Sprite):
    def __init__(self, game, pos, size, color, type):
        self.game = game
        self.pos = pos
        self.size = size 
        self.color = color
        self.velocity = [0,0]
        
        self.velocity = [0,0]
        self.type = type
        self.collisions = {'up':False, 'down': False, 'left': False, 'right':False}
        self.was_on_floor = False
        self.is_on_ceiling = False
        self.is_jumping = False
        

        #animation 
        self.action = ''
        self.anim_offset = (-3, -3)
        self.flip = False
        self.set_action('iddle')

    def set_action(self,action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.type + '/' + self.action].copy()

    def update(self,tilemap, movement, offset=[0,0]):
        self.collisions = {'up':False, 'down': False, 'left': False, 'right':False}
        self.apply_gravity()

        framemove = (self.velocity[0] + movement[0], self.velocity[1] + movement[1])
        self.pos[0]+= framemove[0]
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

        print(framemove[0])
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
        self.jump_value = 100
        self.jumps = self.jump_value
        self.jump_force = 0
        self.coyote = False
        self.display =pygame.surface.Surface(self.size)
        self.display.fill((255,0,0))
        self.is_attacking = False
        
       
       



    def update(self, tilemap, movement):
        self.can_coyote()
        print(self.jump_force)
        player_rect = self.rect()
        if movement[0] == 0:
           
            self.set_action('iddle')

        if movement[0] == 0 and self.is_attacking:
            self.set_action('attack')

        if self.collisions['up'] == True:
            pass
        if movement[0] != 0:
            self.set_action('run')

        if movement[0] != 0 and self.is_attacking:
            self.set_action('attack')

      

  


        self.animation.update()
        print(self.animation.img().get_height())
        return super().update(tilemap, movement = movement)

    
    def jump(self):
        if self.jumps > 0 :
            
            self.velocity[1] -= max(7, self.velocity[1] + 0.2)
            self.jumps -=1
            self.is_jumping = True

   
    def release_jump(self):
        pass

    def can_coyote(self):
        if not self.collisions['down'] and self.was_on_floor and self.velocity[1] >= 0:
            #pygame.time.set_timer(COYOTE_JUMP_EVENT, 500)
            pass

        if not self.collisions['down']:
            self.was_on_floor = False

    def flip_image(self):
        self.flip = not self.flip

    def attack(self, surf, offset = [0,0]):
        self.is_attacking = True
        rect = self.rect()
        if not self.flip:

            surf.blit(self.display, 
                    (rect[0] + 32 - offset[0], rect[1] - offset[1]))
        
        if self.flip:
            surf.blit(self.display, 
                    (rect[0] - 22 - offset[0], rect[1] - offset[1]))