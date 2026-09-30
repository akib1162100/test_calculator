# Instructor answer key

**Beginner zero-division lesson:** the current starter has two active ordinary tests. Uncomment `test_divide_by_zero` first: it expects `ValueError`, but unguarded division raises `ZeroDivisionError`, so the runner reports an error. Restore the two commented guard lines in `calculator.py` to make all three tests pass. The test must verify the intended behavior, rather than be changed to accept the accidental exception. Uncomment the remaining preserved tests and `AppTest` import before using the five-test/power exercise answers below.

Keep this guide separate when handing out the unsolved lab. The starter intentionally remains a two-operation app; the snippets below are the complete changes needed for the exercise. Each runnable solution block is identified by its target file. Apply additions to the stated class/file, not as a second independent application.

## T1–T2 — Trace answers

**T1:** `divide(12, 0)` raises `ValueError`; its `return a / b` line never executes. The UI catches the error and displays the message. Catching only in the UI without a backend guard would leave other callers with different error behavior.

**T2:** `multiply` receives `7` as its first argument. Streamlit reruns the script; distinct widget keys preserve the independent multiplication and division inputs. Reusing local variable names later does not retroactively change an already computed result.

## P0–P1 — Baseline and contract

The baseline has five test methods and both original operations work. The feature branch is `feature/power`. P1 expected outputs in order: `8`, `-8`, `4`, `1`, `0.25`, `0`, `1`, and `ValueError("Zero cannot have a negative exponent.")`.

A negative exponent is a reciprocal: `2 ** -2` is `1 / (2 ** 2)`. Zero has no reciprocal. The explicit `0 ** 0` convention makes the implementation and tests agree on an otherwise context-dependent mathematical case.

## P2 — Backend solution

Append to `calculator.py`:

```python
def power(base: float, exponent: int) -> float:  # Define the new numeric operation.
    if base == 0 and exponent < 0:  # Check the case that would require dividing by zero.
        raise ValueError("Zero cannot have a negative exponent.")  # Use the agreed error contract.
    return base ** exponent  # Use Python's built-in exponentiation operator.
```

The compound condition requires both comparisons to be true. `**` already handles positive, negative, and zero exponents. A loop or a new math package adds no value here. `^` is a common incorrect answer. Checking `base == 0` alone incorrectly rejects valid cases such as `0 ** 4`.

## P3 — Interface solution

Replace the existing backend import in `app.py` with:

```python
from calculator import divide, multiply, power  # Make all three backend functions available.
```

Replace the existing caption with:

```python
st.caption("Change a number to calculate. Multiply/divide: ±1,000,000. Power: base ±100, integer exponent ±10.")  # Describe each input domain.
```

Append at the left margin of `app.py`:

```python
st.subheader("Power")  # Label the third operation.
left, middle, right = st.columns(3)  # Add a row with two inputs and one result.
base = left.number_input("Base", -100.0, 100.0, 2.0, key="power_base")  # Read a bounded decimal base.
exponent = middle.number_input("Exponent", -10, 10, 3, step=1, key="power_exponent")  # Read a bounded integer.
try:  # Attempt the operation that can reject zero with a negative exponent.
    right.metric("Power result", f"{power(base, exponent):g}")  # Display the computed result.
except ValueError as error:  # Catch the backend's expected input error.
    right.error(str(error))  # Render the message beside the inputs.
```

Unique keys are essential. An integer exponent avoids complex outputs for negative bases raised to fractional powers. Bounds keep the demonstration's inputs understandable; they are not a promise of exact arithmetic for every float. Three short explicit rows are reasonable for this lesson; a generic operation registry would make the first extension harder to trace.

## P4 — Backend tests

Update the existing import in `test_calculator.py`:

```python
from calculator import divide, multiply, power  # Include the new function in tests.
```

Insert these methods inside `CalculatorTests`, before `InterfaceTests`:

```python
    def test_power_values(self):  # Check the valid cases from the written contract.
        cases = [(2, 3, 8), (-2, 3, -8), (-2, 2, 4), (5, 0, 1), (2, -2, 0.25), (0, 4, 0), (0, 0, 1)]  # Independent answers.
        for base, exponent, expected in cases:  # Run the same assertion for each input pair.
            with self.subTest(base=base, exponent=exponent):  # Label failing examples clearly.
                self.assertAlmostEqual(power(base, exponent), expected)  # Compare numeric output with the answer.

    def test_power_zero_negative(self):  # Check the invalid combination separately.
        with self.assertRaisesRegex(ValueError, "Zero cannot have a negative exponent"):
            power(0, -1)  # This call must raise the specified type and message.
```

The `with` line is an assertion context: the indented call must raise the named exception containing the regular-expression text. Seven test methods should now be discovered. P3 includes updating the baseline metric expectation (shown below under P5); if a student missed it, the old two-metric assertion will fail after adding the UI. This is an expected output change, not a backend bug.

