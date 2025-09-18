"""
Base Character Class
Contains the foundation for all character types in the turn-based game.
Subclasses inherit the "bones" of the base character and 
fill in the functions with their respective subclass attributes.
"""
import random
import time

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
        else:
            self.attack()

    def take_turn(self, enemy):
        print("\n --- Your Turn! ---")
        time.sleep(1)
        self.print_status()
        enemy.print_status(is_enemy=True)
        
        # Import here to avoid circular imports
        from .wizard import Wizard
        if isinstance(self, Wizard):
            if self.mana < 10 and self.item_count == 0:
                self.health = 0
                print("The wizard drops their staff and falls to the ground. \n" 
                      "They have ran out of mana, and died.")
                return
        while True:
            action_choice = self.action_prompt()
            time.sleep(1)
            mapped_action = self.map_input_to_action(action_choice)
            if mapped_action and self.validate_action(mapped_action):
                self.execute_action(mapped_action, enemy)
                break
            else:
                print("Invalid choice. Please try again.")
        time.sleep(1)

    # def status
        

# Character stat templates
char_warrior = {"health": 150, "rage": 0}
char_rogue = {"health": 100, "stamina": 100}
char_wizard = {"health": 75, "mana": 150}
enemy_1 = {"health": 100, "mana": 100}
