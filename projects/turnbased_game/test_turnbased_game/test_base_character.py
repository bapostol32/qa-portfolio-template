"""
Test suite for base Character class functionality
Tests shared methods and attributes across all character classes
"""
import pytest
from turnbased_game.character_classes import Warrior, Rogue, Wizard


class TestBaseCharacter:
    """Test base Character class shared functionality"""
    
    @pytest.fixture(params=[Warrior, Rogue, Wizard])
    def character(self, request):
        """Fixture providing instances of all character classes"""
        return request.param()
    
    def test_character_initialization(self, character):
        """Test that all character classes initialize properly"""
        assert hasattr(character, 'health')
        assert hasattr(character, 'item_count')
        assert character.health > 0
        assert character.item_count >= 0
    
    def test_character_has_required_methods(self, character):
        """Test that all characters implement required methods"""
        assert hasattr(character, 'attack')
        assert hasattr(character, 'special')
        assert hasattr(character, 'item')
        assert hasattr(character, 'action_prompt')
        assert callable(character.attack)
        assert callable(character.special)
        assert callable(character.item)
        assert callable(character.action_prompt)
    
    def test_print_status_method_exists(self, character):
        """Test that print_status method exists for all characters"""
        assert hasattr(character, 'print_status')
        assert callable(character.print_status)
    
    def test_get_attack_dmg_method_exists(self, character):
        """Test that damage calculation method exists"""
        assert hasattr(character, 'get_attack_dmg')
        assert callable(character.get_attack_dmg)


# Test specific to character health variations
def test_character_class_health_differences():
    """Test that different character classes have different starting health"""
    warrior = Warrior()
    rogue = Rogue()
    wizard = Wizard()
    
    # Verify each class has distinct health values
    health_values = {warrior.health, rogue.health, wizard.health}
    assert len(health_values) == 3, "All character classes should have different health values"
    
    # Verify health ordering (Warrior > Rogue > Wizard typically)
    assert warrior.health > rogue.health > wizard.health


def test_item_count_consistency():
    """Test that all characters start with consistent item counts"""
    warrior = Warrior()
    rogue = Rogue()
    wizard = Wizard()
    
    assert warrior.item_count == rogue.item_count == wizard.item_count == 3
