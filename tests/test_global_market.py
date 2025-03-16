import pytest
from global_market import GlobalMarket
from local_market import LocalMarket
from map import City
from npc import NPC
from resources import Resource, ResourceName
from collections import defaultdict

@pytest.fixture
def setup_global_market():
    cities = []
    npcs = [NPC("NPC1", defaultdict(int)), NPC("NPC2", defaultdict(int))]
    global_market = GlobalMarket([], npcs)
    cities.extend(
        [City("City1", LocalMarket(global_market, {ResourceName.Iron: Resource(ResourceName.Iron, 100), ResourceName.Wood: Resource(ResourceName.Wood, 100)}), []),
        City("City2", LocalMarket(global_market, {ResourceName.Iron: Resource(ResourceName.Iron, 200), ResourceName.Wood: Resource(ResourceName.Wood, 200)}), [])]
    )
    return global_market

def test_initialization(setup_global_market):
    global_market = setup_global_market
    assert global_market.total_gold == 0
    assert global_market.price_change_factor == 5
    assert global_market.number_of_ticks_for_average == 20

def test_update_prices(setup_global_market):
    global_market = setup_global_market
    global_market.update_prices()
    assert len(global_market.price_history[ResourceName.Iron]) == 2

def test_get_resource_price(setup_global_market):
    global_market = setup_global_market
    price = global_market.get_resource_price(ResourceName.Iron)
    assert price == global_market.base_prices[ResourceName.Iron] * (1 + global_market.get_resource_price_change(ResourceName.Iron))

def test_calculate_total_gold(setup_global_market):
    global_market = setup_global_market
    total_gold = global_market.calculate_total_gold()
    assert total_gold == 11000

def test_calculate_base_prices(setup_global_market):
    global_market = setup_global_market
    global_market.calculate_base_prices()
    assert global_market.base_prices[ResourceName.Iron] == global_market.market_share[ResourceName.Iron] / max(1, global_market.total_amount[ResourceName.Iron])

def test_calculate_total_resource_consumed(setup_global_market):
    global_market = setup_global_market
    # Simulate consumption in local markets
    global_market.local_markets[0].consumed_resources[ResourceName.Iron] = 50
    global_market.local_markets[1].consumed_resources[ResourceName.Iron] = 50
    global_market.local_markets[1].consumed_resources[ResourceName.Wood] = 30
    
    global_market.calculate_total_resource_consumed()
    
    assert global_market.total_consumed[ResourceName.Iron] == 100
    assert global_market.total_consumed[ResourceName.Wood] == 30

def test_calculate_total_resource_produced(setup_global_market):
    global_market = setup_global_market
    # Simulate production in local markets
    global_market.local_markets[0].produced_resources[ResourceName.Iron] = 70
    global_market.local_markets[1].produced_resources[ResourceName.Iron] = 80
    global_market.local_markets[1].produced_resources[ResourceName.Wood] = 40
    
    global_market.calculate_total_resource_produced()
    
    assert global_market.total_produced[ResourceName.Iron] == 150
    assert global_market.total_produced[ResourceName.Wood] == 40

def test_calculate_total_resource_amount(setup_global_market):
    global_market = setup_global_market
    # Simulate resources in local markets
    global_market.local_markets[0].resources[ResourceName.Iron].amount = 100
    global_market.local_markets[0].resources[ResourceName.Wood].amount = 0
    global_market.local_markets[1].resources[ResourceName.Iron].amount = 200
    global_market.local_markets[1].resources[ResourceName.Wood].amount = 150
    
    global_market.calculate_total_resource_amount()
    
    assert global_market.total_amount[ResourceName.Iron] == 300
    assert global_market.total_amount[ResourceName.Wood] == 150

def test_get_recent_average_production(setup_global_market):
    global_market = setup_global_market
    # Simulate production history
    global_market.production_history[ResourceName.Iron] = [10, 20, 30, 40, 50]
    global_market.number_of_ticks_for_average = 5
    
    average_production = global_market.get_recent_average_production(ResourceName.Iron)
    
    assert average_production == 30

def test_get_recent_average_consumption(setup_global_market):
    global_market = setup_global_market
    # Simulate consumption history
    global_market.consumption_history[ResourceName.Iron] = [5, 15, 25, 35, 45]
    global_market.number_of_ticks_for_average = 5
    
    average_consumption = global_market.get_recent_average_consumption(ResourceName.Iron)
    
    assert average_consumption == 25

def test_get_market_share_single_resource(setup_global_market):
    global_market = setup_global_market
    global_market.total_gold = 10000
    global_market.total_amount[ResourceName.Iron] = 100
    global_market.price_value_modifiers[ResourceName.Iron] = 1.0
    
    market_share = global_market.get_market_share()
    
    assert market_share[ResourceName.Iron] == 10000

def test_get_market_share_multiple_resources(setup_global_market):
    global_market = setup_global_market
    global_market.total_gold = 10000
    global_market.total_amount[ResourceName.Iron] = 50
    global_market.total_amount[ResourceName.Wood] = 50
    global_market.price_value_modifiers[ResourceName.Iron] = 1.0
    global_market.price_value_modifiers[ResourceName.Wood] = 1.0
    
    market_share = global_market.get_market_share()
    
    assert market_share[ResourceName.Iron] == 5000
    assert market_share[ResourceName.Wood] == 5000

def test_get_market_share_with_modifiers(setup_global_market):
    global_market = setup_global_market
    global_market.total_gold = 10000
    global_market.total_amount[ResourceName.Iron] = 50
    global_market.total_amount[ResourceName.Wood] = 50
    global_market.price_value_modifiers[ResourceName.Iron] = 3.0
    global_market.price_value_modifiers[ResourceName.Wood] = 1.0
    
    market_share = global_market.get_market_share()
    
    assert market_share[ResourceName.Iron] == 7500
    assert market_share[ResourceName.Wood] == 2500

def test_get_market_share_with_defaul_modifiers(setup_global_market):
    global_market = setup_global_market
    global_market.total_gold = 10000
    global_market.total_amount[ResourceName.Iron] = 50
    global_market.total_amount[ResourceName.Wood] = 50
    
    market_share = global_market.get_market_share()
    
    assert market_share[ResourceName.Iron] == 6000
    assert market_share[ResourceName.Wood] == 4000

def test_estimate_base_resource_price(setup_global_market):
    global_market = setup_global_market
    global_market.total_gold = 10000
    global_market.total_amount[ResourceName.Iron] = 0
    global_market.price_value_modifiers[ResourceName.Iron] = 1.0
    
    estimated_price = global_market.estimate_base_resource_price(ResourceName.Iron)
    
    assert estimated_price == 10000  # Since there are 0 Iron, adding 1 should give the total gold as the price

def test_estimate_base_resource_price_with_existing_amount(setup_global_market):
    global_market = setup_global_market
    global_market.total_gold = 10000
    global_market.total_amount[ResourceName.Iron] = 100
    global_market.price_value_modifiers[ResourceName.Iron] = 1.0
    
    estimated_price = global_market.estimate_base_resource_price(ResourceName.Iron)
    
    assert estimated_price == 99.00990099009901  # 10000 / (100 + 1)

