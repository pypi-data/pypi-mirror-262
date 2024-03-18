class Calculator:
    x = 0.0

    def add(self, y):
        self.x = round(self.x + y, 2)
        return self.x

    def subtract(self, y):
        self.x = round(self.x - y, 2)
        return self.x

    def multiply(self, y):
        self.x = round(self.x * y, 2)
        return self.x

    def divide(self, y):
        if y != 0.0:
            self.x = round(self.x / y, 2)
            return self.x
        else:
            return "Division by 0 not possible"

    def root(self, y):
        if y > 0:
            self.x = round(self.x ** (1 / y), 2)
            return self.x
        elif y < 0:
            return "Answer is imaginary number"
        else:
            return "Invalid"

    def reset(self):
        self.x = Calculator.x
        return self.x
