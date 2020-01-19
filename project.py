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
aim_sprite = pygame.sprite.Group()
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
        if x < -58:
            self.c = 0
        else:
            self.c = 1

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                if j == 2 and i == 2:
                    break
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        global bird_iter, kol
        bird_iter += 1
        if self.c == 0 and self.rect[0] == 825:
            self.image = pygame.transform.flip(self.frames[self.cur_frame], True, False)
            self.c = 1
        if self.c == 1 and self.rect[0] == -59:
            self.image = pygame.transform.flip(self.frames[self.cur_frame], True, False)
            self.c = 0
        if bird_iter % 4 == 0:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            if self.c == 0:
                self.image = pygame.transform.flip(self.frames[self.cur_frame], True, False)
            else:
                self.image = self.frames[self.cur_frame]
        if bird_iter > 50:
            bird_iter = 0
        if self.c == 0:
            if bird_iter % random.choice(range(1, 2)) == 0:
                self.rect = self.rect.move(1, 0)
        else:
            if bird_iter % random.choice(range(1, 2)) == 0:
                self.rect = self.rect.move(-1, 0)

        if (v and aim.rect[0] - self.rect[0] < 25 and aim.rect[0] - self.rect[0] > -25 and aim.rect[1] -
                self.rect[1] < 25 and aim.rect[1] - self.rect[1] > -25):
            Explosion(explosion, 15, 1, self.rect[0], self.rect[1])
            self.kill()
            kol += 1


class Explosion(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(explosion_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.kad = 0

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
            self.kad += 1
        if self.kad == 15:
            self.kill()
            self.kad = 0
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



aim_img = pygame.transform.scale(load_image('aim.jpg', -1), (40, 40))
aim = pygame.sprite.Sprite(aim_sprite)
aim.image = aim_img
aim.rect = aim.image.get_rect()
aim.rect.x = 375
aim.rect.y = 207
kol = 20


def creature_bird():
    global kol
    if kol > 0:
        bird = pygame.transform.scale(load_image('bird_blue.png', -1), (170, 150))
        if kol % 2 == 0:
            x, y = random.choice(range(-508, -58)), random.choice(range(450))
        else:
            x, y = random.choice(range(825, 1275)), random.choice(range(450))
        Birds(bird, 3, 3, x, y)
        kol -= 1


explosion = pygame.transform.scale(load_image('explosion.png', -1), (530, 50))
running = True
motion = ''
while running:
    v = False
    screen.fill((130, 0, 255))
    creature_bird()
    birds_sprites.draw(screen)
    explosion_sprites.draw(screen)
    birds_sprites.update()
    explosion_sprites.update()
    aim_sprite.draw(screen)
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
            if event.key == pygame.K_SPACE:
                v = True
                birds_sprites.update()
        if event.type == pygame.KEYUP:
            motion = 'stop'
    if motion == 'left' and aim.rect[0] > 0:
        aim.rect = aim.rect.move(-5, 0)
    if motion == 'right' and aim.rect[0] < 750:
        aim.rect = aim.rect.move(5, 0)
    if motion == 'up' and aim.rect[1] > 0:
        aim.rect = aim.rect.move(0, -5)
    if motion == 'down' and aim.rect[1] < 415:
        aim.rect = aim.rect.move(0, 5)

    pygame.display.flip()
    clock.tick(70)

pygame.quit()
