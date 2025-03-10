import random
from map import City
from npc import NPC
from resources import ResourceName
from collections import defaultdict
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

        self.total_consumed = defaultdict(int)        # Track total consumption and production
        self.total_produced = defaultdict(int)

        self.current_price = {
            ResourceName.Iron: self.get_resource_price(ResourceName.Iron)
        }
        

    def update_prices(self):
        for resource_name in self.price_history.keys():
            self.calculate_total_resource_consumed()
            self.calculate_total_resource_produced()
            self.price_history[resource_name].append(self.current_price[resource_name])
            self.current_price[resource_name] = self.get_resource_price(resource_name)

    def get_resource_price(self, resource_name: ResourceName) -> float:
        return (self.base_prices[resource_name] * (1 + self.get_resource_price_change(resource_name)))

    def get_resource_demand(self, resource_name: ResourceName) -> int:
        return self.total_consumed[resource_name]

    def get_resource_supply(self, resource_name: ResourceName) -> int:
        return self.total_produced[resource_name]

    def get_resource_price_change(self, resource_name: ResourceName) -> float:
        return 0.1 * (self.get_resource_demand(resource_name) / (self.get_resource_supply(resource_name) + 1))
    
    def calculate_total_resource_consumed(self):
        """
        Calculate the total consumed resources across all cities.
        """
        # Reset totals
        for resource_name in self.total_consumed.keys():
            self.total_consumed[resource_name] = 0
            
        # Sum up consumption and production from all cities
        for city in self.cities.values():
            for resource_name in city.consumed_resources:
                self.total_consumed[resource_name] += city.consumed_resources[resource_name]
                
        return self.total_consumed
    
    def calculate_total_resource_produced(self):
        """
        Calculate the total consumed and produced resources across all cities.
        """
        # Reset totals
        for resource_name in self.total_produced.keys():
            self.total_produced[resource_name] = 0
            
        # Sum up consumption and production from all cities
        for city in self.cities.values():                
            for resource_name in city.produced_resources:
                self.total_produced[resource_name] += city.produced_resources[resource_name]
            
        return self.total_produced