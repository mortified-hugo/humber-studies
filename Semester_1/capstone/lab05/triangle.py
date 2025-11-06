from GeometricObject import GeometricObject


class Triangle(GeometricObject):
    __side1: float = 0.0
    __side2: float = 0.0
    __side3: float = 0.0

    __valid = False

    def __init__(self, color: str = 'green', filled: bool = True,
                 side1: float = 3.0, side2: float = 4.0, side3: float = 5.0):
        super().__init__(color, filled)

        self.__side1 = side1
        self.__side2 = side2
        self.__side3 = side3

        self.__valid = self.isValid()

    # Side 1
    def get_side1(self):
        return self.__side1

    def set_side1(self, side1: float):
        self.__side1 = side1

    # Side 2
    def get_side2(self):
        return self.__side2

    def set_side2(self, side2: float):
        self.__side2 = side2

    # Side 3
    def get_side3(self):
        return self.__side3

    def set_side3(self, side3: float):
        self.__side3 = side3

    def isValid(self):
        # A triangle is valid if the sum of any two sides is greater than the third side
        return (self.__side1 + self.__side2 > self.__side3 and
                self.__side1 + self.__side3 > self.__side2 and
                self.__side2 + self.__side3 > self.__side1)

    # Perimeter and Area
    def getPerimiter(self):
        if self.__valid:
            return self.__side1 + self.__side2 + self.__side3
        return None

    def getArea(self):
        if self.__valid:
            s = self.getPerimiter() / 2
            area = (s * (s - self.__side1) * (s - self.__side2) * (s - self.__side3)) ** 0.5
            return area
        return None

    def __str__(self):
        if self.__valid:
            return f'Triangle: side1 = {self.__side1:.1f}, side2 = {self.__side2:.1f}, and side3 = {self.__side3:.1f}'
        else:
            return (f'Invalid Triangle: side1 = {self.__side1:.1f}, side2 = {self.__side2:.1f}, '
                    f'and side3 = {self.__side3:.1f}')


print("Let's build a triangle!\n")

side1, side2, side3 = eval(input("Triangle sides: "))
color = str(input("Triangle color: "))
filled = bool(int(input("Is this Triangle filled? 0 for no, 1 for yes: ")))

triangle = Triangle(color, filled, side1, side2, side3)

if triangle.isValid():
    print("\nYour Triangle:")
    print(f"Area: {triangle.getArea():.2f}")
    print(f"Perimeter: {triangle.getPerimiter():.2f}")
    print(f"Color: {triangle.getColor()}")
    print(f"Is filled: {triangle.isFilled()}")
else:
    print("\nThe Triangle you entered is invalid!")







