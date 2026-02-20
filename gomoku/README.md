# Gomoku (Five in a Row)

A full implementation of the classic Gomoku game using Object-Oriented Programming and layered architecture in Python.

## About Gomoku

Gomoku is a strategic board game where two players take turns placing pieces on a 15×15 board. The first player to get five pieces in a row (horizontally, vertically, or diagonally) wins the game.

## Features

- **15×15 Board**: Standard Gomoku board size
- **Human vs Computer**: Play against AI opponents of varying difficulty
- **Two UI Options**:
  - Console-based interface (text-based)
  - Graphical interface using Tkinter
- **Layered Architecture**:
  - **Domain Layer**: Core entities (Board, Player, GameState)
  - **Business Layer**: Game logic, rules, and AI
  - **Presentation Layer**: Console and GUI implementations
- **AI Difficulty Levels**:
  - **Easy**: Random moves
  - **Medium**: Blocks 1-move wins and takes winning moves
  - **Hard**: Uses minimax algorithm for competitive play
- **Input Validation**: All user inputs are validated
- **Comprehensive Tests**: PyUnit tests for critical game logic

## Project Structure

```
gomoku/
├── domain/                 # Domain layer
│   ├── __init__.py
│   ├── board.py           # Board entity (15x15 grid)
│   ├── player.py          # Player entity
│   └── game_state.py      # Game state enumeration
├── business/              # Business logic layer
│   ├── __init__.py
│   ├── game_rules.py      # Game rules and validation
│   ├── ai.py              # AI implementation
│   └── game_controller.py # Game flow controller
├── presentation/          # Presentation layer
│   ├── __init__.py
│   ├── console_ui.py      # Console interface
│   └── gui.py             # GUI interface (Tkinter)
├── tests/                 # Unit tests
│   ├── __init__.py
│   ├── test_board.py
│   ├── test_game_rules.py
│   └── test_ai.py
├── main.py                # Main entry point
├── requirements.txt       # Project dependencies
└── README.md             # This file
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Hazy2006/gomoku.git
cd gomoku
```

2. Ensure you have Python 3.6 or higher installed:
```bash
python --version
```

3. No additional dependencies required! The game uses only Python's standard library.

## Usage

### Running the Game

Run the main program:
```bash
python main.py
```

You'll be presented with a menu to choose:
1. Console version
2. GUI version
3. Exit

### Game Setup

After selecting a UI, you'll configure the game:
- Enter Player 1's name
- Choose opponent type:
  - Human player (for two-player mode)
  - Computer (Easy) - Random moves
  - Computer (Medium) - Strategic play with blocking
  - Computer (Hard) - Minimax algorithm

### Console Controls

- Enter moves as `row col` (e.g., `7 7` for the center)
- Coordinates range from 0 to 14
- Type your move and press Enter

### GUI Controls

- Click on intersections to place your piece
- Click "New Game" to start over
- Close the window to exit

## Running Tests

Run all tests:
```bash
python -m unittest discover tests
```

Run specific test file:
```bash
python -m unittest tests.test_board
python -m unittest tests.test_game_rules
python -m unittest tests.test_ai
```

## Game Rules

1. The board is 15×15
2. Player 1 (X) uses black pieces, Player 2 (O) uses white pieces
3. Players alternate placing one piece per turn
4. The first player to get exactly 5 or more pieces in a row wins
5. Rows can be horizontal, vertical, or diagonal
6. If the board fills with no winner, the game is a draw

## AI Strategy

### Medium Difficulty
1. **Win if possible**: Checks if AI can complete 5 in a row
2. **Block opponent**: Prevents opponent from completing 5 in a row
3. **Strategic placement**: Places pieces near existing pieces, preferring center

### Hard Difficulty
Uses minimax algorithm with alpha-beta pruning:
- Evaluates multiple moves ahead
- Considers both offensive and defensive positions
- Optimizes for winning while minimizing opponent's chances

## Development

### Architecture

The project follows a clean layered architecture:

- **Domain Layer**: Contains pure data structures and entities with no dependencies
- **Business Layer**: Contains game logic, rules, and AI algorithms
- **Presentation Layer**: Contains UI implementations that use the business layer

This separation allows for:
- Easy testing of game logic independently of UI
- Multiple UI implementations using the same game logic
- Clear separation of concerns

### Design Patterns

- **MVC Pattern**: Controller manages game flow, Models represent data, Views handle presentation
- **Strategy Pattern**: Different AI difficulties use different strategies
- **Dependency Injection**: UI classes receive controller instances

## License

This project is open source and available for educational purposes.

## Author

Created as a demonstration of OOP principles and layered architecture in Python.