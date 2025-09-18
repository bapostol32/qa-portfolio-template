"""
Test suite for Rogue class functionality  
Tests rogue-specific methods, stamina mechanics, and stealth abilities
PASSED dates noted from original test file
"""
import pytest
from turnbased_game.character_classes import Warrior, Rogue, Wizard
from unittest.mock import patch


class TestRogue:
    """Test Rogue class specific functionality"""
    
    @pytest.fixture(params=[Warrior, Rogue, Wizard])
    def enemy(self, request):
        """Create fresh enemy instances for each test"""
        instance = request.param()
        instance.health = 100  # Standardize enemy health for testing
        return instance
    
    def test_rogue_initialization(self):
        """Test rogue initializes with correct values"""
        rogue = Rogue()
        assert rogue.health == 160    # Medium health
        assert rogue.stamina == 100   # Starts with full stamina
        assert rogue.item_count == 3
    
    # PASSED 9/1/25
    def test_rogue_attack(self, enemy):
        """Test rogue attack mechanics and stamina effects"""
        rogue = Rogue()
        rogue.stamina = 100
        starting_health = enemy.health
        
        rogue.attack(enemy)
        
        # Enemy should take damage (variable based on critical hits)
        assert enemy.health in (80, 75, 60)  # Normal, crit, or high crit damage
        
        # Stamina should increase (rogue gains stamina from successful attacks)
        assert rogue.stamina in (120, 125, 140)
    
    # PASSED 9/1/25
    def test_rogue_special(self, enemy):
        """Test rogue special ability (stealth strike)"""
        rogue = Rogue()
        rogue.stamina = 100
        
        rogue.special(enemy)
        
        # Enemy should take significant damage
        assert enemy.health in (55, 50, 30)  # Variable damage based on stealth effectiveness
        
        # Stamina consumption varies based on ability success
        assert rogue.stamina in (50, 70, 90, 100)
    
    # PASSED 9/6/25
    def test_rogue_special_oom(self, enemy, capsys):
        """Test rogue special when out of stamina (OOM = Out of Mana/Stamina)"""
        rogue = Rogue()
        rogue.stamina = 10  # Insufficient stamina
        starting_health = enemy.health
        
        rogue.special(enemy)
        
        # Should print error message
        captured = capsys.readouterr()
        assert "Not enough Stamina." in captured.out
        
        # Enemy health should be unchanged
        assert enemy.health == starting_health
    
    # PASSED 9/1/25
    def test_rogue_item(self):
        """Test rogue item usage (restoration potion - heals health and stamina)"""
        rogue = Rogue()
        rogue.stamina = 100
        rogue.health = 100
        rogue.item_count = 3
        
        rogue.item()
        
        # Both health and stamina should increase
        assert rogue.health == 130     # +30 health
        assert rogue.stamina == 120    # +20 stamina  
        assert rogue.item_count == 2   # Item consumed
    
    def test_rogue_item_no_items(self, capsys):
        """Test rogue item usage when no items available"""
        rogue = Rogue()
        rogue.item_count = 0
        starting_health = rogue.health
        starting_stamina = rogue.stamina
        
        rogue.item()
        
        # Should print error message
        captured = capsys.readouterr()
        assert "No items left." in captured.out
        
        # Stats should be unchanged
        assert rogue.health == starting_health
        assert rogue.stamina == starting_stamina
    
    # PASSED 9/6/25
    def test_rogue_action_prompt(self):
        """Test rogue action prompt input handling"""
        rogue = Rogue()
        
        with patch('builtins.input', return_value='a'):
            result = rogue.action_prompt()
            assert result == 'a'
    
    def test_rogue_print_status(self, capsys):
        """Test rogue status display"""
        rogue = Rogue()
        rogue.print_status(is_enemy=False)
        
        captured = capsys.readouterr()
        assert f"Current Health: 160 | Current Stamina: 100" in captured.out
    
    def test_rogue_can_use_special(self):
        """Test rogue special ability availability check"""
        rogue = Rogue()
        
        # Should not be able to use special without sufficient stamina
        rogue.stamina = 10
        assert not rogue.can_use_special()
        
        # Should be able to use special with sufficient stamina
        rogue.stamina = 50
        assert rogue.can_use_special()
    
    def test_rogue_stamina_management(self, enemy):
        """Test stamina gain and consumption mechanics"""
        rogue = Rogue()
        initial_stamina = rogue.stamina
        
        # Attack should potentially increase stamina
        rogue.attack(enemy)
        # Stamina can increase or stay same based on combat success
        assert rogue.stamina >= initial_stamina
        
        # Stamina should have reasonable bounds
        rogue.stamina = 200
        rogue.attack(enemy)
        assert rogue.stamina <= 250  # Should not exceed reasonable bounds
    
    def test_rogue_critical_hit_mechanics(self, enemy):
        """Test rogue's enhanced critical hit capabilities"""
        rogue = Rogue()
        damage_values = []
        
        # Run multiple attacks to test critical hit variation
        for _ in range(10):
            enemy.health = 100  # Reset enemy health
            rogue.attack(enemy)
            damage_dealt = 100 - enemy.health
            damage_values.append(damage_dealt)
        
        # Should have variation in damage (indicating critical hits)
        assert len(set(damage_values)) > 1, "Rogue should have variable damage from critical hits"
