"""
Rogue Character Class
Dexterity-focused character that prioritizes critical chance and stamina recovery.
"""
from .base_character import Character
from .status_effects import StatusEffect, EffectType, EffectCategory
from typing import Dict, Any
class Rogue(Character):
    """
    Dexterity-focused character
    prioritizes critical chance and stamina recovery
    """
    def __init__(self):
        self.health = 160
        self.max_health = 160  # Maximum health limit
        self.stamina = 100
        self.max_stamina = 100  # Maximum stamina limit
        self.item_count = 3
        super().__init__(self.health, self.stamina)
        from .status_effect_manager import StatusEffectManager
        self.status_effects = StatusEffectManager()

    def attack(self, enemy, is_enemy=False):
        attacker = "You swiftly lunge" if not is_enemy else "Your opponent swiftly lunges"
        target = "your opponent" if not is_enemy else "you"
        print(f"{attacker} towards {target} for a strike...")
        
        # Check for dodge first
        if hasattr(enemy, 'status_effects') and enemy.status_effects.apply_dodge_check(enemy):
            print("💨 Attack dodged!")
            return
        
        dmg = self.get_attack_dmg(base=20, crit=25, super_crit=40, crit_chance=0.4, super_crit_chance=0.33)
        
        # Apply status effect damage modifications
        if hasattr(enemy, 'status_effects'):
            final_damage, narrative_effects = enemy.status_effects.apply_damage_modification(enemy, dmg, is_enemy)
            # Show narrative effects before damage
            for effect_message in narrative_effects:
                print(effect_message)
        else:
            final_damage = dmg
            
        enemy.health -= final_damage
        attacker = "You've done" if not is_enemy else "enemy does"
        target = "enemy" if not is_enemy else "your"
        if final_damage == 25:
            stamina_recovery = 25
            self.stamina += stamina_recovery
            print(f"""CRITICAL HIT. {attacker} {final_damage} to {target} health. 
                    Recovered {stamina_recovery}!""")
        elif final_damage == 40:
            stamina_recovery = 40
            self.stamina += stamina_recovery
            print(f"""SUPER CRITICAL  {attacker} {final_damage} to {target} health. 
                    Recovered {stamina_recovery} stamina""")
        else:
            print(f"{attacker} {final_damage} damage to {target} health.")
        return
    
    def special(self, enemy, is_enemy=False):
        if self.stamina >= 50:
            self.stamina -= 50
            attacker = "You step" if not is_enemy else "Your opponent steps"
            target = "attack from behind your opponent" if not is_enemy else "attacks from from behind you"
            print(f"{attacker} into the shadows... and {target}...")
            
            # Check for dodge first
            if hasattr(enemy, 'status_effects') and enemy.status_effects.apply_dodge_check(enemy):
                print("💨 Attack dodged!")
                return
            
            dmg = self.get_attack_dmg(base=45, crit=60, super_crit=70, crit_chance=0.4, super_crit_chance=0.31)
            
            # Apply status effect damage modifications
            if hasattr(enemy, 'status_effects'):
                final_damage, narrative_effects = enemy.status_effects.apply_damage_modification(enemy, dmg, is_enemy)
                # Show narrative effects before damage
                for effect_message in narrative_effects:
                    print(effect_message)
            else:
                final_damage = dmg
                
            enemy.health -= final_damage
            target = "Enemy takes" if not is_enemy else "You take"
            if final_damage == 60:
                stamina_recovery = 20
                self.stamina += stamina_recovery
                print(f"CRITICAL HIT. {target} {final_damage} damage. Recovered {stamina_recovery} stamina.")
            elif final_damage == 70:
                stamina_recovery = 40
                self.stamina += stamina_recovery
                print(f"SUPER CRITICAL HIT. {target} {final_damage} damage. Recovered {stamina_recovery} stamina.")
            else:
                print(f"{target} {final_damage} damage.")
        else:        
            print("Not enough Stamina.")
        return
    
    def activate_shadow_step(self) -> Dict[str, Any]:
        """"Turns on dodge chance for Rogue"""
        stamina_cost = 60
        if self.stamina < stamina_cost:
            return {'success': False, 'reason': 'insufficient_stamina'}
        self.stamina -= stamina_cost
        shadow_effect = StatusEffect(
            effect_type=EffectType.SHADOW_STEP,
            duration=4,
            magnitude=0.35,
            maintenance_cost=0,
            resource_type = "stamina",
            categories=EffectCategory.DODGE
        )
        self.status_effects.add_effect(shadow_effect)

        return {
            'success': True,
            'effect_applied': 'shadow_step',
            'duration': 4,
            'stamina_used': stamina_cost
        }
        
    def item(self, is_enemy=False):
        if self.item_count > 0:
            # Check if both resources are already at max
            if self.health >= self.max_health and self.stamina >= self.max_stamina:
                target = "You" if not is_enemy else "Enemy"
                print(f"{target} already have full health and stamina. The flask would be wasted.")
                return
                
            self.item_count -= 1
            health_recovery = 45
            stamina_recovery = 20
            
            # Cap both resources at maximum
            actual_health_recovery = min(health_recovery, self.max_health - self.health)
            actual_stamina_recovery = min(stamina_recovery, self.max_stamina - self.stamina)
            
            self.health = min(self.health + health_recovery, self.max_health)
            self.stamina = min(self.stamina + stamina_recovery, self.max_stamina)
            
            target = "You" if not is_enemy else "Enemy"
            print(f"""{target} takes a drink from a flask...
                  Recovers {actual_health_recovery} health and 
                  {actual_stamina_recovery} stamina.""")
        else:
            print("No items left.")
        return
    
