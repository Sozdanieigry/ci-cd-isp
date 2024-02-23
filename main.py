import pygame
import sys
from pygame.locals import  *
import random
pygame.init()
#rtishevandmakishev
clock = pygame.time.Clock()
fps = 75


screen_width = 1100
screen_height = 850
window_size = (1200, 100)
screen = pygame.display.set_mode((screen_width, screen_height))
icon = pygame.image.load('image/icon.png')
pygame.display.set_icon(icon)


pygame.display.set_caption("Pig bird")

font = pygame.font.SysFont('Roboto', 60)

white = (255, 165, 0)

ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
pipe_gap = 150
pipe_frequency = 2000
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0
pass_pipe = False
gameplay = True
label = pygame.font.SysFont('Roboto', 40)
lose_label = label.render('Вы проиграли!', False, (255, 0, 0))
restart_label = label.render('', False, (115, 132, 148))
restart_label_rec = restart_label.get_rect(topleft=(180, 200))


background_image = pygame.image.load("image/sdfe.jpg")
ground_img = pygame.image.load('image/ground1.png')
ground_img = pygame.transform.scale(ground_img, window_size)


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))
class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 8):
            img = pygame.image.load(f'image/bird{num}.png')
            self.images.append(img)


        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False

    def update(self):
        if flying == True:
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 768:
               self.rect.y += int(self.vel)
        if game_over == False:
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.vel = -8
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

            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -10)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -180)


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('image/pipes1.png')

        self.rect = self.image.get_rect()
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
        if position == -1:
            self.rect.topleft = [x, y + int(pipe_gap / 2)]
    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()


bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()
flappy = Bird(100, int(screen_height / 2))

bird_group.add(flappy)




backgroun_x = 0

bg_sound = pygame.mixer.Sound('souds/bad piggies drip.mp3')
bg_sound.play()


run = True
#rtishevandmakishev
while run:



    clock.tick(fps)

    screen.blit(background_image, (backgroun_x, 0))
    screen.blit(background_image, (backgroun_x + 1100, 0))
    screen.blit(ground_img, (ground_scroll, 768))



    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)

    if gameplay:
        screen.blit(ground_img, (ground_scroll, 768))




        if len(pipe_group) > 0:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
                and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
                and pass_pipe == False:
                pass_pipe = True
            if pass_pipe == True:
                if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                    score += 1
                    pass_pipe = False



        draw_text(str(score), font, white, int(screen_width / 2), 20)

        if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
            game_over = True
            gameplay = False


        if flappy.rect.bottom >= 768:
            game_over = True
            flying = False
            gameplay = False



        if game_over == False and flying == True:
            time_now = pygame.time.get_ticks()
            if time_now - last_pipe > pipe_frequency:
                pipe_height = random.randint(-100, 100)
                btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1)
                top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, 1)
                pipe_group.add(btm_pipe)
                pipe_group.add(top_pipe)
                last_pipe = time_now

            ground_scroll -= scroll_speed
            if abs(ground_scroll) > 135:
                ground_scroll = 0
            pipe_group.update()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
                flying = True
    else:

        screen.blit(lose_label, (400, 25))
        screen.blit(restart_label, restart_label_rec)


        mouse = pygame.mouse.get_pos()
        if restart_label_rec.collidepoint(mouse) and pygame.mouse.get_pressed(1):
            gameplay = True


    pygame.display.update()
pygame.quit()
pygame.display.flip()
