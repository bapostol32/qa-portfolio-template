"""
Wizard Character Class
Glass cannon character with high damage output, low health.
All abilities cost resource (mana). Item (mana potion) used to recover mana.
"""
from .base_character import Character
from typing import Dict, Any
from .status_effects import StatusEffect, EffectType, EffectCategory
class Wizard(Character):
    """
    Glass cannon character
    high damage output, low health
    all abilities cost resource(mana)
    item(mana potion) used to recover mana
    """
    def __init__(self):
        self.health = 120
        self.max_health = 120  # Maximum health limit
        self.mana = 180
        self.max_mana = 180    # Maximum mana limit
        self.item_count = 3
        super().__init__(self.health, self.mana)
        
        from .status_effect_manager import StatusEffectManager
        self.status_effects = StatusEffectManager()
    
    def attack(self, enemy, is_enemy=False):
        if self.mana >= 10:
            self.mana -= 10
            attacker = "You raise your staff" if not is_enemy else "The enemy raises their staff"
            target = "Enemy receives" if not is_enemy else "You receive"
            print(f"{attacker} raises their staff and summons a bolt of lightning...")
            
            # Check for dodge first
            if hasattr(enemy, 'status_effects') and enemy.status_effects.apply_dodge_check(enemy):
                print("💨 Attack dodged!")
                return
            
            dmg = self.get_attack_dmg(base=10, crit=35, crit_chance=0.40)
            target = "You" if not is_enemy else "Enemy"
            # Apply status effect damage modifications
            if hasattr(enemy, 'status_effects'):
                final_damage, narrative_effects = enemy.status_effects.apply_damage_modification(enemy, dmg, is_enemy)
                # Show narrative effects before damage
                for effect_message in narrative_effects:
                    print(effect_message)
            
            else:
                final_damage = dmg
                
            enemy.health -= final_damage
            if final_damage == 35:
                mana_recovery = 50
                self.mana += mana_recovery
                
                print(f"CRITICAL HIT. {target} takes {final_damage} damage. Recover {mana_recovery} mana.")
            else:
                mana_recovery = 25
                self.mana += mana_recovery
                print(f"{target} takes {final_damage} damage.")
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
            
            # Check for dodge first
            if hasattr(enemy, 'status_effects') and enemy.status_effects.apply_dodge_check(enemy):
                print("💨 Attack dodged!")
                return
            
            dmg = self.get_attack_dmg(base=60, crit=75, super_crit=0, crit_chance=0.30, super_crit_chance=0)
            
            # Apply status effect damage modifications
            if hasattr(enemy, 'status_effects'):
                final_damage, narrative_effects = enemy.status_effects.apply_damage_modification(enemy, dmg, is_enemy)
                # Show narrative effects before damage
                for effect_message in narrative_effects:
                    print(effect_message)
            else:
                final_damage = dmg
                
            enemy.health -= final_damage
            if final_damage == 75:
                attacker = "Enemy takes" if not is_enemy else "You take"
                print("CRITICAL HIT.")
            print(f"{target} {final_damage} damage.")
        else:
            print("Not enough mana.")
        return
    
    def spell_heal(self, is_enemy=False):
        # main way for wizard to heal
        # still costs mana
        if self.mana >= 25:
            if self.health >= self.max_health:
                target = "You" if not is_enemy else "Your enemy"
                print(f"{target} already have full health. The spell would be wasted.")
                return
                
            self.mana -= 25
            target = "you" if not is_enemy else "your enemy"
            health_recovery = 50
            # Cap health at maximum
            actual_recovery = min(health_recovery, self.max_health - self.health)
            self.health = min(self.health + health_recovery, self.max_health)
            print(f"""A beam of light falls upon
                  {target}...
                  Recover {actual_recovery} health."""
                  )
        else:
            print("Not enough mana.")
        return        
    # STATUS EFFECT
    def cast_magic_bubble(self) -> Dict[str, Any]: 
        """Cast protective magic bubble"""
        mana_cost = 50
        if self.mana < mana_cost:
            return {'success': False, 'reason': 'insufficient_mana'}
        
        self.mana -= mana_cost
        
        bubble_effect = StatusEffect(
            effect_type=EffectType.MAGIC_BUBBLE,
            duration=3,
            magnitude=0.35,  # 35% damage reduction
            maintenance_cost=25,
            resource_type="mana",
            categories=EffectCategory.DAMAGE_REDUCTION | EffectCategory.MANA_DRAIN # "|" operator to 
                                                                                   # combine two enum members into a bitwise 
                                                                                   # OR value that represents both categories at once
        )                                                                          # effect can be checked for both categories
        
        self.status_effects.add_effect(bubble_effect) # Adds effect to status_effect_manager
        
        return { # Returns success dictionary with display updates
            'success': True,
            'effect_applied': 'magic_bubble',
            'duration': 3,
            'mana_used': mana_cost
        } 
                
    
    def item(self, is_enemy=False):
        if self.item_count > 0:
            if self.mana >= self.max_mana:
                target = "You" if not is_enemy else "Your enemy"
                print(f"{target} already have full mana. The potion would be wasted.")
                return
            
            self.item_count -= 1
            target = "You uncork" if not is_enemy else "Your enemy uncorks"
            mana_recovery = 50
            # Cap mana at maximum
            actual_recovery = min(mana_recovery, self.max_mana - self.mana)
            self.mana = min(self.mana + mana_recovery, self.max_mana)
            print(f"""{target} a vial and take a sip...
                  Recover {actual_recovery} mana. """)
        else:
            print("Out of potions.")       
        return 
    
