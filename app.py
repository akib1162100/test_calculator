import streamlit as st  # Import the Python UI framework with a short alias.
from calculator import divide, multiply  # Reuse the backend functions.

st.set_page_config(page_title="Python Calculator", layout="wide")  # Configure the browser page.
st.title("Python Calculator")  # Display the main heading.
st.caption("Change either number to calculate. Inputs are limited to ±1,000,000.")  # Explain the controls.

st.subheader("Multiplication")  # Label the first operation.
left, middle, right = st.columns(3)  # Create one row with two inputs and a result.
a = left.number_input("First factor", -1e6, 1e6, 6.0, key="multiply_a")  # Read the first float; default 6.
b = middle.number_input("Second factor", -1e6, 1e6, 4.0, key="multiply_b")  # Read the second float; default 4.
right.metric("Product", f"{multiply(a, b):g}")  # Call the backend and display its result.

st.subheader("Division")  # Label the second operation.
left, middle, right = st.columns(3)  # Start a separate row beneath multiplication.
a = left.number_input("Numerator", -1e6, 1e6, 12.0, key="divide_a")  # Read the number to divide.
b = middle.number_input("Denominator", -1e6, 1e6, 3.0, key="divide_b")  # Read the divisor, including zero.
try:  # Attempt the calculation, which can reject zero.
    right.metric("Quotient", f"{divide(a, b):g}")  # Display a valid result in the third column.
except ValueError as error:  # Catch the backend's expected validation error.
    right.error(str(error))  # Show a readable message instead of a crash.
