import os

os.system('cls' if os.name == 'nt' else 'clear')  # Clear the console for a fresh start
# it basically checks if the OS is Windows (nt) or Unix-like (posix) and clears the console accordingly


class HealthBar:
    """A class representing a health bar for a character."""

    symbol_remaining: str = "█" # this character is called "Full Block" and is used to represent the remaining health
    symbol_lost: str = "░" # this character is called "Empty Block" and is used to represent the lost health
    barrier: str = "│" # this character is called "Vertical Line" and is used to create a barrier around the health bar
    colors: dict = {
        "red": "\033[91m",
        "purple": "\033[95m",
        "blue": "\033[94m",
        "blue2": "\033[96m",
        "blue3": "\033[94m",
        "green": "\033[92m",
        "green2": "\033[92m",
        "yellow": "\033[93m",
        "gray": "\033[90m",
        "default": "\033[0m"
    } 
    # The variables above are class-level variables, meaning they are shared across all instances of the class.

    def __init__(self, entity, length: int = 20, is_colored: bool = True, color: str = "green") -> None:
        self.entity = entity
        self.length = length
        self.max_value = entity.health_max # Maximum health of the entity
        # Current health of the entity, initialized to its maximum health
        self.current_value = entity.health

        self.is_colored = is_colored
        self.color = self.colors.get(color) or self.colors["default"]

    def update(self) -> None:
        """Update the health bar based on the current health of the entity."""
        self.current_value = self.entity.health

    def draw(self) -> str:
        remaining_bars = round(self.current_value /
                               self.max_value * self.length) # this just calculates how many bars should be filled based on the current health
        lost_bars = self.length - remaining_bars # this just calculates how many bars should be empty based on the current health
        print(
            f"{self.entity.name}'s Health: {self.entity.health}/{self.entity.health_max}")
        print(f"{self.barrier}"
              f"{self.color if self.is_colored else ''}"
              f"{remaining_bars * self.symbol_remaining}"
              f"{lost_bars * self.symbol_lost}"
              f"{self.colors['default'] if self.is_colored else ''}"
              f"{self.barrier}")
