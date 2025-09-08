"""
Creating Classes
base character created in order to be used with subclasses
sub classes inherit the "bones" of the base character and 
Fill in the functions with ther respective subclass attributes
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
    def action_prompt(self):
        raise NotImplementedError
    def print_status(self):
        raise NotImplementedError
    
    def get_attack_dmg(self, 
                       base=None, 
                       crit=None, 
                       super_crit=None, 
                       crit_chance=None, 
                       super_crit_chance=None, 
                       return_range =False
                       ):
        """Enhanced damage calc that returns either damage value
           OR range string
        """
        if return_range:
            #range calc for UI display
            possible_damages = [base]
            if crit_chance > 0 :
                possible_damages.append(crit)
            if super_crit_chance > 0:
                possible_damages.append(super_crit)
            min_damage = min(possible_damages)
            max_damage = max(possible_damages)
            return f"{min_damage} - {max_damage}"
        else:
            #damage calc
            roll = random.random()
            if super_crit and roll < super_crit_chance:
                return super_crit
            elif roll < crit_chance:
                return crit
            else:
                return base


char_warrior = {"health": 150, "rage": 0}
char_rogue = {"health" : 100, "stamina": 100}
char_wizard = {"health" : 75, "mana": 150}
enemy_1 = {"health" : 100, "mana" : 100}

# Warrior class -----------------------------------------------------------------
class Warrior(Character):
    def __init__(self):
        self.health = 200
        self.rage = 0
        self.item_count = 3
        super().__init__(self.health, self.rage) # inherits from class Character

    def attack(self, enemy, is_enemy=False):
        if is_enemy:
            print("Your enemy swings their blade at you...")
        else:    
            print(f"You swing your blade at your opponent...")
        dmg = self.get_attack_dmg(base=25, crit=40, crit_chance=0.2)
        enemy.health -= dmg
        if dmg == 40:
            print("CRITICAL HIT")
            rage_gain = 20
        else:
            rage_gain = 10
        self.rage += rage_gain
        if is_enemy:
            print(f"You take {dmg} damage! Enemy recovers {rage_gain} rage.")
        else:    
            print(f"Enemy takes {dmg} damage! Recovered {rage_gain} rage.")
        return
    
    
    def special(self, enemy, is_enemy=False):
        if self.can_use_special():
            self.rage -= 20
            if is_enemy:
                print("The enemy unleashes its fury...")
            else:
                print("You unleash your inner fury opon your opponent...")
                dmg = self.get_attack_dmg(base=50, crit=75, crit_chance=0.33)
                enemy.health -= dmg
                if dmg == 75:
                    print("CRITICAL HIT")
                print(f"Does {dmg} damage.")
        else:
            print("Not enough Rage.")
        return
    def get_action_info(self):
        return {
            "attack": {
                "letter" : "A",
                "name" : "Blade Strike",
                "damage" : self.get_attack_dmg(base=25, crit=40, crit_chance=0.2, return_range=True),
                "cost" : "0 rage",
                "effect" : "Recover 10-20 rage",
                "available" : True,
                "requirement" : None
            },
            "special": {
                "letter": "B",
                "name" : "Fury Strike",
                "damage" : self.get_attack_dmg(base=50, crit=75, crit_chance=0.33, return_range=True),
                "cost" : "20 rage",
                "available" : True,
                "requirement" : None
            },
            "item": {
                "letter" : "C",
                "name" : "Health Potion",
                "damage" : "Heals 60 Health",
                "cost" : "1 potion",
                "effect" : f"({self.item_count} remaining)",
                "available" : self.item > 0,
                "requirement" : "Requires potion"
            }
        }
    def can_use_special(self):
        if self.rage >= 20:
            return True
        return False
    
    def item(self):
        if self.item_count > 1:
            self.item_count -= 1
            health_recovery = 60
            self.health += health_recovery
            print(f"You drink a potion. You recover {health_recovery} health.")
            return
    
    # damage calc
    def get_attack_dmg(self, base=20, crit=30, crit_chance=0.2, return_range=True): 
        return crit if random.random() < crit_chance else base
    
    def get_available_actions(self):
        """
        returns list of actions player can perform based on 
        available resources.
        """
        actions = ["attack"]
        if self.can_use_special():
            actions.append("special")
        if self.item_count > 0:
            actions.append("item")
        return actions
    
    def validate_action(self, action):
        available = self.get_available_actions()
        return action in available
    
    
    
    def print_status(self, is_enemy=False):
        if is_enemy:
            print(f"Enemy Health: {self.health} | Enemy Rage: {self.rage}")
        else:  
            print(f"Current Health: {self.health} | Current Rage: {self.rage}")
     
# Rogue class --------------------------------------------------------------------
class Rogue(Character):
    def __init__(self):
        self.health = 160
        self.stamina = 100
        self.item_count = 3
        super().__init__(self.health, self.stamina)

    def attack(self, enemy, is_enemy=False):
        if is_enemy:
            print("Your opponent swiftly lunfes towards you for a strike")
        else:
            print("You swiftly lunge towards you opponent for a strike...")
            dmg = self.get_attack_dmg(base=20, crit=25, super_crit=40, crit_chance=0.4, super_crit_chance=0.33)
            enemy.health -= dmg
            if dmg == 25:
                stamina_recovery = 25
                self.stamina += stamina_recovery
                print(f"""CRITICAL HIT. You've done {dmg} to enemy health. 
                        Recovered {stamina_recovery}!""")
            elif dmg == 40:
                stamina_recovery = 40
                self.stamina += stamina_recovery
                print(f"""SUPER CRITICAL HIT. You've done {dmg} to enemy health. 
                        Recovered {stamina_recovery} stamina""")
            else:
                stamina_recovery = 20
                self.stamina += stamina_recovery
                print(f"You've done {dmg} damage to enemy health.")
        return
    
    def special(self, enemy, is_enemy=False):
        if self.stamina >= 50:
            if is_enemy:
                print("Your opponent steps into the shadows... and attacks from behind you...")
            else:
                print("step into the shadows...and behind your opponent...")
                self.stamina -= 50
                dmg = random.choice([45, 45, 50, 50, 70])
                dmg = self.get_attack_dmg(base=45, crit=60, super_crit=70, crit_chance=0.4, super_crit_chance=0.3)
                enemy.health -= dmg
                if dmg == 50:
                    stamina_recovery = 20
                    self.stamina += stamina_recovery
                    print(f"CRITICAL HIT. Enemy takes {dmg} damage.")
                elif dmg == 70:
                    stamina_recovery = 40
                    self.stamina += stamina_recovery
                    print(f"""SUPER CRITICAL HIT. Enemy takes {dmg} damage.
                        Recovered {stamina_recovery} stamina.""")
        else:
            print("Not enough Stamina.")
        return
    # damage calc
    def get_attack_dmg(self, base, crit, super_crit, crit_chance, super_crit_chance):
        roll = random.random()
        if super_crit and roll < super_crit_chance:
            return super_crit
        elif roll <crit_chance:
            return crit
        else:
            return base
        
    def item(self):
        if self.item_count > 1:
            self.item_count -= 1
            health_recovery = 30
            stamina_recovery = 20
            self.health += health_recovery
            self.stamina += stamina_recovery
            print(f"""Takes a drink from flask...
                  Recovers {health_recovery} health and 
                  {stamina_recovery} stamina.""")
        return
    
    def action_prompt(self):
        action = input("""Choose action A/B/C:
                       A) Attack: Costs 0 Stamina. 20 - 40 damage. Recover 20 - 40 Stamina.
                       B) Special: Costs 40 Stamina. 45 - 70 damage. Critical hits restore Stamina.
                       C) Item: Recovers 30 Health and 20 Stamina.""").lower()
        return action
    
    def print_status(self, is_enemy=False):
        if is_enemy:
            print(f"Enemy Health: {self.health} | Enemy Stamina: {self.stamina}")
        else:
            print(f"Current Health: {self.health} | Current Stamina: {self.stamina}")
      
# Wizard class -----------------------------------------------------------------------                    
class Wizard(Character):
    """
    Glass cannon character
    high damage output, low health
    all abilities cost resource(mana)
    item(mana potion) used to recover mana
    """
    def __init__(self):
        self.health = 120
        self.mana = 180
        self.item_count = 3
        super().__init__(self.health, self.mana)
    
    def attack(self, enemy, is_enemy=False):
        # normal attack
        # stil costs mana
        # 20% crit chance
        # critical hits recover mana
        if self.mana >= 10:
            self.mana -= 10
            if is_enemy:
                print("The enemy Wizard raises their staff and summons a bolt of lightning...")
            else:
                print("You raise your staff and summon a bolt of lightning...")
            dmg = random.choice([10, 10, 10, 10, 30])
            dmg = self.get_attack_dmg(base=10, crit=30, crit_chance=0.2)
            enemy.health -= dmg
            if dmg == 30:
                mana_recovery = 50
                self.mana += mana_recovery
                print(f"CRITICAL HIT. Enemy takes {dmg} damage. ")
            else:
                mana_recovery = 25
                self.mana += mana_recovery
                print(f"Enemy takes {dmg} damage.")
        else:
            print("Not enough mana.")
        return

    def special(self, enemy):
        # high damage/cost heavy attack
        if self.mana >= 75:
            print("""You raise your staff and summon a giant fireball
                   towards your opponent...""")
            self.mana -= 75
            dmg = random.choice([60, 60, 60, 75])
            dmg = self.get_attack_dmg(base=60, crit=75, super_crit=0, crit_chance=0.25, super_crit_chance=0)
            enemy.health -= dmg
            if dmg == 75:
                print(f"CRITICAL HIT. Enemy takes {dmg} damage.")
        else:
            print("Not enough mana.")
        return
    
    def get_attack_dmg(self, base, crit, super_crit, crit_chance, super_crit_chance):
        roll = random.random()
        if super_crit and roll < super_crit_chance:
            return super_crit
        elif roll <crit_chance:
            return crit
        else:
            return base
        
    def spell_heal(self):
        # main way for wizard to heal
        # still costs mana
        if self.health > 1 and self.mana >= 25:
            self.mana -= 25
            health_recovery = 40
            self.health += health_recovery
            print(f"""You raise your staff and call upon 
                  a beam of light over yourself...
                  You recover {health_recovery} health."""
                  )
        else:
            print("Not enough mana.")
        return        
    
    def item(self):
        if self.item_count > 1:
            self.item_count -= 1
            mana_recovery = 50
            self.mana += mana_recovery
            print(f"""You uncork a vial and take a sip...
                  You recover {mana_recovery} mana. """)
        else:
            print("Out of potions.") # Make sure to alter in game loop so this doesn't waste a turn  
                                     # Maybe route it back to Player's turn          
        return 
    def action_prompt(self):
        action = input("""Choose action A/B/C:
                        A) Attack: 10 - 30 damage. Costs 10 mana. Recover 25 - 50 mana.
                        B) Special": 60 - 75 damage. Costs 75 mana. 
                        C) Mana Potion: Recovers 50 mana.
                        D) Healing Spell: Restores 30 health. Costs 25 mana.""").lower()
        return action
    def print_status(self, is_enemy=False):
        if is_enemy:
            print(f"Enemy Health: {self.health} | Enemy Mana: {self.mana}")
        else:
            print(f"Current Health: {self.health} | Current Mana: {self.mana}")

# Enemy AI class ---------------------------------------------------------------------
class EnemyAI:
    def __init__(self, character_class):
        self.character = character_class()
    # main logic used during enemy turn in order
    # to decide best action
    # based on available resources and player/enemy status
    def choose_action(self, player):
        health_percentage = self.character.health / self._get_max_health()
        if health_percentage < 0.25:
            return self._desperate_action(player) # prioritizes survival
        elif health_percentage <0.5:
            return self._defensive_action(player) # prioritizes health while still chance for attack
        
        else: 
            return self._offensive_action(player) # prioritizes attack methods

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
        # just for wizard to heal
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
        enemny behavior for health is 25% - 50%
        mixes healing and offense
        """
        # Wizard will always prioritize healing when available
        if isinstance(self.character, Wizard) and self.character.mana >=25:
            return "heal"
        if self.character.item_count > 0:
            return "item"
        if self._can_use_special():
            return "special"
        return "attack"
    
    def _offensive_action(self, player):
        """
        default enemy when health is > 50%
        """
        # Always go for killing blow
        if self._can_use_special() and player.health <= 50:
            return "special"
        
        # Use special when available
        if self._has_excess_resources():
            return "special"
        return "attack" # fallback option
    
    def _should_use_special(self, player):
        """
        always returns optimal choice for special usage
        """
        # when not to use special
        if not self._can_use_special():
            return False # aligns with optimal resource management
        # always go for killing blow 
        if player.health <= 50:
            return True
        # use when available
        if self._has_excess_resources():
            return True
        # conserve resources and use basic attack if sufficient to kill player
        if player.health <= 30:
            return False
        # default use for healthy target
        return True
    
    def _can_use_special(self):
        # method to determine if class is able to use special
        # based on class resource
        # important for preventing the ai from trying impossible actions
        if isinstance(self.character, Warrior):
            return self.character.rage >= 20
        elif isinstance(self.character, Rogue):
            return self.character.stamina >= 50
        if isinstance(self.character, Wizard):
            return self.character.mana >= 75
        return False # returns False otherwise
                     # safety fallback to prevent crashes
    
    def _has_excess_resources(self):
        # method to determine if class has healthy amount of resources
        # encourages special ability use
        # based on class resource
        if isinstance(self.character, Warrior):
            return self.character.rage >= 40 # double the resource requirements 
                                             # are considered abundant/excess
        elif isinstance(self.character, Rogue):
            return self.character.stamina >= 80
        elif isinstance(self.character, Wizard):
            return self.character.mana >= 150
        return False
    
    def execute_action(self, action, player):
        # enemy action method during turn
        # separates decision making from action execution for code hygeine
        # Action: action string is returned by choose_action()
        # Player: The player character to target with attacks
        if action == "attack":
            self.character.attack(player, is_enemy=True)
        elif action == "special":
            self.character.special(player, is_enemy=True)
        elif action == "item":
            self.character.item()
        elif action == "heal":
            self.character.spell_heal()
        else:
            self.character.attack(player, is_enemy=True) # Fallback in case action string 
                                                         # is invalid/unexpected
                                                         # ensures an action is always executed
    
    def take_turn(self, player):
        # main method called from the game loop
        # Player: the player character object
        print("\n --- Enemy Turn ---") # display status
        self.character.print_status(is_enemy=True) # shows enemy health
        action = self.choose_action(player) 
        self.execute_action(action, player)
        time.sleep(1) # pause for dramatic effect


