import numpy.random as rd


class Craps:
    die1: int = 0
    die2: int = 0
    point: int = 0

    def roll_dice(self) -> int:
        self.die1 = rd.randint(1, 7)
        self.die2 = rd.randint(1, 7)
        result = self.die1 + self.die2
        self.print_dice(result)
        return result

    def print_dice(self, result: int):
        print(f"You rolled {self.die1} + {self.die2} = {result}!")

    def play_round(self):
        first_roll = self.roll_dice()

        if first_roll in (7, 11):
            print("")
            print("You win!")
        elif first_roll in (2, 3, 12):
            print("You lose!")
        else:
            self.point = first_roll
            print(f"The point is {self.point}!")
            self.continue_round()

    def continue_round(self):
        while True:
            roll = self.roll_dice()

            if roll == self.point:
                print("You win!")
                return
            elif roll == 7:
                print("You lose!")
                return


Craps().play_round()
