# character_classes/status_effects.py
from dataclasses import dataclass
from typing import Dict, Any
from enum import Enum, Flag

class EffectType(Enum): # Enum created simple named constants
    MAGIC_BUBBLE = "magic_bubble"
    BERSERKER_RAGE = "berserker_rage" 
    SHADOW_STEP = "shadow_step"

class EffectCategory(Flag): # Flag creates constants that can be combined using "|" operator
    """What capabilities this effect provides"""
    NONE = 0
    DODGE = 1                    # Provides dodge chance
    DAMAGE_REDUCTION = 2         # Reduces incoming damage
    DAMAGE_AMPLIFICATION = 4     # Increases incoming damage
    RAGE_CONVERSION = 8          # Converts damage to rage
    MANA_DRAIN = 16             # Costs mana per turn

@dataclass # Auto-generates boilerplate methods for clean data-holding classes
class StatusEffect:
    effect_type: EffectType
    duration: int
    magnitude: float
    maintenance_cost: int
    resource_type: str
    categories: EffectCategory   # What this effect can do

    def to_dict(self) -> Dict[str, Any]: 
        return {
            'effect_type': self.effect_type.value,    # Extracts string from EffectTypr enum (e.g. "magic_buibble")
            'duration': self.duration,                # Copies the distinct attributes
            'magnitude': self.magnitude,              # Attribute cont.
            'maintenance_cost': self.maintenance_cost,# Attribute cont.
            'resource_type': self.resource_type,      # Attribute cont.
            'categories': self.categories.value       # Extract int value from Flag enum
        }