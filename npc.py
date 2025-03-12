from resources import ResourceName, Resource
from map import City
import random

class NPC:
    def __init__(self, name: str, resources: dict[ResourceName, Resource]):
        self.name = name
        self.resources = resources
        self.gold = 500

    def trade(self, city: City):
        pass
        # """Trade with a city using local market prices"""
        # # Simple trade logic - buy or sell based on price and available resources
        # for resource_name, resource in self.resources.items():
        #     if resource_name in city.resources:
        #         # Get local price from city's market
        #         local_price = city.get_local_price(resource_name)
                
        #         # Decide whether to buy or sell based on price and random chance
        #         if random.random() < 0.5:  # 50% chance to attempt a buy
        #             self.try_buy_resource(city, resource_name, local_price)
        #         else:  # 50% chance to attempt a sell
        #             self.try_sell_resource(city, resource_name, local_price)
    
    def try_buy_resource(self, city: City, resource_name: ResourceName, price: float):
        """Try to buy a resource from the city"""
        # Only buy if city has resources and NPC has enough gold
        city_resource = city.resources[resource_name]
        if city_resource.amount > 0 and self.gold >= price:
            # Buy 1 unit
            amount_to_buy = 1
            cost = amount_to_buy * price
            
            # Transfer resource and gold
            city_resource.amount -= amount_to_buy
            self.resources[resource_name].amount += amount_to_buy
            self.gold -= cost
            city.gold += cost
    
    def try_sell_resource(self, city: City, resource_name: ResourceName, price: float):
        """Try to sell a resource to the city"""
        # Only sell if NPC has resources and city has enough gold
        if self.resources[resource_name].amount > 0 and city.gold >= price:
            # Sell 1 unit
            amount_to_sell = 1
            revenue = amount_to_sell * price
            
            # Transfer resource and gold
            self.resources[resource_name].amount -= amount_to_sell
            city.resources[resource_name].amount += amount_to_sell
            self.gold += revenue
            city.gold -= revenue