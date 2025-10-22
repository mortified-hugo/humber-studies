import random


class Craps:
    def __init__(self):
        self.point = None

    @staticmethod
    def roll_dice():
        die1 = random.randint(1, 6)
        die2 = random.randint(1, 6)
        return die1 + die2

    def play_round(self):
        first_roll = self.roll_dice()
        print(f"First roll: {first_roll}")

        if first_roll in (7, 11):
            print("You win!")
            return "win"
        elif first_roll in (2, 3, 12):
            print("You lose!")
            return "lose"
        else:
            self.point = first_roll
            print(f"Point is set to: {self.point}")
            return self.continue_round()

    def continue_round(self):
        while True:
            roll = self.roll_dice()
            print(f"Rolled: {roll}")

            if roll == self.point:
                print("You hit your point! You win!")
                return "win"
            elif roll == 7:
                print("You rolled a 7! You lose!")
                return "lose"

Claps_game = Craps()
result = Claps_game.play_round()
