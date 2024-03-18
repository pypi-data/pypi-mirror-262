class Calculator:
    # Calculator's memory: initial value
    x = 0.0

    # Definition of a function that performs addition
    def add(self, y):
        self.x = round(self.x + y, 2)
        return self.x

    # Definition of a function that performs subtraction
    def subtract(self, y):
        self.x = round(self.x - y, 2)
        return self.x

    # Definition of a function that performs multiplication
    def multiply(self, y):
        self.x = round(self.x * y, 2)
        return self.x

    # Definition of a function that performs division
    # Restrictions: input cannot be 0 - invalid function
    def divide(self, y):
        if y != 0.0:
            self.x = round(self.x / y, 2)
            return self.x
        else:
            return "Division by 0 not possible"

    # Definition of a function that finds n-th root of a number
    # Restrictions: input cannot be 0 - invalid function; input cannot be less than 0 - answer is imaginary number
    def root(self, y):
        if y > 0:
            self.x = round(self.x ** (1 / y), 2)
            return self.x
        elif y < 0:
            return "Answer is imaginary number"
        elif y == 0:
            return "Invalid"

    # Definition of a function that sets calculator's memory to initial value
    def reset(self):
        self.x = Calculator.x
        return self.x
