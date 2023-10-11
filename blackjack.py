import random
import tkinter as tk

class BlackjackGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack")

        self.deck = Deck()
        self.player = Player("Player")
        self.computer = Player("Computer")

        self.player_score_label = tk.Label(root, text="Player's Score: 0")
        self.player_score_label.pack()

        self.computer_score_label = tk.Label(root, text="Computer's Score: 0")
        self.computer_score_label.pack()

        self.player_cards_label = tk.Label(root, text="Player's Cards:")
        self.player_cards_label.pack()

        self.computer_cards_label = tk.Label(root, text="Computer's Cards:")
        self.computer_cards_label.pack()

        self.player_buttons_frame = tk.Frame(root)
        self.player_buttons_frame.pack()

        self.hit_button = tk.Button(self.player_buttons_frame, text="Hit", command=self.player_hit)
        self.hit_button.pack(side=tk.LEFT)

        self.stand_button = tk.Button(self.player_buttons_frame, text="Stand", command=self.player_stand)
        self.stand_button.pack(side=tk.LEFT)

        self.new_game_button = tk.Button(root, text="Начать игру заново", command=self.start_new_game)
        self.new_game_button.pack()

        self.play_game()

    def player_hit(self):
        card = self.deck.deal_card()
        self.player.add_card_to_hand(card)
        self.update_player_ui()
        if self.player.calculate_hand_value() > 21:
            self.end_game("Computer wins!", show_computer_cards=True)

    def player_stand(self):
        while self.computer.calculate_hand_value() < 17:
            card = self.deck.deal_card()
            self.computer.add_card_to_hand(card)
        self.update_computer_ui()
        if self.computer.calculate_hand_value() > 21 or self.computer.calculate_hand_value() < self.player.calculate_hand_value():
            self.end_game("Player wins!", show_computer_cards=True)
        elif self.computer.calculate_hand_value() == self.player.calculate_hand_value():
            self.end_game("It's a tie!", show_computer_cards=True)
        else:
            self.end_game("Computer wins!", show_computer_cards=True)

    def update_player_ui(self):
        player_hand = ", ".join(str(card) for card in self.player.hand)
        self.player_cards_label.config(text=f"Player's Cards: {player_hand}")
        self.player_score_label.config(text=f"Player's Score: {self.player.calculate_hand_value()}")

    def update_computer_ui(self):
        computer_hand = ", ".join(str(card) for card in self.computer.hand)
        self.computer_cards_label.config(text=f"Computer's Cards: {computer_hand}")
        self.computer_score_label.config(text=f"Computer's Score: {self.computer.calculate_hand_value()}")

    def play_game(self):
        self.deck = Deck()
        self.player.hand.clear()
        self.computer.hand.clear()
        self.player_score_label.config(text="Player's Score: 0")
        self.computer_score_label.config(text="Computer's Score: 0")
        self.player_cards_label.config(text="Player's Cards:")
        self.computer_cards_label.config(text="Computer's Cards:")
        self.hit_button.config(state=tk.NORMAL)
        self.stand_button.config(state=tk.NORMAL)

        for _ in range(2):
            self.player.add_card_to_hand(self.deck.deal_card())
            self.computer.add_card_to_hand(self.deck.deal_card())
        self.update_player_ui()

    def start_new_game(self):
        self.play_game()

    def end_game(self, result, show_computer_cards=False):
        self.hit_button.config(state=tk.DISABLED)
        self.stand_button.config(state=tk.DISABLED)
        if result == "Player wins!":
            self.player_score_label.config(text=result, fg="green")
        else:
            self.player_score_label.config(text=result, fg="red")
        if show_computer_cards:
            self.update_computer_ui()

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank} of {self.suit} ({self.get_value()} points)"

    def get_value(self):
        card_values = {"Two": 2, "Three": 3, "Four": 4, "Five": 5, "Six": 6, "Seven": 7, "Eight": 8, "Nine": 9, "Ten": 10, "Jack": 10, "Queen": 10, "King": 10, "Ace": 11}
        return card_values[self.rank]

class Deck:
    def __init__(self):
        self.suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        self.ranks = ["Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King", "Ace"]
        self.cards = [Card(suit, rank) for suit in self.suits for rank in self.ranks]
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def add_card_to_hand(self, card):
        self.hand.append(card)

    def calculate_hand_value(self):
        value = 0
        num_aces = 0

        for card in self.hand:
            value += card.get_value()

        while value > 21 and num_aces > 0:
            value -= 10
            num_aces -= 1

        return value

if __name__ == "__main__":
    root = tk.Tk()
    game = BlackjackGame(root)
    root.mainloop()
