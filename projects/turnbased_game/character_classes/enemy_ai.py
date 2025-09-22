"""
Enemy AI Class
Intelligent enemy behavior system that adapts strategy based on health status
and available resources.
"""
import random
import time
from .warrior import Warrior
from .rogue import Rogue
from .wizard import Wizard
from .status_effects import  EffectType

class EnemyAI:
    def __init__(self, character_class):
        self.character = character_class()
    
    # main logic used during enemy turn in order
    # to decide best action
    def choose_action(self, player):
        health_percentage = self.character.health / self._get_max_health()
        if health_percentage < 0.25:
            return self._desperate_action(player)  # prioritizes survival
        elif health_percentage < 0.5:
            return self._defensive_action(player)  # prioritizes health while still chance for attack
        else: 
            return self._offensive_action(player)  # prioritizes attack methods

    def _get_max_health(self):
        """
        creates a new instance of the same class
        consistently gets original health
        """
        fresh_instance = self.character.__class__()
        return fresh_instance.health

    def _desperate_action(self, player):
        """
        enemy behavior for when health is < 25%
        prioritizes survival
        """
        if self._can_use_status_abilities() and self._should_use_status_effects(player):
        # Wizard: Magic Bubble for damage reduction (defensive)
            if isinstance(self.character, Wizard):
                return "cast_magic_bubble"
            # Rogue: Shadow Step for dodge chance (defensive)
            elif isinstance(self.character, Rogue):
                return "activate_shadow_step"
            elif isinstance(self.character, Warrior) and self.character.item_count > 0: # Makes sure Warrior can heal after
                return "enter_berserker_rage" 
        if isinstance(self.character, Wizard) and self.character.mana >= 25:
            return "heal"
        if self.character.item_count > 0:
            return "item"
        # if unable to heal the character will resort to offense
        if self._can_use_special():
            return "special"
        return "attack"
    
    def _defensive_action(self, player):
        """
        enemy behavior for health is 25% - 50%
        mixes healing and offense
        """
        if self._can_use_status_abilities() and self._should_use_status_effects(player):
            if isinstance(self.character, Wizard):
                return "cast_magic_bubble"
            elif isinstance(self.character, Rogue):
                return "activate_shadow_step"
        if isinstance(self.character, Wizard) and self.character.mana >= 25:
            return random.choice(("heal", "attack")) 
        if self.character.item_count > 0:
            return random.choice(("item", "attack"))
        if self._can_use_special():
            return "special"
        return "attack"
    
    def _offensive_action(self, player):
        """
        default enemy when health is > 50%
        """
        # AGGRESSIVE STATUS EFFECTS - When Safe to Risk
        if self._can_use_status_abilities() and self._should_use_status_effects(player):
            # Warrior: Berserker Rage when healthy (aggressive)
            if isinstance(self.character, Warrior) and self.character.health > 100:
                return "enter_berserker_rage"
        # Always go for killing blow
        if self._can_use_special() and player.health <= 50:
            return "special"
        
        # Use special when available
        if self._has_excess_resources():
            return "special"
        return "attack"  # fallback option
    
    def _should_use_special(self, player):
        """
        always returns optimal choice for special usage
        """
        # when not to use special
        if not self._can_use_special():
            return False  # aligns with optimal resource management
        # always go for killing blow 
        if player.health <= 50:
            return True
        # use when available
        if self._has_excess_resources():
            return True
        # conserve resources and use basic attack if sufficient to kill player
        if player.health <= 30:
            return False
        return True
    
    def _can_use_special(self):
        # method to determine if class is able to use special
        # important for preventing the ai from trying impossible actions
        if isinstance(self.character, Warrior):
            return self.character.rage >= 30
        elif isinstance(self.character, Rogue):
            return self.character.stamina >= 50
        if isinstance(self.character, Wizard):
            return self.character.mana >= 75
        return False 
    
    def _can_use_status_abilities(self): # Checks if there are enough resources for status effect
        if isinstance(self.character, Wizard):
            return self.character.mana >= 50  
        elif isinstance(self.character, Warrior):
            return self.character.rage >= 75 
        elif isinstance(self.character, Rogue):
            return self.character.stamina >= 60  
        return False

    def _should_use_status_effects(self, player):
        """Determine if now is a good time to use status abilities"""
        # Don't use if already active
        if hasattr(self.character, 'status_effects'):
            if isinstance(self.character, Wizard) and self.character.status_effects.has_effect(EffectType.MAGIC_BUBBLE):
                return False
            if isinstance(self.character, Warrior) and self.character.status_effects.has_effect(EffectType.BERSERKER_RAGE):
                return False
            if isinstance(self.character, Rogue) and self.character.status_effects.has_effect(EffectType.SHADOW_STEP):
                return False
        
        return True
    
    def _has_excess_resources(self):
        # method to determine if class has healthy amount of resources
        # encourages special ability use
        if isinstance(self.character, Warrior):
            return self.character.rage >= 45  # double the resource requirements 
                                             # are considered abundant/excess
        elif isinstance(self.character, Rogue):
            return self.character.stamina >= 75
        elif isinstance(self.character, Wizard):
            return self.character.mana >= 100
        return False
    
    def execute_action(self, action, player):
        # enemy action method during turn
        # separates decision making from action execution for code hygiene
        if action == "attack":
            self.character.attack(player, is_enemy=True)
        elif action == "special":
            self.character.special(player, is_enemy=True)
        elif action == "item":
            self.character.item(is_enemy=True)
        elif action == "heal":
            self.character.spell_heal(is_enemy=True)
        elif action == "cast_magic_bubble":
            result = self.character.cast_magic_bubble()
            if result['success']:
                print("Enemy wizard casts a protective magic bubble!")
            else:
                print("Enemy wizard failed to cast magic bubble.")
                self.character.attack(player, is_enemy=True)  # Fallback
        elif action == "activate_shadow_step":
            result = self.character.activate_shadow_step()
            if result['success']:
                print("Enemy rogue melts into the shadows!")
            else:
                print("Enemy rogue failed to activate shadow step.")
                self.character.attack(player, is_enemy=True)  # Fallback
        elif action == "enter_berserker_rage":
            result = self.character.enter_berserker_rage()
            if result['success']:
                print("Enemy warrior enters a berserker rage!")
            else:
                print("Enemy warrior failed to enter berserker rage.")
                self.character.attack(player, is_enemy=True)  # Fallback
        else:
            self.character.attack(player, is_enemy=True)
            
    def take_turn(self, player):
        # main method called from the game loop
        print("\n --- Enemy Turn ---")
        time.sleep(1)  # display status
        self.character.print_status(is_enemy=True)
        if isinstance(self.character, Wizard) and self.character.mana < 10 and self.character.item_count <= 0:
            self.character.health = 0
            print("""
                The enemy wizard drops their staff and falls to the ground.
                They have run out of mana and died.
                """)
        time.sleep(1)  # shows enemy health
        action = self.choose_action(player) 
        self.execute_action(action, player)
        time.sleep(1)  # pause for dramatic effect
