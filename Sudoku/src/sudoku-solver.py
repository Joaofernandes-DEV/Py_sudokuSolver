"""
Módulo principal para o Resolvedor de Sudoku com interface gráfica.
Utiliza backtracking para solução e gera puzzles com diferentes dificuldades.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random
from typing import List, Tuple, Optional


class SudokuBoard:
    """Classe responsável pela lógica do tabuleiro Sudoku"""

    def __init__(self):
        self.grid: List[List[int]] = [[0] * 9 for _ in range(9)]
        self.fixed_cells: List[List[bool]] = [[False] * 9 for _ in range(9)]

    def generate_new_puzzle(self, difficulty: str) -> None:
        """
        Gera um novo puzzle com base na dificuldade especificada

        Args:
            difficulty (str): Nível de dificuldade ('fácil', 'médio' ou 'difícil')
        """
        base = [
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
        self.grid = [row.copy() for row in base]

        for _ in range(removals):
            row, col = random.randint(0, 8), random.randint(0, 8)
            while self.grid[row][col] == 0:
                row, col = random.randint(0, 8), random.randint(0, 8)
            self.grid[row][col] = 0

        self.fixed_cells = [[cell != 0 for cell in row] for row in self.grid]

    def solve(self) -> bool:
        """Resolve o puzzle usando backtracking"""
        empty = self.find_empty_cell()
        if not empty:
            return True

        row, col = empty
        for num in range(1, 10):
            if self.is_valid_move(row, col, num):
                self.grid[row][col] = num
                if self.solve():
                    return True
                self.grid[row][col] = 0
        return False

    def find_empty_cell(self) -> Optional[Tuple[int, int]]:
        """Encontra a próxima célula vazia no grid"""
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    return (i, j)
        return None

    def is_valid_move(self, row: int, col: int, num: int) -> bool:
        """Verifica se um número é válido em uma posição específica"""
        return (
            self._valid_in_row(row, num) and
            self._valid_in_column(col, num) and
            self._valid_in_box(row - row % 3, col - col % 3, num)
        )

    def _valid_in_row(self, row: int, num: int) -> bool:
        return num not in self.grid[row]

    def _valid_in_column(self, col: int, num: int) -> bool:
        return num not in [self.grid[i][col] for i in range(9)]

    def _valid_in_box(self, start_row: int, start_col: int, num: int) -> bool:
        for i in range(3):
            for j in range(3):
                if self.grid[start_row + i][start_col + j] == num:
                    return False
        return True

    def clear_board(self) -> None:
        """Limpa todas as células não fixas do tabuleiro"""
        for i in range(9):
            for j in range(9):
                if not self.fixed_cells[i][j]:
                    self.grid[i][j] = 0


class SudokuGUI:
    """Classe responsável pela interface gráfica do usuário"""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.board = SudokuBoard()
        self.setup_ui()

    def setup_ui(self) -> None:
        """Configura todos os componentes da interface"""
        self.root.title("Resolvedor de Sudoku")
        self.root.minsize(400, 400)
        self._create_control_panel()
        self._create_grid()
        self._configure_grid_layout()

    def _create_control_panel(self) -> None:
        """Cria o painel de controle superior"""
        self.control_frame = ttk.Frame(self.root)
        self.control_frame.grid(row=0, column=0, columnspan=9, sticky='ew', pady=10)

        self.difficulty = tk.StringVar(value='fácil')
        self.diff_select = ttk.Combobox(
            self.control_frame,
            textvariable=self.difficulty,
            values=('fácil', 'médio', 'difícil'),
            width=10
        )
        self.diff_select.grid(row=0, column=0, padx=5)

        ttk.Button(
            self.control_frame,
            text='Novo Jogo',
            command=self._handle_new_game
        ).grid(row=0, column=1, padx=5)

        ttk.Button(
            self.control_frame,
            text='Resolver',
            command=self._handle_solve
        ).grid(row=0, column=2, padx=5)

        ttk.Button(
            self.control_frame,
            text='Limpar',
            command=self._handle_clear
        ).grid(row=0, column=3, padx=5)

    def _create_grid(self) -> None:
        """Cria a grade de células do Sudoku"""
        self.cells = [[None] * 9 for _ in range(9)]
        for i in range(9):
            for j in range(9):
                validate_cmd = (self.root.register(self._validate_input), '%P')
                entry = ttk.Entry(
                    self.root,
                    width=3,
                    font=('Arial', 16),
                    justify='center',
                    validate='key',
                    validatecommand=validate_cmd
                )
                entry.grid(row=i + 1, column=j, padx=2, pady=2, sticky='nsew')
                self.cells[i][j] = entry

    def _configure_grid_layout(self) -> None:
        """Configura o layout responsivo da grade"""
        for i in range(9):
            self.root.grid_columnconfigure(i, weight=1)
            self.root.grid_rowconfigure(i + 1, weight=1)
        self.root.grid_rowconfigure(0, weight=0)

    def _validate_input(self, value: str) -> bool:
        """Valida a entrada do usuário"""
        return value == "" or (value.isdigit() and 1 <= int(value) <= 9)

    def _handle_new_game(self) -> None:
        """Atualiza a interface com um novo jogo"""
        self.board.generate_new_puzzle(self.difficulty.get())
        self._update_grid_display()

    def _handle_solve(self) -> None:
        """Inicia a resolução do puzzle e atualiza a interface"""
        if self.board.solve():
            self._update_grid_display(solved=True)
            messagebox.showinfo("Sucesso", "Sudoku resolvido com sucesso!")
        else:
            messagebox.showerror("Erro", "Não foi possível resolver o Sudoku")

    def _handle_clear(self) -> None:
        """Limpa todas as células editáveis"""
        self.board.clear_board()
        self._update_grid_display()
        messagebox.showinfo("Limpo", "Tabuleiro resetado para o estado inicial!")

    def _update_grid_display(self, solved: bool = False) -> None:
        """Atualiza a exibição das células na interface"""
        for i in range(9):
            for j in range(9):
                self.cells[i][j].delete(0, tk.END)
                value = self.board.grid[i][j]
                if value != 0:
                    self.cells[i][j].insert(0, str(value))

                state = 'disabled' if self.board.fixed_cells[i][j] else 'normal'
                fg_color = 'green' if solved and not self.board.fixed_cells[i][j] else 'black'

                self.cells[i][j].config(
                    state=state,
                    foreground=fg_color,
                    style='Fixed.TEntry' if state == 'disabled' else 'TEntry'
                )


if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuGUI(root)

    # Configuração de estilos
    style = ttk.Style()
    style.configure('Fixed.TEntry', background='#f0f0f0')

    root.mainloop()
