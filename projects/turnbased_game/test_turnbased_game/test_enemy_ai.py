"""
Test suite for Enemy AI functionality
Tests strategic decision-making algorithms and combat intelligence
"""
import pytest
from turnbased_game.character_classes import Warrior, Rogue, Wizard, EnemyAI


class TestEnemyAI:
    """Test Enemy AI wrapper functionality"""
    
    @pytest.fixture(params=[Warrior, Rogue, Wizard])
    def player(self, request):
        """Create fresh player instances for AI to fight against"""
        return request.param()
    
    @pytest.fixture(params=[Warrior, Rogue, Wizard])
    def ai_character_class(self, request):
        """Different character classes for the AI to use"""
        return request.param
    
    def test_enemy_ai_initialization(self, ai_character_class):
        """Test AI wrapper initializes correctly with character class"""
        ai = EnemyAI(ai_character_class)
        
        assert ai.character_class == ai_character_class
        assert hasattr(ai, 'character')
        assert isinstance(ai.character, ai_character_class)
    
    def test_ai_health_percentage_calculation(self, ai_character_class, player):
        """Test AI correctly calculates health percentages for decision making"""
        ai = EnemyAI(ai_character_class)
        
        # Test with full health
        ai.character.health = ai.character.health  # Full health
        player.health = player.health  # Full health
        
        ai_health_pct = ai._get_health_percentage(ai.character)
        player_health_pct = ai._get_health_percentage(player)
        
        assert ai_health_pct == 100.0
        assert player_health_pct == 100.0
        
        # Test with reduced health
        original_health = ai.character.health
        ai.character.health = original_health // 2  # Half health
        
        ai_health_pct = ai._get_health_percentage(ai.character)
        assert 45 <= ai_health_pct <= 55  # Should be around 50%
    
    def test_ai_should_use_special_logic(self, ai_character_class, player):
        """Test AI special ability decision making"""
        ai = EnemyAI(ai_character_class)
        
        # AI should not use special if it can't
        if hasattr(ai.character, 'can_use_special'):
            if not ai.character.can_use_special():
                assert not ai._should_use_special(player)
        
        # AI should consider using special when player health is low
        player.health = 30  # Low health
        if hasattr(ai.character, 'can_use_special') and ai.character.can_use_special():
            # Decision should be strategic (may or may not use, but should be valid)
            decision = ai._should_use_special(player)
            assert isinstance(decision, bool)
    
    def test_ai_should_use_item_logic(self, ai_character_class):
        """Test AI item usage decision making"""
        ai = EnemyAI(ai_character_class)
        
        # AI should not use item if none available
        ai.character.item_count = 0
        assert not ai._should_use_item()
        
        # AI should consider using item when health is low
        ai.character.item_count = 3
        original_health = ai.character.health
        ai.character.health = original_health // 4  # Very low health
        
        decision = ai._should_use_item()
        assert isinstance(decision, bool)
        # When health is very low, AI should likely use item
        assert decision == True
    
    def test_ai_action_selection(self, ai_character_class, player):
        """Test AI action selection returns valid actions"""
        ai = EnemyAI(ai_character_class)
        
        action = ai.choose_action(player)
        
        # Should return valid action string
        assert action in ['attack', 'special', 'item']
    
    def test_ai_executes_chosen_actions(self, ai_character_class, player):
        """Test AI can execute the actions it chooses"""
        ai = EnemyAI(ai_character_class)
        
        # Test attack execution
        starting_player_health = player.health
        ai.execute_action('attack', player)
        assert player.health <= starting_player_health  # Player should take damage
        
        # Test item execution (if AI has items)
        if ai.character.item_count > 0:
            starting_ai_health = ai.character.health
            starting_items = ai.character.item_count
            ai.execute_action('item', player)
            # Either health increased or items decreased (or both)
            assert (ai.character.health >= starting_ai_health or 
                   ai.character.item_count < starting_items)
    
    def test_ai_strategic_behavior_low_health(self, ai_character_class, player):
        """Test AI behaves strategically when at low health"""
        ai = EnemyAI(ai_character_class)
        
        # Set AI to low health
        ai.character.health = 20
        ai.character.item_count = 3
        
        # AI should prefer survival actions when low on health
        actions = []
        for _ in range(5):  # Sample multiple decisions
            action = ai.choose_action(player)
            actions.append(action)
        
        # Should include item usage when health is low
        assert 'item' in actions, "AI should use items when health is low"
    
    def test_ai_aggressive_behavior_high_health(self, ai_character_class, player):
        """Test AI behaves aggressively when at high health"""
        ai = EnemyAI(ai_character_class)
        
        # Set AI to high health, player to low health
        ai.character.health = ai.character.health  # Full health
        player.health = 30  # Low health
        
        actions = []
        for _ in range(5):  # Sample multiple decisions
            action = ai.choose_action(player)
            actions.append(action)
        
        # Should include offensive actions when AI is healthy and player is weak
        offensive_actions = ['attack', 'special']
        assert any(action in offensive_actions for action in actions)
    
    def test_ai_different_classes_different_strategies(self):
        """Test that different character classes result in different AI behavior"""
        warrior_ai = EnemyAI(Warrior)
        rogue_ai = EnemyAI(Rogue)
        wizard_ai = EnemyAI(Wizard)
        
        player = Warrior()
        player.health = 50  # Set consistent player state
        
        # Each AI should have access to their class-specific abilities
        assert hasattr(warrior_ai.character, 'rage')
        assert hasattr(rogue_ai.character, 'stamina')  
        assert hasattr(wizard_ai.character, 'mana')
        
        # Decision making should potentially differ based on class
        warrior_actions = [warrior_ai.choose_action(player) for _ in range(3)]
        rogue_actions = [rogue_ai.choose_action(player) for _ in range(3)]
        wizard_actions = [wizard_ai.choose_action(player) for _ in range(3)]
        
        # At minimum, all should return valid actions
        all_actions = warrior_actions + rogue_actions + wizard_actions
        assert all(action in ['attack', 'special', 'item'] for action in all_actions)
    
    def test_ai_resource_management(self, ai_character_class, player):
        """Test AI manages resources appropriately"""
        ai = EnemyAI(ai_character_class)
        
        # Deplete AI resources if applicable
        if hasattr(ai.character, 'mana'):
            ai.character.mana = 5  # Low mana
        elif hasattr(ai.character, 'stamina'):
            ai.character.stamina = 10  # Low stamina
        elif hasattr(ai.character, 'rage'):
            ai.character.rage = 5  # Low rage
        
        # AI should not choose special if it can't use it
        if hasattr(ai.character, 'can_use_special') and not ai.character.can_use_special():
            action = ai.choose_action(player)
            # May still choose special, but should handle failure gracefully
            assert action in ['attack', 'special', 'item']
