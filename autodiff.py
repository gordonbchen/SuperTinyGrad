from __future__ import annotations


class Var:
    """A differentiable variable."""

    def __init__(
        self,
        value: float,
        children: tuple[Var, Var] | None = None,
        derivs: tuple[float, float] | None = None,
    ) -> None:
        """Initialize variable."""
        self.value = value

        # Allow constants to not have children.
        self.children = children if children else tuple()
        self.derivs = derivs if derivs else tuple()

        # Accumulated when backward called.
        self.deriv = 0.0
        
    def backward(self, deriv: float = 1.0) -> None:
        """Backpropagate derivative to children."""
        self.deriv += deriv

        for (child, child_deriv) in zip(self.children, self.derivs):
            child.backward(deriv * child_deriv)

    def _force_var(x: Var | float) -> Var:
        """Force a value or var to be a var."""
        return x if type(x) == Var else Var(x)

    def __add__(self, other: Var | float) -> Var:
        other = Var._force_var(other)

        # Create output variable.
        value = self.value + other.value
        children = (self, other)
        derivs = (1.0, 1.0)
        return Var(value, children, derivs)
    
    def __mul__(self, other: Var | float) -> Var:
        other = Var._force_var(other)

        # Create output variable.
        value = self.value * other.value
        children = (self, other)
        derivs = (other.value, self.value)
        return Var(value, children, derivs)
    

if __name__ == "__main__":
    x = Var(5.0)
    y = x + 2
    z = (y * x) + x

    z.backward()
    print(z.deriv)
    print(y.deriv)
    print(x.deriv)
