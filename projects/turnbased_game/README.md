# Turn-Based RPG with Pygame Integration

A sophisticated turn-based RPG that evolved from a simple CLI game into a visual pygame experience. This project demonstrates advanced Python programming concepts, professional code organization, and the integration of game logic with visual interfaces.

## 🎯 Core Features

### Game Mechanics
- **Three Character Classes**: Warrior (rage-based), Rogue (stamina-based), Wizard (mana-based)
- **Strategic Combat System**: Each class has unique attack patterns, special abilities, and resource management
- **Intelligent Enemy AI**: Health-percentage-based decision making for challenging gameplay
- **Rich Combat Data**: `attack_get_result()` method returns comprehensive battle information for visual integration

### Technical Achievements
- **Professional Code Architecture**: Modular design with separated character classes and game logic
- **Pygame Visual Layer**: Window management, event handling, and foundation for visual game interface
- **Dual-Mode Capability**: Maintains both CLI and visual game modes
- **Comprehensive Testing**: pytest-based test suite with fixtures and mocking

## 🛠️ Technologies & Patterns

### Core Technologies
- **Python 3.12+** - Modern Python with type hints and advanced features
- **Pygame 2.6+** - Graphics library for visual game development
- **pytest** - Professional testing framework with fixtures and parametrization

### Design Patterns Implemented
- **Inheritance & Polymorphism** - Base character class with specialized subclasses
- **Strategy Pattern** - Enemy AI wrapper for flexible decision-making algorithms
- **Observer Pattern** - Event-driven game state management
- **Data Transfer Objects** - Rich data structures for pygame integration
- **Command Pattern** - Action-based combat system

## 🚀 How to Run

### CLI Mode (Original)
```bash
cd projects/turnbased_game/main_gameloop
python main_game_loop.py
```

### Pygame Visual Mode (Development)
```bash
cd projects/turnbased_game
python pygame_window_test.py
```

### Run Tests
```bash
cd projects/turnbased_game
pytest test_turnbased_game/ -v
```

## 📁 Project Structure

```
turnbased_game/
├── character_classes/          # Character system
│   ├── base_character.py      # Base Character class with shared functionality
│   ├── warrior.py             # Warrior class (rage-based tank)
│   ├── rogue.py               # Rogue class (stamina-based assassin)
│   ├── wizard.py              # Wizard class (mana-based spellcaster)
│   └── enemy_ai.py            # Enemy AI wrapper for strategic gameplay
├── main_gameloop/             # Game execution
│   ├── main_game_loop.py      # Main CLI game launcher
│   └── turnbased_game.py      # Core game loop logic
├── test_turnbased_game/       # Test suite
│   ├── test_base_character.py # Base class tests
│   ├── test_warrior.py        # Warrior-specific tests
│   ├── test_rogue.py          # Rogue-specific tests
│   ├── test_wizard.py         # Wizard-specific tests
│   ├── test_enemy_ai.py       # Enemy AI tests
│   └── README.md              # Test documentation
├── pygame_window_test.py      # Pygame visual development
└── README.md                  # This file
```

## 🎮 Character Classes Deep Dive

### Warrior (Tank)
- **Health**: 200 (highest survivability)
- **Resource**: Rage (gained from taking/dealing damage)
- **Playstyle**: Durable melee fighter with burst potential
- **Special**: Fury unleash (high damage, rage-dependent)

### Rogue (Assassin)  
- **Health**: 160 (balanced)
- **Resource**: Stamina (regenerates, consumed by abilities)
- **Playstyle**: Fast attacks with critical hit potential
- **Special**: Stealth strike (variable damage based on stamina)

### Wizard (Spellcaster)
- **Health**: 120 (lowest, high-risk/high-reward)
- **Resource**: Mana (finite, requires management)
- **Playstyle**: Powerful magic attacks with resource constraints
- **Special**: Devastating spells (mana-dependent)

## 📚 Development Journey

### Phase 1: Foundation (August 2024)
**Challenge**: Original implementation used heavily nested `if` statements for each character class, creating "spaghetti code" that was hard to maintain and extend.

**Solution**: Implemented inheritance and polymorphism with a base Character class and specialized subclasses.

#### 8/15/24 - Architecture Redesign
- Created base Character class with shared attributes and methods
- Refactored Warrior, Rogue, Wizard as subclasses inheriting from base
- Simplified game loop to use polymorphic method calls instead of class-specific conditionals
- Added action prompt functionality to base class for consistent player interface

#### 8/16/24 - User Experience Enhancement  
- Implemented class-specific action prompts so players understand each character's unique abilities
- Added clear differentiation between attack, special, and item actions for each class

