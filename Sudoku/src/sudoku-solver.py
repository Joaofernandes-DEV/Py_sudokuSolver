import tkinter as tk
from tkinter import ttk
import random

class ResolvedorSudoku:
    def __init__(self, root):
        self.root = root
        self.root.title("Resolvedor de Sudoku")
        self.grade = [[0]*9 for _ in range(9)]
        self.fixos = [[False]*9 for _ in range(9)]
        self.criar_widgets()
        self.gerar_novo_puzzle('fácil')

    def criar_widgets(self):
        frame_controle = tk.Frame(self.root)
        frame_controle.grid(row=0, column=0, columnspan=9)
        
        self.dificuldade = tk.StringVar()
        self.seletor_dificuldade = ttk.Combobox(frame_controle, textvariable=self.dificuldade, 
                                              values=('fácil', 'médio', 'difícil'), width=8)
        self.seletor_dificuldade.grid(row=0, column=0, padx=5)
        
        self.botao_novo = ttk.Button(frame_controle, text='Novo Jogo', 
                                    command=lambda: self.gerar_novo_puzzle(self.dificuldade.get()))
        self.botao_novo.grid(row=0, column=1, padx=5)
        
        self.botao_resolver = ttk.Button(frame_controle, text='Resolver', command=self.resolver_puzzle)
        self.botao_resolver.grid(row=0, column=2, padx=5)

        self.campos = [[None]*9 for _ in range(9)]
        for i in range(9):
            for j in range(9):
                campo = tk.Entry(self.root, width=2, font=('Arial', 18), justify='center')
                campo.grid(row=i+1, column=j, padx=1, pady=1)
                self.campos[i][j] = campo

    def gerar_novo_puzzle(self, dificuldade):
        grade_base = [
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
        
        remocoes = {'fácil': 30, 'médio': 40, 'difícil': 50}[dificuldade]
        self.grade = [linha.copy() for linha in grade_base]
        
        for _ in range(remocoes):
            linha = random.randint(0, 8)
            coluna = random.randint(0, 8)
            while self.grade[linha][coluna] == 0:
                linha = random.randint(0, 8)
                coluna = random.randint(0, 8)
            self.grade[linha][coluna] = 0

        self.fixos = [[self.grade[i][j] != 0 for j in range(9)] for i in range(9)]
        
        for i in range(9):
            for j in range(9):
                self.campos[i][j].delete(0, tk.END)
                if self.grade[i][j] != 0:
                    self.campos[i][j].insert(0, str(self.grade[i][j]))
                self.campos[i][j].config(
                    state='disabled' if self.fixos[i][j] else 'normal',
                    disabledbackground='#f0f0f0' if self.fixos[i][j] else 'white'
                )

    def resolver_puzzle(self):
        for i in range(9):
            for j in range(9):
                if not self.fixos[i][j]:
                    valor = self.campos[i][j].get()
                    self.grade[i][j] = int(valor) if valor.isdigit() else 0
        
        if self.resolver():
            for i in range(9):
                for j in range(9):
                    if not self.fixos[i][j]:
                        self.campos[i][j].delete(0, tk.END)
                        self.campos[i][j].insert(0, str(self.grade[i][j]))
        else:
            print("Não existe solução")

    def resolver(self):
        vazio = self.encontrar_vazio()
        if not vazio:
            return True
        linha, coluna = vazio
        
        for num in range(1, 10):
            if self.eh_valido(linha, coluna, num):
                self.grade[linha][coluna] = num
                if self.resolver():
                    return True
                self.grade[linha][coluna] = 0
        return False

    def encontrar_vazio(self):
        for i in range(9):
            for j in range(9):
                if self.grade[i][j] == 0:
                    return (i, j)
        return None

    def eh_valido(self, linha, coluna, num):
        if num in self.grade[linha]:
            return False
        
        if num in [self.grade[i][coluna] for i in range(9)]:
            return False
        
        linha_inicio, coluna_inicio = 3*(linha//3), 3*(coluna//3)
        for i in range(3):
            for j in range(3):
                if self.grade[linha_inicio+i][coluna_inicio+j] == num:
                    return False
        return True

if __name__ == "__main__":
    root = tk.Tk()
    jogo = ResolvedorSudoku(root)
    root.mainloop()