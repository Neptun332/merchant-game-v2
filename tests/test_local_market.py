import pytest
from local_market import LocalMarket
from global_market import GlobalMarket
from resources import Resource, ResourceName
from collections import defaultdict

@pytest.fixture
def setup_local_market():
    global_market = GlobalMarket([], [])
    resources = {
        ResourceName.Iron: Resource(ResourceName.Iron, 100),
        ResourceName.Wood: Resource(ResourceName.Wood, 200)
    }
    local_market = LocalMarket(global_market, resources)
    return local_market

def test_initialization(setup_local_market):
    local_market = setup_local_market
    assert local_market.gold == 5000
    assert local_market.price_change_factor == 5
    assert local_market.number_of_ticks_for_average == 20

def test_update_prices(setup_local_market):
    local_market = setup_local_market
    local_market.update_prices()
    assert len(local_market.price_history[ResourceName.Iron]) == 2

def test_get_resource_price(setup_local_market):
    local_market = setup_local_market
    price = local_market.get_resource_price(ResourceName.Iron)
    assert price == int(local_market.base_prices[ResourceName.Iron] * (1 + local_market.get_resource_price_change(ResourceName.Iron)))

def test_add_produced_resource(setup_local_market):
    local_market = setup_local_market
    local_market.add_produced_resource(ResourceName.Iron, 50)
    assert local_market.resources[ResourceName.Iron].amount == 150
    assert local_market.produced_resources[ResourceName.Iron] == 50

def test_remove_consumed_resource(setup_local_market):
    local_market = setup_local_market
    local_market.remove_consumed_resource(ResourceName.Iron, 50)
    assert local_market.resources[ResourceName.Iron].amount == 50
    assert local_market.consumed_resources[ResourceName.Iron] == 50

def test_get_recent_average_production(setup_local_market):
    local_market = setup_local_market
    local_market.production_history[ResourceName.Iron] = [10, 20, 30, 40, 50]
    local_market.number_of_ticks_for_average = 5
    average_production = local_market.get_recent_average_production(ResourceName.Iron)
    assert average_production == 30

def test_get_recent_average_consumption(setup_local_market):
    local_market = setup_local_market
    local_market.consumption_history[ResourceName.Iron] = [5, 15, 25, 35, 45]
    local_market.number_of_ticks_for_average = 5
    average_consumption = local_market.get_recent_average_consumption(ResourceName.Iron)
    assert average_consumption == 25
