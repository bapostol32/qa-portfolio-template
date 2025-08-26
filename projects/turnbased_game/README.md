# Turn-Based Game

A simple CLI-based turn-based game written in Python. Built as a hands-on project to solidify programming fundamentals.

## 🎯 Features

- Player vs Enemy turn-based combat
- Basic health, attack, resource logic
- Modular code with classes for future scalability
- Improved code structure using polymorphism

## 🛠️ Technologies

- Python 3
- OOP principles (with polymorphism)
- Terminal I/O

## 🚀 How to Run

```bash
python turnbased_game.py```

## 📚 Dev Journey

Originally built game loop using heavily nested `if` statements. Refactored using polymorphism to simplify game loop logic.
    - Originally had game loop consist of nested if statements for each of my original classes (Warrior, Rogue, Wizard). 
        - Resulted in really messy "spaghetti" code that ran a risk of adding complications as more features were added
### 8/15/24
- For the solution I ended up deciding on creating a base class that would have an empty set of attributes and functions.
- That would be filled in by my original 3 classes as subclasses.
- For The game loop we now only need to use the instantation for each action.
- I then considered the player's ability to distinguish between the different classes abilities.
- All 3 classes have an attack, special, and item action with all with different damage outputs and resource management. 
- The player would need to know what each class's did in the input statement. 

### 8/16/25        
- I added an action prompt function to the base class for each subclass to inherit with their own print statement of the action choices the player can make.

## 8/25/25
- IDEA: passive abilty for warrior
        - after receiving damage, gain rage.

## 8/25/25
- Set up virtual environment on all devices to isolate packages

      
## 🧪 Testing

- Testing framework: `pytest`

### 8/24/25 
- Test coverage includes:
  - `Warrior` subclass (attributes, methods, edge cases)
  - Game loop logic: 
    - utilized pytest fixture to create fresh enemy class for
    - each warrior function as needed.
  - Subclass-specific actions
  - To run tests:
  ```bash
  pytest -k test_warrior_attack()

  pytest -k test_warrior_special()
  ```
<!-- 8/25/25 -->
- Used mock method within uniitest to test action prompt function
- See `/docs/testing.md` for detailed test cases and coverage.

## 📸 Screenshots

> _Check the `/screenshots` folder for examples of code before/after refactoring._
