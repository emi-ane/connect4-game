#!/usr/bin/env python
# coding: utf-8

# In[3]:
# new comment


import pygame
import numpy as np

class Game:
    def __init__(self, rows=6, columns=7, cell=90):
        # Initialize game settings (grid size, cell size, winner status, and empty grid)
        self.rows = rows
        self.columns = columns
        self.cell_width = cell
        self.cell_height = cell
        self.winner = 0  # No winner at the start
        self.grid = np.zeros((self.rows, self.columns), dtype=int)  # Create an empty grid

    def ask_player_names(self):
        # Ask players for their names
        self.player1_name = input("Player 1 enter your name : ")
        self.player2_name = input("Player 2 enter your name : ")

        # Determine who starts: The player with the shorter name goes first
        if len(self.player1_name) <= len(self.player2_name):
            self.turn = 1
            print(f"{self.player1_name} starts the match")
        else:
            self.turn = 2
            print(f"{self.player2_name} starts the match")

    def grid_dimen(self):
        # Define game board dimensions and colors
        self.disc_radius = self.cell_width // 2 - 7  # Calculate disc radius
        self.top_bar = self.disc_radius * 3  # Space at the top for player info
        self.window_width = self.columns * self.cell_width
        self.window_height = self.rows * self.cell_height + self.top_bar
        self.window = pygame.display.set_mode((self.window_width, self.window_height))  # Create game window
        self.disc_color = (0, 255, 0)  # Default disc color
