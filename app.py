import streamlit as st  # Import the Python UI framework with a short alias.
from calculator import divide, multiply,power   # Reuse the backend functions.(add power)

st.set_page_config(page_title="Python Calculator", layout="wide")  # Configure the browser page.
st.title("Python Calculator")  # Display the main heading.
st.caption(
    "Change a number to calculate. "
    "Multiply/divide inputs: ±1,000,000. "
    "Power: base ±100, integer exponent ±10."
)  # Explain the controls.  # Explain the controls.

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



st.subheader("Power")  # Label the new operation.
left, middle, right = st.columns(3)  # Create two input columns and one output column.

base = left.number_input(
    "Base",  # Visible label for the first input.
    min_value=-100.0,  # Smallest allowed base.
    max_value=100.0,  # Largest allowed base.
    value=2.0,  # Initial base; float arguments allow decimal values.
    key="power_base",  # Unique identifier for this widget.
)

exponent = middle.number_input(
    "Exponent",  # Visible label for the second input.
    min_value=-10,  # Smallest allowed exponent.
    max_value=10,  # Largest allowed exponent.
    value=3,  # Initial exponent; integer arguments select integer input.
    step=1,  # Increase or decrease by one.
    key="power_exponent",  # Distinguish this widget from every other input.
)

try:  # Attempt the operation that can reject invalid inputs.
    result = power(base, exponent)  # Send the widget values to the backend.
    right.metric("Power result", f"{result:g}")  # Display the result in the third column.
except ValueError as error:  # Handle the backend's expected validation error.
    right.error(str(error))  # Render its message beside the inputs.