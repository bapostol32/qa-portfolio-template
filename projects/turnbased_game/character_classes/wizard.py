"""
Wizard Character Class
Glass cannon character with high damage output, low health.
All abilities cost resource (mana). Item (mana potion) used to recover mana.
"""
from .base_character import Character


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
            dmg = self.get_attack_dmg(base=10, crit=30, crit_chance=0.35)
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
            health_recovery = 45
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
        if self.item_count > 0 and self.mana < 180:
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
                "damage": "Restores 45 health",
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
