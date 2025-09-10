
"turnbased_game"
# Support both direct execution and module execution
try:
    # When run as module: python -m projects.turnbased_game.main_gameloop.main_game_loop
    from projects.turnbased_game.character_classes.char_classes import Warrior, Rogue, Wizard, EnemyAI
except ImportError:
    # When run directly: python main_game_loop.py
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    from projects.turnbased_game.character_classes.char_classes import Warrior, Rogue, Wizard, EnemyAI
import random
import pygame
import time


# pygame.init()
# screen1 = pygame.display.set_mode((800, 600))


# Choosing player class -------------------------------------------------------------
def choose_class():
    while True:

        char_choice = input("""Choose your class A/B/C: 
                            A) Warrior : Simple. Heavy. Angry. 
                            B) Rogue   : Fast. Deadly. Runs on stamina.
                            C) Wizard  : Spell-casting. Ranged. Everything costs mana. Run out of mana, die.
                            """).lower()
        if char_choice == "a":
            player = Warrior()
            print("class chosen: Warrior")
            break
        elif char_choice == "b":
            player = Rogue()
            print("class chosen: Rogue")
            break
        elif char_choice == "c":
            player = Wizard()
            print("class chosen: Wizard")
            break
        else:
            print("incorrect input. Please try again.")
    return player

# Creating enemy -------------------------------------------------------------------------
def enemy_class():
    enemy_choice = random.choice(["warrior", "rogue", "wizard"])
    if enemy_choice == "warrior":
        enemy_ai = EnemyAI(Warrior)
    elif enemy_choice == "rogue":
        enemy_ai = EnemyAI(Rogue)
    elif enemy_choice == "wizard":
        enemy_ai = EnemyAI(Wizard)
    print(f"Enemy has chosen a class: {enemy_choice.upper()}")
    return enemy_ai
# Status Check
def gl_print_status(player, enemy):
    player.print_status()
    time.sleep(1)
    enemy.character.print_status(is_enemy=True)
# Game Loop
# The following block ensures that interactive code only runs when this file is executed directly,
# not when imported (e.g., during testing with pytest).
if __name__ == "__main__":
    # Start the game by choosing player and enemy classes
    player = choose_class()
    enemy = enemy_class()

    # Main game loop
    while player.health > 0 and enemy.character.health > 0:
        # Player's turn
        gl_print_status(player, enemy)
        player.take_turn(enemy.character)
        time.sleep(1)
        if enemy.character.health <= 0:
            print("====Your opponent has been slain. You are victorious!!====")
            break
        # Enemy's turn (random action)
        print("\n Enemy's turn!")
        enemy.take_turn(player)
        if player.health <= 0:
            print("You have been slain.")
            break
    print("=== Game Over! ===")

