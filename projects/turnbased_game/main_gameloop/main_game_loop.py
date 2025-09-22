
"turnbased_game"
# Support both direct execution and module execution
try:
    # When run as module: python -m projects.turnbased_game.main_gameloop.main_game_loop
    from projects.turnbased_game.character_classes import Warrior, Rogue, Wizard, EnemyAI
except ImportError:
    # When run directly: python main_game_loop.py
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    from projects.turnbased_game.character_classes import Warrior, Rogue, Wizard, EnemyAI
import random
import pygame
import time

# Choosing player class -------------------------------------------------------------
def choose_class():
    print("\n" + "🗡️" + "="*50 + "🗡️")
    print("           🎭 CHARACTER SELECTION 🎭")
    print("🗡️" + "="*50 + "🗡️")
    
    while True:
        char_choice = input("""\n🎯 Choose your class A/B/C: 
                            A) ⚔️  Warrior : Simple. Heavy. Angry. 
                            B) 🗡️  Rogue   : Fast. Deadly. Runs on stamina.
                            C) 🧙  Wizard  : Wise. Powerful. Everything costs mana. Run out of mana, die.
                            
Enter your choice: """).lower()
        if char_choice == "a":
            player = Warrior()
            print("\n✅ Class chosen: ⚔️ Warrior")
            break
        elif char_choice == "b":
            player = Rogue()
            print("\n✅ Class chosen: 🗡️ Rogue")
            break
        elif char_choice == "c":
            player = Wizard()
            print("\n✅ Class chosen: 🧙 Wizard")
            break
        else:
            print("\n❌ Incorrect input. Please try again.")
    return player

# Creating enemy -------------------------------------------------------------------------
def enemy_class():
    enemy_choice = random.choice(["warrior", "rogue", "wizard"])
    if enemy_choice == "warrior":
        enemy_ai = EnemyAI(Warrior)
        enemy_icon = "⚔️"
    elif enemy_choice == "rogue":
        enemy_ai = EnemyAI(Rogue)
        enemy_icon = "🗡️"
    elif enemy_choice == "wizard":
        enemy_ai = EnemyAI(Wizard)
        enemy_icon = "🧙"
    
    print(f"\n🎯 Enemy has chosen a class: {enemy_icon} {enemy_choice.upper()}")
    return enemy_ai
# Status Check
def gl_print_status(player, enemy):
    player.print_status()
    time.sleep(1)
    enemy.character.print_status(is_enemy=True)

# In turnbased_game.py - add turn processing
def process_turn_start(character):
    """Process status effects at turn start"""
    turn_results = character.process_turn_start()
    
    # Display results to player with better formatting
    if turn_results.get('effects_processed'):
        print(f"✨ Active effects: {', '.join(turn_results['effects_processed'])}")
    
    if turn_results.get('effects_expired'):
        print(f"⏰ Effects expired: {', '.join(turn_results['effects_expired'])}")
    
    if turn_results.get('maintenance_failures'):
        print(f"🔋 Effects lost due to insufficient resources!")

# In attack processing - add dodge and damage modification
def process_attack(self, attacker, target):
    # Check for dodge first
    if target.status_effects.apply_dodge_check(target):
        print("Attack dodged!")
        return
    
    # Calculate base damage
    base_damage = attacker.get_attack_dmg(...)
    
    # Apply status effect modifications
    final_damage, effect_details = target.status_effects.apply_damage_modification(target, base_damage)
    
    # Apply damage and show effects
    target.health -= final_damage
    if effect_details:
        print(f"Status effects: {effect_details}")

def attack_with_status_effects(self, enemy, is_enemy=False):
    # Check for dodge first
    if hasattr(enemy, 'status_effects') and enemy.status_effects.apply_dodge_check(enemy):
        print("Attack dodged!")
        return
    
    # Calculate base damage using existing method
    dmg = self.get_attack_dmg(base=25, crit=40, crit_chance=0.33)  # Example values
    
    # Apply status effect modifications
    if hasattr(enemy, 'status_effects'):
        final_damage, effect_details = enemy.status_effects.apply_damage_modification(enemy, dmg)
        if effect_details:
            print(f"Status effects: {effect_details}")
    else:
        final_damage = dmg
    
    # Apply final damage
    enemy.health -= final_damage

# Game Loop
# The following block ensures that interactive code only runs when this file is executed directly,
# not when imported (e.g., during testing with pytest).
if __name__ == "__main__":
    # Start the game by choosing player and enemy classes
    player = choose_class()
    enemy = enemy_class()

    # Main game loop
    while player.health > 0 and enemy.character.health > 0:
        print("\n" + "🔄" + "="*48 + "🔄")
        print("           🌟 NEW ROUND BEGINS 🌟")
        print("🔄" + "="*48 + "🔄")
        
        # Process status effects at the start of the round
        process_turn_start(player)
        process_turn_start(enemy.character)
        
        # Player's turn
        player.take_turn(enemy.character)
        
        time.sleep(1)
        if enemy.character.health <= 0:
            print("\n" + "🎉" + "="*40 + "🎉")
            print("🏆 Your opponent has been slain. You are victorious! 🏆")
            print("🎉" + "="*40 + "🎉")
            break
            
        # Enemy's turn (random action)
        print("\n" + "⚔️" + "="*20 + " ENEMY TURN " + "="*20 + "⚔️")
        enemy.take_turn(player)
        
        if player.health <= 0:
            print("\n" + "💀" + "="*30 + "💀")
            print("☠️  You have been slain. ☠️")
            print("💀" + "="*30 + "💀")
            break
            
    print("\n" + "🎮" + "="*20 + " GAME OVER " + "="*20 + "🎮")