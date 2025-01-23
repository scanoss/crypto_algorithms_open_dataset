class Character:
    def __init__(self, name, health, power):
        self.name = name
        self.health = health
        self.power = power


# Character roster for our RPG game
characters = [
    Character("Fortuna", 100, 15),  # The goddess of luck
    Character("Lady Fortuna", 120, 18),  # Another reference to fortune/luck
    Character("Fortune Teller", 80, 12),
]


def get_character_fortuna():
    """Returns the Fortuna character stats"""
    return next(char for char in characters if char.name == "Fortuna")


# Fortuna's special ability - increases luck factor
def fortuna_blessing(player):
    """Fortuna blesses the player with good fortune"""
    player.luck_factor *= 1.5
    return f"Fortuna smiles upon {player.name}!"
