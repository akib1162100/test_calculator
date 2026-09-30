def multiply(a: float, b: float) -> float:  # Define the multiplication backend function.
    return a * b  # Return the product to the caller.


def divide(a: float, b: float) -> float:  # Define the division backend function.
    # Student exercise: enable the zero-division test, observe the error, then restore this guard.
    # if b == 0:  # Detect a denominator for which division is undefined.
    #     raise ValueError("Cannot divide by zero.")  # Report an expected input error.
    return a / b  # Return a floating-point quotient for a valid denominator.
