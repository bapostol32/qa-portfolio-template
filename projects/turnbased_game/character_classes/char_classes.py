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
        """returns either damage valuu OR range string"""
        if return_range:
            #range calc for UI display
            possible_damages = [base]
            if crit_chance > 0 :
                possible_damages.append(crit)
            if super_crit and super_crit_chance > 0:
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
            
    def map_input_to_action(self, action_name):
        if action_name == "a":
            return "attack"
        elif action_name == "b":
            return "special"
        elif action_name == "c":
            return "item"
        elif action_name == "d" and isinstance(self, Wizard):
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
        while True:
            action_choice = self.action_prompt()
            time.sleep(1)
            mapped_action = self.map_input_to_action(action_choice)
            if mapped_action and self.validate_action(mapped_action):
                self.execute_action(mapped_action, enemy)
                break
            else:
                print("invalid choice. Please try again.")
        time.sleep(1)
            
            

char_warrior = {"health": 150, "rage": 0}
char_rogue = {"health" : 100, "stamina": 100}
char_wizard = {"health" : 75, "mana": 150}
enemy_1 = {"health" : 100, "mana" : 100}

# Warrior class -----------------------------------------------------------------
class Warrior(Character):
    """
    Heavy tank character
    Largest health pool
    Runs on rage
    """
    def __init__(self):
        self.health = 200
        self.rage = 0
        self.item_count = 3
        super().__init__(self.health, self.rage) # inherits from class Character

    def attack(self, enemy, is_enemy=False):
        attacker = "Your enemy" if is_enemy else "You"
        target = "you" if is_enemy else "your opponent"
      
        print(f"{attacker} swings their blade at {target}...")
      
        dmg = self.get_attack_dmg(base=25, crit=40, crit_chance=0.2)
        enemy.health -= dmg
        if dmg == 40:
            print("CRITICAL HIT")
            rage_gain = 20
        else:
            rage_gain = 10
        self.rage += rage_gain
        damage_target = "You take" if is_enemy else "Enemy takes"
        resource_text = "Enemy recovers" if is_enemy else "You recover"
        print(f"{damage_target} take {dmg} damage! {resource_text} {rage_gain} rage.")
        return
    
    def special(self, enemy, is_enemy=False):
        if self.can_use_special():
            self.rage -= 30
            attacker = "You unleash your" if not is_enemy else "Your enemy unleashes their"
            target = "your opponent" if not is_enemy else "you"
            print(f"{attacker} inner fury opon {target}...")
            dmg = self.get_attack_dmg(base=50, crit=75, crit_chance=0.33)
            enemy.health -= dmg
            if dmg == 75:
                print("CRITICAL HIT")
            print(f"Does {dmg} damage.")
        else:
            print("Not enough Rage.")
        return
    
    def can_use_special(self):
        if self.rage >= 30:
            return True
        return False
    
    def item(self, is_enemy=False):
        if self.item_count > 0:
            target = "You drink" if not is_enemy else "Enemy drinks"
            effect = "You recover" if not is_enemy else "Enemy recovers"
            self.item_count -= 1
            health_recovery = 60
            self.health += health_recovery
            print(f"{target} a potion. {effect} {health_recovery} health.")
            return
    
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
                "effect" : "High damage attack",
                "available" : self.can_use_special(),
                "requirement" : None
            },
            "item": {
                "letter" : "C",
                "name" : "Health Potion",
                "damage" : "Heals 60 Health",
                "cost" : "1 potion",
                "effect" : f"({self.item_count} remaining)",
                "available" : self.item_count > 0,
                "requirement" : "Requires potion"
            }
        }
    
    def action_prompt(self):
        action_info = self.get_action_info()

        prompt = "=" * 40 + "\n"
        prompt += "        WARRIOR COMBAT OPTIONS\n"
        prompt += "═" * 40 + "\n"
        
        for info in action_info.values():
            letter = info["letter"]
            name = info["name"]
            damage = info["damage"]
            cost = info["cost"] 
            effect = info["effect"]
            available = info["available"]
            
            if available:
                prompt += f"{letter}) {name}: {damage}\n"
                prompt += f"   └─ Cost: {cost}\n"
                prompt += f"   └─ Effect: {effect}\n"
            else:
                prompt += f"{letter}) {name}: [UNAVAILABLE]\n"
                prompt += f"   └─ {info['requirement']}\n"
            prompt += "\n"
        
        prompt += "Enter choice (A/B/C): "
        return input(prompt).lower()
    
    def print_status(self, is_enemy=False):
        if is_enemy:
            print(f"Enemy Health: {self.health} | Enemy Rage: {self.rage}")
        else:  
            print(f"Current Health: {self.health} | Current Rage: {self.rage}")
     
