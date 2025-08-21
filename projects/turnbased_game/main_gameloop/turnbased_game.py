
"turnbased_game"
import random

# Creating Classes
# base character created in order to be used with subclasses
# sub classes inherit the "bones" of the base character and 
# Fill in the functions with ther respective subclass attributes
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
    
char_warrior = {"health": 150, "rage": 0}
char_rogue = {"health" : 100, "stamina": 100}
char_wizard = {"health" : 75, "mana": 150}
enemy_1 = {"health" : 100, "mana" : 100}

# Warrior class -----------------------------------------------------------------
class Warrior(Character):
    def __init__(self):
        self.health = 180
        self.rage = 0
        super().__init__(self.health, self.rage) # inherits from class Character

    def attack(self, enemy, is_enemy=False):
        if is_enemy:
            print("Your enemy swings their blade at you...")
        else:    
            print(f"You swing your blade at your opponent...")
        dmg = random.choice([20, 20, 20, 20, 30])
        enemy.health -= dmg
        if dmg == 30:
            print("CRITICAL HIT")
            rage_gain = 10
        rage_gain = 10
        self.rage += rage_gain
        print(f"Enemy takes {dmg}! Recovered {rage_gain} rage.")

        return
    
    def special(self):
        if self.rage >= 20:
            self.rage -= 20
            dmg = random.choice([50, 50, 75])
            if dmg == 75:
                print("CRITICAL HIT")
            enemy_1["health"] -= dmg
            print(f"""You unleash your inner fury at your opponent. 
                  Enemy took {dmg}!""")
        else:
            print("Not enough Rage.")
        return
    
    def item(self):
        health_recovery = 60
        self.health += health_recovery
        print(f"You drink a potion. You recover {health_recovery} health.")
        return
    
    def action_prompt(self):

        action = input("""Choose action A/B/C:
                    A) Attack: 20 - 30 damage. Costs 0 rage. Recover up to 20 rage.
                    B) Special: 50 - 75 damage. Costs 20 rage.
                    C) Item: Health potion. Recovers 40 health.
                    """).lower()
        return action
    
    def print_status(self, is_enemy=False):
        if is_enemy:
            print(f"Enemy Health: {self.health} | Enemy Rage: {self.rage}")
        else:  
            print(f"Current Health: {self.health} | Current Rage: {self.rage}")
    
    def enemy_turn(self): 
        if self.health < 40 and enemy.health < 40:
            print("The enemy risks it all to strike a killing blow!")
            player.attack()

            player.item()
        

# Rogue class --------------------------------------------------------------------
class Rogue(Character):
    def __init__(self):
        self.health = 130
        self.stamina = 100
        self.item = 3
        super().__init__(self.health, self.stamina)

    def attack(self, enemy):
        print("You swiftly lunge towards you opponent for a strike...")
        dmg = random.choice([20, 20, 25, 25, 40])
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
            print(f"You've done {dmg} damage to enemy health.")
        return
    
    def special(self, enemy):
        if self.stamina >= 40:
            print("step into the shadows...and behind your opponent...")
            self.stamina -= 40
            dmg = random.choice([45, 45, 50, 50, 70])
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
    
    def item(self):
        if self.item > 1:
            self.item -= 1
            health_recovery = 30
            stamina_recovery = 20
            self.health += health_recovery
            self.stamina += stamina_recovery
            print(f"""You take a drink from your flask...
                  You recover {health_recovery} health and 
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
    def __init__(self):
        self.health = 100
        self.mana = 150
        self.item = 3
        super().__init__(self.health, self.mana)
    
    def attack(self, enemy):
        if self.mana >= 10:
            self.mana -= 10
            print("You raise your staff and summon a bolt of lightning...")
            dmg = random.choice([10, 10, 10, 10, 30])
            enemy.health -= dmg
            if dmg == 30:
                mana_recovery = 50
                print(f"CRITICAL HIT. Enemy takes {dmg} damage. ")
            else:
                mana_recovery = 25
                self.mana += mana_recovery
                print(f"Enemy takes {dmg} damage.")
        else:
            print("Not enough mana.")
        return

    def special(self, enemy):
        if self.mana >= 75:
            print("""You raise your staff and summon a giant fireball
                   towards your opponent...""")
            self.mana -= 75
            dmg = random.choice([60, 60, 60, 75])
            enemy.health -= dmg
            if dmg == 75:
                print(f"CRITICAL HIT. Enemy takes {dmg} damage.")
        else:
            print("Not enough mana.")
        return
    
    def spell_heal(self):
        if self.health > 1 and self.mana >= 25:
            self.mana -= 25
            health_recovery = 30
            self.health += health_recovery
            print(f"""You raise your staff and call upon 
                  a beam of light over yourself...
                  You recover {health_recovery} health."""
                  )
        else:
            print("Not enough mana.")
        return        
    
    def item(self):
        if self.item > 1:
            self.item -= 1

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

# Choosing player class -------------------------------------------------------------
def choose_class():
    while True:

        char_choice = input("""Choose your class A/B/C: 
                            A) Warrior
                            B) Rogue
                            C) Wizard """).lower()
        if char_choice == "a":
            player_1 = Warrior()
            print("class chosen: Warrior")
            break
        elif char_choice == "b":
            player_1 = Rogue()
            print("class chosen: Rogue")
            break
        elif char_choice == "c":
            player_1 = Wizard()
            print("class chosen: Wizard")
            break
        else:
            print("incorrect input. Please try again.")      
    return player_1

# Creating enemy -------------------------------------------------------------------------
def enemy_class():
    enemy_choice = random.choice(["warrior", "rogue", "wizard"])
    if enemy_choice == "warrior":
        enemy_1 = Warrior()
    elif enemy_choice == "rogue":
        enemy_1 = Rogue()
    elif enemy_choice == "wizard":
        enemy_1 = Wizard()
    print(f"Enemy has chosen a class: {enemy_choice.upper()}")
    return enemy_1
# Status Check
def gl_print_status(player, enemy):
    player.print_status()
    enemy.print_status(is_enemy=True)
# Game Loop
player = choose_class()
enemy = enemy_class()

while player.health > 0 and enemy.health > 0:
    # Player's turn
    while True:
        
        gl_print_status(player, enemy)
        print("\n Your turn!")
        action = player.action_prompt()
        if action == "A":
            player.attack(enemy)
            break
        elif action == "B":
            player.special(enemy)
            break
        elif action == "C":
            player.item()
            break
        elif action == "D" and isinstance(player, Wizard):
            player.spell_heal()
            break
        else:
            print("Invalid action. Please choose A, B, or C.")
            continue

    # Check if enemy is defeated
        if enemy.health <= 0:
            print("Your opponent has been slain. You are victorious!")
            break

        # Enemy's turn (random action)
        print("\n Enemy's turn!")
        
        if enemy.health < 40 and not isinstance(enemy, Wizard):
            if isinstance(enemy, Warrior):
                enemy.item()
                continue
            
            elif isinstance(enemy, Rogue):
                enemy.item()
                continue

    # def enemy_turn():