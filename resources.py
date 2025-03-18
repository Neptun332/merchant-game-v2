from enum import Enum
import random  # For simulating real-time data updates

class ResourceName(str, Enum):
    Iron = "Iron"
    Wood = "Wood"
    Wheat = "Wheat"
    Stone = "Stone"
    Tools = "Tools"

class Resource:
    def __init__(self, name: ResourceName, amount: int):
        self.name = name
        self.amount = amount

    def __str__(self):
        return f"{self.name}: {self.amount}"

