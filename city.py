import random
from local_market import LocalMarket
from production_buildings import ProductionBuilding
from resources import ResourceName


class City:
    def __init__(self, name: str, local_market: LocalMarket, production_buildings: list[ProductionBuilding]):
        self.name = name
        self.development_level = 1.0  # Base development level, can be increased over time

        
        self.local_market = local_market
        self.production_buildings = production_buildings

    def consume_resources(self):
        """Consume random amounts of resources each game tick."""
        for resource_name in ResourceName:
            # Random consumption between 1 and 5 units
            consumption_amount = random.randint(0, 3)
            self.local_market.remove_consumed_resource(resource_name, consumption_amount)


    def produce_resources(self):
        for production_building in self.production_buildings:
            production_building.produce(self)

        
    def get_local_price(self, resource_name: ResourceName) -> float:
        """Get the current local price for a resource"""
        return self.local_market.current_price[resource_name]