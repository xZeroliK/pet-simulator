import random

from functions import *
from constants import *


class Toy(pg.sprite.Sprite):
    def __init__(self, image_list):
        pg.sprite.Sprite.__init__(self)
        self.random_image = get_random_item(image_list)
        self.image = load_image(f"images/toys/{self.random_image}", TOY_SIZE, TOY_SIZE)
        self.rect = self.image.get_rect()
        self.rect.y = MENU_NAV_YPAD // 2 - 25
        self.rect.x = random.randint(MENU_NAV_XPAD, SCREEN_WIDTH - MENU_NAV_XPAD - self.image.get_width())
        self.fall_speed = 5

    def update(self):
        if self.rect.top <= SCREEN_HEIGHT - MENU_NAV_YPAD:
            self.rect.y += self.fall_speed
        else:
            self.kill()
