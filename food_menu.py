from functions import *
from constants import *
from food import Food
from button import Button


class FoodMenu:
    def __init__(self, game):
        self.game = game
        self.menu_page = load_image("images/menu/menu_page.png", SCREEN_WIDTH, SCREEN_HEIGHT)

        self.bottom_label_off = load_image("images/menu/bottom_label_off.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.bottom_label_on = load_image("images/menu/bottom_label_on.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.top_label_off = load_image("images/menu/top_label_off.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.top_label_on = load_image("images/menu/top_label_on.png", SCREEN_WIDTH, SCREEN_HEIGHT)

        self.items = [
            Food("Мясо", 30, "images/food/meat.png", 10),
            Food("Корм", 40, "images/food/dog food.png", 15),
            Food("Элитный корм", 100, "images/food/dog food elite.png", 25, medicine_power=2),
            Food("Лекарство", 200, "images/food/medicine.png", 0, medicine_power=10)
        ]

        self.current_item = 0

        self.item_rect = self.items[0].image.get_rect()
        self.item_rect.center = (SCREEN_WIDTH // ITEM_RECT_RATIO, SCREEN_HEIGHT // ITEM_RECT_RATIO)

        self.next_button = Button(
            "Вперёд",
            SCREEN_WIDTH - MENU_NAV_XPAD - BUTTON_WIDTH,
            SCREEN_HEIGHT - MENU_NAV_YPAD,
            width=int(BUTTON_WIDTH // MENU_BUTTON_RATIO),
            height=int(BUTTON_HEIGHT // MENU_BUTTON_RATIO),
            func=self.to_next
        )
        self.prev_button = Button(
            "Назад",
            MENU_NAV_XPAD + 30,
            SCREEN_HEIGHT - MENU_NAV_YPAD,
            width=int(BUTTON_WIDTH // MENU_BUTTON_RATIO),
            height=int(BUTTON_HEIGHT // MENU_BUTTON_RATIO),
            func=self.to_prev
        )
        self.buy_button = Button(
            "Съесть",
            SCREEN_WIDTH // 2 - (BUTTON_WIDTH // 1.5) // 2,
            SCREEN_HEIGHT // 2 + 95,
            width=int(BUTTON_WIDTH // 1.5),
            height=int(BUTTON_HEIGHT // 1.5),
            func=self.buy
        )

        self.price_text = text_render(self.items[self.current_item].price)
        self.price_text_rect = self.price_text.get_rect()
        self.price_text_rect.center = (SCREEN_WIDTH // 2, 180)

        self.name_text = text_render(self.items[self.current_item].name)
        self.name_text_rect = self.name_text.get_rect()
        self.name_text_rect.center = (SCREEN_WIDTH // 2, 120)

    def to_next(self):
        if self.current_item != len(self.items) - 1:
            self.current_item += 1

        self.price_text = text_render(self.items[self.current_item].price)
        self.price_text_rect = self.price_text.get_rect()
        self.price_text_rect.center = (SCREEN_WIDTH // 2, 180)

        self.name_text = text_render(self.items[self.current_item].name)
        self.name_text_rect = self.name_text.get_rect()
        self.name_text_rect.center = (SCREEN_WIDTH // 2, 120)

    def to_prev(self):
        if self.current_item != 0:
            self.current_item -= 1

        self.price_text = text_render(self.items[self.current_item].price)
        self.price_text_rect = self.price_text.get_rect()
        self.price_text_rect.center = (SCREEN_WIDTH // 2, 180)

        self.name_text = text_render(self.items[self.current_item].name)
        self.name_text_rect = self.name_text.get_rect()
        self.name_text_rect.center = (SCREEN_WIDTH // 2, 120)

    def buy(self):
        if self.game.money >= self.items[self.current_item].price:
            self.game.money -= self.items[self.current_item].price

            self.game.satiety += self.items[self.current_item].satiety
            if self.game.satiety > 100:
                self.game.satiety = 100

            self.game.health += self.items[self.current_item].medicine_power
            if self.game.health > 100:
                self.game.health = 100

    def update(self):
        self.next_button.update()
        self.prev_button.update()
        self.buy_button.update()

    def is_clicked(self, event):
        self.next_button.is_clicked(event)
        self.prev_button.is_clicked(event)
        self.buy_button.is_clicked(event)

    def draw(self, screen):
        screen.blit(self.menu_page, (0, 0))
        screen.blit(self.items[self.current_item].image, self.item_rect)

        self.next_button.draw(screen)
        self.prev_button.draw(screen)
        self.buy_button.draw(screen)

        screen.blit(self.price_text, self.price_text_rect)
        screen.blit(self.name_text, self.name_text_rect)
