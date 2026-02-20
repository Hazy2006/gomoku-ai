"""Player entity for Gomoku game."""


class Player:
    """Represents a player in the Gomoku game."""

    def __init__(self, name, symbol, is_human=True):
        """Initialize a player.

        Args:
            name: Player name
            symbol: Player symbol (PLAYER_X or PLAYER_O)
            is_human: Whether the player is human or computer
        """
        self._name = name
        self._symbol = symbol
        self._is_human = is_human

    @property
    def name(self):
        """Get player name."""
        return self._name

    @property
    def symbol(self):
        """Get player symbol."""
        return self._symbol

    @property
    def is_human(self):
        """Check if player is human."""
        return self._is_human

    def __str__(self):
        """String representation of player."""
        player_type = "Human" if self._is_human else "Computer"
        return f"{self._name} ({player_type})"