### Phase 2: Advanced Features (August 2024)
#### 8/24/24 - Professional Testing Framework
- Implemented comprehensive pytest test suite with fixtures
- Added parametrized testing for multiple character classes
- Resolved relative assertion challenges for consistent health testing
- Achieved thorough test coverage for all character methods and edge cases

#### 8/25/24 - Enhanced Mechanics
- **Warrior Enhancement**: Added rage gain from receiving damage (passive ability)
- **Testing Advancement**: Implemented unittest.mock for input validation testing
- **Environment Setup**: Established virtual environments across all development devices

### Phase 3: AI & Strategy (September 2024)
#### 9/3/24 - Pygame Integration Begins
- Started transition from CLI to visual game interface
- Established pygame development foundation

#### 9/4/24 - Enemy AI Breakthrough
**Problem**: Random enemy actions created poor player experience and lacked strategic challenge.

**Solution**: Implemented Enemy AI "wrapper" system using health-percentage-based decision making.

**Key Innovation**: 
- Created strategic AI that evaluates player/enemy health and resource states
- Used action strings for clean separation between AI logic and character methods
- Implemented condition-based methods (e.g., `_should_use_special()`) for intelligent decision making
- Maintained clean architecture by keeping AI logic separate from character classes

### Phase 4: Visual Development (September 2024)
#### 9/11/24 - Pygame Foundation
- Established basic pygame window with proper event handling
- Implemented frame rate control and clean exit functionality
- Created visual layout zones for character display and UI elements

#### 9/12/24 - Professional Code Organization
- Organized pygame code into proper main() function structure
- Added comprehensive error handling and cleanup procedures
- Implemented dual exit methods (X button and ESC key)

#### 9/15/24 - Visual Interface Development
- **Text Rendering System**: Added font loading and text surface creation
- **Layout Planning**: Created visual reference zones for game elements
- **Integration Foundation**: Prepared for connecting existing game logic with visual interface

#### 9/18/24 - Project Maturation
- **Documentation Overhaul**: Comprehensive README restructuring
- **Test Organization**: Separated test cases into modular, maintainable files
- **Code Architecture**: Achieved professional-grade project structure with clear separation of concerns

## 🎨 Pygame Integration Features

### Current Visual Capabilities
- **Window Management**: 1200x800 game window with proper initialization
- **Event Handling**: Mouse and keyboard input processing
- **Layout Zones**: Visual areas defined for player, enemy, health bars, and action buttons
- **Text Rendering**: Font system for displaying game information
- **Performance**: 60 FPS frame rate control with efficient rendering

### Integration with Game Logic
- **attack_get_result() Method**: Returns rich data structures perfect for visual feedback
- **Animation Triggers**: Built-in support for visual effects (`sword_swing`, `critical_flash`)
- **Sound Integration**: Framework ready for audio effects
- **Dual-Mode Design**: Maintains both CLI and visual game modes

## 🧪 Testing Framework

### Test Coverage
- **Character Classes**: Comprehensive testing for Warrior, Rogue, Wizard, and base Character
- **Enemy AI**: Strategic decision-making algorithm validation
- **Edge Cases**: Resource depletion, critical hits, boundary conditions
- **Integration**: Game loop and character interaction testing

### Testing Achievements
- **Fixture-based Testing**: Parameterized tests across multiple character classes
- **Mock Implementation**: Input validation and user interaction testing
- **Relative Assertions**: Flexible health and resource validation
- **Date-tracked Progress**: Test pass dates documented for development tracking

### Test Organization
See `/test_turnbased_game/README.md` for detailed test documentation and individual test files.

## 🚀 Future Roadmap

### Immediate Goals
- **Complete Pygame Integration**: Full visual interface with character sprites
- **Asset Integration**: Hand-drawn character art and animation systems
- **Interactive Combat**: Click-based actions and visual feedback
- **Sound System**: Audio effects for attacks, spells, and criticals

### Advanced Features
- **Multiple Enemy Types**: Expand beyond single-enemy encounters
- **Leveling System**: Character progression and skill trees
- **Equipment System**: Weapons and armor with stat modifications
- **Save/Load**: Game state persistence

## 📈 Learning Outcomes

This project demonstrates mastery of:
- **Object-Oriented Design**: Inheritance, polymorphism, encapsulation
- **Game Development**: State management, event handling, rendering loops
- **Software Testing**: Test-driven development with comprehensive coverage
- **Code Architecture**: Clean separation of concerns and modular design
- **Version Control**: Git workflow with iterative development
- **Documentation**: Professional README and code commenting

## 📝 Contributing

This project serves as a learning portfolio demonstrating progression from basic programming concepts to advanced game development techniques. Each commit represents a milestone in the development journey.

---

*Last Updated: September 18, 2025*  
*Total Development Time: 2+ months*  
*Technologies Mastered: Python OOP, Pygame, pytest, Git*
