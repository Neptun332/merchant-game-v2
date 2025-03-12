from city import City
from events import EventManager
from local_market import LocalMarket
from map import GameMap
from npc import NPC
from resources import ResourceName, Resource
from global_market import GlobalMarket
from display import Display


class Game:
    def __init__(self):
        self.display = Display(title="Resource Prices")
        self.event_manager = EventManager()
        self.game_map = GameMap()
        self.npcs = []
        self.global_market = GlobalMarket(self.game_map.cities, self.npcs)


    def setup(self):
        # Setup cities
        city1 = City(
            name="CityA",
            local_market=LocalMarket(
                global_market=self.global_market, 
                resources={
                    ResourceName.Iron: Resource(ResourceName.Iron, 100),
                    ResourceName.Wood: Resource(ResourceName.Wood, 100),
                    ResourceName.Wheat: Resource(ResourceName.Wheat, 100),
                    ResourceName.Stone: Resource(ResourceName.Stone, 100),
                    ResourceName.Tools: Resource(ResourceName.Tools, 100)
                }
            )
        )
        city2 = City(
            name="CityB",
            local_market=LocalMarket(
                global_market=self.global_market, 
                resources={
                    ResourceName.Iron: Resource(ResourceName.Iron, 50),
                    ResourceName.Wood: Resource(ResourceName.Wood, 50),
                    ResourceName.Wheat: Resource(ResourceName.Wheat, 50),
                    ResourceName.Stone: Resource(ResourceName.Stone, 50),
                    ResourceName.Tools: Resource(ResourceName.Tools, 50)
                }
            )
        )
        city3 = City(
            name="CityC",
            local_market=LocalMarket(
                global_market=self.global_market, 
                resources={
                    ResourceName.Iron: Resource(ResourceName.Iron, 150),
                    ResourceName.Wood: Resource(ResourceName.Wood, 150),
                    ResourceName.Wheat: Resource(ResourceName.Wheat, 150),
                    ResourceName.Stone: Resource(ResourceName.Stone, 150),
                    ResourceName.Tools: Resource(ResourceName.Tools, 150)
                }
            )
        )
        self.game_map.add_city(city1)
        self.game_map.add_city(city2)
        self.game_map.add_city(city3)

        # Setup NPCs
        npc1 = NPC(
            name="Trader Joe",
            resources={
                ResourceName.Iron: Resource(ResourceName.Iron, 10),
                ResourceName.Wood: Resource(ResourceName.Wood, 10),
                ResourceName.Wheat: Resource(ResourceName.Wheat, 10),
                ResourceName.Stone: Resource(ResourceName.Stone, 10),
                ResourceName.Tools: Resource(ResourceName.Tools, 10)
            }
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
            
            # Game loop logic
            for npc in self.npcs:
                city = self.game_map.get_city("CityA")
                if city:
                    npc.trade(city)

            self.display.draw(self.global_market)
            self.display.update()
            
            if iter > 1000:
                running = False  # Stop after one loop for this example
            iter += 1
            

if __name__ == "__main__":
    game = Game()
    game.run() 