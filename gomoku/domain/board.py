"""Board entity for Gomoku game."""


class Board: # We declare a class in order to construct an object, the board itself
    """Represents a 15x15 Gomoku board."""

    # Variables to represent the board size and the players
    # While the size is an obvious choice, the other variables are represented as keys
    BOARD_SIZE = 15
    EMPTY = 0
    PLAYER_X = 1
    PLAYER_O = 2


    def __init__(self):
        """Initialize an empty board."""
        self._grid = [[self.EMPTY for _ in range(self.BOARD_SIZE)]
                      for _ in range(self.BOARD_SIZE)]

    def get_cell(self, row, col):
        """Get the value at a specific cell.

        Args:
            row: Row index (0-14)
            col: Column index (0-14)

        Returns:
            Cell value (EMPTY, PLAYER_X, or PLAYER_O)
        """
        if not self._is_valid_position(row, col):
            raise ValueError(f"Invalid position: ({row}, {col})")
        return self._grid[row][col]

    def set_cell(self, row, col, value):
        """Set the value at a specific cell.

        Args:
            row: Row index (0-14)
            col: Column index (0-14)
            value: Cell value (EMPTY, PLAYER_X, or PLAYER_O)
        """
        if not self._is_valid_position(row, col):
            raise ValueError(f"Invalid position: ({row}, {col})")
        if value not in [self.EMPTY, self.PLAYER_X, self.PLAYER_O]:
            raise ValueError(f"Invalid value: {value}")
        self._grid[row][col] = value

    def is_empty(self, row, col):
        """Check if a cell is empty.

        Args:
            row: Row index (0-14)
            col: Column index (0-14)

        Returns:
            True if cell is empty, False otherwise
        """
        return self.get_cell(row, col) == self.EMPTY

    def is_full(self):
        """Check if the board is full.

        Returns:
            True if no empty cells remain, False otherwise
        """
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                if self._grid[row][col] == self.EMPTY:
                    return False
        return True

    def get_empty_cells(self):
        """Get all empty cells on the board.

        Returns:
            List of tuples (row, col) representing empty cells
        """
        empty_cells = []
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                if self._grid[row][col] == self.EMPTY:
                    empty_cells.append((row, col))
        return empty_cells

    def clear(self):
        """Clear the board, setting all cells to empty."""
        self._grid = [[self.EMPTY for _ in range(self.BOARD_SIZE)]
                      for _ in range(self.BOARD_SIZE)]

    def _is_valid_position(self, row, col):
        """Check if a position is valid.

        Args:
            row: Row index
            col: Column index

        Returns:
            True if position is valid, False otherwise
        """
        return 0 <= row < self.BOARD_SIZE and 0 <= col < self.BOARD_SIZE

    def get_grid(self):
        """Get a copy of the board grid.

        Returns:
            2D list representing the board state
        """
        return [row[:] for row in self._grid]