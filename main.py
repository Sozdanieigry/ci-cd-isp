

import pygame
from pygame.locals import  *

pygame.init()
#rtishevandmakishev
clock = pygame.time.Clock()
fps = 60

screen_width = 1100
screen_height = 850
window_size = (1200, 100)
screen = pygame.display.set_mode((screen_width, screen_height))
icon = pygame.image.load('image/ara.jpg')
pygame.display.set_icon(icon)


pygame.display.set_caption("Ara bird")

ground_scroll = 0
scroll_speed = 4



background_image = pygame.image.load("image/background.jpg")
ground_img = pygame.image.load('image/ground.png')
ground_img = pygame.transform.scale(ground_img, window_size )

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img = pygame.image.load(f'image/bird{num}.png')
            self.images.append(img)


        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False

    def update(self):
        self.vel += 0.5
        if self.vel > 8:
            self.vel = 8
        if self.rect.bottom < 768:
           self.rect.y += int(self.vel)

        if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
            self.clicked = True
            self.vel = -5
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False




        self.counter += 1
        flap_cooldown = 5

        if self.counter > flap_cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
        self.image = self.images[self.index]

        self.image = pygame.transform.rotate(self.images[self.index], self.vel )

bird_group = pygame.sprite.Group()
flappy = Bird(100, int(screen_height / 2))

bird_group.add(flappy)




run = True
#rtishevandmakishev
while run:
    clock.tick(fps)

    screen.blit(background_image, (0, 0))
    screen.blit(ground_img, (ground_scroll, 768))

    bird_group.draw(screen)
    bird_group.update()
    ground_scroll -= scroll_speed

    if abs(ground_scroll) > 135:
        ground_scroll = 0


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            exit()
    pygame.display.update()
pygame.quit()
pygame.display.flip()

