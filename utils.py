import pygame 
import os


PATH_IMG = 'img/'
def load_image(path):
    img = pygame.image.load(PATH_IMG + path).convert_alpha()
    return img

def load_images(path):
    imgs = []
    for i in os.listdir(PATH_IMG + path):
        imgs.append(load_image(path + '/' + i))
    return imgs


class Animation:
    def __init__(self, images, img_duration=12, loop=True):
        self.images = images
        self.img_duration = img_duration
        self.loop = loop
        self.done = False
        self.frame = 0

    def copy(self):
        return Animation(self.images, self.img_duration, self.loop)

    def update(self):
        
        
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_duration * len(self.images))

        else:
            self.frame = min(self.frame + 1, self.img_duration * len(self.images) - 1)

        if self.frame >= self.img_duration * len(self.images) - 1:
            self.done = True
            
            

        else:
            self.frame += 1

        
    def img(self):
        return self.images[self.frame // self.img_duration]