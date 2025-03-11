from resources import ResourceName, Resource
import random
from local_market import LocalMarket
from city import City


class GameMap:
    def __init__(self):
        self.cities: dict[str, City] = {}

    def add_city(self, city: City):
        self.cities[city.name] = city 

    def get_city(self, name: str) -> City | None:
        return self.cities.get(name, None)
