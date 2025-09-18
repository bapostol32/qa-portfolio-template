"""
Test suite for Wizard class functionality
Tests wizard-specific methods, mana mechanics, and spell abilities
"""
import pytest
from turnbased_game.character_classes import Warrior, Rogue, Wizard
from unittest.mock import patch


class TestWizard:
    """Test Wizard class specific functionality"""
    
    @pytest.fixture(params=[Warrior, Rogue, Wizard])
    def enemy(self, request):
        """Create fresh enemy instances for each test"""
        instance = request.param()
        instance.health = 100  # Standardize enemy health for testing
        return instance
    
    def test_wizard_initialization(self):
        """Test wizard initializes with correct values"""
        wizard = Wizard()
        assert wizard.health == 120    # Lowest health (glass cannon)
        assert wizard.mana == 100      # Starts with full mana
        assert wizard.item_count == 3
    
    def test_wizard_attack(self, enemy):
        """Test wizard attack mechanics and mana consumption"""
        wizard = Wizard()
        wizard.mana = 100
        starting_health = enemy.health
        starting_mana = wizard.mana
        
        wizard.attack(enemy)
        
        # Mana should be consumed for basic attacks
        assert wizard.mana < starting_mana
        
        # Enemy should take magical damage
        assert enemy.health < starting_health
    
    def test_wizard_special(self, enemy):
        """Test wizard special ability (powerful spell)"""
        wizard = Wizard()
        wizard.mana = 100  # Ensure sufficient mana
        
        wizard.special(enemy)
        
        # Enemy should take significant magical damage
        assert enemy.health < 100  # Should deal substantial damage
        
        # Mana should be heavily consumed
        assert wizard.mana < 100
    
    def test_wizard_special_insufficient_mana(self, enemy, capsys):
        """Test wizard special when insufficient mana"""
        wizard = Wizard()
        wizard.mana = 5  # Insufficient mana
        starting_health = enemy.health
        
        wizard.special(enemy)
        
        # Should print error message
        captured = capsys.readouterr()
        assert "Not enough Mana." in captured.out
        
        # Enemy health should be unchanged
        assert enemy.health == starting_health
    
    def test_wizard_item(self):
        """Test wizard item usage (mana potion)"""
        wizard = Wizard()
        wizard.mana = 50      # Reduce mana to test restoration
        wizard.health = 100   # Reduce health to test healing
        starting_items = wizard.item_count
        
        wizard.item()
        
        # Both mana and health should be restored
        assert wizard.mana > 50    # Mana should increase
        assert wizard.health > 100 # Health should increase
        
        # Item count should decrease
        assert wizard.item_count == starting_items - 1
    
    def test_wizard_item_no_items(self, capsys):
        """Test wizard item usage when no items available"""
        wizard = Wizard()
        wizard.item_count = 0
        starting_health = wizard.health
        starting_mana = wizard.mana
        
        wizard.item()
        
        # Should print error message
        captured = capsys.readouterr()
        assert "No items left." in captured.out
        
        # Stats should be unchanged
        assert wizard.health == starting_health
        assert wizard.mana == starting_mana
    
    def test_wizard_action_prompt(self):
        """Test wizard action prompt input handling"""
        wizard = Wizard()
        
        with patch('builtins.input', return_value='a'):
            result = wizard.action_prompt()
            assert result == 'a'
    
    def test_wizard_print_status(self, capsys):
        """Test wizard status display"""
        wizard = Wizard()
        wizard.print_status(is_enemy=False)
        
        captured = capsys.readouterr()
        assert f"Current Health: 120 | Current Mana: 100" in captured.out
    
    def test_wizard_can_use_special(self):
        """Test wizard special ability availability check"""
        wizard = Wizard()
        
        # Should not be able to use special without sufficient mana
        wizard.mana = 10
        assert not wizard.can_use_special()
        
        # Should be able to use special with sufficient mana
        wizard.mana = 50
        assert wizard.can_use_special()
    
    def test_wizard_mana_depletion_vulnerability(self, enemy):
        """Test wizard's vulnerability when mana depleted"""
        wizard = Wizard()
        wizard.mana = 0  # No mana available
        
        # Basic attack should still work but be less effective
        starting_health = enemy.health
        wizard.attack(enemy)
        
        # Should still deal some damage but limited
        damage_dealt = starting_health - enemy.health
        assert damage_dealt > 0, "Wizard should still deal some damage without mana"
        assert damage_dealt < 30, "Wizard damage should be limited without mana"
    
    def test_wizard_mana_management(self, enemy):
        """Test mana consumption and management"""
        wizard = Wizard()
        initial_mana = wizard.mana
        
        # Multiple attacks should gradually deplete mana
        for _ in range(3):
            wizard.attack(enemy)
            enemy.health = 100  # Reset enemy health
        
        # Mana should be reduced from multiple spell casts
        assert wizard.mana < initial_mana
        assert wizard.mana >= 0  # Should not go negative
    
    def test_wizard_high_damage_potential(self, enemy):
        """Test wizard's high damage potential with full mana"""
        wizard = Wizard()
        wizard.mana = 100  # Full mana
        
        # Special attack with full mana should deal significant damage
        wizard.special(enemy)
        
        damage_dealt = 100 - enemy.health
        assert damage_dealt >= 40, "Wizard special should deal high damage with full mana"
    
    def test_wizard_glass_cannon_design(self):
        """Test wizard's glass cannon design (low health, high damage potential)"""
        wizard = Wizard()
        warrior = Warrior()
        rogue = Rogue()
        
        # Wizard should have lowest health
        assert wizard.health < warrior.health
        assert wizard.health < rogue.health
        
        # But should have highest potential damage output (tested through mana system)
        assert wizard.mana == 100  # Full magical potential
