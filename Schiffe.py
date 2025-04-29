import tkinter as tk
import random
from tkinter import messagebox

class BattleshipGame:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Schiffe versenken - 1 Spieler")

        self.ships = [[0] * 8 for _ in range(8)]
        self.remaining_ships = 0
        self.button_grid = [[None] * 8 for _ in range(8)]
        self.shots_counter = 0

        self.create_ships()
        self.create_game_board()
        self.create_counter_label()

    def create_ships(self):
        self.ships = [[0] * 8 for _ in range(8)]
        self.remaining_ships = 13

        for size in [2, 3, 3, 5]:
            placed = False
            while not placed:
                orientation = random.choice(["horizontal", "vertical"])
                if orientation == "horizontal":
                    row = random.randint(0, 7)
                    col = random.randint(0, 8 - size)
                else:
                    row = random.randint(0, 8 - size)
                    col = random.randint(0, 7)
                if self.can_place_ship(row, col, size, orientation):
                    self.place_ship(row, col, size, orientation)
                    placed = True

    def can_place_ship(self, row, col, size, orientation):
        if orientation == "horizontal":
            if col + size > 8:
                return False
        else:
            if row + size > 8:
                return False

        for i in range(size):
            if orientation == "horizontal":
                if self.ships[row][col + i] != 0:
                    return False
            else:
                if self.ships[row + i][col] != 0:
                    return False

        
        if orientation == "horizontal":
            for i in range(size):
                if row > 0 and self.ships[row - 1][col + i] != 0:
                    return False
                if row < 7 and self.ships[row + 1][col + i] != 0:
                    return False
        else:
            for i in range(size):
                if col > 0 and self.ships[row + i][col - 1] != 0:
                    return False
                if col < 7 and self.ships[row + i][col + 1] != 0:
                    return False

        return True

    def place_ship(self, row, col, size, orientation):
        for i in range(size):
            if orientation == "horizontal":
                self.ships[row][col + i] = size
            else:
                self.ships[row + i][col] = size

    def shoot(self, row, col):
        self.shots_counter += 1
        if self.ships[row][col] != 0:
            self.ships[row][col] = 0
            self.button_grid[row][col].config(text="⛵", state=tk.DISABLED)
            self.remaining_ships -= 1
            if self.remaining_ships == 0:
                messagebox.showinfo("Spiel beendet", f"Alle Schiffe versenkt!\nSchüsse: {self.shots_counter}")
                self.window.destroy()
        else:
            self.button_grid[row][col].config(text="O", state=tk.DISABLED)
        self.update_counter_label()

    def create_game_board(self):
        for row in range(8):
            for col in range(8):
                button = tk.Button(self.window,width=2,height=1,font=("Arial", 14, "bold"),bg="blue")
                button.grid(row=row+1, column=col+1)
                button.config(command=self.create_shoot_handler(row, col))
                self.button_grid[row][col] = button

        for col in range(8):
            label = tk.Label(self.window,text=chr(ord("A") + col),font=("Arial", 12, "bold"))
            label.grid(row=0, column=col+1)

        for row in range(8):
            label = tk.Label(self.window,text=row+1,font=("Arial", 12, "bold"))
            label.grid(row=row+1, column=0)
            
        for row in range(9):
            self.window.grid_rowconfigure(row, weight=1)
        for col in range(9):
            self.window.grid_columnconfigure(col, weight=1)

    def create_shoot_handler(self, row, col):
        def handler():
            self.shoot(row, col)
        return handler

    def create_counter_label(self):
        self.counter_label = tk.Label(self.window,text="Schüsse: 0",font=("Arial", 12, "bold"))
        self.counter_label.grid(row=9, columnspan=8)

    def update_counter_label(self):
        self.counter_label.config(text=f"Schüsse: {self.shots_counter}")

    def run(self):
        self.window.mainloop()

game = BattleshipGame()
game.run()
