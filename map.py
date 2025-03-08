from resources import ResourceName, Resource

class City:
    def __init__(self, name: str, resources: dict[ResourceName, Resource]):
        self.name = name
        self.resources = resources

class GameMap:
    def __init__(self):
        self.cities: dict[str, City] = {}

    def add_city(self, city: City):
        self.cities[city.name] = city 

    def get_city(self, name: str) -> City | None:
        return self.cities.get(name, None)
