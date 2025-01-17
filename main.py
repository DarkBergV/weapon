import pygame
import sys
from sprites import Body

WINDTH = 640

LENGTH = 480

RENDER_SCALE = 2.0


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
        self.player = Body(self, [0,0], [16,16], (255,0,0))


    def run(self):
        while self.running:
            self.display_screen.fill((255,255,255))
            self.scroll[0] += (self.movement[0] - self.movement[1]) * 2
            self.scroll[1] += (self.movement[2] - self.movement[3]) * 2

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        self.movement[0] = True
                    if event.key == pygame.K_a:
                        self.movement[1] = True
                    if event.key == pygame.K_w:
                        self.movement[3] = True
                    if event.key == pygame.K_s:
                        self.movement[2] = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_d:
                        self.movement[0] = False
                    if event.key == pygame.K_a:
                        self.movement[1] = False
                    if event.key == pygame.K_w:
                        self.movement[3] = False
                    if event.key == pygame.K_s:
                        self.movement[2] = False


            self.player.update((self.movement[0] - self.movement[1], self.movement[2] - self.movement[3]), [0,0])
            self.player.render(self.display_screen, (0,0))


            self.screen.blit(pygame.transform.scale(self.display_screen, self.screen.get_size()), (0,0))
            pygame.display.update()
            self.clock.tick(60)
g = Main()

while g.running:
    g.run()

pygame.quit()
sys.exit()