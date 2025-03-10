from enum import Enum
import random  # For simulating real-time data updates

class ResourceName(str, Enum):
    Iron = "Iron"

class Resource:
    def __init__(self, name: ResourceName, amount: int):
        self.name = name
        self.amount = amount

    def __str__(self):
        return f"{self.name}: {self.amount}"



# Example usage:
# resource_prices = {
#     'Gold': [100],
#     'Silver': [50],
#     'Copper': [30]
# }
# plot_resource_prices_real_time(resource_prices)
