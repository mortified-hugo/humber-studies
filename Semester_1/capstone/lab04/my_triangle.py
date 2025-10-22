class MyTriangle:
    def __init__(self, side1, side2, side3):
        self.side1 = side1
        self.side2 = side2
        self.side3 = side3

        # Verify that this is a valid triangle
        if self.isValid():
            self.p = self.perimeter()
            self.a = self.area()

        else:
            print("Input is Invalid.")
            self.p = None
            self.a = None

    def isValid(self):
        # A triangle is valid if the sum of any two sides is greater than the third side
        return (self.side1 + self.side2 > self.side3 and
                self.side1 + self.side3 > self.side2 and
                self.side2 + self.side3 > self.side1)

    def perimeter(self):
        return self.side1 + self.side2 + self.side3

    def area(self):
        s = self.perimeter() / 2
        area = (s * (s - self.side1) * (s - self.side2) * (s - self.side3)) ** 0.5
        return round(area, 2)


triangle_sides = eval(input("Enter three sides: "))
triangle = MyTriangle(*triangle_sides)  # Unpack the tuple

if triangle.isValid():
    print(f"The area of the triangle is {triangle.a}")
