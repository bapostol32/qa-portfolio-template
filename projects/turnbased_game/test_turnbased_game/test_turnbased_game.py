import os
import unittest
import pytest
from turnbased_game.character_classes.char_classes import Warrior, Rogue, Wizard

from unittest.mock import patch

# testing warrior health with base class 
def test_warrior_health():
    warrior = Warrior()
    assert warrior.health == 180

# create fixture for fresh enemy to player classes
@pytest.fixture(params=[Warrior,Rogue,Wizard])
def enemy(request):
    instance = request.param()
    instance.health = 100
    return instance

# PASSED 8/24/25
def test_warrior_attack(enemy):
    warrior = Warrior()
    enemy.health = 100
    starting_health = enemy.health
    warrior.attack(enemy)
    assert warrior.rage in (10, 20)
    assert enemy.health in (starting_health -20, starting_health - 30)

# PASSED 8/25/25
def test_warrior_special(enemy):
    warrior = Warrior()
    warrior.rage = 20
    warrior.special(enemy)
    assert warrior.rage == 0
    assert enemy.health in (50, 25)

# PASSED 8/25/25
def test_warrior_item():
    warrior = Warrior()
    warrior.health = 100
    warrior.item()
    assert warrior.health == 160

from unittest.mock import patch

def test_warrior_action_prompt():
    warrior = Warrior()
    warrior.rage = 0
    with patch('builtins.input', return_value='a'):
        result = warrior.action_prompt()
        assert result == 'a'

# PASSED 9/1/25
def test_rogue_attack(enemy):
    rogue = Rogue()
    rogue.stamina = 100
    rogue.attack(enemy)
    assert enemy.health in (80, 75, 60)
    assert rogue.stamina in (120, 125, 140,)

# PASSED 9/1/25
def test_rogue_special(enemy):
    rogue = Rogue()
    rogue.stamina = 100
    rogue.special(enemy)
    assert enemy.health in (55, 50, 30)
    assert rogue.stamina in (60, 80, 100)

# PASSED 9/1/25
def test_rogue_item():
    rogue = Rogue()
    rogue.stamina = 100
    rogue.health = 100
    rogue.item_count = 3
    rogue.item()
    assert rogue.health == 130
    assert rogue.stamina == 120
    assert rogue.item_count == 2
