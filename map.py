from resources import ResourceName, Resource
import random

class City:
    def __init__(self, name: str, resources: dict[ResourceName, Resource]):
        self.name = name
        self.resources = resources
        self.development_level = 1.0  # Base development level, can be increased over time
        self.gold = 500

        self.produced_resources = {}
        self.consumed_resources = {}

    def consume_resources(self):
        """Consume random amounts of resources each game tick."""
        for resource_name, resource in self.resources.items():
            # Random consumption between 1 and 5 units
            consumption_amount = random.randint(0, 3)
            # Ensure we don't consume more than available
            actual_consumption = min(consumption_amount, resource.amount)
            resource.amount -= actual_consumption
            self.consumed_resources[resource_name] = actual_consumption

    def produce_resources(self):
        """Produce resources based on city development level each game tick."""
        for resource_name, resource in self.resources.items():
            # Base production is 1-3 units, multiplied by development level
            base_production = random.randint(1, 2)
            production_amount = int(base_production * self.development_level)
            resource.amount += production_amount
            self.produced_resources[resource_name] = production_amount

class GameMap:
    def __init__(self):
        self.cities: dict[str, City] = {}

    def add_city(self, city: City):
        self.cities[city.name] = city 

    def get_city(self, name: str) -> City | None:
        return self.cities.get(name, None)
