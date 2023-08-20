class Var:
    """Differentiable variable."""

    def __init__(self, value, child=None):
        """Initialize variable value."""
        self.value = value
        self.child = child

        # Set at __op__() call.
        self.partial_deriv = 1

        # Set at calc_deriv() call.
        self.deriv = 0

    def calc_deriv(self, uphill_deriv=1):
        """Calculate derivatives."""
        self.deriv = uphill_deriv * self.partial_deriv

        if self.child:
            self.child.calc_deriv(self.deriv)

    def __add__(self, other):
        self.partial_deriv = 1
        return Var(self.value + other, child=self)

    def __sub__(self, other):
        return self.__add__(-1 * other)

    def __mul__(self, other):
        self.partial_deriv = other
        return Var(self.value * other, child=self)

    def __truediv__(self, other):
        return self.__mul__(1 / other)

    def __pow__(self, other):
        self.partial_deriv = other * (self.value ** (other - 1))
        return Var(self.value ** other, child=self)

    def __neg__(self):
        self.partial_deriv = -1
        return Var(-1 * self.value, child=self)


x = Var(2)
y = (x + 2) ** 3
z = -y / 2

z.calc_deriv()

print(f"dz/dy = {y.deriv}")
print(f"dz/dx = {x.deriv}")