## P5 — Interface tests

Replace the original metric-list assertion in `test_rows_and_changed_inputs`:

```python
        self.assertEqual([m.value for m in app.metric], ["24", "4", "8"])  # Include the new default power output.
```

Insert these methods inside `InterfaceTests`, before the final `if __name__ ...` block:

```python
    def test_power_input(self):  # Verify that both new widgets reach the backend.
        app = AppTest.from_file("app.py").run()  # Start a fresh simulated app session.
        app.number_input(key="power_base").set_value(3.0)  # Set the base without running yet.
        app.number_input(key="power_exponent").set_value(4).run()  # Set the exponent and apply both changes.
        self.assertFalse(app.exception)  # Reject an unhandled runtime error.
        self.assertEqual(app.metric[2].value, "81")  # Check the third row's displayed output.

    def test_power_error_and_recovery(self):  # Exercise invalid input followed by a correction.
        app = AppTest.from_file("app.py").run()  # Start an independent session.
        app.number_input(key="power_base").set_value(0.0)  # Prepare the invalid zero base.
        app.number_input(key="power_exponent").set_value(-1).run()  # Request its reciprocal.
        self.assertFalse(app.exception)  # The UI must handle the error.
        self.assertEqual(app.error[0].value, "Zero cannot have a negative exponent.")  # Check the message.
        app.number_input(key="power_exponent").set_value(2).run()  # Correct the input.
        self.assertFalse(app.error)  # Ensure the obsolete error disappears.
        self.assertEqual(app.metric[2].value, "0")  # Check the valid replacement result.
```

Expected final command and result, run from the project root:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s . -p "test_*.py" -v
```

Expect **9 tests, OK**. Tests must remain inside their classes. A method pasted outside a `TestCase` class may not be discovered, producing a misleading green run with fewer tests.

## P6 — Workflow change

Replace the student-task marker in `.github/workflows/deploy.yml` with:

```yaml
      - name: Run tests # Add the behavioral test gate to the existing ordered job.
        run: python -m unittest discover -s . -p "test_*.py" -v # Fail this job if any discovered test fails.
```

Retain all other workflow sections. The job has install, syntax check, tests, and the conditional hook step in that order. GitHub normally skips later steps after a failure; a separate `needs` relationship is unnecessary because this is one job. If students instead split testing and deployment into separate jobs, the deployment job must explicitly depend on the testing job with `needs`, as well as preserving its event restriction.

## P7 — Evidence and debugging

With `return base * exponent`, syntax checking succeeds but several power assertions fail. For example, `power(2, 3)` returns `6` instead of `8`, and the interface produces `12` instead of `81` for `3, 4`. Restore `**`, rerun locally, and push the correction. Require failure evidence followed by a passing run, rather than only a screenshot of a green icon.

On the pull request, the hook is skipped even when tests pass. On the merged `main` revision, tests pass and the hook is requested. Check Render's status and revision to finish live verification. Never ask students to submit the hook URL. A green workflow with fewer than nine tests is incomplete evidence for this particular solution.

The optional disposable-deployment experiment is the direct demonstration that a failing test on `main` blocks the hook. Branch protection/rulesets and the workflow serve different purposes: one controls merging, the other controls whether deployment is requested after checks.

## P8 — Model explanations

1. A backend function defines computation but does not render controls. `app.py` must import and call it using widget values.
2. Backend tests can pass even when the UI calls the wrong function, swaps inputs, or never forwards a changed value. An interface test exercises that connection.
3. A failed test must stop the pipeline before an externally visible deployment is requested. Testing afterward detects the error too late for this gate.
4. The hook starts asynchronous work. Render can later fail dependency installation, startup, or health checks after Actions has finished.
5. Passing the commit SHA prevents the hook from selecting a newer, potentially unchecked revision that arrived after this run started. It does not itself solve every overlapping-deployment ordering problem.
6. A mobile client would need a defined HTTP API with input parsing, validation, and response/error formats. The arithmetic functions and their unit tests could remain; the Streamlit UI and interface tests would no longer be the only client path.

## Assessment notes

Use the 100-point rubric in the student lab. Accept equivalent clear implementations that satisfy the contract and use meaningful tests. Award partial credit for correct arithmetic with incomplete UI wiring, but not full testing credit for assertions that repeat the implementation. A student who cannot host should document that limitation accurately and provide the local test results plus a reviewed workflow; do not record a deployment as verified without evidence.

The project connects a concrete need (browser input) to UI composition, calculation functions, exception handling, tests, and a deployment gate. Ask students to name which file and test would change for square root before asking them to implement it. This checks whether they understand the separation rather than merely copying the power row.
