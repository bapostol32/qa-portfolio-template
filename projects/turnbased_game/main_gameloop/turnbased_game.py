
"turnbased_game"
from turnbased_game.character_classes import Warrior, Rogue, Wizard
import random


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

# The following block ensures that interactive code only runs when this file is executed directly,
# not when imported (e.g., during testing with pytest).
if __name__ == "__main__":
    # Start the game by choosing player and enemy classes
    player = choose_class()
    enemy = enemy_class()

    # Main game loop
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