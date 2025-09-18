# 🎮 Turn-Based Combat Game

A CLI-based turn-based RPG written in Python, showcasing object-oriented programming principles and intelligent AI systems. This project demonstrates clean code architecture through refactoring from nested conditionals to polymorphic design patterns.

## ✨ Features

- **Three Unique Character Classes**: Warrior (rage-based), Rogue (stamina-based), Wizard (mana-based)
- **Intelligent Enemy AI**: Adaptive strategy system that responds to health status and available resources
- **Turn-Based Combat**: Strategic gameplay with attack, special abilities, and item management
- **Polymorphic Design**: Clean, maintainable code using OOP principles
- **Comprehensive Testing**: Full test suite with pytest

## 🛠️ Technologies & Patterns

- **Language**: Python 3.9+
- **Design Patterns**: 
  - Polymorphism for character actions
  - Observer Pattern for game state
  - Command Pattern for action handling
  - Data Transfer Objects (DTO)
- **Testing**: pytest with fixtures and mocking
- **Environment**: Virtual environment for dependency isolation

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- Virtual environment (recommended)

### Installation & Setup
```bash
# Clone the repository
git clone <repository-url>
cd turnbased_game

# Set up virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the game
python main_gameloop/main_game_loop.py
```

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=character_classes

# Run specific test categories
pytest -k "test_warrior"
```

## 🎯 Character Classes

| Class   | Health | Resource | Strengths | Weaknesses |
|---------|--------|----------|-----------|------------|
| Warrior | 200    | Rage     | High durability, rage builds with damage | Slow start, limited range |
| Rogue   | 160    | Stamina  | High critical chance, resource recovery | Moderate health |
| Wizard  | 120    | Mana     | Highest damage potential | Glass cannon, dies if mana depleted |

## 🤖 Enemy AI System

The AI system uses a three-tier decision-making process:

- **Desperate (< 25% health)**: Prioritizes survival and healing
- **Defensive (25-50% health)**: Balanced approach with strategic healing
- **Offensive (> 50% health)**: Aggressive tactics and resource management

## 📈 Development Journey

### Code Architecture Evolution

**Before**: Nested conditional statements creating "spaghetti code"
```python
# Original approach - difficult to maintain
if player_class == "warrior":
    if action == "attack":
        # warrior attack logic
    elif action == "special":
        # warrior special logic
elif player_class == "rogue":
    # repeat similar pattern...
```

**After**: Polymorphic design with base class inheritance
```python
# Refactored approach - clean and extensible
player.action_prompt()  # Each class implements its own behavior
player.execute_action(action, enemy)
```

### Key Milestones

- **August 15, 2024**: Implemented base class architecture with polymorphism
- **August 16, 2024**: Added class-specific action prompts for better UX
- **August 24-25, 2024**: Comprehensive test suite with pytest fixtures
- **September 3-4, 2024**: Enemy AI wrapper implementation
- **September 12, 2024**: Bug fixes and wizard death condition implementation

## 🧪 Testing Strategy

The project maintains high test coverage across:

- **Unit Tests**: Individual class methods and edge cases
- **Integration Tests**: Game loop and character interactions
- **Fixture Usage**: Clean, isolated test environments
- **Mock Testing**: Action prompts and user input validation

### Test Coverage Highlights
- Character attribute validation
- Combat calculations and damage dealing
- Resource management (mana, stamina, rage)
- Enemy AI decision-making logic
- Edge cases (out of resources, death conditions)

## 📁 Project Structure

```
turnbased_game/
├── character_classes/
│   ├── base_character.py      # Abstract base class
│   ├── warrior.py            # Warrior implementation
│   ├── rogue.py              # Rogue implementation
│   ├── wizard.py             # Wizard implementation
│   └── enemy_ai.py           # AI decision system
├── main_gameloop/
│   ├── main_game_loop.py     # Game entry point
│   └── turnbased_game.py     # Core game logic
├── test_turnbased_game/
│   └── test_turnbased_game.py # Test suite
└── README.md
```

## 🔮 Future Enhancements

- [ ] Pygame GUI implementation
- [ ] Multiplayer support
- [ ] Additional character classes
- [ ] Equipment and inventory system
- [ ] Save/load game functionality
- [ ] Advanced AI difficulty levels

## 🎓 Learning Outcomes

This project demonstrates proficiency in:
- Object-oriented programming and design patterns
- Code refactoring and technical debt management
- Test-driven development practices
- Software architecture planning
- Game logic and AI implementation

---

*Built with ❤️ as part of a comprehensive programming portfolio*
