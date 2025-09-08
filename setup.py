#!/usr/bin/env python3
"""
Setup script for Turn-Based RPG Game
"""

from setuptools import setup, find_packages

setup(
    name="turnbased-rpg",
    version="1.0.0",
    description="A turn-based RPG game with strategic AI enemies",
    author="Brian Apostol",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "pygame>=2.0.0",
    ],
    entry_points={
        "console_scripts": [
            "turnbased-game=projects.turnbased_game.main_gameloop.main_game_loop:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
