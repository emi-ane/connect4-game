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

    def color_players(self):
        # Assign colors to players
        self.p1 = (128, 0, 128)  # Purple for Player 1
        self.p2 = (255, 192, 203)  # Pink for Player 2

    def disc_grid_color(self):
        # Define grid and empty slot colors
        self.grid_color = (0, 0, 255)  # Blue for the grid
        self.empty_color = (0, 0, 0)  # Black for empty spaces

    def display_turn(self):
        # Display current player's turn
        if self.turn == 1:
            self.disc_color = self.p1  # Set disc color to Player 1's color
            print(f"{self.player1_name} (Violet) play.")
        else:
            self.disc_color = self.p2  # Set disc color to Player 2's color
            print(f"{self.player2_name} (Pink) play.")

    def draw_grid(self):
        # Draw the game board and the placed discs
        self.window.fill(self.empty_color)  # Clear the board

        # Loop through each row and column to draw the grid
        for i in range(self.rows):
            for j in range(self.columns):
                # Draw grid rectangles
                pygame.draw.rect(self.window, self.grid_color,
                                 (j * self.cell_width, i * self.cell_height + self.top_bar,
                                  self.cell_width, self.cell_height))

                # Draw a disc if the slot is occupied
                if self.grid[i][j] == 1:  # Player 1's disc
                    pygame.draw.circle(self.window, self.p1,
                                       (j * self.cell_width + self.cell_width // 2,
                                        i * self.cell_height + self.cell_height // 2 + self.top_bar),
                                        self.disc_radius)
                elif self.grid[i][j] == 2:  # Player 2's disc
                    pygame.draw.circle(self.window, self.p2,
                                       (j * self.cell_width + self.cell_width // 2,
                                        i * self.cell_height + self.cell_height // 2 + self.top_bar),
                                        self.disc_radius)
                else:  # Empty slot
                    pygame.draw.circle(self.window, self.empty_color,
                                       (j * self.cell_width + self.cell_width // 2,
                                        i * self.cell_height + self.cell_height // 2 + self.top_bar),
                                        self.disc_radius)

    def change_turn(self):
        # Switch the player's turn
        self.turn = 1 if self.turn == 2 else 2
        self.display_turn()  

    def draw_disc(self):
        # Draw the disc at the current mouse position
        pygame.draw.circle(self.window, self.disc_color, (pygame.mouse.get_pos()[0], self.disc_radius), self.disc_radius)

    def drop_disc(self, columns):
        # Drop a disc in the selected column (if there's space)
        for i in range(self.rows - 1, -1, -1):  # Start from the bottom row
            if self.grid[i][columns] == 0:  # Find the first empty row
                self.grid[i][columns] = self.turn  # Place the disc
                return True  # Successfully placed
        return False  # Column full, placement failed

    def check_winner(self):
        # Check for four consecutive identical values (horizontal, vertical, diagonal)
        
        # Horizontal check
        for i in range(self.grid.shape[0]):
            for j in range(self.grid.shape[1] - 3):
                if np.all(self.grid[i, j:j + 4] == self.grid[i, j]) and self.grid[i, j] != 0:
                    self.winner = self.grid[i, j]

        # Vertical check
        for i in range(self.grid.shape[0] - 3):
            for j in range(self.grid.shape[1]):
                if np.all(self.grid[i:i + 4, j] == self.grid[i, j]) and self.grid[i, j] != 0:
                    self.winner = self.grid[i, j]

        # Diagonal (top-left to bottom-right) check
        for i in range(self.grid.shape[0] - 3):
            for j in range(self.grid.shape[1] - 3):
                if np.all(self.grid[i:i + 4, j:j + 4].diagonal() == self.grid[i, j]) and self.grid[i, j] != 0:
                    self.winner = self.grid[i, j]

        # Diagonal (bottom-left to top-right) check
        for i in range(3, self.grid.shape[0]):
            for j in range(self.grid.shape[1] - 3):
                if np.all(np.diag(np.fliplr(self.grid[i - 3:i + 1, j:j + 4])) == self.grid[i, j]) and self.grid[i, j] != 0:
                    self.winner = self.grid[i, j]

    def draw_winner(self):
        # Display winner's name
        font = pygame.font.SysFont("Arial", self.top_bar)
        text = font.render(f'{self.player1_name if self.winner == 1 else self.player2_name} won', True, (255, 255, 255))
        self.window.blit(text, (0, 0))

    def ask_continue_game(self):
        # Ask if players want to start a new match
        choice = input("Do you want to play a new match? (yes/no): ").lower()
        if choice == 'yes':
            self.grid = np.zeros((self.rows, self.columns), dtype=int)  # Reset grid
            self.winner = 0  # Reset winner
            print("New match started")
            return True
        else:
            print("End of game")
        return False

    def play(self):
        # Main game loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEMOTION and not self.winner:
                    self.draw_grid()
                    self.draw_disc()

                if event.type == pygame.MOUSEBUTTONDOWN and not self.winner:
                    columns = pygame.mouse.get_pos()[0] // self.cell_width
                    if self.drop_disc(columns):
                        self.draw_grid()
                        self.check_winner()
                        if self.winner:
                            print(f"{self.player1_name if self.winner == 1 else self.player2_name} won")
                            self.draw_winner()
                            if not self.ask_continue_game():
                                running = False
                        self.change_turn()

            pygame.display.update()
        pygame.quit()

# Initialize the game
pygame.init()

game = Game()
game.ask_player_names()
game.grid_dimen()
game.color_players()
game.disc_grid_color()
game.play()


# In[ ]:




