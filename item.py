from functions import *
from constants import *


class Item:
    def __init__(self, name, price, file, is_bought=False, is_using=False):
        self.name = name
        self.price = price
        self.is_bought = is_bought
        self.is_using = is_using
        self.file = file

        self.image = load_image(self.file, DOG_WIDTH // ITEM_RATIO, DOG_HEIGHT // ITEM_RATIO)
        self.full_image = load_image(self.file, DOG_WIDTH, DOG_HEIGHT)
