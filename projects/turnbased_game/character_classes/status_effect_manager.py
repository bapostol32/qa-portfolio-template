from typing import List, Dict, Tuple, Optional, Any
import random
from .status_effects import StatusEffect, EffectType

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

    def apply_damage_modification(self, character, base_damage: int):
        """Apply ALL damage modifications automatically"""
        modified_damage = base_damage
        effect_details = {}
        
        for effect in self.active_effects:
            if EffectCategory.DAMAGE_REDUCTION in effect.categories:
                reduction = int(base_damage * effect.magnitude)
                modified_damage = max(0, modified_damage - reduction)
                effect_details[f'{effect.effect_type.value}_reduction'] = reduction
                
            if EffectCategory.DAMAGE_AMPLIFICATION in effect.categories:
                extra_damage = int(base_damage * effect.magnitude)
                modified_damage += extra_damage
                effect_details[f'{effect.effect_type.value}_extra'] = extra_damage
        
        return modified_damage, effect_details

    def _can_maintain_effect(self, character, effect: StatusEffect) -> bool:
        """Check if character can afford maintenance cost"""
        if effect.maintenance_cost == 0:
            return True
            
        if effect.resource_type == "mana":
            return character.mana >= effect.maintenance_cost
        elif effect.resource_type == "rage":
            return character.rage >= effect.maintenance_cost
        elif effect.resource_type == "stamina":
            return character.stamina >= effect.maintenance_cost
        return False