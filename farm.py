import random
from enum import Enum

class Season(Enum):
    SPRING = 1
    SUMMER = 2
    FALL = 3
    WINTER = 4

class Crop:
    def __init__(self, name, growth_time, sell_price):
        self.name = name
        self.growth_time = growth_time
        self.sell_price = sell_price
        self.current_growth = 0

class Animal:
    def __init__(self, name, product, production_time, sell_price):
        self.name = name
        self.product = product
        self.production_time = production_time
        self.sell_price = sell_price
        self.current_production = 0

class FarmGame:
    def __init__(self):
        self.day = 1
        self.season = Season.SPRING
        self.money = 1000
        self.crops = []
        self.animals = []
        self.inventory = {}

    def plant_crop(self, crop):
        if self.money >= 10:  # Assume planting cost is 10
            self.crops.append(crop)
            self.money -= 10
            print(f"Planted {crop.name}")
        else:
            print("Not enough money to plant crop")

    def buy_animal(self, animal):
        if self.money >= 50:  # Assume animal cost is 50
            self.animals.append(animal)
            self.money -= 50
            print(f"Bought {animal.name}")
        else:
            print("Not enough money to buy animal")

    def harvest_crops(self):
        for crop in self.crops[:]:
            if crop.current_growth >= crop.growth_time:
                self.crops.remove(crop)
                self.inventory[crop.name] = self.inventory.get(crop.name, 0) + 1
                print(f"Harvested {crop.name}")

    def collect_animal_products(self):
        for animal in self.animals:
            if animal.current_production >= animal.production_time:
                animal.current_production = 0
                self.inventory[animal.product] = self.inventory.get(animal.product, 0) + 1
                print(f"Collected {animal.product} from {animal.name}")

    def sell_products(self):
        for item, quantity in self.inventory.items():
            if quantity > 0:
                sell_price = next((c.sell_price for c in [Crop("Wheat", 0, 0), Crop("Corn", 0, 0), Animal("Cow", "Milk", 0, 0)] if c.name == item or c.product == item), 0)
                earnings = sell_price * quantity
                self.money += earnings
                print(f"Sold {quantity} {item}(s) for ${earnings}")
        self.inventory = {}

    def advance_day(self):
        self.day += 1
        if self.day % 30 == 1:
            self.season = Season((self.season.value % 4) + 1)
            print(f"New season: {self.season.name}")

        for crop in self.crops:
            crop.current_growth += 1

        for animal in self.animals:
            animal.current_production += 1

        self.harvest_crops()
        self.collect_animal_products()

    def display_status(self):
        print(f"\nDay: {self.day}, Season: {self.season.name}, Money: ${self.money}")
        print("Crops:", ", ".join(crop.name for crop in self.crops))
        print("Animals:", ", ".join(animal.name for animal in self.animals))
        print("Inventory:", dict(self.inventory))

def main():
    game = FarmGame()
    wheat = Crop("Wheat", 7, 20)
    corn = Crop("Corn", 10, 30)
    cow = Animal("Cow", "Milk", 3, 25)

    while True:
        game.display_status()
        action = input("Enter action (plant/buy/sell/next/quit): ").lower()

        if action == "plant":
            crop_choice = input("Choose crop to plant (wheat/corn): ").lower()
            if crop_choice == "wheat":
                game.plant_crop(wheat)
            elif crop_choice == "corn":
                game.plant_crop(corn)

        elif action == "buy":
            game.buy_animal(cow)

        elif action == "sell":
            game.sell_products()

        elif action == "next":
            game.advance_day()

        elif action == "quit":
            break

        else:
            print("Invalid action")

if __name__ == "__main__":
    main()