from collections import defaultdict
from resources import ResourceName, Resource

class LocalMarket:
    def __init__(self, global_market: 'GlobalMarket',  resources: dict[ResourceName, Resource]):        
        self.global_market = global_market
        self.global_market.local_markets.append(self)

        self.resources = resources
        self.gold = 500
        self.price_change_factor = 5

        self.produced_resources = defaultdict(int)
        self.consumed_resources = defaultdict(int)
        
        # Price data
        self.base_prices = defaultdict(int)
        self.current_price = defaultdict(float)
        self.price_history = defaultdict(list)
        
        # History tracking
        self.consumption_history = defaultdict(list)
        self.production_history = defaultdict(list)
        self.amount_history = defaultdict(list)
        
        self.base_prices = self.global_market.current_price
        self.current_price[ResourceName.Iron] = self.base_prices[ResourceName.Iron]
        self.price_history[ResourceName.Iron] = [self.current_price[ResourceName.Iron]]
        
    
    def update_prices(self):      
        self.base_prices = self.global_market.current_price
        
        # Update prices and history
        for resource_name in self.base_prices.keys():
            self.current_price[resource_name] = self.get_resource_price(resource_name)
            self.price_history[resource_name].append(self.current_price[resource_name])
            
            # Update history
            self.consumption_history[resource_name].append(self.consumption_history[resource_name])
            self.production_history[resource_name].append(self.production_history[resource_name])
            self.amount_history[resource_name].append(self.resources[resource_name].amount)

    def get_resource_price(self, resource_name: ResourceName) -> float:
        """Calculate the current price for a resource"""
        return self.base_prices[resource_name] * (1 + self.get_resource_price_change(resource_name))
    
    def get_resource_demand(self, resource_name: ResourceName) -> int:
        """Get the current demand for a resource"""
        return self.consumed_resources[resource_name]
    
    def get_resource_supply(self, resource_name: ResourceName) -> int:
        """Get the current supply for a resource"""
        return self.produced_resources[resource_name] + self.resources[resource_name].amount
    
    def get_resource_price_change(self, resource_name: ResourceName) -> float:
        return self.price_change_factor * (self.get_resource_demand(resource_name) / (self.get_resource_supply(resource_name) + 1))
    
    def add_produced_resource(self, resource_name: ResourceName, amount: int):
        self.resources[resource_name].amount += amount
        self.produced_resources[resource_name] = amount

    def remove_consumed_resource(self, resource_name: ResourceName, amount: int):
        # Ensure we don't consume more than available
        actual_consumption = min(amount, self.resources[resource_name].amount)
        self.resources[resource_name].amount -= actual_consumption
        self.consumed_resources[resource_name] = actual_consumption
    