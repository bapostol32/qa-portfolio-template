"""
Warrior Character Class
Heavy tank character with largest health pool and rage-based abilities.
"""
from .base_character import Character


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
        super().__init__(self.health, self.rage)  # inherits from class Character

    def attack(self, enemy, is_enemy=False):
        attacker = "Your enemy" if is_enemy else "You"
        target = "you" if is_enemy else "your opponent"
      
        print(f"{attacker} swings their blade at {target}...")
      
        dmg = self.get_attack_dmg(base=25, crit=40, crit_chance=0.33)
        enemy.health -= dmg
        if dmg == 40:
            print("CRITICAL HIT")
            rage_gain = 25
        else:
            rage_gain = 15
        self.rage += rage_gain
        damage_target = "You take" if is_enemy else "Enemy takes"
        resource_text = "Enemy recovers" if is_enemy else "You recover"
        print(f"{damage_target} take {dmg} damage! {resource_text} {rage_gain} rage.")
        return
    
    def attack_get_result(self, enemy, is_enemy=False):
        # 'before' values for pygame animations
        enemy_health_before = enemy.health
        rage_before = self.rage
        # value change
        dmg = self.get_attack_dmg(base=25, crit=40, crit_chance=0.33)
        enemy.health -= dmg
        if dmg == 40:
            rage_gain = 25
            is_critical = True
        else:
            rage_gain = 15
            is_critical = False
        self.rage += rage_gain
        # return rich data for pygame
        return {
            'action_type': 'attack',
            'damage': dmg,
            'critical_hit': is_critical,
            'rage_gain': rage_gain,
            'attacker': 'enemy' if is_enemy else 'player',
            'target_health_before': enemy_health_before,
            'target_health_after': enemy.health,
            'attacker_rage_before': rage_before,
            'attacker_rage_after': self.rage,
            'animation_triggers': ['sword_swing', 'critical_flash'] if is_critical else ['sword_swing'],
            'sound_effects': ['sword_hit', 'critical_sound'] if is_critical else ['sword_hit']
        }
    
    def special(self, enemy, is_enemy=False):
        if self.can_use_special():
            self.rage -= 30
            attacker = "You unleash your" if not is_enemy else "Your enemy unleashes their"
            target = "your opponent" if not is_enemy else "you"
            print(f"{attacker} inner fury opon {target}...")
            dmg = self.get_attack_dmg(base=50, crit=75, crit_chance=0.35)
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
        Returns list of actions player can perform based on 
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
                "letter": "A",
                "name": "Blade Strike",
                "damage": self.get_attack_dmg(base=25, crit=40, crit_chance=0.2, return_range=True),
                "cost": "0 rage",
                "effect": "Recover 10-20 rage when used. Rage required to perform spew",
                "available": True,
                "requirement": None
            },
            "special": {
                "letter": "B",
                "name": "Fury Strike",
                "damage": self.get_attack_dmg(base=50, crit=75, crit_chance=0.33, return_range=True),
                "cost": "20 rage",
                "effect": "High damage attack",
                "available": self.can_use_special(),
                "requirement": "Requires 30 rage."
            },
            "item": {
                "letter": "C",
                "name": "Health Potion",
                "damage": "Heals 60 Health",
                "cost": "1 potion",
                "effect": f"({self.item_count} remaining)",
                "available": self.item_count > 0,
                "requirement": "Requires potion"
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
