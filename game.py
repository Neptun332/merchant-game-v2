import numpy as np
from events import EventManager
from map import GameMap
from npc import NPC
from resources import ResourceName, Resource
from global_market import GlobalMarket
from display import Display
from city_factory import CityFactory


class Game:
    def __init__(self):
        self.seed = 2137
        np.random.seed(self.seed)
        self.npcs = []
        self.global_market = GlobalMarket({}, self.npcs)
        self.city_factory = CityFactory(self.global_market)
        self.game_map = GameMap(self.city_factory, self.seed)
        self.global_market.cities = self.game_map.cities
        self.display = Display(title="Resource Prices")
        self.event_manager = EventManager()

    def setup(self):
        # Setup NPCs
        npc1 = NPC(
            name="Trader Joe",
            resources={
                ResourceName.Iron: Resource(ResourceName.Iron, 10),
                ResourceName.Wood: Resource(ResourceName.Wood, 10),
                ResourceName.Wheat: Resource(ResourceName.Wheat, 10),
                ResourceName.Stone: Resource(ResourceName.Stone, 10),
                ResourceName.Tools: Resource(ResourceName.Tools, 10),
            },
        )
        self.npcs.append(npc1)

    def run(self):
        self.setup()
        running = True
        iter = 0
        while running:
            self.global_market.update_prices()
            # Process city resource consumption and production
            for city_name, city in self.game_map.cities.items():
                city.consume_resources()
                city.produce_resources()

            # # Game loop logic
            # for npc in self.npcs:
            #     city = next(iter(self.game_map.cities.values()), None)
            #     if city:
            #         npc.trade(city)

            if not self.display.handle_input(self.game_map):
                break
            self.display.draw(self.global_market, self.game_map)
            self.display.update()

            if iter > 2000:
                running = False  # Stop after one loop for this example
            iter += 1


if __name__ == "__main__":
    game = Game()
    game.run()
