# Turn-Based Game

A simple CLI-based turn-based game written in Python. Built as a hands-on project to solidify programming fundamentals. Currently being reworked into Pygame.

## 🎯 Features

- Player vs Enemy turn-based combat
- Basic health, attack, resource logic
- Modular code with classes for future scalability
- Improved code structure using polymorphism

## 🛠️ Technologies

- Python 3
- OOP principles (with polymorphism)
- Code Wrapping
- Observer Patters
- DTO
- Command Patterns
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

- test_warrior_attack()
- when creating this test function I decided on using a fixture to assign fresh enemies(made up of the same classes as player classes) for my classes to attack
- initally ran into a problem where I wanted to have an enemy base health of 100. I didn't account for the classes having their own starting health values and came up with failed tests due to incorrect assertions
- implemented relative assertions to keep health consistent

- pytest -k test_warrior_special()

## -- 8/25/25 -->
- Used mock method within uniitest to test action prompt function
- See `/docs/testing.md` for detailed test cases and coverage.

## 9/3/25
- started move to pygame

## 9/4/25

- Decided to implement an enemy AI "wrapper" to solve for best enemy game logic implementation
- to be used with current classes
- uses enemy game logic to determine action
- uses health percentages to streamline health management
- implemented action strings instead of using the commands themselves

This was a huge breakthrough after dealing with the dilemma of how to improve enemy game logic.
Original game logic was based off of random actions with higher chances of different actions based on player and enemy health and resources. This was deemed inefficient during testing and created an obscure player experience. Fights didn't seem challanging and didn't reward player skill
After analyzing the problem I narrowed my available options to 2: Either have enemy versions of actions buried within each class. This felt messy and would make it hard to update enemy game logic. Option 2 was to use a "wrapper" that would call from each class and character instance. Then, I would implement logic using methods that would be called based on enemy conditions (health, resource availability). The game loop would then simply call the enemy methods and would already consider the booleans.
E.g. def _should_use_special(self, player):
        if not self.can_use_special():
          return False
        if player.health <= 50:
          return True
        etc...
## 📸 Screenshots

> _Check the `/screenshots` folder for examples of code before/after refactoring._
