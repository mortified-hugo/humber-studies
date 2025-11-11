# 1
"""
In a section in the notebook, implement a program that reads an unspecified number
of integers and finds the ones that have the most occurrences. For example, if you
enter 2 3 40 3 5 4 –3 3 3 2 0, the number 3 occurs most often. Enter all numbers in
one line. If not one but several numbers have the most occurrences, all of them
should be reported.
"""


class NumberOccurrences:
    __list_of_numbers = []
    __count_dict = {}
    __number_with_max_occurrences = []

    response = "The number with the most occurrences is "

    def __init__(self, new_list: list[str]):
        self.__list_of_numbers = new_list
        for number in self.__list_of_numbers:
            if self.__count_dict.get(number) is None:
                self.__count_dict[number] = 1
            else:
                self.__count_dict[number] += 1

        max_occurrences = max(self.__count_dict.values())

        self.__number_with_max_occurrences = [key for key, value
                                              in self.__count_dict.items() if value == max_occurrences]

        self.generate_response()

    def generate_response(self):
        plural = "The numbers with the most occurrences are "  # Grammar
        if len(self.__number_with_max_occurrences) == 1:
            # The Number is x
            self.response += str(self.__number_with_max_occurrences[0])

        else:
            last_number = f" and {self.__number_with_max_occurrences.pop(-1)}"
            answers = ", ".join(self.__number_with_max_occurrences)
            # The numbers are x, y and z
            self.response = plural + answers + last_number


list_of_numbers = input("Enter the numbers: ").split(" ")

count_numbers = NumberOccurrences(list_of_numbers)
print(count_numbers.response)





