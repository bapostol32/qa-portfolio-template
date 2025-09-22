"""
Base Character Class
Contains the foundation for all character types in the turn-based game.
Subclasses inherit the "bones" of the base character and 
fill in the functions with their respective subclass attributes.
"""
import random
import time
from typing import Dict, Any
from .status_effects import StatusEffect, EffectType, EffectCategory
class Character:
    def __init__(self, health, resource):
        self.health = health
        self.resource = resource
    
    def attack(self):
        raise NotImplementedError
    
    def special(self):
        raise NotImplementedError
    
    def item(self):
        raise NotImplementedError
    
    def print_status(self):
        raise NotImplementedError
    
    def get_attack_dmg(self, 
                       base=None, 
                       crit=None, 
                       super_crit=None, 
                       crit_chance=None, 
                       super_crit_chance=None, 
                       return_range=False
                       ):
        """Returns either damage value OR range string"""
        if return_range:
            # Range calc for UI display
            possible_damages = [base]
            if crit_chance > 0:
                possible_damages.append(crit)
            if super_crit and super_crit_chance > 0:
                possible_damages.append(super_crit)
            min_damage = min(possible_damages)
            max_damage = max(possible_damages)
            return f"{min_damage} - {max_damage}"
        else:
            # Damage calc
            roll = random.random()
            if super_crit and roll < super_crit_chance:
                return super_crit
            elif roll < crit_chance:
                return crit
            else:
                return base
            
    def map_input_to_action(self, action_name):
        if action_name == "a":
            return "attack"
        elif action_name == "b":
            return "special"
        elif action_name == "c":
            return "item"
        elif action_name == "d":
            # Import here to avoid circular imports
            from .wizard import Wizard
            if isinstance(self, Wizard):
                return "heal"
        elif action_name == "e":
            # Status effect abilities
            from .wizard import Wizard
            from .warrior import Warrior
            from .rogue import Rogue
            if isinstance(self, Wizard):
                return "magic_bubble"
            elif isinstance(self, Warrior):
                return "berserker_rage"
            elif isinstance(self, Rogue):
                return "shadow_step"
        else:
            return None
        
    def execute_action(self, action_name, enemy):
        if action_name == "attack":
            self.attack(enemy)
        elif action_name == "special":
            self.special(enemy)
        elif action_name == "item":
            self.item()
        elif action_name == "heal":
            self.spell_heal()
        elif action_name == "magic_bubble":
            result = self.cast_magic_bubble()
            if result['success']:
                print("You weave a protective barrier around yourself!")
            else:
                print(f"Failed to cast Magic Bubble: {result.get('reason', 'Unknown error')}")
        elif action_name == "berserker_rage":
            result = self.enter_berserker_rage()
            if result['success']:
                print("You unleash your inner fury and enter a berserker rage!")
            else:
                print(f"Failed to enter Berserker Rage: {result.get('reason', 'Unknown error')}")
        elif action_name == "shadow_step":
            result = self.activate_shadow_step()
            if result['success']:
                print("You meld with the shadows, becoming harder to hit!")
            else:
                print(f"Failed to activate Shadow Step: {result.get('reason', 'Unknown error')}")
        else:
            self.attack(enemy)

    def take_turn(self, enemy):
        print("\n" + "="*50)
        print("🎯 YOUR TURN!")
        print("="*50)
        time.sleep(1)
        
        print("\n📊 CURRENT STATUS:")
        self.print_status()
        self.print_active_status_effects()
        
        print("\n🏹 ENEMY STATUS:")
        enemy.print_status(is_enemy=True)
        enemy.print_active_status_effects(is_enemy=True)
        
        # Import here to avoid circular imports
        from .wizard import Wizard
        if isinstance(self, Wizard):
            if self.mana < 10 and self.item_count == 0:
                self.health = 0
                print("\n💀 The wizard drops their staff and falls to the ground.")
                print("   They have ran out of mana, and died.")
                return
                
        print("\n" + "-"*30)
        while True:
            action_choice = self.action_prompt()
            time.sleep(1)
            mapped_action = self.map_input_to_action(action_choice)
            if mapped_action and self.validate_action(mapped_action):
                self.execute_action(mapped_action, enemy)
                break
            else:
                print("\n❌ Invalid choice. Please try again.")
                print("\n" + "="*40)
                print("📋 STATUS REFRESH")
                print("="*40)
                
                print("\n📊 YOUR STATUS:")
                self.print_status()
                self.print_active_status_effects()
                
                print("\n🏹 ENEMY STATUS:")
                enemy.print_status(is_enemy=True)
                enemy.print_active_status_effects(is_enemy=True)
                print("\n" + "-"*30)
        time.sleep(1)

    def process_turn_start(self) -> Dict[str, Any]:
        """Process status effects at turn start"""
        if hasattr(self, 'status_effects'):
            return self.status_effects.process_turn_effects(self)
        return {}

    def has_status_effect(self, effect_type) -> bool:
        """Check if character has specific status effect"""
        if hasattr(self, 'status_effects'):
            if hasattr(self.status_effects, 'has_effect'):
                return self.status_effects.has_effect(effect_type)
            else:
                # Fallback if method doesn't exist - check manually
                return any(effect.effect_type == effect_type for effect in self.status_effects.active_effects)
        return False

    def print_active_status_effects(self, is_enemy=False):
        """Display active status effects"""
        if not hasattr(self, 'status_effects') or not self.status_effects.active_effects:
            return  # No status effects to display
        
        prefix = "   🌟 Enemy" if is_enemy else "   🌟 You"
        effects_info = []
        
        for effect in self.status_effects.active_effects:
            effect_name = effect.effect_type.value.replace('_', ' ').title()
            duration = effect.duration
            
            # Add specific effect descriptions
            if effect.effect_type.value == "magic_bubble":
                effects_info.append(f"🔮 {effect_name} ({duration} turns) - 35% damage reduction")
            elif effect.effect_type.value == "berserker_rage":
                effects_info.append(f"⚔️ {effect_name} ({duration} turns) - +25% damage taken → rage")
            elif effect.effect_type.value == "shadow_step":
                effects_info.append(f"🌫️ {effect_name} ({duration} turns) - 30% dodge chance")
            else:
                effects_info.append(f"✨ {effect_name} ({duration} turns)")
        
        if effects_info:
            effect_text = "has" if is_enemy else "have"
            print(f"{prefix} {effect_text} active effects: {' | '.join(effects_info)}")
        

# Character stat templates
char_warrior = {"health": 150, "rage": 0}
char_rogue = {"health": 100, "stamina": 100}
char_wizard = {"health": 75, "mana": 150}
enemy_1 = {"health": 100, "mana": 100}
