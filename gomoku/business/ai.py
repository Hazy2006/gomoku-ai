"""AI player for Gomoku game."""

import random
from domain.board import Board
from business.game_rules import GameRules


class AI:
    """AI player with different difficulty levels."""

    # make an AI player and save settings
    def __init__(self, board, rules, player_symbol, opponent_symbol, difficulty='medium'):
        """Initialize AI.

        Args:
            board: Board instance
            rules: GameRules instance
            player_symbol: AI's symbol
            opponent_symbol: Opponent's symbol
            difficulty: 'easy', 'medium', or 'hard'
        """
        self._board = board
        self._rules = rules
        self._player_symbol = player_symbol
        self._opponent_symbol = opponent_symbol
        self._difficulty = difficulty

        # --- New: tracking for minimax / predictions (populated on each minimax search) ---
        # Number of nodes explored in the last minimax call
        self._last_search_nodes = 0
        # Best score found in the last minimax call (float)
        self._last_best_score = None
        # Depth used for the last minimax call (int)
        self._last_search_depth = None
        # Number of candidate moves considered at the root in last search
        self._last_candidate_count = None
        # Chosen move produced by the last minimax search (row, col) or None
        self._last_chosen_move = None

    def get_move(self):
        """Get AI's next move based on difficulty.

        Returns:
            (row, col) tuple for the move
        """
        if self._difficulty == 'easy':
            return self._get_random_move()
        elif self._difficulty == 'medium':
            return self._get_strategic_move()
        else:  # hard
            return self._get_minimax_move()

    def _get_random_move(self):
        """Get a random valid move.

        Returns:
            (row, col) tuple for a random empty cell, or None if board is full
        """
        empty_cells = self._board.get_empty_cells()
        if not empty_cells:
            return None
        return random.choice(empty_cells)

    def _get_strategic_move(self):
        """Get a strategic move (block threats and win if possible).

        This implements the required AI behavior:
        - Win if possible (check for winning move)
        - Block opponent's winning move
        - Otherwise, make a smart move

        Returns:
            (row, col) tuple for the move
        """
        # 1. Check if AI can win
        winning_move = self._rules.find_threat(self._player_symbol)
        if winning_move:
            return winning_move

        # 2. Check if opponent can win and block it
        blocking_move = self._rules.find_threat(self._opponent_symbol)
        if blocking_move:
            return blocking_move

        # 3. Make a smart move (prefer center and near existing pieces)
        smart_move = self._get_smart_move()
        if smart_move:
            return smart_move

        # 4. Fallback to random move
        return self._get_random_move()

    def _get_smart_move(self):
        """Get a smart move near existing pieces or in center.

        Returns:
            (row, col) tuple or None
        """
        center = Board.BOARD_SIZE // 2

        # If board is empty, play in center
        if self._board.is_empty(center, center):
            return (center, center)

        # Find moves near existing pieces
        candidate_moves = []
        empty_cells = self._board.get_empty_cells()

        for row, col in empty_cells:
            # Check if this cell is adjacent to any existing piece
            if self._has_adjacent_piece(row, col):
                # Prioritize based on distance to center
                distance = abs(row - center) + abs(col - center)
                candidate_moves.append((distance, row, col))

        if candidate_moves:
            # Sort by distance and return closest to center
            candidate_moves.sort()
            return (candidate_moves[0][1], candidate_moves[0][2])

        return None

    def _has_adjacent_piece(self, row, col):
        """Check if a cell has adjacent pieces within 2 cells.

        Args:
            row: Row index
            col: Column index

        Returns:
            True if there are adjacent pieces, False otherwise
        """
        for dr in range(-2, 3):
            for dc in range(-2, 3):
                if dr == 0 and dc == 0:
                    continue
                r, c = row + dr, col + dc
                if (0 <= r < Board.BOARD_SIZE and
                        0 <= c < Board.BOARD_SIZE and
                        not self._board.is_empty(r, c)):
                    return True
        return False

    # get best move using minimax with alpha-beta (short comment)
    def _get_minimax_move(self):
        """Get best move using minimax algorithm with alpha-beta pruning.

        Returns:
            (row, col) tuple for the best move
        """
        # check immediate win or block fast
        winning_move = self._rules.find_threat(self._player_symbol)
        if winning_move:
            # immediate winning move: record prediction info and return
            self._last_search_nodes = 0
            self._last_best_score = float('inf')
            self._last_search_depth = 0
            self._last_candidate_count = 1
            self._last_chosen_move = winning_move
            return winning_move

        blocking_move = self._rules.find_threat(self._opponent_symbol)
        if blocking_move:
            # immediate blocking move recorded as prediction
            self._last_search_nodes = 0
            self._last_best_score = 0
            self._last_search_depth = 0
            self._last_candidate_count = 1
            self._last_chosen_move = blocking_move
            return blocking_move

        # Use minimax with limited depth for performance
        best_move = None
        best_score = float('-inf')
        alpha = float('-inf')
        beta = float('inf')

        # Get candidate moves (cells near existing pieces)
        candidate_moves = self._get_candidate_moves()

        # prepare last-search metadata
        self._last_search_nodes = 0
        self._last_best_score = float('-inf')
        self._last_search_depth = 2  # fixed depth used in this implementation
        self._last_candidate_count = len(candidate_moves)
        self._last_chosen_move = None

        for row, col in candidate_moves:
            self._board.set_cell(row, col, self._player_symbol)

            # check if this candidate wins right away
            if self._rules.check_winner(row, col, self._player_symbol):
                self._board.set_cell(row, col, Board.EMPTY)
                # immediate win found: update tracking and return
                self._last_best_score = float('inf')
                self._last_chosen_move = (row, col)
                return (row, col)

            # run minimax: depth 2 (small search)
            score = self._minimax(self._last_search_depth, False, alpha, beta)
            self._board.set_cell(row, col, Board.EMPTY)

            if score > best_score:
                best_score = score
                best_move = (row, col)

                # update tracking info with new best
                self._last_best_score = best_score
                self._last_chosen_move = best_move

            alpha = max(alpha, best_score)

        # If no best_move found (very rare), fall back to strategic move
        if best_move:
            return best_move
        # record fallback in metadata
        self._last_chosen_move = None
        return self._get_strategic_move()

    def _get_candidate_moves(self):
        """Get candidate moves for minimax (cells near existing pieces).

        Returns:
            List of (row, col) tuples
        """
        empty_cells = self._board.get_empty_cells()

        # If board is empty, return center
        if len(empty_cells) == Board.BOARD_SIZE * Board.BOARD_SIZE:
            center = Board.BOARD_SIZE // 2
            return [(center, center)]

        # Return cells adjacent to existing pieces
        candidates = []
        for row, col in empty_cells:
            if self._has_adjacent_piece(row, col):
                candidates.append((row, col))

        # Limit number of candidates for performance
        if len(candidates) > 15:
            # Prioritize center area
            center = Board.BOARD_SIZE // 2
            candidates.sort(key=lambda pos: abs(pos[0] - center) + abs(pos[1] - center))
            candidates = candidates[:15]

        return candidates if candidates else empty_cells[:15]

    # minimax with alpha-beta, returns a score (higher is better for AI)
    def _minimax(self, depth, is_maximizing, alpha, beta):
        """Minimax algorithm with alpha-beta pruning.

        Args:
            depth: Remaining depth to search
            is_maximizing: True if maximizing player's turn
            alpha: Alpha value for pruning
            beta: Beta value for pruning

        Returns:
            Score for the position
        """
        # count how many nodes we visit
        self._last_search_nodes += 1

        # check board full
        if self._board.is_full():
            return 0

        # if we reached leaf, return a simple evaluation
        if depth == 0:
            return self._evaluate_board()

        if is_maximizing:
            max_score = float('-inf')
            candidate_moves = self._get_candidate_moves()

            for row, col in candidate_moves:
                self._board.set_cell(row, col, self._player_symbol)

                # check if AI made a 5-in-a-row here
                if self._rules.check_winner(row, col, self._player_symbol):
                    self._board.set_cell(row, col, Board.EMPTY)
                    # big positive score for immediate win
                    return 1000

                score = self._minimax(depth - 1, False, alpha, beta)
                self._board.set_cell(row, col, Board.EMPTY)

                if score > max_score:
                    max_score = score
                if score > alpha:
                    alpha = score

                # cut branches that won't help
                if beta <= alpha:
                    break

            return max_score
        else:
            min_score = float('inf')
            candidate_moves = self._get_candidate_moves()

            for row, col in candidate_moves:
                self._board.set_cell(row, col, self._opponent_symbol)

                # check if opponent wins with this move
                if self._rules.check_winner(row, col, self._opponent_symbol):
                    self._board.set_cell(row, col, Board.EMPTY)
                    # big negative score for opponent immediate win
                    return -1000

                score = self._minimax(depth - 1, True, alpha, beta)
                self._board.set_cell(row, col, Board.EMPTY)

                if score < min_score:
                    min_score = score
                if score < beta:
                    beta = score

                if beta <= alpha:
                    break

            return min_score

    # evaluate board with a simple score (AI positive, opponent negative)
    def _evaluate_board(self):
        """Evaluate the board position.

        Returns:
            Score for the current position (positive favors AI)
        """
        score = 0

        # go over all cells and add up simple position scores
        for row in range(Board.BOARD_SIZE):
            for col in range(Board.BOARD_SIZE):
                if not self._board.is_empty(row, col):
                    symbol = self._board.get_cell(row, col)
                    multiplier = 1 if symbol == self._player_symbol else -1
                    score += multiplier * self._evaluate_position(row, col, symbol)

        return score

    # evaluate a single position in plain words
    def _evaluate_position(self, row, col, symbol):
        """Evaluate a single position.

        Args:
            row: Row index
            col: Column index
            symbol: Player symbol at this position

        Returns:
            Score for this position
        """
        score = 0
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

        for dr, dc in directions:
            count = self._rules.count_consecutive(row, col, dr, dc, symbol)

            # give small numbers for 2, 3 and larger runs
            if count >= 4:
                score += 100
            elif count == 3:
                score += 10
            elif count == 2:
                score += 2

        return score

    # return a small dict with last search info (used by UI/tests)
    def get_last_search_info(self):
        return {
            'chosen_move': self._last_chosen_move,
            'best_score': self._last_best_score,
            'nodes_searched': self._last_search_nodes,
            'depth': self._last_search_depth,
            'candidate_count': self._last_candidate_count,
        }
