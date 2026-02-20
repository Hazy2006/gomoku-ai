"""Game state entity for Gomoku game."""

from enum import Enum

# We can think of this like a dictionary of states the game can be in
class GameState(Enum):
    """Represents the current state of the game."""
    NOT_STARTED = 0
    IN_PROGRESS = 1
    PLAYER_X_WON = 2
    PLAYER_O_WON = 3
    DRAW = 4