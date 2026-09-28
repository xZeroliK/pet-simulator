from functions import *
from constants import *

class Food:
    def __init__(self, name, price, file, satiety, medicine_power=0):
        self.name = name
        self.price = price
        self.satiety = satiety
        self.medicine_power = medicine_power
        self.image = load_image(file, FOOD_SIZE, FOOD_SIZE)