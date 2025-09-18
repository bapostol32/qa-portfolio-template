# Test Documentation

## 📋 Test Overview

This directory contains comprehensive test suites for the Turn-Based RPG project. Tests are organized by functionality and include detailed documentation of test cases, bugs encountered, and resolution dates.

## 🗂️ Test File Organization

### Character Class Tests
- **`test_base_character.py`** - Base Character class functionality
- **`test_warrior.py`** - Warrior-specific methods and mechanics
- **`test_rogue.py`** - Rogue-specific methods and mechanics  
- **`test_wizard.py`** - Wizard-specific methods and mechanics
- **`test_enemy_ai.py`** - Enemy AI decision-making algorithms

### Integration Tests
- **`test_game_integration.py`** - Cross-class interactions and game flow
- **`test_pygame_integration.py`** - Visual interface and event handling (future)

## 🧪 Test Results Summary

### Current Status
- **Total Tests**: [TO BE FILLED]
- **Passing**: [TO BE FILLED]
- **Last Run**: [TO BE FILLED]
- **Coverage**: [TO BE FILLED]%

### Test Progress by Date

#### August 24, 2025
- ✅ `test_warrior_attack()` - PASSED
- ✅ `test_warrior_health()` - PASSED
- 🔧 **Bug Fixed**: Health assertion issues with relative health values

#### August 25, 2025  
- ✅ `test_warrior_special()` - PASSED
- ✅ `test_warrior_item()` - PASSED
- ✅ Mock testing implementation for action prompts

#### September 1, 2025
- ✅ `test_rogue_attack()` - PASSED
- ✅ `test_rogue_special()` - PASSED
- ✅ `test_rogue_item()` - PASSED

#### September 6, 2025
- ✅ `test_rogue_action_prompt()` - PASSED
- ✅ `test_rogue_special_oom()` - PASSED (Out of Mana handling)
- ✅ `test_rogue_print_status()` - PASSED

## 🐛 Bugs Encountered & Resolutions

### Bug #1: Health Assertion Inconsistencies
- **Date**: August 24, 2025
- **Description**: Test failures due to incorrect health value assumptions
- **Root Cause**: Each character class has different starting health values
- **Resolution**: Implemented relative assertions using starting health as baseline
- **Files Affected**: `test_warrior.py`
- **Status**: ✅ RESOLVED

### Bug #2: [TO BE FILLED]
- **Date**: [DATE]
- **Description**: [DESCRIPTION]
- **Root Cause**: [CAUSE]
- **Resolution**: [SOLUTION]
- **Files Affected**: [FILES]
- **Status**: [STATUS]

## 🔧 Test Configuration

### Required Dependencies
```bash
pip install pytest
pip install pytest-cov  # For coverage reports
```

### Running Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest test_warrior.py

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=character_classes

# Run specific test function
pytest -k test_warrior_attack
```

### Test Fixtures
Tests use pytest fixtures for:
- **Fresh enemy instances** for each test
- **Parameterized testing** across multiple character classes
- **Mock objects** for input/output testing

## 📊 Coverage Goals

### Current Coverage by Module
- **base_character.py**: [TO BE FILLED]%
- **warrior.py**: [TO BE FILLED]%
- **rogue.py**: [TO BE FILLED]%
- **wizard.py**: [TO BE FILLED]%
- **enemy_ai.py**: [TO BE FILLED]%

### Target Coverage: 95%+

## 🔍 Test Case Categories

### Unit Tests
- ✅ Character initialization
- ✅ Attack calculations
- ✅ Special ability mechanics
- ✅ Resource management
- ✅ Item usage
- ✅ Health/resource boundaries

### Integration Tests
- ✅ Character vs character combat
- ✅ Enemy AI decision making
- ⏳ Game loop integration (in progress)
- ⏳ Pygame event handling (planned)

### Edge Case Tests
- ✅ Zero health scenarios
- ✅ Resource depletion
- ✅ Maximum damage calculations
- ✅ Invalid input handling

## 📝 Test Writing Guidelines

### Naming Conventions
- Test files: `test_[module_name].py`
- Test functions: `test_[function_name]_[scenario]()`
- Test classes: `Test[ClassName]`

### Documentation Requirements
- Clear test function names describing what is being tested
- Comments explaining complex test logic
- Assertion messages for better failure diagnostics
- Date stamps for when tests were written/last modified

### Best Practices
1. **One assertion per test** when possible
2. **Use fixtures** for common setup
3. **Test both positive and negative cases**
4. **Include boundary value testing**
5. **Mock external dependencies**

---

*Last Updated: [DATE]*  
*Test Suite Maintainer: [YOUR NAME]*
