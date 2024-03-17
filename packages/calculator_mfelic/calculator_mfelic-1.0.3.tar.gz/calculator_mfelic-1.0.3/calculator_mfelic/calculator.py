import cmath

class Calculator:
    """A simple calculator class."""

    total: float = 0.0

    def __init__(self) -> None:
        """Initialize the calculator."""
        self.reset()  # Reset total to 0.0 when initialized

    def add(self, n: float) -> float:
        """Add a number to the total.

        Args:
            n (float): The number to add.

        Returns:
            float: The updated total.
        """
        self.total += n
        return self.total
    
    def sub(self, n: float) -> float:
        """Subtract a number from the total.

        Args:
            n (float): The number to subtract.

        Returns:
            float: The updated total.
        """
        self.total -= n
        return self.total
    
    def mult(self, n: float) -> float:
        """Multiply the total by a number.

        Args:
            n (float): The number to multiply by.

        Returns:
            float: The updated total.
        """
        self.total *= n
        return self.total
    
    def div(self, n: float) -> float:
        """Divide the total by a number.

        Args:
            n (float): The number to divide by.

        Returns:
            float: The updated total.
        """
        if n == 0:
            raise ZeroDivisionError("Division by zero is not allowed")
        self.total /= n
        return self.total
    
    def nroot(self, n: float) -> float:
        """Calculate the nth root of the total.

        Args:
            n (float): The index of the root.

        Returns:
            complex: The result of taking the nth root of the total.
        """
        if self.total < 0:
            raise ValueError("Cannot compute nth root of a negative number")
        if n <= 0:
            raise ValueError("Index for nth root must be a positive number")
        try:
            self.total = self.total ** (1.0 / n)
        except OverflowError:
            raise OverflowError("Result too large to compute")
        return self.total
    
    def reset(self) -> float:
        """Reset the total to 0.

        Returns:
            float: The updated total (0.0).
        """
        self.total = 0.0
        return self.total
