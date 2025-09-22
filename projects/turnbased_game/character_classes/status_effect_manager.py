from typing import List, Dict, Tuple, Optional, Any
import random
from .status_effects import StatusEffect, EffectType, EffectCategory

class StatusEffectManager:
    """
    Manages stat effects using Observer pattern
    """
    def __init__(self): # constructor method (called when creating a new manager)
        self.active_effects: List[StatusEffect] = [] # empty list to store active effects
    
    def add_effect(self, effect: StatusEffect) -> None:
        """Add new status effect"""
        # Removes existing effect of same type (no stacking)
        self.remove_effect_by_type(effect.effect_type)
        self.active_effects.append(effect)

    def remove_effect_by_type(self, effect_type: EffectType) -> None:
        """Remove effect by type"""
        self.active_effects = [
            effect for effect in self.active_effects 
            if effect.effect_type != effect_type
        ] # List comprehension -- new list with filtered contents
          # Keep only effects that DON'T match the type we want to remove

    def process_turn_effects(self, character) -> Dict[str, Any]: # Called at the start of every turn
                                                                 # Manager handles effects, doesn't need 
                                                                 # to know character details
                                                                 # (Type Safety) Dict[str, Any] means it 
                                                                 # returns a dict with string keys
        """PROCESS ALL EFFECTS AT TURN START, RETURN RESULTS"""
        results = {
            'effects_processed': [], # List of effects that successfully processed this turn
            'effects_expired': [],   # List of effects that reached '0' duration and expired
            'resource_costs': {},    # Dict showing which resources were spent and how much
            'maintenance_failures': [] # List of effects that were removed due to 
                                       # insufficient resources
        }                              # ^ Good for UI integration

        effects_to_remove = []

        for effect in self.active_effects:
            # checks maintenence costs
            if not self._can_maintain_effect(character, effect): # checks character's current resource
                                                                 # compares maintenence cost (returns bool)
                effects_to_remove.append(effect)
                results['maintenance_failures'].append(effect.effect_type.value)
                
                continue
            # Deduct maintenence cost
            if effect.maintenance_cost > 0: # deducts if effect has a cost
                self._deduct_maintenance_cost(character, effect)
                results['resource_costs'][effect.resource_type] = effect.maintenance_cost # UI
            
            # Reduce duration (turn counter)
            effect.duration -= 1
            results['effects_processed'].append(effect.effect_type.value) # UI
            # Check expiration
            if effect.duration <= 0:
                effects_to_remove.append(effect)
                results['effects_expired'].append(effect.effect_type.value) # UI
            
        # Remove expired/failed effects
        for effect in effects_to_remove:
            self.active_effects.remove(effect)
        
        return results
    
    # Completely generic methods!
    def apply_dodge_check(self, character) -> bool:
        """Check for ANY effect that provides dodge"""
        for effect in self.active_effects:
            if EffectCategory.DODGE in effect.categories:
                dodge_chance = effect.magnitude
                if random.random() < dodge_chance:
                    return True
        return False

    def apply_damage_modification(self, character, base_damage: int, is_enemy: bool = False):
        """Apply ALL damage modifications automatically with dynamic messaging"""
        modified_damage = base_damage
        narrative_effects = []
        
        for effect in self.active_effects:
            if EffectCategory.DAMAGE_REDUCTION in effect.categories:
                reduction = int(base_damage * effect.magnitude)
                modified_damage = max(0, modified_damage - reduction)
                
                # Dynamic variables using your approach  
                if effect.effect_type.value == "magic_bubble":
                    # From defender's perspective
                    defender = "you" if not is_enemy else "them"
                    possessive = "Your" if not is_enemy else "The enemy's"
                    narrative_effects.append(f"🫧 {possessive} magical bubble shields {defender} from {reduction} damage!")
                else:
                    defender = "damage by" if not is_enemy else "your damage by"
                    possessive = "Your" if not is_enemy else "Enemy"
                    narrative_effects.append(f"🛡️ {possessive} protection reduces {defender} {reduction}!")
                    
            if EffectCategory.DAMAGE_AMPLIFICATION in effect.categories:
                extra_damage = int(base_damage * effect.magnitude)
                modified_damage += extra_damage
                
                # Handle rage conversion for Berserker Rage
                if (effect.effect_type.value == "berserker_rage" and 
                    EffectCategory.RAGE_CONVERSION in effect.categories and
                    hasattr(character, 'rage')):
                    rage_gain = extra_damage  # Convert extra damage to rage
                    character.rage += rage_gain
                    
                    # Dynamic messaging with rage conversion (from defender's perspective)
                    target = "them to take" if not is_enemy else "you to take" 
                    possessive = "Enemy's" if not is_enemy else "Your"
                    rage_text = "Enemy gains" if not is_enemy else "You gain"
                    narrative_effects.append(f"⚔️ {possessive} berserker rage causes {target} {extra_damage} extra damage!")
                    narrative_effects.append(f"🔥 {rage_text} {rage_gain} rage from the pain!")
                else:
                    # Regular damage amplification without rage conversion
                    if effect.effect_type.value == "berserker_rage":
                        target = "them to take" if not is_enemy else "you to take"
                        possessive = "Enemy's" if not is_enemy else "Your"
                        narrative_effects.append(f"⚔️ {possessive} berserker rage causes {target} {extra_damage} extra damage!")
                    else:
                        target = "enemy to take" if not is_enemy else "you to take"
                        narrative_effects.append(f"💥 Effect causes {target} {extra_damage} extra damage!")
        
        return modified_damage, narrative_effects

    def _can_maintain_effect(self, character, effect: StatusEffect) -> bool:
        """Check if character can afford maintenance cost"""
        if effect.maintenance_cost == 0: # returns True for free effects
            return True
            
        if effect.resource_type == "mana":
            return character.mana >= effect.maintenance_cost
        elif effect.resource_type == "rage":
            return character.rage >= effect.maintenance_cost
        elif effect.resource_type == "stamina":
            return character.stamina >= effect.maintenance_cost
        return False
    
    def _deduct_maintenance_cost(self, character, effect: StatusEffect) -> None:
        """Deduct maintenance cost from character resources"""
        if effect.resource_type == "mana":
            character.mana -= effect.maintenance_cost
        elif effect.resource_type == "rage":
            character.rage -= effect.maintenance_cost
        elif effect.resource_type == "stamina":
            character.stamina -= effect.maintenance_cost

    def get_active_effects_summary(self) -> List[Dict[str, Any]]:
        """Get summary of all active effects"""
        return [effect.to_dict() for effect in self.active_effects]

    def has_effect(self, effect_type: EffectType) -> bool:
        """Check if specific effect is active"""
        return any(effect.effect_type == effect_type for effect in self.active_effects)