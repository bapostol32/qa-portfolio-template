
import pytest
from ..main_gameloop.turnbased_game import Warrior

# # testing warrior health with base class
def test_warrior_health():
    warrior = Warrior()
    assert warrior.health == 180

# create fixture for fresh enemy to warrior
@pytest.fixture
def enemy():
    enemy = Warrior()
    enemy.health = 100
    return enemy

def test_warrior_attack(enemy):
    print("test atack")
    warrior = Warrior()
    warrior.attack(enemy)
    assert warrior.rage == 10
    assert enemy.health in (80, 70)