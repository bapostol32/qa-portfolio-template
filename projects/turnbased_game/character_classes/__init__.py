# This file makes the character_classes directory a Python package

# Import all classes for easy access
from .base_character import Character
from .warrior import Warrior
from .rogue import Rogue
from .wizard import Wizard
from .enemy_ai import EnemyAI

# Make classes available when importing the package
__all__ = ['Character', 'Warrior', 'Rogue', 'Wizard', 'EnemyAI']