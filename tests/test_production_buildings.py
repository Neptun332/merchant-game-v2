import pytest
from production_buildings import Farm, IronMine, WoodCutterCottage, StoneMine, ToolsSmithy
from local_market import LocalMarket
from global_market import GlobalMarket
from resources import Resource, ResourceName
from city import City
from collections import defaultdict

@pytest.fixture
def setup_test_environment():
    global_market = GlobalMarket([], [])
    resources = {
        ResourceName.Iron: Resource(ResourceName.Iron, 100),
        ResourceName.Wood: Resource(ResourceName.Wood, 100),
        ResourceName.Wheat: Resource(ResourceName.Wheat, 100),
        ResourceName.Stone: Resource(ResourceName.Stone, 100),
        ResourceName.Tools: Resource(ResourceName.Tools, 100),
    }
    local_market = LocalMarket(global_market, resources)
    city = City("TestCity", local_market, [])
    global_market.update_prices()
    return city

def test_farm_initialization():
    farm = Farm()
    assert farm.produced_resource == ResourceName.Wheat
    assert farm.level == 1
    assert len(farm.required_resources_for_one_production_cycle) == 0
    assert 3 <= farm.base_production <= 7

def test_iron_mine_initialization():
    iron_mine = IronMine()
    assert iron_mine.produced_resource == ResourceName.Iron
    assert iron_mine.level == 1
    assert iron_mine.required_resources_for_one_production_cycle == {ResourceName.Wheat: 1}

def test_production_with_no_requirements(setup_test_environment):
    city = setup_test_environment
    farm = Farm()
    initial_wheat = city.local_market.resources[ResourceName.Wheat].amount
    farm.produce(city)
    assert city.local_market.resources[ResourceName.Wheat].amount > initial_wheat

def test_production_with_requirements(setup_test_environment):
    city = setup_test_environment
    iron_mine = IronMine()
    initial_iron = city.local_market.resources[ResourceName.Iron].amount
    initial_wheat = city.local_market.resources[ResourceName.Wheat].amount
    iron_mine.produce(city)
    assert city.local_market.resources[ResourceName.Iron].amount > initial_iron
    assert city.local_market.resources[ResourceName.Wheat].amount < initial_wheat

def test_cannot_produce_without_resources(setup_test_environment):
    city = setup_test_environment
    tools_smithy = ToolsSmithy()
    city.local_market.resources[ResourceName.Iron].amount = 0
    assert not tools_smithy.can_produce(city)

def test_production_worth_calculation(setup_test_environment):
    city = setup_test_environment
    iron_mine = IronMine()
    # Make iron very valuable compared to wheat
    city.local_market.current_price[ResourceName.Iron] = 100
    city.local_market.current_price[ResourceName.Wheat] = 1
    assert iron_mine.is_production_worth_it(city)
    
    # Make iron worthless compared to wheat
    city.local_market.current_price[ResourceName.Iron] = 1
    city.local_market.current_price[ResourceName.Wheat] = 100
    assert not iron_mine.is_production_worth_it(city)

def test_complex_production_chain(setup_test_environment):
    city = setup_test_environment
    tools_smithy = ToolsSmithy()
    initial_tools = city.local_market.resources[ResourceName.Tools].amount
    initial_iron = city.local_market.resources[ResourceName.Iron].amount
    initial_wheat = city.local_market.resources[ResourceName.Wheat].amount
    
    tools_smithy.produce(city)
    
    assert city.local_market.resources[ResourceName.Tools].amount > initial_tools
    assert city.local_market.resources[ResourceName.Iron].amount < initial_iron
    assert city.local_market.resources[ResourceName.Wheat].amount < initial_wheat
