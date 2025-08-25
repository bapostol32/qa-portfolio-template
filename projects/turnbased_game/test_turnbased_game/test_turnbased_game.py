import os
import unittest
import pytest
from turnbased_game.main_gameloop.turnbased_game import Warrior
from unittest.mock import patch

# testing warrior health with base class 
def test_warrior_health():
    warrior = Warrior()
    assert warrior.health == 180

# create fixture for fresh enemy to warrior
@pytest.fixture
def enemy():
    enemy = Warrior()
    enemy.health = 100
    return enemy

# PASSED 8/24/25
def test_warrior_attack(enemy):
    warrior = Warrior()
    warrior.attack(enemy)
    assert warrior.rage == 10
    assert enemy.health in (80, 70)

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
