"""
Demo script to showcase the Gomoku game.
This demonstrates a simulated game between two players.
"""

from domain.board import Board
from business.game_controller import GameController


def print_board_simple(controller):
    """Print a simple board representation."""
    board = controller.board
    print("\n   ", end="")

    # Column headers
    for col in range(min(10, Board.BOARD_SIZE)):
        print(f"{col:2}", end=" ")
    print(" ...")

    # Board rows (showing first 10 rows and columns)
    for row in range(min(10, Board.BOARD_SIZE)):
        print(f"{row:2} ", end="")

        for col in range(min(10, Board.BOARD_SIZE)):
            cell = board.get_cell(row, col)
            if cell == Board.EMPTY:
                symbol = "."
            elif cell == Board.PLAYER_X:
                symbol = "X"
            else:
                symbol = "O"

            print(f" {symbol} ", end="")

        print(f" ... {row:2}")

    print("   " + "..." * 10)
    print()


def demo_console_game():
    """Demonstrate a simulated console game."""
    print("=" * 60)
    print("GOMOKU DEMO - Simulated Game")
    print("=" * 60)
    print("\nCreating a game: Player X vs Computer (Medium)")

    controller = GameController("Player X", "Computer (Medium)", False, 'medium')
    controller.start_game()

    print("\nStarting position:")
    print_board_simple(controller)

    # Simulate some moves
    moves = [
        (7, 7, "Player X starts in the center"),
        (None, None, "Computer's turn"),
        (7, 8, "Player X extends horizontally"),
        (None, None, "Computer's turn"),
        (7, 6, "Player X extends the other way"),
        (None, None, "Computer's turn"),
    ]

    move_count = 0
    for row, col, description in moves:
        move_count += 1
        print(f"\nMove {move_count}: {description}")

        if row is not None:
            # Player move
            controller.make_move(row, col)
        else:
            # AI move
            ai_move = controller.get_ai_move()
            if ai_move:
                r, c = ai_move
                controller.make_move(r, c)
                print(f"         Computer places at ({r}, {c})")

        if move_count % 2 == 0:  # Show board after each pair of moves
            print_board_simple(controller)

        if controller.is_game_over():
            print("\n" + "=" * 60)
            print("GAME OVER!")
            winner = controller.get_winner()
            if winner:
                print(f"{winner.name} wins!")
            else:
                print("It's a draw!")
            print("=" * 60)
            break

    if not controller.is_game_over():
        print("\n(Demo ends here - game continues...)")
        print("\nCurrent board state:")
        print_board_simple(controller)


def demo_features():
    """Demonstrate key features of the game."""
    print("\n" + "=" * 60)
    print("KEY FEATURES DEMONSTRATION")
    print("=" * 60)

    print("\n1. WIN DETECTION")
    print("-" * 60)
    controller = GameController("Player X", "Player O", True, 'medium')
    controller.start_game()

    # Create a horizontal win for Player X
    for col in range(5):
        controller.board.set_cell(0, col, Board.PLAYER_X)

    print("Horizontal win for Player X:")
    for col in range(8):
        cell = controller.board.get_cell(0, col)
        symbol = "X" if cell == Board.PLAYER_X else "."
        print(f" {symbol} ", end="")
    print()

    from business.game_rules import GameRules
    rules = GameRules(controller.board)
    print(f"Win detected: {rules.check_winner(0, 4, Board.PLAYER_X)}")

    print("\n2. AI BLOCKING")
    print("-" * 60)
    controller2 = GameController("Player X", "Computer", False, 'medium')
    controller2.start_game()

    # Create a threat for Player X
    for col in range(4):
        controller2.board.set_cell(5, col, Board.PLAYER_X)

    print("Player X has 4 in a row:")
    for col in range(8):
        cell = controller2.board.get_cell(5, col)
        symbol = "X" if cell == Board.PLAYER_X else "."
        print(f" {symbol} ", end="")
    print()

    # Switch to AI turn
    controller2._current_player = controller2.player2
    ai_move = controller2.get_ai_move()
    print(f"AI blocks at position: {ai_move}")
    print(f"Expected blocking position: (5, 4)")

    print("\n3. AI WINNING MOVE")
    print("-" * 60)
    controller3 = GameController("Player X", "Computer", False, 'medium')
    controller3.start_game()

    # Create a winning opportunity for AI
    for col in range(4):
        controller3.board.set_cell(7, col, Board.PLAYER_O)

    print("Computer has 4 in a row:")
    for col in range(8):
        cell = controller3.board.get_cell(7, col)
        symbol = "O" if cell == Board.PLAYER_O else "."
        print(f" {symbol} ", end="")
    print()

    # Switch to AI turn
    controller3._current_player = controller3.player2
    ai_move = controller3.get_ai_move()
    print(f"AI wins at position: {ai_move}")
    print(f"Expected winning position: (7, 4)")

    print("\n4. INPUT VALIDATION")
    print("-" * 60)
    board = Board()

    print("Testing invalid inputs:")
    try:
        board.get_cell(-1, 0)
        print("  ✗ Failed to catch negative row")
    except ValueError:
        print("  ✓ Correctly rejects negative row")

    try:
        board.get_cell(0, 15)
        print("  ✗ Failed to catch out-of-bounds column")
    except ValueError:
        print("  ✓ Correctly rejects out-of-bounds column")

    try:
        board.set_cell(0, 0, 999)
        print("  ✗ Failed to catch invalid cell value")
    except ValueError:
        print("  ✓ Correctly rejects invalid cell value")

    print("\n5. DIFFICULTY LEVELS")
    print("-" * 60)
    print("  • Easy:   Random moves")
    print("  • Medium: Blocks wins and takes winning moves")
    print("  • Hard:   Uses minimax algorithm for strategic play")


if __name__ == "__main__":
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 18 + "GOMOKU GAME DEMO" + " " * 24 + "║")
    print("╚" + "═" * 58 + "╝")

    demo_console_game()
    demo_features()

    print("\n" + "=" * 60)
    print("To play the game yourself, run: python main.py")
    print("=" * 60)
    print()