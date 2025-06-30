import tkinter as tk
import random

class RockPaperScissorsGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Rock, Paper, Scissors")
        self.root.geometry("500x400")  # Set fixed window size
        self.root.resizable(False, False)  # Prevent resizing

        self.user_score = 0
        self.computer_score = 0

        # Title
        self.title_label = tk.Label(root, text="Rock, Paper, Scissors", font=("Arial", 24, "bold"))
        self.title_label.pack(pady=20)

        # Score display
        self.score_label = tk.Label(root, text=self.get_score_text(), font=("Arial", 16))
        self.score_label.pack()

        # Choices frame
        self.choice_frame = tk.Frame(root)
        self.choice_frame.pack(pady=20)

        # Choice buttons (larger size)
        button_font = ("Arial", 14)
        self.rock_button = tk.Button(self.choice_frame, text="Rock", width=12, height=2,font=button_font, command=lambda: self.play("rock"))
        self.paper_button = tk.Button(self.choice_frame, text="Paper", width=12, height=2,font=button_font, command=lambda: self.play("paper"))
        self.scissors_button = tk.Button(self.choice_frame, text="Scissors", width=12, height=2,font=button_font, command=lambda: self.play("scissors"))

        self.rock_button.grid(row=0, column=0, padx=10)
        self.paper_button.grid(row=0, column=1, padx=10)
        self.scissors_button.grid(row=0, column=2, padx=10)

        # Result display
        self.result_label = tk.Label(root, text="", font=("Arial", 16), fg="blue", wraplength=480, justify="center")
        self.result_label.pack(pady=20)

        # Reset button
        self.reset_button = tk.Button(root, text="Reset Game", font=("Arial", 14), width=16, height=2,command=self.reset_game)
        self.reset_button.pack(pady=10)

    def get_score_text(self):
        return f"Score - You: {self.user_score} | Computer: {self.computer_score}"

    def play(self, user_choice):
        computer_choice = random.choice(["rock", "paper", "scissors"])
        result = self.determine_winner(user_choice, computer_choice)

        if result == "user":
            self.user_score += 1
            outcome = "You win!"
        elif result == "computer":
            self.computer_score += 1
            outcome = "Computer wins!"
        else:
            outcome = "It's a tie!"

        self.score_label.config(text=self.get_score_text())
        self.result_label.config(
            text=f"You chose {user_choice}, computer chose {computer_choice}. {outcome}")

    def determine_winner(self, user, computer):
        if user == computer:
            return "tie"
        elif (user == "rock" and computer == "scissors") or \
             (user == "scissors" and computer == "paper") or \
             (user == "paper" and computer == "rock"):
            return "user"
        else:
            return "computer"

    def reset_game(self):
        self.user_score = 0
        self.computer_score = 0
        self.score_label.config(text=self.get_score_text())
        self.result_label.config(text="")

if __name__ == "__main__":
    root = tk.Tk()
    game = RockPaperScissorsGame(root)
    root.mainloop()