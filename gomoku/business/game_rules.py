"""Game rules and validation for Gomoku."""

from domain.board import Board


class GameRules:
    """Contains game rules and validation logic."""

    WIN_LENGTH = 5  # Number of consecutive pieces needed to win

    def __init__(self, board):
        """Initialize game rules with a board.

        Args:
            board: Board instance
        """
        self._board = board

    def is_valid_move(self, row, col):
        """Check if a move is valid.

        Args:
            row: Row index
            col: Column index

        Returns:
            True if move is valid, False otherwise
        """
        try:
            return self._board.is_empty(row, col)
        except ValueError:
            return False

    def check_winner(self, last_row, last_col, player_symbol):
        """Check if a player has won after placing a piece.

        Args:
            last_row: Row of the last move
            last_col: Column of the last move
            player_symbol: Symbol of the player who made the move

        Returns:
            True if player has won, False otherwise
        """
        # Check all four directions: horizontal, vertical, diagonal, anti-diagonal
        directions = [
            (0, 1),  # Horizontal
            (1, 0),  # Vertical
            (1, 1),  # Diagonal
            (1, -1)  # Anti-diagonal
        ]

        for dr, dc in directions:
            if self._count_consecutive(last_row, last_col, dr, dc, player_symbol) >= self.WIN_LENGTH:
                return True

        return False

    def _count_consecutive(self, row, col, dr, dc, symbol):
        """Count consecutive pieces in a direction.

        Args:
            row: Starting row
            col: Starting column
            dr: Row direction (-1, 0, or 1)
            dc: Column direction (-1, 0, or 1)
            symbol: Player symbol to count

        Returns:
            Number of consecutive pieces including the starting position
        """
        count = 1  # Count the piece at (row, col)

        # Count in positive direction
        count += self._count_in_direction(row, col, dr, dc, symbol)

        # Count in negative direction
        count += self._count_in_direction(row, col, -dr, -dc, symbol)

        return count

    def _count_in_direction(self, row, col, dr, dc, symbol):
        """Count consecutive pieces in one direction.

        Args:
            row: Starting row
            col: Starting column
            dr: Row direction (-1, 0, or 1)
            dc: Column direction (-1, 0, or 1)
            symbol: Player symbol to count

        Returns:
            Number of consecutive pieces in the direction (not including start)
        """
        count = 0
        r, c = row + dr, col + dc

        while (0 <= r < Board.BOARD_SIZE and
               0 <= c < Board.BOARD_SIZE and
               self._board.get_cell(r, c) == symbol):
            count += 1
            r += dr
            c += dc

        return count

    def find_threat(self, player_symbol):
        """Find if there's a winning move for the player.

        Args:
            player_symbol: Symbol to check for winning move

        Returns:
            (row, col) tuple if a winning move exists, None otherwise
        """
        empty_cells = self._board.get_empty_cells()

        for row, col in empty_cells:
            # Temporarily place the piece
            self._board.set_cell(row, col, player_symbol)

            # Check if this creates a win
            if self.check_winner(row, col, player_symbol):
                self._board.set_cell(row, col, Board.EMPTY)
                return (row, col)

            # Restore the cell
            self._board.set_cell(row, col, Board.EMPTY)

        return None

    def count_consecutive(self, row, col, dr, dc, symbol):
        """Count consecutive pieces in a direction.

        Args:
            row: Starting row
            col: Starting column
            dr: Row direction (-1, 0, or 1)
            dc: Column direction (-1, 0, or 1)
            symbol: Player symbol to count

        Returns:
            Number of consecutive pieces including the starting position
        """
        return self._count_consecutive(row, col, dr, dc, symbol)