"""
Rogue Character Class
Dexterity-focused character that prioritizes critical chance and stamina recovery.
"""
from .base_character import Character


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
            print(f"{attacker} {dmg} damage to {target} health. Recovered {stamina_recovery} stamina.")
        return
    
    def special(self, enemy, is_enemy=False):
        if self.stamina >= 50:
            self.stamina -= 50
            attacker = "You step" if not is_enemy else "Your opponent steps"
            target = "attack from behind your opponent" if not is_enemy else "attacks from from behind you"
            print(f"{attacker} into the shadows... and {target}...")
            dmg = self.get_attack_dmg(base=45, crit=60, super_crit=70, crit_chance=0.4, super_crit_chance=0.31)
            enemy.health -= dmg
            target = "Enemy takes" if not is_enemy else "You take"
            if dmg == 60:
                stamina_recovery = 20
                self.stamina += stamina_recovery
                print(f"CRITICAL HIT. {target} {dmg} damage. Recovered {stamina_recovery} stamina.")
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
    
    def item(self, is_enemy=False):
        if self.item_count > 0:
            self.item_count -= 1
            health_recovery = 45
            stamina_recovery = 20
            self.health += health_recovery
            self.stamina += stamina_recovery
            target = "You" if not is_enemy else "Enemy"
            print(f"""{target} takes a drink from a flask...
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
                "available": self.item_count > 0,
                "requirement": "Requires flask"
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
        
        prompt += "Enter choice (A/B/C): "
        return input(prompt).lower()
    
    def print_status(self, is_enemy=False):
        if is_enemy:
            print(f"Enemy Health: {self.health} | Enemy Stamina: {self.stamina}")
        else:
            print(f"Current Health: {self.health} | Current Stamina: {self.stamina}")
