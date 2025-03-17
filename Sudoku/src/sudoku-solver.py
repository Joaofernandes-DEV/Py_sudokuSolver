import tkinter as tk
from tkinter import ttk, messagebox
import random

class SudokuSolver:
    def __init__(self, root):
        self.root = root
        self.root.title("Resolvedor de Sudoku")
        self.root.minsize(400, 400)
        self.grid = [[0]*9 for _ in range(9)]
        self.fixed = [[False]*9 for _ in range(9)]
        self.create_widgets()
        self.generate_new_puzzle('fácil')
        self.configure_grid_resize()

    def configure_grid_resize(self):
        for i in range(9):
            self.root.grid_columnconfigure(i, weight=1)
            self.root.grid_rowconfigure(i+1, weight=1)
        self.root.grid_rowconfigure(0, weight=0)

    def create_widgets(self):
        control_frame = tk.Frame(self.root)
        control_frame.grid(row=0, column=0, columnspan=9, sticky='ew', pady=10)
        
        self.difficulty = tk.StringVar(value='fácil')
        self.diff_select = ttk.Combobox(control_frame, textvariable=self.difficulty, 
                                      values=('fácil', 'médio', 'difícil'), width=10)
        self.diff_select.grid(row=0, column=0, padx=5)
        
        self.new_btn = ttk.Button(control_frame, text='Novo Jogo', 
                                command=lambda: self.generate_new_puzzle(self.difficulty.get()))
        self.new_btn.grid(row=0, column=1, padx=5)
        
        self.solve_btn = ttk.Button(control_frame, text='Resolver', command=self.solve_puzzle)
        self.solve_btn.grid(row=0, column=2, padx=5)

        self.entries = [[None]*9 for _ in range(9)]
        for i in range(9):
            for j in range(9):
                validate_cmd = (self.root.register(self.validate_input), '%P')
                entry = tk.Entry(self.root, width=3, font=('Arial', 16), justify='center',
                               validate='key', validatecommand=validate_cmd)
                entry.grid(row=i+1, column=j, padx=2, pady=2, sticky='nsew')
                self.entries[i][j] = entry

    def validate_input(self, value):
        """Valida se a entrada é um número entre 1 e 9 ou vazio"""
        if value == "":
            return True
        if value.isdigit() and 1 <= int(value) <= 9:
            return True
        return False

    def generate_new_puzzle(self, difficulty):
        base_grid = [
            [5, 3, 4, 6, 7, 8, 9, 1, 2],
            [6, 7, 2, 1, 9, 5, 3, 4, 8],
            [1, 9, 8, 3, 4, 2, 5, 6, 7],
            [8, 5, 9, 7, 6, 1, 4, 2, 3],
            [4, 2, 6, 8, 5, 3, 7, 9, 1],
            [7, 1, 3, 9, 2, 4, 8, 5, 6],
            [9, 6, 1, 5, 3, 7, 2, 8, 4],
            [2, 8, 7, 4, 1, 9, 6, 3, 5],
            [3, 4, 5, 2, 8, 6, 1, 7, 9]
        ]
        
        removals = {'fácil': 30, 'médio': 40, 'difícil': 50}[difficulty]
        self.grid = [row.copy() for row in base_grid]
        
        for _ in range(removals):
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            while self.grid[row][col] == 0:
                row = random.randint(0, 8)
                col = random.randint(0, 8)
            self.grid[row][col] = 0

        self.fixed = [[self.grid[i][j] != 0 for j in range(9)] for i in range(9)]
        
        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0, tk.END)
                if self.grid[i][j] != 0:
                    self.entries[i][j].insert(0, str(self.grid[i][j]))
                self.entries[i][j].config(
                    state='disabled' if self.fixed[i][j] else 'normal',
                    disabledbackground='#f0f0f0' if self.fixed[i][j] else 'white',
                    fg='black' if self.fixed[i][j] else 'blue'
                )

    def solve_puzzle(self):
        if self.solve():
            for i in range(9):
                for j in range(9):
                    if not self.fixed[i][j]:
                        self.entries[i][j].delete(0, tk.END)
                        self.entries[i][j].insert(0, str(self.grid[i][j]))
                        self.entries[i][j].config(fg='green')
            messagebox.showinfo("Sucesso", "Sudoku resolvido com sucesso!")
        else:
            messagebox.showerror("Erro", "Não foi possível resolver o Sudoku")

    def solve(self):
        empty = self.find_empty()
        if not empty:
            return True
        row, col = empty
        
        for num in range(1, 10):
            if self.is_valid(row, col, num):
                self.grid[row][col] = num
                if self.solve():
                    return True
                self.grid[row][col] = 0
        return False

    def find_empty(self):
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    return (i, j)
        return None

    def is_valid(self, row, col, num):
        if num in self.grid[row]:
            return False
        
        if num in [self.grid[i][col] for i in range(9)]:
            return False
        
        start_row, start_col = 3*(row//3), 3*(col//3)
        for i in range(3):
            for j in range(3):
                if self.grid[start_row+i][start_col+j] == num:
                    return False
        return True

if __name__ == "__main__":
    root = tk.Tk()
    game = SudokuSolver(root)
    root.mainloop()
