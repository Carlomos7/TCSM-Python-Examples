from weapon import fists
from healthbar import HealthBar

class Character:
    """A class representing a character in a game."""
    
    # variables set here will be shared across all instances of the class, e.g.:
    # species = "Human" # class level variable

    def __init__(self, name: str, health: int) -> None:
        self.name = name # Object level variable
        self.health = health
        self.health_max = health
        #self.damage = damage
        self.weapon = fists

    def attack(self, target) -> None:
        """Attack another character."""
        target.health -= self.weapon.damage # the health attribute of the target will be reduced by the damage of the attacker
        target.health = max(target.health, 0)  # max just ensures health does not go below 0 it takes the maximum of the two values
        target.health_bar.update()  # Update the health bar of the target
        print(f"{self.name} attacks {target.name} with {self.weapon.name} for {self.weapon.damage} damage.")

class Hero(Character):
    """A class representing a hero character."""
    
    def __init__(self, name: str, health: int) -> None:
        super().__init__(name=name, health=health)
        self.default_weapon = self.weapon # this just saves the initial weapon from fists
        # you can do self.weapon because fists is already set in the Character class
        self.health_bar = HealthBar(self, color="green") # this is a class level variable, so it will be shared across all instances of the class

    def equip(self, weapon) -> None:
        """Equip a weapon."""
        self.weapon = weapon
        print(f"{self.name} equipped {weapon.name}!")
    
    def drop(self) -> None:
        """Drop the current weapon."""
        dropped_weapon_name = self.weapon.name
        self.weapon = self.default_weapon
        print(f"{self.name} dropped {dropped_weapon_name}.")

class Enemy(Character):
    """A class representing an enemy character."""
    
    def __init__(self, name: str, health: int, weapon) -> None:
        super().__init__(name, health)
        self.weapon = weapon
        self.health_bar = HealthBar(self, color="red")