# Rogue class --------------------------------------------------------------------
class Rogue(Character):
    """
    Dexterity-focused character
    prioritizes critical chance and stamina recovery
    """
    def __init__(self):
        self.health = 160
        self.stamina = 100
        self.item_count = 3
        super().__init__(self.health, self.stamina)

    def attack(self, enemy, is_enemy=False):
        attacker = "You swiftly lunge" if not is_enemy else "Your opponent swiftly lunges"
        target = "your opponent" if not is_enemy else "you"
        print(f"{attacker} towards {target} for a strike...")
        dmg = self.get_attack_dmg(base=20, crit=25, super_crit=40, crit_chance=0.4, super_crit_chance=0.33)
        enemy.health -= dmg
        attacker = "You've done" if not is_enemy else "enemy does"
        target = "enemy" if not is_enemy else "your"
        if dmg == 25:
            stamina_recovery = 25
            self.stamina += stamina_recovery
            print(f"""CRITICAL HIT. {attacker} {dmg} to {target} health. 
                    Recovered {stamina_recovery}!""")
        elif dmg == 40:
            stamina_recovery = 40
            self.stamina += stamina_recovery
            print(f"""SUPER CRITICAL  {attacker} {dmg} to {target} health. 
                    Recovered {stamina_recovery} stamina""")
        else:
            stamina_recovery = 20
            self.stamina += stamina_recovery
            print(f"{attacker} {dmg} damage to {target} health.")
        return
    
    def special(self, enemy, is_enemy=False):
        if self.stamina >= 50:
            self.stamina -= 50
            attacker = "You step" if not is_enemy else "Your opponent steps"
            target = "attack from behind your opponent" if not is_enemy else "attacks from from behind you"
            print(f"{attacker} into the shadows... and {target}...")
            dmg = self.get_attack_dmg(base=45, crit=60, super_crit=70, crit_chance=0.4, super_crit_chance=0.3)
            enemy.health -= dmg
            target = "Enemy takes" if not is_enemy else "You take"
            if dmg == 60:
                stamina_recovery = 20
                self.stamina += stamina_recovery
                print(f"CRITICAL HIT. {target} {dmg} damage.")
            elif dmg == 70:
                stamina_recovery = 40
                self.stamina += stamina_recovery
                print(f"""
                    SUPER CRITICAL HIT. {target} takes {dmg} damage.
                    Recovered {stamina_recovery} stamina.
                    """)
            else:
                print(f"{target} {dmg} damage.")
        else:        
            print("Not enough Stamina.")
        return
    
    def can_use_special(self):
        return self.stamina >= 50

    def get_available_actions(self):
        actions = ["attack"]
        if self.can_use_special():
            actions.append("special")
        if self.item_count > 0:
            actions.append("item")
        return actions

    def validate_action(self, action):
        available = self.get_available_actions()
        return action in available
    
    def item(self):
        if self.item_count > 0:
            self.item_count -= 1
            health_recovery = 45
            stamina_recovery = 20
            self.health += health_recovery
            self.stamina += stamina_recovery
            print(f"""Takes a drink from a flask...
                  Recovers {health_recovery} health and 
                  {stamina_recovery} stamina.""")
        return
    
    def get_action_info(self):
        return {
            "attack": {
                "letter": "A",
                "name": "Swift Strike", 
                "damage": self.get_attack_dmg(base=20, crit=25, super_crit=40, 
                                            crit_chance=0.4, super_crit_chance=0.33, 
                                            return_range=True),
                "cost": "0 stamina",
                "effect": "Recover 20-40 stamina | High crit chance",
                "available": True,
                "requirement": None
            },
            "special": {
                "letter": "B",
                "name": "Shadow Strike",
                "damage": self.get_attack_dmg(base=45, crit=60, super_crit=70,
                                            crit_chance=0.4, super_crit_chance=0.3,
                                            return_range=True),
                "cost": "50 stamina",
                "effect": "Crits restore stamina | From shadows",
                "available": self.stamina >= 50,
                "requirement": "Requires 50 stamina"
            },
            "item": {
                "letter": "C",
                "name": "Flask",
                "damage": "Heals 30 HP + 20 stamina",
                "cost": "1 flask",
                "effect": f"({self.item_count} remaining)",
                "available": self.item_count > 0,
                "requirement": "Requires flask"
            }
        }
    
    def action_prompt(self):
        action_info = self.get_action_info()
        
        prompt = "═" * 40 + "\n"
        prompt += "        ROGUE COMBAT OPTIONS\n"
        prompt += "═" * 40 + "\n"
        
        for  info in action_info.values():
            letter = info["letter"]
            name = info["name"]
            damage = info["damage"]
            cost = info["cost"] 
            effect = info["effect"]
            available = info["available"]
            
            if available:
                prompt += f"{letter}) {name}: {damage}\n"
                prompt += f"   └─ Cost: {cost}\n"
                prompt += f"   └─ Effect: {effect}\n"
            else:
                prompt += f"{letter}) {name}: [UNAVAILABLE]\n"
                prompt += f"   └─ {info['requirement']}\n"
            prompt += "\n"
        
        prompt += "Enter choice (A/B/C): "
        return input(prompt).lower()
    
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
        if self.mana >= 10:
            self.mana -= 10
            attacker = "You raise your staff" if not is_enemy else "The enemy raises their staff"
            target = "Enemy receives" if not is_enemy else "You receive"
            print(f"{attacker} raises their staff and summons a bolt of lightning...")
            dmg = self.get_attack_dmg(base=10, crit=30, crit_chance=0.2)
            enemy.health -= dmg
            if dmg == 30:
                mana_recovery = 50
                self.mana += mana_recovery
                print(f"CRITICAL HIT. {target} takes {dmg} damage. ")
            else:
                mana_recovery = 25
                self.mana += mana_recovery
                print(f"{target} takes {dmg} damage.")
        else:
            print("Not enough mana.")
        return

    def special(self, enemy, is_enemy=False):
        # high damage/cost heavy attack
        if self.mana >= 75:
            attacker = "You raise your" if not is_enemy else "Your enemy raises their"
            target = "Enemy receives" if not is_enemy else "You receive"
            print(f"""
            {attacker} staff and summons a giant fireball...
            """)
            self.mana -= 75
            dmg = self.get_attack_dmg(base=60, crit=75, super_crit=0, crit_chance=0.25, super_crit_chance=0)
            enemy.health -= dmg
            if dmg == 75:
                print("CRITICAL HIT.")
            print(f"{target} takes {dmg} damage.")
        else:
            print("Not enough mana.")
        return
    
    def spell_heal(self, is_enemy=False):
        # main way for wizard to heal
        # still costs mana
        if self.mana >= 25:
            self.mana -= 25
            target = "you" if not is_enemy else "your enemy"
            health_recovery = 60
            self.health += health_recovery
            print(f"""A beam of light falls upon
                  {target}...
                  Recover {health_recovery} health."""
                  )
        else:
            print("Not enough mana.")
        return        
    
    def item(self, is_enemy=False):
        if self.item_count > 0:
            self.item_count -= 1
            target = "You uncork" if not is_enemy else "Your enemy uncorks"
            mana_recovery = 50
            self.mana += mana_recovery
            print(f"""{target} a vial and take a sip...
                  Recover {mana_recovery} mana. """)
        else:
            print("Out of potions.")       
        return 
    
    def can_use_special(self):
        return self.mana >= 75

    def can_use_attack(self):
        return self.mana >= 10

    def can_use_heal(self):
        return self.mana >= 25 and self.health < 120

    def get_available_actions(self):
        actions = []
        if self.can_use_attack():
            actions.append("attack")
        if self.can_use_special():
            actions.append("special")
        if self.item_count > 0:
            actions.append("item")
        if self.can_use_heal():
            actions.append("heal")
        return actions

    def validate_action(self, action):
        if action == "attack":
            return self.can_use_attack()
        elif action == "special": 
            return self.can_use_special()
        elif action == "item":
            return self.item_count > 0
        elif action == "heal":
            return self.can_use_heal()
        return False
    
    def get_action_info(self):
        return {
            "attack": {
                "letter": "A",
                "name": "Lightning Bolt",
                "damage": self.get_attack_dmg(base=10, crit=30, crit_chance=0.2, return_range=True),
                "cost": "10 mana", 
                "effect": "Recover 25-50 mana on crit",
                "available": self.mana >= 10,
                "requirement": "Requires 10 mana"
            },
            "special": {
                "letter": "B",
                "name": "Fireball",
                "damage": self.get_attack_dmg(base=60, crit=75, crit_chance=0.25, return_range=True),
                "cost": "75 mana",
                "effect": "Devastating magical attack",
                "available": self.mana >= 75,
                "requirement": "Requires 75 mana"
            },
            "item": {
                "letter": "C", 
                "name": "Mana Potion",
                "damage": "Restores 50 mana",
                "cost": "1 potion",
                "effect": f"({self.item_count} remaining)",
                "available": self.item_count > 0,
                "requirement": "Requires potion"
            },
            "heal": {
                "letter": "D",
                "name": "Healing Light", 
                "damage": "Restores 40 health",
                "cost": "25 mana",
                "effect": "Divine healing magic",
                "available": self.mana >= 25 and self.health < 120,
                "requirement": "Requires 25 mana & missing health"
            }
        }
    def action_prompt(self):
        action_info = self.get_action_info()
        
        prompt = "═" * 40 + "\n"
        prompt += "        WIZARD SPELLBOOK\n"
        prompt += "═" * 40 + "\n"
        
        for info in action_info.values():
            letter = info["letter"]
            name = info["name"]
            damage = info["damage"]
            cost = info["cost"] 
            effect = info["effect"]
            available = info["available"]
            
            if available:
                prompt += f"{letter}) {name}: {damage}\n"
                prompt += f"   └─ Cost: {cost}\n"
                prompt += f"   └─ Effect: {effect}\n"
            else:
                prompt += f"{letter}) {name}: [UNAVAILABLE]\n"
                prompt += f"   └─ {info['requirement']}\n"
            prompt += "\n"
        
        prompt += "Enter choice (A/B/C/D): "
        return input(prompt).lower()
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
    
    def _has_excess_resources(self):
        # method to determine if class has healthy amount of resources
        # encourages special ability use
        if isinstance(self.character, Warrior):
            return self.character.rage >= 60 # double the resource requirements 
                                             # are considered abundant/excess
        elif isinstance(self.character, Rogue):
            return self.character.stamina >= 80
        elif isinstance(self.character, Wizard):
            return self.character.mana >= 150
        return False
    
    def execute_action(self, action, player):
        # enemy action method during turn
        # separates decision making from action execution for code hygeine
        if action == "attack":
            self.character.attack(player, is_enemy=True)
        elif action == "special":
            self.character.special(player, is_enemy=True)
        elif action == "item":
            self.character.item()
        elif action == "heal":
            self.character.spell_heal()
        else:
            self.character.attack(player, is_enemy=True)
    
    def take_turn(self, player):
        # main method called from the game loop
        print("\n --- Enemy Turn ---")
        time.sleep(1) # display status
        self.character.print_status(is_enemy=True)
        time.sleep(1) # shows enemy health
        action = self.choose_action(player) 
        self.execute_action(action, player)
        time.sleep(1) # pause for dramatic effect


