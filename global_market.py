import random
from local_market import LocalMarket
from map import City
from npc import NPC
from resources import ResourceName
from collections import defaultdict


class GlobalMarket:

    def __init__(self, cities: list[City], npcs: list[NPC]):
        self.cities = cities
        self.npcs = npcs

        self.price_change_factor = 5
        self.number_of_ticks_for_average = 20
        self.total_gold = 0  
        self.base_prices = defaultdict(float)

        self.price_history = {
            ResourceName.Iron: [self.base_prices[ResourceName.Iron]]
        }
        
        # Track total consumption and production
        self.total_consumed = defaultdict(int)
        self.total_produced = defaultdict(int)
        self.total_amount = defaultdict(int)

        # Track history of consumption and production
        self.consumption_history = defaultdict(list)
        self.production_history = defaultdict(list)
        self.amount_history = defaultdict(list)
        self.base_prices_history = defaultdict(list)
        
        # Pre-populate with keys from base_prices
        for resource_name in self.base_prices.keys():
            self.total_consumed[resource_name] = 0
            self.total_produced[resource_name] = 0

        self.current_price = {
            ResourceName.Iron: self.get_resource_price(ResourceName.Iron)
        }

        self.local_markets: list[LocalMarket] = []
        self.price_value_modifiers = {
            ResourceName.Iron: 1.5,
            ResourceName.Wood: 1,
            ResourceName.Wheat: 0.5,
            ResourceName.Stone: 1,
            ResourceName.Tools: 2
        }
        self.market_share = defaultdict(float)
        

    def update_prices(self):
        # Calculate total consumption and production
        self.calculate_total_resource_consumed()
        self.calculate_total_resource_produced()
        self.calculate_total_resource_amount()
        self.calculate_total_gold()
        self.market_share = self.get_market_share()
        self.calculate_base_prices()
        
        for resource_name in self.price_history.keys():
            # Update price history
            self.price_history[resource_name].append(self.current_price[resource_name])
            self.current_price[resource_name] = self.get_resource_price(resource_name)

            self.consumption_history[resource_name].append(self.total_consumed[resource_name])
            self.production_history[resource_name].append(self.total_produced[resource_name])
            self.amount_history[resource_name].append(self.total_amount[resource_name])
            self.base_prices_history[resource_name].append(self.base_prices[resource_name])

        for local_market in self.local_markets:
            local_market.update_prices()

    def get_resource_price(self, resource_name: ResourceName) -> float:
        return (self.base_prices[resource_name] * (1 + self.get_resource_price_change(resource_name)))

    def get_resource_demand(self, resource_name: ResourceName) -> int:
        return self.get_recent_average_consumption(resource_name)

    def get_resource_supply(self, resource_name: ResourceName) -> int:
        return self.get_recent_average_production(resource_name) + self.total_amount[resource_name]

    def get_resource_price_change(self, resource_name: ResourceName) -> float:
        return self.price_change_factor * (self.get_resource_demand(resource_name) / (self.get_resource_supply(resource_name) + 1))
    
    def calculate_total_resource_consumed(self):
        """
        Calculate the total consumed resources across all cities.
        """
        # Reset totals
        for resource_name in self.total_consumed.keys():
            self.total_consumed[resource_name] = 0
            
        # Sum up consumption and production from all cities
        for local_market in self.local_markets:
            for resource_name in local_market.consumed_resources:
                self.total_consumed[resource_name] += local_market.consumed_resources[resource_name]
                
    
    def calculate_total_resource_produced(self):
        """
        Calculate the total produced resources across all cities.
        """
        # Reset totals
        for resource_name in self.total_produced.keys():
            self.total_produced[resource_name] = 0
            
        # Sum up consumption and production from all cities
        for local_market in self.local_markets:
            for resource_name in local_market.produced_resources:
                self.total_produced[resource_name] += local_market.produced_resources[resource_name]

        
    def calculate_total_resource_amount(self):
        """
        Calculate the total amount resources across all cities.
        """
        # Reset totals
        for resource_name in self.total_amount.keys():
            self.total_amount[resource_name] = 0
            
        # Sum up consumption and production from all cities
        for local_market in self.local_markets:
            for resource_name in local_market.resources:
                self.total_amount[resource_name] += local_market.resources[resource_name].amount

    def calculate_total_gold(self):
        """
        Calculate the total gold across all entities
        """
        self.total_gold = 0
        # Sum up consumption and production from all cities
        for local_market in self.local_markets:
            self.total_gold += local_market.gold
            
        for npc in self.npcs:
            self.total_gold += npc.gold

        return self.total_gold

    def calculate_base_prices(self):
        for resource_name, market_share in self.market_share.items():
            self.base_prices[resource_name] = market_share / max(1, self.total_amount[resource_name])
        return self.base_prices


    def get_recent_average_production(self, resource_name: ResourceName):
        return sum(self.production_history[resource_name][-self.number_of_ticks_for_average:]) / self.number_of_ticks_for_average
    
    def get_recent_average_consumption(self, resource_name: ResourceName):
        return sum(self.consumption_history[resource_name][-self.number_of_ticks_for_average:]) / self.number_of_ticks_for_average
    
    def get_proportional_value_for_single_unit(self):
        number_of_units_per_resource = [self.price_value_modifiers[resource_name] * ammount for resource_name, ammount in self.total_amount.items()]

        return self.total_gold / (sum(number_of_units_per_resource) + 1)
    
    def get_number_of_units_per_resource(self, aditional_resource_ammount: dict[ResourceName, int] = defaultdict(int)):
        return {resource_name: self.price_value_modifiers[resource_name] * (ammount + aditional_resource_ammount[resource_name]) for resource_name, ammount in self.total_amount.items()}
    
    
    def get_market_share(self, aditional_resource_ammount: dict[ResourceName, int] = defaultdict(int)):
        number_of_units_per_resource = self.get_number_of_units_per_resource(aditional_resource_ammount)
        price_of_single_unit = self.total_gold / (max(1, sum(number_of_units_per_resource.values())))
        market_share = {}
        for resource_name in self.total_amount.keys():
            market_share[resource_name] = number_of_units_per_resource[resource_name] * price_of_single_unit
        return market_share

    def estimate_base_resource_price(self, resource_name: ResourceName):
        aditional_resource_ammount = defaultdict(int)
        aditional_resource_ammount[resource_name] = 1
        market_share = self.get_market_share(aditional_resource_ammount)
        return market_share[resource_name] / max(1, self.total_amount[resource_name])            
