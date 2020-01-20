import pygame
import sys
import os
import random
import sqlite3

pygame.init()
size = width, height = 825, 550
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
pygame.display.set_caption('ОХОТА НА ПТИЧЕК')

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
        global bird_iter, kol, killed_birds
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
            killed_birds += 1


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
time1 = 60
con = sqlite3.connect('records.db')
cur = con.cursor()
best_result = cur.execute("""SELECT best_result FROM best_results""").fetchall()
con.close()
explosion = pygame.transform.scale(load_image('explosion.png', -1), (530, 50))
sky = pygame.transform.scale(load_image('sky.jpg'), (825, 490))


def terminate():
    pygame.quit()
    sys.exit()


def creature_bird():
    global kol
    if kol > 0:
        bird = pygame.transform.scale(load_image('bird_blue.png', -1), (170, 150))
        if kol % 2 == 0:
            x, y = random.choice(range(-508, -58)), random.choice(range(440))
        else:
            x, y = random.choice(range(825, 1275)), random.choice(range(440))
        Birds(bird, 3, 3, x, y)
        kol -= 1


def game_over():
    while True:
        screen.blit(sky, (0, 0))
        the_end = pygame.font.Font(None, 56).render("Игра окончена!", 1, (0, 56, 65))
        new_game = pygame.font.Font(None, 26).render('Чтобы начать новую игру, нажмите "пробел"', 1, (0, 56, 65))
        screen.blit(new_game, (243, 300))
        screen.blit(the_end, (283, 250))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
        pygame.display.flip()


class Menu:
    def __init__(self, punkts=[120, 140, u'Punkt', (250, 250, 30), (224, 176, 255)]):
        self.punkts = punkts

    def render(self, poverh, font, num_punkt):
        for i in self.punkts:
            if num_punkt == i[5]:
                poverh.blit(font.render(i[2], 1, i[4]), (i[0], i[1]))
            else:
                poverh.blit(font.render(i[2], 1, i[3]), (i[0], i[1]))

    def menu(self):
        done = True
        pygame.font.init()
        menu_font = pygame.font.SysFont('Comic Sana MS', 100)
        punkt = 0
        while done:
            screen.fill((204, 235, 255))
            mp = pygame.mouse.get_pos()
            for i in self.punkts:
                if mp[0] > i[0] and mp[0] < i[0] + 155 and mp[1] > i[1] and mp[1] < i[1] + 50:
                    punkt = i[5]
            self.render(screen, menu_font, punkt)

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        sys.exit()
                    if e.key == pygame.K_UP:
                        if punkt > 0:
                            punkt -= 1
                    if e.key == pygame.K_DOWN:
                        if punkt < len(self.punkts) - 1:
                            punkt += 1
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    if punkt == 0:
                        done = False
                    elif punkt == 1:
                        sys.exit()
            screen.blit(screen, (0, 0))
            pygame.display.flip()


punkts = [(120, 140, u'ИГРАТЬ', (184, 121, 175), (51, 3, 66), 0),
          (130, 210, u'ВЫХОД', (184, 121, 175), (51, 3, 66), 1)]
game = Menu(punkts)
game.menu()


def start_screen():
    while True:
        screen.blit(sky, (0, 0))
        screen.fill((166, 189, 215), pygame.Rect(0, 490, 825, 60))
        new_game = pygame.font.Font(None, 26).render('Чтобы начать игру, нажмите "пробел"', 1, (0, 56, 65))
        screen.blit(new_game, (243, 300))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
        pygame.display.flip()


running = True
motion = ''
killed_birds = 0

while running:
    v = False
    if time1 >= -1:
        time1 -= 1 / 70
    if int(time1) == 0 and time1 < 0:
        if best_result[0][0] < killed_birds:
            con = sqlite3.connect('records.db')
            cur = con.cursor()
            inquiry = 'UPDATE best_results SET best_result = ' + str(killed_birds)
            best_result = cur.execute(inquiry).fetchall()
            best_result = cur.execute("""SELECT best_result FROM best_results""").fetchall()
            con.commit()
            con.close()
        game_over()
        punkts = [(120, 140, u'ИГРАТЬ', (184, 121, 175), (51, 3, 66), 0),
                  (130, 210, u'ВЫХОД', (184, 121, 175), (51, 3, 66), 1)]
        game = Menu(punkts)
        game.menu()
        time1 = 60
        birds_sprites.empty()
        kol = 20
        killed_birds = 0
    screen.blit(sky, (0, 0))
    screen.fill((166, 189, 215), pygame.Rect(0, 490, 825, 60))
    f1 = pygame.font.Font(None, 36)
    text1 = f1.render(str(killed_birds), 1, (0, 0, 0))
    screen.blit(text1, (250, 505))
    text2 = f1.render('Количество птичек:', 1, (0, 0, 0))
    screen.blit(text2, (5, 505))
    text3 = f1.render('Время:', 1, (0, 0, 0))
    screen.blit(text3, (350, 505))
    text4 = f1.render(str(int(time1)), 1, (0, 0, 0))
    screen.blit(text4, (440, 505))
    best = f1.render('Лучший результат:', 1, (0, 0, 0))
    screen.blit(best, (510, 505))
    text5 = f1.render(str(best_result[0][0]), 1, (0, 0, 0))
    screen.blit(text5, (750, 505))

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
    if motion == 'down' and aim.rect[1] < 448:
        aim.rect = aim.rect.move(0, 5)

    pygame.display.flip()
    clock.tick(70)

pygame.quit()
