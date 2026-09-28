import pygame as pg
from constants import *
from functions import load_image


class Dog(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = load_image('images/dog.png', DOG_WIDTH // 2, DOG_HEIGHT // 2)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.centery = SCREEN_HEIGHT - MENU_NAV_YPAD - 10

        self.speed = 4

    def update(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.rect.x -= self.speed
        elif keys[pg.K_d]:
            self.rect.x += self.speed
        if self.rect.left <= MENU_NAV_XPAD:
            self.rect.x += self.speed
        elif self.rect.right >= SCREEN_WIDTH - MENU_NAV_XPAD:
            self.rect.x -= self.speed
