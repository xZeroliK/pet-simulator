import json
from random import randint
from button import *
from clothes_menu import ClothesMenu
from food_menu import FoodMenu
from mini_game import MiniGame
from dog import Dog
from toy import Toy


class Game:
    def __init__(self):
        # Создание окна
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("Виртуальный питомец")
        self.data = {}

        with open("save_data.json", encoding="utf-8") as f:
            self.data = json.load(f)

        self.happiness = self.data["happiness"]
        self.satiety = self.data["satiety"]
        self.health = self.data["health"]
        self.money = self.data["money"]
        self.coins_per_second = self.data["coins_per_second"]
        self.costs_of_upgrade = {}

        self.clock = pg.time.Clock()

        self.click_sound = pg.mixer.Sound("sounds/click_sound.mp3")
        self.click_sound.set_volume(0.3)

        for key, value in self.data["costs_of_upgrade"].items():
            self.costs_of_upgrade[int(key)] = value

        self.mode = "Main"

        self.background = load_image("images/background.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.body_image = load_image("images/dog.png", DOG_WIDTH, DOG_HEIGHT)
        self.happiness_image = load_image("images/happiness.png", ICON_SIZE, ICON_SIZE)
        self.food_image = load_image("images/satiety.png", ICON_SIZE, ICON_SIZE)
        self.health_image = load_image("images/health.png", ICON_SIZE, ICON_SIZE)
        self.money_image = load_image("images/money.png", ICON_SIZE, ICON_SIZE)

        button_x = SCREEN_WIDTH - BUTTON_WIDTH - PADDING

        self.eat_button = Button(
            "Еда",
            button_x,
            PADDING + ICON_SIZE,
            func=self.food_menu_on
        )
        self.clothes_button = Button(
            "Одежда",
            button_x,
            PADDING * 2 + ICON_SIZE + BUTTON_HEIGHT,
            func=self.clothes_menu_on
        )
        self.play_button = Button(
            "Игры",
            button_x,
            PADDING * 3 + ICON_SIZE + BUTTON_HEIGHT * 2,
            func=self.mini_game_on
        )
        self.upgrade_button = Button(
            "Улучшить",
            SCREEN_WIDTH - ICON_SIZE,
            0,
            width=BUTTON_WIDTH // 3,
            height=BUTTON_HEIGHT // 3,
            text_font=font_mini,
            func=self.increase_money
        )

        self.buttons = [
            self.eat_button,
            self.clothes_button,
            self.play_button,
            self.upgrade_button
        ]

        self.dog = Dog()

        self.clothes_menu = ClothesMenu(self, self.data["clothes"])
        self.food_menu = FoodMenu(self)
        self.mini_game = MiniGame(self)

        self.INCREASE_COINS = pg.USEREVENT + 1
        pg.time.set_timer(self.INCREASE_COINS, 1000)

        self.DECREASE = pg.USEREVENT + 1
        pg.time.set_timer(self.DECREASE, 1000)

        self.run()

    def increase_money(self):
        for cost, is_upgraded in self.data["costs_of_upgrade"].items():
            if not is_upgraded and self.money >= int(cost):
                self.coins_per_second += 1
                self.money -= int(cost)
                self.data["costs_of_upgrade"][cost] = True
                break

    def clothes_menu_on(self):
        self.mode = "Clothes menu"

    def food_menu_on(self):
        self.mode = "Food menu"

    def mini_game_on(self):
        self.mode = "Mini game"
        self.mini_game.new_game()

    def run(self):
        while True:
            self.event()
            self.update()
            self.draw()
            self.clock.tick(FPS)

    def event(self):
        for event_type in pg.event.get():
            if event_type.type == pg.QUIT:
                if self.mode == "Game over":
                    default_data = read_json("default_data.json")
                    write_json("save_data.json", default_data)
                else:
                    saved_data = change_data(self)
                    write_json("save_data.json", saved_data)

                pg.quit()
                exit()
            if event_type.type == pg.KEYDOWN:
                if event_type.key == pg.K_ESCAPE:
                    self.mode = "Main"

            if event_type.type == self.INCREASE_COINS:
                self.money += self.coins_per_second

            if event_type.type == self.DECREASE:
                chance = randint(1, 10)
                if chance <= 5:
                    self.satiety -= 1
                elif 5 < chance <= 9:
                    self.happiness -= 1
                else:
                    self.health -= 1

            if event_type.type == pg.MOUSEBUTTONDOWN:
                if event_type.button == 1:
                    self.money += self.coins_per_second
                    self.click_sound.play()

            if self.mode == "Main":
                for button in self.buttons:
                    button.is_clicked(event_type)
            elif self.mode == "Clothes menu":
                self.clothes_menu.is_clicked(event_type)
            elif self.mode == "Food menu":
                self.food_menu.is_clicked(event_type)

    def update(self):
        if self.mode == "Clothes menu":
            self.clothes_menu.update()
        elif self.mode == "Food menu":
            self.food_menu.update()
        elif self.mode == "Mini game":
            self.mini_game.update()
        elif self.mode == "Main":
            for button in self.buttons:
                button.update()

        for indicator in ("happiness", "health", "satiety"):
            value = getattr(self, indicator)

            if value <= 0:
                setattr(self, indicator, 0)
                self.mode = "Game over"
                break

        # if self.happiness <= 0 or self.satiety <= 0 or self.health <= 0:
        #     self.mode = "Game over"

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.happiness_image, (PADDING, PADDING))
        self.screen.blit(self.food_image, (PADDING, PADDING * 2 + ICON_SIZE))
        self.screen.blit(self.health_image, (PADDING, PADDING * 3 + ICON_SIZE * 2))
        self.screen.blit(self.money_image, (SCREEN_WIDTH - PADDING - ICON_SIZE, PADDING))
        self.screen.blit(self.body_image, (SCREEN_WIDTH // 2 - DOG_WIDTH // 2, DOG_Y))

        self.screen.blit(text_render(self.happiness), (PADDING + ICON_SIZE, PADDING * 6))
        self.screen.blit(text_render(self.satiety), (PADDING + ICON_SIZE, PADDING * 7 + ICON_SIZE))
        self.screen.blit(text_render(self.health), (PADDING + ICON_SIZE, PADDING * 8 + ICON_SIZE * 2))
        self.screen.blit(text_render(self.money), (SCREEN_WIDTH - PADDING - ICON_SIZE - PADDING * 7, PADDING * 6))

        for button in self.buttons:
            button.draw(self.screen)

        for item in self.clothes_menu.items:
            if item.is_using:
                self.screen.blit(item.full_image, (SCREEN_WIDTH // 2 - DOG_WIDTH // 2, DOG_Y))

        if self.mode == "Clothes menu":
            self.clothes_menu.draw(self.screen)
        elif self.mode == "Food menu":
            self.food_menu.draw(self.screen)
        elif self.mode == "Mini game":
            self.mini_game.draw(self.screen)
        elif self.mode == "Game over":
            text = font_maxi.render("ПРОИГРЫШ", True, "red")
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(text, text_rect)

        pg.display.flip()


if __name__ == "__main__":
    Game()
