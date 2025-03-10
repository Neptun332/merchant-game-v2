import random
from map import City
from npc import NPC
from resources import ResourceName

class GlobalMarket:

    def __init__(self, cities: list[City], npcs: list[NPC]):
        self.cities = cities
        self.npcs = npcs

        self.base_prices = {
            ResourceName.Iron: 100
        }
        self.price_history = {
            ResourceName.Iron: [self.base_prices[ResourceName.Iron]]
        }
        self.current_price = {
            ResourceName.Iron: self.get_resource_price(ResourceName.Iron)
        }

    def update_prices(self):
        for resource_name in self.price_history.keys():
            self.price_history[resource_name].append(self.current_price[resource_name])
            self.current_price[resource_name] = self.get_resource_price(resource_name)

    def get_resource_price(self, resource_name: ResourceName) -> float:
        return (self.base_prices[resource_name] * (1 + self.get_resource_price_change(resource_name)))

    def get_resource_demand(self, resource_name: ResourceName) -> float:
        return random.randint(0, 10)

    def get_resource_supply(self, resource_name: ResourceName) -> float:
        return random.randint(0, 10)

    def get_resource_price_change(self, resource_name: ResourceName) -> float:
        return 0.1 * (self.get_resource_demand(resource_name) / (self.get_resource_supply(resource_name) + 1))

