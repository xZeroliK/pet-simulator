import random

from toy import Toy
from constants import *
from dog import Dog
from functions import *


class MiniGame:
    def __init__(self, game):
        self.game = game
        self.background = load_image("images/game_background.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.pet = Dog()
        self.toys = pg.sprite.Group()
        self.score = 0
        self.start_time = pg.time.get_ticks()
        self.game_time = 1000 * 5

        self.toys_images = ["ball.png", "blue bone.png", "red bone.png"]

    def new_game(self):
        self.pet = self.pet
        self.toys = pg.sprite.Group()
        self.score = 0
        self.start_time = pg.time.get_ticks()
        self.game_time = 1000 * 5

    def update(self):
        self.pet.update()
        self.toys.update()

        if random.randint(0, 100) == 0:
            self.toys.add(Toy(self.toys_images))

        hits = pg.sprite.spritecollide(self.pet, self.toys, True, pg.sprite.collide_rect_ratio(0.6))
        self.score += len(hits)

        if pg.time.get_ticks() - self.start_time > self.game_time:
            self.game.happiness += self.score // 2
            self.game.mode = "Main"

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        screen.blit(self.pet.image, self.pet.rect)
        screen.blit(text_render(self.score), (MENU_NAV_XPAD + 20, 80))
        self.toys.draw(screen)
