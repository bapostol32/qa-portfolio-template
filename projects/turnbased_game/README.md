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

### Phase 1: Foundation (August 2025)

**The Problem I Inherited:**
When I started this project, I had what I thought was a working turn-based game. But every time I wanted to add a new character class or modify existing behavior, I found myself lost in a maze of nested `if` statements. The code looked something like:

*"If warrior and attack, do this... if wizard and attack, do that... if rogue and special, check stamina then..."*

I realized I had "spaghetti code" where everything was tangled together, making code hard to maintain and even harder to expand.

**My Learning Moment:**
This was my first real encounter with why code architecture matters. I could have kept adding more `if` statements, but I knew that wasn't sustainable. I needed to learn about object-oriented design patterns.

**The Refactor That Changed Everything:**

#### 8/15/25 - Architecture Redesign
- Created base Character class with shared attributes and methods
- Refactored Warrior, Rogue, Wizard as subclasses inheriting from base
- Simplified game loop to use polymorphic method calls instead of class-specific conditionals
- Added action prompt functionality to base class for consistent player interface

#### 8/16/25 - User Experience Enhancement  
- Implemented class-specific action prompts so players understand each character's unique abilities
- Added clear differentiation between attack, special, and item actions for each class

**What I Learned:** This was my introduction to the power of object-oriented design. Instead of asking "what type of character is this?" everywhere in my code, I could just call `character.attack()` and let polymorphism handle the rest. It was like switching from manual labor to using the right tools.

### Phase 2: Advanced Features (August 2025)

**Discovering Professional Development Practices:**

#### 8/24/25 - Professional Testing Framework

- Implemented comprehensive pytest test suite with fixtures
- Added parametrized testing for multiple character classes
- Resolved relative assertion challenges for consistent health testing
- Achieved thorough test coverage for all character methods and edge cases

#### 8/25/25 - Enhanced Mechanics

- **Warrior Enhancement**: Added rage gain from receiving damage (passive ability)
- **Testing Advancement**: Implemented unittest.mock for input validation testing
- **Environment Setup**: Established virtual environments across all development devices

**My Testing Journey:** This was when I learned that "it works on my machine" isn't enough. Writing tests forced me to think about edge cases I'd never considered. What happens when a warrior runs out of rage mid-fight? What if someone enters invalid input? Testing made my code bulletproof.

### Phase 3: AI & Strategy (September 2025)

**Making Enemies Actually Challenging:**

#### 9/3/25 - Pygame Integration Begins

- Started transition from CLI to visual game interface
- Established pygame development foundation

#### 9/4/25 - Enemy AI Breakthrough

**The Problem I Faced:** My enemies were just attacking randomly, which made combat boring and unpredictable. Players couldn't develop strategies because enemy behavior was purely random.

**My Solution:** I designed an Enemy AI "wrapper" system that makes intelligent decisions based on battlefield conditions.

**Key Innovation:**

- Created strategic AI that evaluates player/enemy health and resource states
- Used action strings for clean separation between AI logic and character methods
- Implemented condition-based methods (e.g., `_should_use_special()`) for intelligent decision making
- Maintained clean architecture by keeping AI logic separate from character classes

**What This Taught Me:** This was my first experience with the Strategy pattern. I learned that good AI isn't about complex algorithms - it's about making decisions that create engaging gameplay. The enemy now feels like a real opponent, not a random number generator.

### Phase 4: Visual Development (September 2025)

**From Text to Graphics:**

#### 9/11/25 - Pygame Foundation

- Established basic pygame window with proper event handling
- Implemented frame rate control and clean exit functionality
- Created visual layout zones for character display and UI elements

#### 9/12/25 - Professional Code Organization

- Organized pygame code into proper main() function structure
- Added comprehensive error handling and cleanup procedures
- Implemented dual exit methods (X button and ESC key)

#### 9/15/25 - Visual Interface Development

- **Text Rendering System**: Added font loading and text surface creation
- **Layout Planning**: Created visual reference zones for game elements
- **Integration Foundation**: Prepared for connecting existing game logic with visual interface

#### 9/18/25 - Project Maturation & Advanced Systems

- **Documentation Overhaul**: Comprehensive README restructuring
- **Test Organization**: Separated test cases into modular, maintainable files
- **Code Architecture**: Achieved professional-grade project structure with clear separation of concerns
- **Status Effects System Design**: Architected multi-turn passive abilities using DTO and Observer patterns

