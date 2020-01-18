import pygame
import sys
import os
import random
import time

pygame.init()
size = width, height = 825, 490
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()


birds_sprites = pygame.sprite.Group()
explosion_sprites = pygame.sprite.Group()
iter = 0
bird_iter = 0


class Birds(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(birds_sprites)
        self.c = 0
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        if x == -170:
            self.c = 0
        else:
            self.c = 1

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                if j == 2 and i == 2 and self.c == 1:
                    break
                if j == 2 and i == 0 and self.c == 0:
                    break
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        global bird_iter
        bird_iter += 1
        if bird_iter % 5 == 0:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
        if bird_iter > 50:
            bird_iter = 0


class Explosion(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(explosion_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        global iter
        iter += 1
        if iter % 2 == 0:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
        if iter > 50:
            iter = 0


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


kol = 15
aim = pygame.transform.scale(load_image('aim.jpg', -1), (40, 40))
while kol > 0:
    bird = pygame.transform.scale(load_image('bird_blue.png', -1), (170, 150))
    x, y = random.choice((-170, 825)), random.choice(range(450))
    if x == -170:
        bird = pygame.transform.flip(bird, True, False)
    Birds(bird, 3, 3, x, y)
    kol -= 1
explosion = pygame.transform.scale(load_image('explosion.png', -1), (530, 50))
explosion = Explosion(explosion, 15, 1, 300, 150)
x = 375
y = 207
running = True
motion = ''
while running:
    screen.fill((130, 0, 255))
    birds_sprites.draw(screen)
    explosion_sprites.draw(screen)
    birds_sprites.update()
    explosion_sprites.update()
    screen.blit(aim, (x, y))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                motion = 'left'
            if event.key == pygame.K_RIGHT:
                motion = 'right'
            if event.key == pygame.K_UP:
                motion = 'up'
            if event.key == pygame.K_DOWN:
                motion = 'down'
        if event.type == pygame.KEYUP:
            motion = 'stop'
    if motion == 'left' and x > 0:
        x -= 5
    if motion == 'right' and x < 750:
        x += 5
    if motion == 'up' and y > 0:
        y -= 5
    if motion == 'down' and y < 415:
        y += 5
    pygame.display.flip()
    clock.tick(70)

pygame.quit()
