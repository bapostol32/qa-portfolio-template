
"turnbased_game"
import random

# Creating Classes
char_warrior = {"health": 150, "rage": 0}
char_rogue = {"health" : 100, "stamina": 100}
char_wizard = {"health" : 75, "mana": 150}
enemy_1 = {"health" : 100, "mana" : 100}

# Warrior class
class Warrior:
    def __init__(self, health, rage):
        self.health = health
        self.rage = rage

    def warrior_attack(self):
        if self.health > 1:
            print(f"You swing your blade at your opponent...")
            dmg = random.choice([20, 20, 20, 20, 30])
            enemy_1["health"] -= dmg
            if dmg == 30:
                print("CRITICAL HIT")
                rage_gain = 10
            rage_gain = 10
            self.rage += rage_gain
            print(f"Enemy takes {dmg}! Recovered {rage_gain} rage.")
        else:
            print("Not enough Rage.")
        return
    
    def warrior_special(self):
        if self.health > 1 and self.rage >= 20:
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
    
    def warrior_item(self):
        if self.health > 1:
            health_recovery = 40
            self.health += health_recovery
            print(f"You drink a potion. You recover {health_recovery} health.")
        return

# Rogue class
class Rogue:
    def __init__(self, health, stamina):
        self.health = health
        self.stamina = stamina

    def rogue_attack(self):
        if self.health > 1:
            print("You swiftfully lunge towards you opponent for a strike...")
            dmg = random.choice([20, 20, 25, 25, 40])
            enemy_1["health"] -= dmg
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
        else:
            print("Not enough Stamina.")
        return
    
    def rogue_special(self):
        if self.health and self.stamina >= 40:
            print("You step into the shadows...and behind your opponent...")
            self.stamina -= 40
            dmg = random.choice([45, 45, 50, 50, 70])
            enemy_1["health"] -= dmg
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
    def rogue_item(self):
        if self.health >1:
            health_recovery = 30
            stamina_recovery = 20
            self.health += health_recovery
            self.stamina += stamina_recovery
            print(f"""You take a drink from your flask...
                  You recover {health_recovery} health and 
                  {stamina_recovery} stamina.""")
        return
    
# Wizard class                     
class Wizard:
    def __init__(self, health, mana):
        self.health = health
        self.mana = mana
    
    def wizard_attack(self):
        if self.health > 1 and self.mana >= 10:
            self.mana -= 10
            print("You raise your staff and summon a bolt of lightning...")
            dmg = random.choice([10, 10, 10, 10, 30])
            enemy_1["health"] -= dmg
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

    def wizard_special(self):
        if self.health >1 and self.mana >= 75:
            print("""You raise your staff and summon a giant fireball
                   towards your opponent...""")
            self.mana -= 75
            dmg = random.choice([60, 60, 60, 75])
            enemy_1["health"] -= dmg
            if dmg == 75:
                print(f"CRITICAL HIT. Enemy takes {dmg} damage.")
        else:
            print("Not enough mana.")
        return
    
    def wizard_heal(self):
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
    
    def wizard_item(self):
        if self.health > 1:
            mana_recovery = 50
            self.mana += mana_recovery
            print(f"""You uncork a vial and take a sip...
                  You recover {mana_recovery} mana. """)            
        return
# Choosing player class
def choose_class():
    while True:

        char_choice = input("Choose your class: Warrior, Rogue, Wizard: ").lower()
        if char_choice == "warrior":
            player_1 = Warrior(**char_warrior)
            print("class chosen: Warrior")
            break
        elif char_choice == "rogue":
            player_1 = Rogue(**char_rogue)
            print("class chosen: Rogue")
            break
        elif char_choice == "wizard":
            player_1 = Wizard(**char_wizard)
            print("class chosen: Wizard")
            break
        else:
            print("incorrect input. Please try again.")      
    return player_1

# Creating enemy   
def enemy_class():
    enemy_choice = random.choice(["warrior", "rogue", "wizard"])
    if enemy_choice == "warrior":
        enemy_1 = Warrior(**char_warrior)
    elif enemy_choice == "rogue":
        enemy_1 = Rogue(**char_rogue)
    elif enemy_choice == "wizard":
        enemy_1 = Wizard(**char_wizard)
    print(f"Enemy has chosen a class: {enemy_choice.upper()}")
    return enemy_1
# Status Check
def print_status(player, enemy):
    if isinstance(player, Warrior):
        print(f"Your Health: {player.health} | Your Rage: {player.rage}")
    elif isinstance(player, Rogue):
        print(f"Your Health: {player.health} | Stamina: {player.stamina}")
    elif isinstance(player, Wizard):
        print(f"Your Health: {player.health} | Your Mana: {player.mana}")

    if isinstance(enemy, Warrior):
        print(f"Enemy Health: {enemy.health} | Enemy Rage: {enemy.rage}")
    elif isinstance(enemy, Rogue):
        print(f"Enemy Health: {enemy.health} | Enemy Stamina: {enemy.stamina}")
    elif isinstance(enemy, Wizard):
        print(f"Enemy Health: {enemy.health} | Enemy Mana: {enemy.mana}")
    
# Game Loop
player = choose_class()
enemy = enemy_class()

while player.health > 0 and enemy.health > 0:
    # Player's turn
    while True:
        print_status(player, enemy)
        print("\n Your turn!")
        if isinstance(player, Warrior):
            action = input("""Choose action A/B/C:
                        A) Attack: 20 - 30 damage. Costs 0 rage. Recover up to 20 rage.
                        B) Special: 50 - 75 damage. Costs 20 rage.
                        C) Item: Health potion. Recovers 40 health.
                        """).upper()
            if action == "A":
                player.warrior_attack()
                break
            elif action == "B":
                player.warrior_special()
                break
            elif action == "C":
                player.warrior_item()
                break
            else:
                print("Invalid action. Please choose A, B, or C.")
        elif isinstance(player, Rogue):
            action = input("""Choose action A/B/C:
                        A) Attack: 20 - 40 damage. Costs 0 stamina. Recover up to 40 stamina.
                        B) Special: 45 - 70 damage. Costs 40 stamina. Critical hits recover up to 40 stamina. 
                        C) Item: Mysterious Flask. Recovers 30 health and 20 stamina. 
                            """).upper()
            if action == "A":
                player.rogue_attack()
                break
            elif action == "B":
                player.rogue_special()
                break
            elif action == "C":
                player.rogue_item()
                break
            else:
                print("Incalid action. Please choos A, B, or C.")
        elif isinstance(player, Wizard):
            action = input("""Choose action A/B/C:
                        A) Attack: 10 - 30 damage. Costs 10 mana. Recover 25 - 50 mana.
                        B) Special": 60 - 75 damage. Costs 75 mana. 
                        C) Healing Spell: Restores 30 health. Costs 25 mana.
                        D) Mana Potion: Recovers 50 mana.""")
            if action == "A":
                player.wizard_attack()
            elif action == "B":
                player.wizard_special()
            elif action == "C":
                player.wizard_heal()
            elif action == "D":
                player.wizard_item
                

    # Check if enemy is defeated
        if enemy.health <= 0:
            print("Your opponent has been slain. You are victorious!")
            break

        # Enemy's turn (random action)
        print("\n Enemy's turn!")
        
        if enemy.health < 40 and not isinstance(enemy, Wizard):
            if isinstance(enemy, Warrior):
                enemy.warrior_item()
                continue
            
            elif isinstance(enemy, Rogue):
                enemy.rogue_item()
                continue

    # def enemy_turn():
