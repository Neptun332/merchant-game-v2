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
        
        # Track total consumption and production
        self.total_consumed = defaultdict(int)
        self.total_produced = defaultdict(int)
        
        # Track history of consumption and production
        self.consumption_history = {ResourceName.Iron: [0]}
        self.production_history = {ResourceName.Iron: [0]}
        self.net_change_history = {ResourceName.Iron: [0]}
        
        # Pre-populate with keys from base_prices
        for resource_name in self.base_prices.keys():
            self.total_consumed[resource_name] = 0
            self.total_produced[resource_name] = 0

        self.current_price = {
            ResourceName.Iron: self.get_resource_price(ResourceName.Iron)
        }
        

    def update_prices(self):
        # Calculate total consumption and production
        self.calculate_total_resource_consumed()
        self.calculate_total_resource_produced()
        
        for resource_name in self.price_history.keys():
            # Update price history
            self.price_history[resource_name].append(self.current_price[resource_name])
            self.current_price[resource_name] = self.get_resource_price(resource_name)
            
            # Update consumption and production history
            if resource_name in self.total_consumed:
                self.consumption_history[resource_name].append(self.total_consumed[resource_name])
            
            if resource_name in self.total_produced:
                self.production_history[resource_name].append(self.total_produced[resource_name])
                
            # Calculate and update net change history
            net_change = self.total_produced.get(resource_name, 0) - self.total_consumed.get(resource_name, 0)
            if resource_name in self.net_change_history:
                self.net_change_history[resource_name].append(net_change)
            else:
                self.net_change_history[resource_name] = [net_change]

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
            
        # Sum up consumption from all cities
        for city_name, city in self.cities.items():
            if hasattr(city, 'consumed_resources'):
                for resource_name, amount in city.consumed_resources.items():
                    # defaultdict will automatically create entry with default value 0 if key doesn't exist
                    self.total_consumed[resource_name] += amount
                
        return self.total_consumed
    
    def calculate_total_resource_produced(self):
        """
        Calculate the total produced resources across all cities.
        """
        # Reset totals
        for resource_name in self.total_produced.keys():
            self.total_produced[resource_name] = 0
            
        # Sum up production from all cities
        for city_name, city in self.cities.items():
            if hasattr(city, 'produced_resources'):
                for resource_name, amount in city.produced_resources.items():
                    # defaultdict will automatically create entry with default value 0 if key doesn't exist
                    self.total_produced[resource_name] += amount
            
        return self.total_produced