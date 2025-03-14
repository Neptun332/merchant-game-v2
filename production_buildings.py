

from abc import ABC, abstractmethod
import random
from resources import ResourceName

class ProductionBuilding(ABC):

    def can_produce(self, city: 'City') -> bool:
        """Check if the building can produce resources based on current resource availability."""
        if len(self.required_resources_for_one_production_cycle) == 0:
            return True
        return all([city.local_market.resources[resource_name].amount >= required_amount 
                     for resource_name, required_amount in self.required_resources_for_one_production_cycle.items()])
    
    def is_production_worth_it(self, city: 'City') -> bool:
        """Check if the production is worth it based on current resource prices."""
        cost_of_all_required_resources = sum([city.local_market.current_price[resource_name] * required_amount  for resource_name, required_amount in self.required_resources_for_one_production_cycle.items()])
        cost_of_all_produced_resources = city.local_market.global_market.estimate_base_resource_price(self.produced_resource) * int(2 * self.level) #TODO: Change this
        return cost_of_all_produced_resources > cost_of_all_required_resources
        

    def produce(self, city: 'City'):
        if self.can_produce(city) and self.is_production_worth_it(city):
            base_production = random.randint(1, 2)
            production_amount = int(base_production * self.level)
            city.local_market.add_produced_resource(self.produced_resource, production_amount)

    @property
    @abstractmethod
    def produced_resource(self):
        pass

    @property
    @abstractmethod
    def level(self):
        pass

    @property
    @abstractmethod
    def required_resources_for_one_production_cycle(self):
        pass
    
    

class Farm(ProductionBuilding):

    def __init__(self) -> None:
        self._produced_resource = ResourceName.Wheat
        self._level = 1
        self._required_resources_for_one_production_cycle = {}

    @property
    def produced_resource(self):
        return self._produced_resource

    @property
    def level(self):
        return self._level

    @property
    def required_resources_for_one_production_cycle(self):
        return self._required_resources_for_one_production_cycle
    
class IronMine(ProductionBuilding):

    def __init__(self) -> None:
        self._produced_resource = ResourceName.Iron
        self._level = 1
        self._required_resources_for_one_production_cycle = {}

    @property
    def produced_resource(self):
        return self._produced_resource

    @property
    def level(self):
        return self._level

    @property
    def required_resources_for_one_production_cycle(self):
        return self._required_resources_for_one_production_cycle
    
class WoodCutterCottage(ProductionBuilding):

    def __init__(self) -> None:
        self._produced_resource = ResourceName.Wood
        self._level = 1
        self._required_resources_for_one_production_cycle = {}

    @property
    def produced_resource(self):
        return self._produced_resource

    @property
    def level(self):
        return self._level

    @property
    def required_resources_for_one_production_cycle(self):
        return self._required_resources_for_one_production_cycle
    
class StoneMine(ProductionBuilding):

    def __init__(self) -> None:
        self._produced_resource = ResourceName.Stone
        self._level = 1
        self._required_resources_for_one_production_cycle = {}

    @property
    def produced_resource(self):
        return self._produced_resource

    @property
    def level(self):
        return self._level

    @property
    def required_resources_for_one_production_cycle(self):
        return self._required_resources_for_one_production_cycle
    
class ToolsSmithy(ProductionBuilding):

    def __init__(self) -> None:
        self._produced_resource = ResourceName.Tools
        self._level = 1
        self._required_resources_for_one_production_cycle = {
            ResourceName.Iron: 4
        }

    @property
    def produced_resource(self):
        return self._produced_resource

    @property
    def level(self):
        return self._level

    @property
    def required_resources_for_one_production_cycle(self):
        return self._required_resources_for_one_production_cycle
    
    

