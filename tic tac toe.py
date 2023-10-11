import tkinter as tk
import tkinter.messagebox
import random
from tkinter import Tk, Button


class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Крестики-Нолики")
        self.theme = "light"  # Изначально устанавливаем светлую тему

        # Создаем кнопку "Сменить тему" и кнопку "Играть заново"
        self.theme_button = tk.Button(self.root, text="Сменить тему", command=self.toggle_theme)
        self.theme_button.grid(row=0, column=0)  # Кнопка "Сменить тему" в первой колонке
        self.restart_button = tk.Button(self.root, text="Играть заново", command=self.restart_game)
        self.restart_button.grid(row=0, column=1)  # Кнопка "Играть заново" во второй колонке

        # Переменная для хранения режима игры
        self.game_mode = tk.StringVar()
        self.game_mode.set("two_players")

        # Создаем радиокнопки для выбора режима игры
        self.two_players_radio = tk.Radiobutton(root, text="Играть вдвоем", variable=self.game_mode,
                                                value="two_players")
        self.with_bot_radio = tk.Radiobutton(root, text="Играть с ботом", variable=self.game_mode, value="with_bot")

        self.two_players_radio.grid(row=0, column=0)
        self.with_bot_radio.grid(row=0, column=1)

        # Создаем кнопку "Начать игру заново" в главном окне
        self.restart_button = tk.Button(root, text="Играть заново", command=self.restart_game)
        self.restart_button.grid(row=1, column=0, columnspan=2)

        # Создаем доску для игры
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.game_over = False

        self.buttons = [[None for _ in range(3)] for _ in range(3)]


        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(root, text=" ", width=5, height=2, font=("Helvetica", 24),
                                               command=lambda i=i, j=j: self.make_move(i, j))
                self.buttons[i][j].grid(row=i + 2, column=j)

        # Создаем метку для отображения победителя
        self.winner_label = tk.Label(root, text="", font=("Helvetica", 16))
        self.winner_label.grid(row=5, columnspan=2)

    def toggle_theme(self):
        if self.theme == "light":
            self.theme = "dark"
        else:
            self.theme = "light"
        self.apply_theme()

    def apply_theme(self):
        if self.theme == "light":
            self.root.configure(bg="white")  # Устанавливаем цвет фона светлой темы
        else:
            self.root.configure(bg="black")  # Устанавливаем цвет фона темной темы

    def restart_game(self):
        # Очищаем доску и сбрасываем состояние игры
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.game_over = False

        # Скрываем текст метки победителя
        self.winner_label.config(text="")

        # Отображаем доску
        for i in range(3):
            for j in range(3):
                self.buttons[i][j]["text"] = ""

        # Возвращаем радиокнопки
        self.two_players_radio.grid()
        self.with_bot_radio.grid()

        # Отображаем кнопку "Играть заново"
        self.restart_button.grid()
    def make_move(self, row, col):
        if not self.game_over and self.board[row][col] == " ":
            self.board[row][col] = self.current_player
            self.buttons[row][col]["text"] = self.current_player
            self.buttons[row][col]["fg"] = "red" if self.current_player == "X" else "blue"  # Красный для X, синий для O
            if self.check_win(self.current_player):
                self.display_winner(self.current_player)
            elif self.check_draw():
                self.display_draw()
            else:
                self.current_player = "X" if self.current_player == "O" else "O"

                if self.current_player == "O" and self.game_mode.get() == "with_bot":
                    self.bot_move()

    def bot_move(self):
        empty_cells = [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == " "]
        if empty_cells:
            row, col = random.choice(empty_cells)
            self.make_move(row, col)

    def check_win(self, symbol):
        for i in range(3):
            if all(self.board[i][j] == symbol for j in range(3)) or all(self.board[j][i] == symbol for j in range(3)):
                return True
        main_diagonal = [self.board[i][i] for i in range(3)]
        anti_diagonal = [self.board[i][2 - i] for i in range(3)]
        return all(cell == symbol for cell in main_diagonal) or all(cell == symbol for cell in anti_diagonal)

    def check_draw(self):
        return all(cell != " " for row in self.board for cell in row)

    def display_winner(self, symbol):
        self.game_over = True
        message = f"{symbol} победил!"
        self.winner_label.config(text=message)


if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()