# Helper/Gameloop Methods ----------------------------------------------------------------------------------    

    def can_use_special(self):
        return self.stamina >= 50

    def get_available_actions(self):
        actions = ["attack"]
        if self.can_use_special():
            actions.append("special")
        if self.item_count > 0 and (self.health < self.max_health or self.stamina < self.max_stamina):
            actions.append("item")
        if self.stamina >= 60 and not self.has_status_effect(EffectType.SHADOW_STEP):
            actions.append("shadow_step")
        return actions

    def validate_action(self, action):
        if action == "attack":
            return True
        elif action == "special":
            return self.can_use_special()
        elif action == "item":
            return self.item_count > 0 and (self.health < self.max_health or self.stamina < self.max_stamina)
        elif action == "shadow_step":
            return self.stamina >= 60 and not self.has_status_effect(EffectType.SHADOW_STEP)
        return False
    
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
                                            crit_chance=0.37, super_crit_chance=0.35,
                                            return_range=True),
                "cost": "50 stamina",
                "effect": "Crits restore stamina | From shadows",
                "available": self.stamina >= 50,
                "requirement": "Requires 50 stamina"
            },
            "item": {
                "letter": "C",
                "name": "Flask",
                "damage": "Heals 45 HP + 20 stamina",
                "cost": "1 flask",
                "effect": f"({self.item_count} remaining)",
                "available": self.item_count > 0 and (self.health < self.max_health or self.stamina < self.max_stamina),
                "requirement": "Requires flask & missing health/stamina"
            },
            "shadow_step": {
                "letter": "E",
                "name": "Shadow Step",
                "damage": "35% dodge chance",
                "cost": "60 stamina",
                "effect": "Enhanced evasion for 4 turns",
                "available": self.stamina >= 60 and not self.has_status_effect(EffectType.SHADOW_STEP),
                "requirement": "Requires 60 stamina & not in shadows"
            }
        }
    
    def action_prompt(self):
        action_info = self.get_action_info()
        
        prompt = "═" * 40 + "\n"
        prompt += "        ROGUE COMBAT OPTIONS\n"
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
        
        prompt += "Enter choice (A/B/C/E): "
        return input(prompt).lower()
    
    def print_status(self, is_enemy=False):
        if is_enemy:
            print(f"   🩸 Enemy Health: {self.health}/{self.max_health} | 💨 Enemy Stamina: {self.stamina}/{self.max_stamina}")
        else:
            print(f"   🩸 Current Health: {self.health}/{self.max_health} | 💨 Current Stamina: {self.stamina}/{self.max_stamina}")
        self.print_active_status_effects(is_enemy)
