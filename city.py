import random
from local_market import LocalMarket
from resources import Resource, ResourceName


class City:
    def __init__(self, name: str, local_market: LocalMarket):
        self.name = name
        self.development_level = 1.0  # Base development level, can be increased over time

        
        self.local_market = local_market

    def consume_resources(self):
        """Consume random amounts of resources each game tick."""
        for resource_name in ResourceName:
            # Random consumption between 1 and 5 units
            consumption_amount = random.randint(0, 3)
            self.local_market.remove_consumed_resource(resource_name, consumption_amount)


    def produce_resources(self):
        """Produce resources based on city development level each game tick."""
        for resource_name in ResourceName:
            # Base production is 1-3 units, multiplied by development level
            base_production = random.randint(1, 2)
            production_amount = int(base_production * self.development_level)
            self.local_market.add_produced_resource(resource_name, production_amount)

        
    def get_local_price(self, resource_name: ResourceName) -> float:
        """Get the current local price for a resource"""
        return self.local_market.current_price[resource_name]