# Helper/Gameloop methods --------------------------------------------------------------------------
    def can_use_special(self):
        return self.mana >= 75

    def can_use_attack(self):
        return self.mana >= 10

    def can_use_heal(self):
        return self.mana >= 25 and self.health < self.max_health

    def get_available_actions(self):
        actions = []
        if self.can_use_attack():
            actions.append("attack")
        if self.can_use_special():
            actions.append("special")
        if self.item_count > 0 and self.mana < self.max_mana:
            actions.append("item")
        if self.can_use_heal():
            actions.append("heal")
        if self.mana >= 50 and not self.has_status_effect(EffectType.MAGIC_BUBBLE):
            actions.append("magic_bubble")
        return actions

    def validate_action(self, action):
        if action == "attack":
            return self.can_use_attack()
        elif action == "special": 
            return self.can_use_special()
        elif action == "item":
            return self.item_count > 0 and self.mana < self.max_mana
        elif action == "heal":
            return self.can_use_heal()
        elif action == "magic_bubble":
            return self.mana >= 50 and not self.has_status_effect(EffectType.MAGIC_BUBBLE)
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
                "available": self.item_count > 0 and self.mana < self.max_mana,
                "requirement": "Requires potion & missing mana"
            },
            "heal": {
                "letter": "D",
                "name": "Healing Light", 
                "damage": "Restores 50 health",
                "cost": "25 mana",
                "effect": "Divine healing magic",
                "available": self.mana >= 25 and self.health < self.max_health,
                "requirement": "Requires 25 mana & missing health"
            },
            "magic_bubble": {
                "letter": "E",
                "name": "Magic Bubble",
                "damage": "35% damage reduction",
                "cost": "50 mana + 25/turn",
                "effect": "Protective barrier for 3 turns",
                "available": self.mana >= 50 and not self.has_status_effect(EffectType.MAGIC_BUBBLE),
                "requirement": "Requires 50 mana & no active bubble"
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
        
        prompt += "Enter choice (A/B/C/D/E): "
        return input(prompt).lower()

    def print_status(self, is_enemy=False):
        if is_enemy:
            print(f"Enemy Health: {self.health} | Enemy Mana: {self.mana}")
        else:
            print(f"Current Health: {self.health} | Current Mana: {self.mana}")
        self.print_active_status_effects(is_enemy)
