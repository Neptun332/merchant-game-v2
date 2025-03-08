from resources import ResourceName, Resource
from map import City
class NPC:
    def __init__(self, name: str, resources: dict[ResourceName, Resource]):
        self.name = name
        self.resources = resources

    def trade(self, city: City):
        # Simple trade logic
        pass