import random

from city import City
from global_market import GlobalMarket
from local_market import LocalMarket
from production_buildings import Farm, IronMine, ToolsSmithy
from resources import Resource, ResourceName


class CityFactory:
    def __init__(self, global_market: GlobalMarket):
        self.global_market = global_market

    def create_city(
        self,
        position: tuple[int, int],
        name: str | None = None,
        initial_resource_amount: int | None = None,
    ) -> City:
        city_name = name or self.generate_city_name()
        resource_amount = initial_resource_amount or random.randint(50, 150)

        resources = {
            resource_name: Resource(resource_name, resource_amount)
            for resource_name in ResourceName
        }

        return City(
            position=position,
            name=city_name,
            production_buildings=[IronMine(), Farm(), ToolsSmithy()],
            local_market=LocalMarket(
                global_market=self.global_market,
                resources=resources,
            ),
        )

    def generate_city_name(self) -> str:
        prefixes = [
            "Bel",
            "Bran",
            "Cal",
            "Dor",
            "Eld",
            "Fal",
            "Gal",
            "Kar",
            "Lor",
            "Mar",
            "Nor",
            "Pra",
            "Riv",
            "Val",
            "Vil",
        ]
        middles = ["a", "e", "i", "o", "u", "en", "an", "el", "or", "ar"]
        suffixes = [
            "berg",
            "bourg",
            "burg",
            "chester",
            "dorf",
            "ford",
            "grad",
            "haven",
            "holm",
            "mont",
            "port",
            "shire",
            "stadt",
            "ton",
            "vale",
            "wick",
        ]

        return f"{random.choice(prefixes)}{random.choice(middles)}{random.choice(suffixes)}"
