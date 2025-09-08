# QA Portfolio Template

## Turn-Based RPG Game

A sophisticated turn-based RPG featuring three character classes and intelligent AI enemies.

### Features
- **Three Character Classes**: Warrior, Rogue, and Wizard with unique abilities
- **Strategic AI System**: Enemies adapt their behavior based on health status
- **Dynamic Combat**: Critical hits, resource management, and tactical decisions
- **Professional Code Structure**: Object-oriented design with composition patterns

### How to Run

From the `qa-portfolio-template` directory:

**Option 1: Simple launcher**
```bash
python3 run_game.py
```

**Option 2: Module execution**
```bash
python3 -m projects.turnbased_game.main_gameloop.main_game_loop
```

**Option 3: Direct execution**
```bash
python3 projects/turnbased_game/main_gameloop/main_game_loop.py
```

### Requirements
- Python 3.8+
- pygame 2.0+

### Game Classes
- **Warrior**: High health, rage-based abilities
- **Rogue**: Stealth attacks, stamina management  
- **Wizard**: Magical spells, mana system

Enjoy the game!