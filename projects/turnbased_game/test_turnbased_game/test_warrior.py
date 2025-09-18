"""
Test suite for Warrior class functionality
Tests warrior-specific methods, rage mechanics, and combat abilities
PASSED dates noted from original test file
"""
import pytest
from turnbased_game.character_classes import Warrior, Rogue, Wizard
from unittest.mock import patch


class TestWarrior:
    """Test Warrior class specific functionality"""
    
    @pytest.fixture(params=[Warrior, Rogue, Wizard])
    def enemy(self, request):
        """Create fresh enemy instances for each test"""
        instance = request.param()
        instance.health = 100  # Standardize enemy health for testing
        return instance
    
    def test_warrior_initialization(self):
        """Test warrior initializes with correct values"""
        warrior = Warrior()
        assert warrior.health == 200  # Warrior has highest health
        assert warrior.rage == 0      # Starts with no rage
        assert warrior.item_count == 3
    
    # PASSED 8/24/25
    def test_warrior_attack(self, enemy):
        """Test warrior attack mechanics and rage generation"""
        warrior = Warrior()
        starting_health = enemy.health
        
        warrior.attack(enemy)
        
        # Rage should increase after attack
        assert warrior.rage in (15, 25)  # Base rage gain or critical rage gain
        
        # Enemy should take damage
        expected_damage_range = [starting_health - 40, starting_health - 25]  # crit or normal
        assert enemy.health in expected_damage_range
    
    # PASSED 8/25/25  
    def test_warrior_special(self, enemy):
        """Test warrior special ability (fury unleash)"""
        warrior = Warrior()
        warrior.rage = 30  # Set sufficient rage for special
        
        warrior.special(enemy)
        
        # Rage should be consumed
        assert warrior.rage == 0
        
        # Enemy should take significant damage
        assert enemy.health in (25, 50)  # Expected damage range for special
    
    def test_warrior_special_insufficient_rage(self, enemy, capsys):
        """Test warrior special when not enough rage"""
        warrior = Warrior()
        warrior.rage = 10  # Insufficient rage
        starting_health = enemy.health
        
        warrior.special(enemy)
        
        # Should print error message
        captured = capsys.readouterr()
        assert "Not enough Rage." in captured.out
        
        # Enemy health should be unchanged
        assert enemy.health == starting_health
    
    # PASSED 8/25/25
    def test_warrior_item(self):
        """Test warrior item usage (health potion)"""
        warrior = Warrior()
        warrior.health = 100  # Reduce health to test healing
        starting_items = warrior.item_count
        
        warrior.item()
        
        # Health should increase
        assert warrior.health == 160  # 100 + 60 healing
        
        # Item count should decrease
        assert warrior.item_count == starting_items - 1
    
    def test_warrior_item_no_items(self, capsys):
        """Test warrior item usage when no items available"""
        warrior = Warrior()
        warrior.item_count = 0
        starting_health = warrior.health
        
        warrior.item()
        
        # Should print error message
        captured = capsys.readouterr()
        assert "No items left." in captured.out
        
        # Health should be unchanged
        assert warrior.health == starting_health
    
    def test_warrior_action_prompt(self):
        """Test warrior action prompt input handling"""
        warrior = Warrior()
        warrior.rage = 0  # No rage for special
        
        with patch('builtins.input', return_value='a'):
            result = warrior.action_prompt()
            assert result == 'a'
    
    def test_warrior_print_status(self, capsys):
        """Test warrior status display"""
        warrior = Warrior()
        warrior.print_status(is_enemy=False)
        
        captured = capsys.readouterr()
        assert f"Current Health: 200 | Current Rage: 0" in captured.out
    
    def test_warrior_can_use_special(self):
        """Test warrior special ability availability check"""
        warrior = Warrior()
        
        # Should not be able to use special without rage
        warrior.rage = 0
        assert not warrior.can_use_special()
        
        # Should be able to use special with sufficient rage
        warrior.rage = 30
        assert warrior.can_use_special()
    
    def test_warrior_rage_mechanics(self, enemy):
        """Test rage gain from combat"""
        warrior = Warrior()
        initial_rage = warrior.rage
        
        # Attack should generate rage
        warrior.attack(enemy)
        assert warrior.rage > initial_rage
        
        # Rage should cap at reasonable levels
        warrior.rage = 100
        warrior.attack(enemy)
        assert warrior.rage <= 125  # Should not exceed reasonable bounds
