from events import EventManager
from map import GameMap, City
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
        city1 = City("CityA", {ResourceName.Iron: Resource(ResourceName.Iron, 100)})
        city2 = City("CityB", {ResourceName.Iron: Resource(ResourceName.Iron, 80)})
        self.game_map.add_city(city1)
        self.game_map.add_city(city2)

        # Setup NPCs
        npc1 = NPC("Trader Joe", {ResourceName.Iron: Resource(ResourceName.Iron, 10)})
        self.npcs.append(npc1)

    def run(self):
        self.setup()
        running = True
        iter = 0
        while running:
            # Game loop logic
            for npc in self.npcs:
                city = self.game_map.get_city("CityA")
                if city:
                    npc.trade(city)
            self.global_market.update_prices()

            self.display.draw(self.global_market.price_history[ResourceName.Iron])
            self.display.update()
            
            if iter > 1000:
                running = False  # Stop after one loop for this example
            iter += 1
            

if __name__ == "__main__":
    game = Game()
    game.run() 