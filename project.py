import pygame
import sys
import os
import random
import time

pygame.init()
size = width, height = 825, 490
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()


all_sprites = pygame.sprite.Group()


class Birds(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows):
        super().__init__(all_sprites)
        self.kol = 15
        while self.kol > 0:
            self.frames = []
            self.cut_sheet(sheet, columns, rows)
            self.cur_frame = 0
            self.image = self.frames[self.cur_frame]
            self.rect = self.rect.move(random.choice((0, 600)), random.choice(range(450)))
            print(self.rect)
            self.kol -= 1
            pygame.display.flip()

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
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class Explosion(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
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
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


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
bird = pygame.transform.scale(load_image('bird_blue.png', -1), (170, 150))
bird = Birds(bird, 3, 3)
explosion = pygame.transform.scale(load_image('explosion.png', -1), (710, 60))
explosion = Explosion(explosion, 15, 1, 400, 150)
x = 375
y = 207
running = True
motion = ''
while running:
    screen.fill((255, 0, 255))
    all_sprites.draw(screen)
    all_sprites.update()
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
        x -= 30
    if motion == 'right' and x < 750:
        x += 30
    if motion == 'up' and y > 0:
        y -= 30
    if motion == 'down' and y < 415:
        y += 30
    pygame.display.flip()
    clock.tick(15)

pygame.quit()
>>>>>>> Stashed changes