**The Visualization Challenge:** Moving from CLI to graphics meant rethinking everything. How do you take a text-based game and make it visual without breaking all your existing logic? This taught me about separation of concerns - keep the game logic separate from the presentation layer.

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

## 🔄 Advanced Systems Architecture

### Challenge: Multi-Turn Status Effects (September 2025)

**The Problem I Encountered:**
After months of developing my turn-based combat system, I realized something was missing. Players could attack, use specials, and heal - but every action was instant and isolated. Combat felt too simplistic, like a series of disconnected exchanges rather than strategic warfare.

I wanted to add depth: *What if a wizard could cast a protective bubble that lasted multiple turns? What if a warrior's rage could build and persist across the battle? What if a rogue could enter a heightened state where attacks sometimes missed entirely?*

**The Challenge I Faced:**
I needed to implement three specific abilities that completely changed my game's architecture:

- **Wizard's Magic Bubble**: 35% damage reduction lasting 3 turns, with 25 mana maintenance each turn
- **Warrior's Berserker Rage**: Take 25% extra damage, but that extra damage fuels rage buildup  
- **Rogue's Shadow Step**: 30% chance to completely dodge incoming attacks

The tricky part? These effects needed to persist across multiple turns, cost resources to maintain, and interact with my existing combat system without breaking everything I'd already built.

**My Research and Decision Process:**
I spent time analyzing different architectural patterns. My first instinct was to add flags to each character class, but I quickly realized this would create a maintenance nightmare. What happens when effects stack? How do I handle expiration? What about resource costs?

After researching design patterns, I discovered the Observer pattern combined with Data Transfer Objects (DTOs) could solve my problems elegantly.

**Technical Solution - Why DTO + Observer?**
I chose this architecture because it solved four critical requirements:

1. **StatusEffect DTO**: Encapsulates all effect properties (duration, magnitude, costs) in a clean, testable structure
2. **StatusEffectManager**: Uses Observer pattern to track and process effects without character classes knowing the implementation details  
3. **Non-Invasive Integration**: Hooks into my existing combat flow through damage calculation methods
4. **Modular Extensibility**: New effect types only require new handlers, not changes to core character code

**Implementation Architecture:**

```text
Effect Lifecycle: Activation → Turn Processing → Resource Management → Expiration
Damage Pipeline: Dodge Check → Base Damage → Effect Modifications → Final Damage + Bonuses
```

**What I Learned:**
This was my first experience with truly complex system integration. I learned that when adding major features to existing code, the architecture matters more than the implementation. The Observer pattern's loose coupling meant I could add sophisticated multi-turn mechanics without touching my carefully tested character classes.

The most valuable lesson? **Plan for complexity early.** What started as "just add some flags" became a deep dive into design patterns, but the result is a system that can handle any status effect I can imagine.

**Current Status:** Architecture designed and documented, ready for implementation.

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
- **Status Effects Implementation**: Multi-turn passive abilities with resource management
- **Complete Pygame Integration**: Full visual interface with character sprites
- **Asset Integration**: Hand-drawn character art and animation systems
- **Interactive Combat**: Click-based actions and visual feedback
- **Sound System**: Audio effects for attacks, spells, and criticals

### Advanced Features
- **Status Effect Combinations**: Stackable and conflicting effect interactions
- **Multiple Enemy Types**: Expand beyond single-enemy encounters
- **Leveling System**: Character progression and skill trees
- **Equipment System**: Weapons and armor with stat modifications
- **Save/Load**: Game state persistence

## 📈 Learning Outcomes

This project demonstrates mastery of:
- **Object-Oriented Design**: Inheritance, polymorphism, encapsulation
- **Design Patterns**: Observer pattern, DTO pattern, Strategy pattern implementation
- **Game Development**: State management, event handling, rendering loops, multi-turn effect systems
- **Software Testing**: Test-driven development with comprehensive coverage
- **Code Architecture**: Clean separation of concerns and modular design
- **System Integration**: Complex feature addition without breaking existing functionality
- **Version Control**: Git workflow with iterative development
- **Documentation**: Professional README and code commenting

## 📝 Contributing

This project serves as a learning portfolio demonstrating progression from basic programming concepts to advanced game development techniques. Each commit represents a milestone in the development journey.

---

*Last Updated: September 18, 2025*  
*Total Development Time: 2+ months*  
*Technologies Mastered: Python OOP, Pygame, pytest, Git*
