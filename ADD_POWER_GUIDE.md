# Add power, test all functions, and deploy

This guide starts from your current beginner calculator: multiplication and division work, two simple tests are active, and the zero-division guard and its test are commented out. Follow the changes in order. You will finish with three operations and five active test methods.

**Line references were checked against your local files on 2026-09-30.** They refer to the files **before any edits in this guide**. Adding lines moves later line numbers, so always match the quoted code as well. Your GitHub copy may have different line numbers. Do not copy line numbers into source code.

## Navigation

- [Change map: every edit and its location](#change-map)
- [1. Enable the zero-division test and observe the error](#step-1)
- [2. Fix division by restoring the guard](#step-2)
- [3. Add the power backend function](#step-3)
- [4. Add the power interface row](#step-4)
- [5. Add power tests](#step-5)
- [6. Run tests and try the app](#step-6)
- [7. Add tests to GitHub Actions](#step-7)
- [8. Commit, push, and verify deployment](#step-8)
- [Troubleshooting](#troubleshooting)
- [References and verification](#references)

<a id="change-map"></a>
## Change map

| Step | File and original lines | Exact action |
|---|---|---|
| 1 | `test_calculator.py`, lines 19–21 | Uncomment the existing zero-division test. |
| 2 | `calculator.py`, lines 7–8 | Uncomment the existing zero-division guard. |
| 3 | `calculator.py`, after line 9 | Append `power` after the division function, at the left margin. |
| 4A | `app.py`, line 2 | Replace the calculator import to include `power`. |
| 4B | `app.py`, line 6 | Replace the caption to describe the new input ranges. |
| 4C | `app.py`, after original line 21 | Append the third UI row, outside the division error handler. |
| 5A | `test_calculator.py`, line 3 | Replace the calculator import to include `power`. |
| 5B | `test_calculator.py`, after original line 21 | Insert two methods inside `CalculatorTests`, before the final `if __name__` block. |
| 7 | `.github/workflows/deploy.yml`, line 26 | Replace the student-task comment with the test step. |

Only edit the four files in this table. Keep your other comments and examples. You do not need a new package, server, repository, or Render service.

<a id="step-1"></a>
## 1. Enable the zero-division test and observe the error

**Location:** [test_calculator.py, original line 19](D:/RA_docs/MISC/python-calculator-classroom/test_calculator.py:19).

Find the commented block beginning with:

```text
    # def test_divide_by_zero(self):
```

**Replace only its three code lines** with this active version. Preserve the indentation: four spaces before `def`, eight before `with`, and twelve before `divide`.

```python
    def test_divide_by_zero(self):
        with self.assertRaisesRegex(ValueError, "Cannot divide by zero"):
            divide(5, 0)
```

| Line | Explanation |
|---|---|
| `def test_divide_by_zero(self):` | Defines a test method that unittest discovers by its `test_` prefix. |
| `with self.assertRaisesRegex(...)` | Requires the call inside this block to raise `ValueError` with the specified message text. |
| `divide(5, 0)` | Exercises the zero-denominator case that the ordinary division test misses. |

Do **not** restore the backend guard yet. In PowerShell, from the project folder, run:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s . -p "test_*.py" -v
```

Expected result: **3 tests run; 1 error**. The traceback contains `ZeroDivisionError: division by zero`.

Why? The existing implementation reaches `a / b`. Python raises `ZeroDivisionError`, but our application contract requires the deliberate `ValueError` and readable message. The runner reports this as an **error**, which still makes the overall run unsuccessful and returns a nonzero exit code. The test exposes missing behavior; changing the test to accept the accidental exception would not implement the intended contract.

[Back to navigation](#navigation)

<a id="step-2"></a>
## 2. Fix division by restoring the guard

**Location:** [calculator.py, original line 7](D:/RA_docs/MISC/python-calculator-classroom/calculator.py:7).

Find the two commented lines starting with `# if b == 0:` and `#     raise ValueError(...)`. **Uncomment those lines only**, leaving the return statement beneath them unchanged:

```python
    if b == 0:
        raise ValueError("Cannot divide by zero.")
```

These lines belong **inside `divide`**, directly before `return a / b`. The `if` has four leading spaces; `raise` has eight. The first line identifies an invalid denominator; the second stops the calculation with the error type and message expected by the test.

Run the same test command again. Expected result: **3 tests, OK**. You have demonstrated the sequence: passing ordinary examples → new edge-case test errors → fix → all tests pass.

[Back to navigation](#navigation)

<a id="step-3"></a>
## 3. Add the power backend function

**Location:** [calculator.py, original line 9](D:/RA_docs/MISC/python-calculator-classroom/calculator.py:9).

Find the last line of `divide`:

```text
    return a / b  # Return a floating-point quotient for a valid denominator.
```

**Insert two blank lines after it, then paste this function.** Its `def` must start at the left margin, not inside `divide`:

```python
def power(base: float, exponent: int) -> float:
    if base == 0 and exponent < 0:
        raise ValueError("Zero cannot have a negative exponent.")
    return base ** exponent
```

| Line | Explanation |
|---|---|
| `def power(base: float, exponent: int) -> float:` | Names the function and documents its numeric inputs/result. Type hints do not enforce values at runtime. |
| `if base == 0 and exponent < 0:` | Detects the case that would require taking a reciprocal of zero. Both comparisons must be true. |
| `raise ValueError(...)` | Reports that invalid input using the same exception-handling pattern as division. |
| `return base ** exponent` | Uses Python's exponentiation operator. `^` is not the power operator. |

The interface will supply an integer exponent. Positive, zero, and negative exponents are supported. This lesson follows Python's convention that `0 ** 0` is `1`.

[Back to navigation](#navigation)

<a id="step-4"></a>
## 4. Add the power interface row

### 4A. Replace the import

**Location:** [app.py, original line 2](D:/RA_docs/MISC/python-calculator-classroom/app.py:2).

Find `from calculator import divide, multiply`. **Replace that line**, rather than adding a duplicate import:

```python
from calculator import divide, multiply, power
```

This makes the new backend function available to the interface.

### 4B. Replace the caption

**Location:** [app.py, original line 6](D:/RA_docs/MISC/python-calculator-classroom/app.py:6).

Find the existing `st.caption(...)` line. **Replace the entire line** with:

```python
st.caption(
    "Change a number to calculate. "
    "Multiply/divide inputs: ±1,000,000. "
    "Power: base ±100, integer exponent ±10."
)
```

`st.caption` renders explanatory text. Python joins the adjacent string literals inside the parentheses into one string. The closing parenthesis ends the call.

### 4C. Append the new row

**Location:** [app.py, original line 21](D:/RA_docs/MISC/python-calculator-classroom/app.py:21).

Find the last line of the existing division error handler:

```text
    right.error(str(error))  # Show a readable message instead of a crash.
```

**Insert a blank line after it, then paste this block.** Start `st.subheader` at the left margin; otherwise the power controls might appear only when division fails.

```python
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
```

The closing `)` lines finish each widget call. `f"{result:g}"` formats a number without unnecessary trailing zeros; general formatting may round the displayed value. Streamlit updates the output when an input change is committed.

[Back to navigation](#navigation)

<a id="step-5"></a>
## 5. Add power tests

### 5A. Replace the test import

**Location:** [test_calculator.py, original line 3](D:/RA_docs/MISC/python-calculator-classroom/test_calculator.py:3).

Replace `from calculator import divide, multiply` with:

```python
from calculator import divide, multiply, power
```

Keep `import unittest` and the original multiplication/division tests.

### 5B. Insert the two new methods

**Location:** [test_calculator.py, original line 21](D:/RA_docs/MISC/python-calculator-classroom/test_calculator.py:21).

Find `divide(5, 0)` at the end of the zero-division test you enabled in step 1. **Insert a blank line after it and add these methods.** Both `def` lines have four leading spaces so they remain inside `CalculatorTests`.

Paste them **before** the existing, left-aligned `if __name__ == "__main__":` block, which originally starts at line 25. Do not put them inside that block or inside another test method.

```python
    def test_power(self):
        self.assertEqual(power(2, 3), 8)  # Positive exponent.
        self.assertEqual(power(-2, 3), -8)  # Negative base with an odd exponent.
        self.assertEqual(power(5, 0), 1)  # Zero exponent.
        self.assertEqual(power(2, -2), 0.25)  # Negative exponent gives a reciprocal.
        self.assertEqual(power(0, 4), 0)  # Zero base with a positive exponent.
        self.assertEqual(power(0, 0), 1)  # The convention selected for this lesson.

    def test_power_zero_negative(self):
        with self.assertRaisesRegex(
            ValueError, "Zero cannot have a negative exponent"
        ):
            power(0, -1)
```

Each `assertEqual(actual, expected)` checks a known answer. The second method requires the invalid call to raise `ValueError` with the agreed message. Its multiline `with` statement ends at `):`; the indented `power(0, -1)` is the call being checked.

Keep additional examples commented until you want to teach them. This guide uses ordinary unit tests and does not require interface tests. If your copy still contains commented interface tests, leave them commented.

[Back to navigation](#navigation)

<a id="step-6"></a>
## 6. Run tests and try the app

Run this from the project folder:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s . -p "test_*.py" -v
```

The environment's interpreter runs `unittest`; `discover` finds tests; `-s .` starts in the current directory; `-p` selects test filenames; `-v` displays individual test names. On macOS/Linux, substitute `.venv/bin/python` for the Windows interpreter path.

Expected active methods:

| Method | Purpose |
|---|---|
| `test_multiply` | Ordinary multiplication |
| `test_divide` | Ordinary division |
| `test_divide_by_zero` | Invalid denominator |
| `test_power` | Valid power examples |
| `test_power_zero_negative` | Invalid zero/negative combination |

Expected summary: **5 tests, OK**. Six assertions in `test_power` still count as one method.

Start the app, or refresh it if already running:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Open [the local app](http://localhost:8501) and check:

| Operation | Inputs | Expected display |
|---|---|---|
| Multiply | 6 and 4 | 24 |
| Divide | 12 and 3 | 4 |
| Divide | 12 and 0 | Cannot divide by zero. |
| Power | 2 and 3 | 8 |
| Power | 2 and -2 | 0.25 |
| Power | 0 and -1 | Zero cannot have a negative exponent. |
| Power, after correcting the previous input | 0 and 2 | 0; the error disappears |

[Back to navigation](#navigation)

<a id="step-7"></a>
## 7. Add tests to GitHub Actions

**Location:** [deploy.yml, original line 26](D:/RA_docs/MISC/python-calculator-classroom/.github/workflows/deploy.yml:26).

Find this exact marker:

```text
      # STUDENT TASK: insert the Run tests step here, before the deployment step.
```

**Replace that comment with these two lines.** If you already added an equivalent test step, keep the existing one and do not duplicate it.

```yaml
      - name: Run tests
        run: python -m unittest discover -s . -p "test_*.py" -v
```

The first line labels a step in the existing job. The second runs the same discovery command as the local check, using the Python interpreter configured on GitHub's runner. There are **six spaces before `- name`** and **eight spaces before `run`**. Match the adjacent steps and use spaces, not tabs.

This step must be **after** `Check Python syntax` and **before** `Request Render deployment`. A nonzero exit code stops later ordinary steps, so failing tests prevent the deployment request. Retain the existing deployment condition and secret mapping. Do not add `continue-on-error` or `if: always()` to bypass a failed test.

```text
Checkout → Set up Python → Install → Syntax check → Run tests → Request deployment
```

Keep Render Auto-Deploy Off so this workflow controls the deployment request. A pull request runs checks but does not deploy; a successful push to `main` reaches the deployment step.

[Back to navigation](#navigation)

<a id="step-8"></a>
## 8. Commit, push, and verify deployment

After local checks pass:

```powershell
git add calculator.py app.py test_calculator.py .github/workflows/deploy.yml
git commit -m "Add power calculation and automated tests"
git push
```

Line 1 stages the four edited files. Line 2 records the change. Line 3 uploads the current branch to its configured upstream. If you are using a new feature branch, use `git push -u origin YOUR_BRANCH_NAME` for its first push and open a pull request into `main`.

1. Open your repository on GitHub.
2. Navigate to **Actions → latest CI and deploy run → check-and-deploy**.
3. Expand **Run tests** and confirm five tests passed.
4. On a `main` push, confirm **Request Render deployment** succeeded. On a pull request, this step should be skipped; merge the passing change to trigger the `main` run.
5. Open **Render → your calculator service → Deploys**. Confirm the corresponding revision becomes Live.
6. Open the public application URL and repeat the manual examples from step 6.

The deployment hook requests asynchronous work. A successful Actions request is not proof that Render's build and startup have finished. No new secret is required for power: keep using the existing `RENDER_DEPLOY_HOOK_URL` repository secret.

[Back to navigation](#navigation)

<a id="troubleshooting"></a>
## Troubleshooting

| Symptom | What to check |
|---|---|
| Only two tests run | Uncomment `test_divide_by_zero` and put the two new methods inside `CalculatorTests`. |
| Zero-division test reports `ZeroDivisionError` | Restore the guard in `calculator.py`, step 2. |
| `NameError: power is not defined` | Update both imports: `app.py` and `test_calculator.py`. |
| Power row appears only during a division error | Start the new UI block at the left margin, outside `except`. |
| `IndentationError` | Functions at file scope use no leading spaces; class methods use four; method bodies use eight. |
| All tests pass but workflow does not deploy | A pull request is intentionally excluded. Deployment runs after a successful push/merge to `main`. |
| `Missing RENDER_DEPLOY_HOOK_URL secret` | GitHub repository → Settings → Secrets and variables → Actions → Secrets → add/update the repository secret. |
| Actions succeeds but public app is unchanged | Check Render's revision, deploy status, and build/runtime logs. |

<a id="references"></a>
## References and verification

The file citations in each step point to the actual local starter lines used to write this guide. They are location references, not claims that the changes have already been applied. Follow the quoted source anchors when working from a GitHub copy or after earlier edits shift the line numbers.

Official references used for the original project and applicable to this guide:

- [Python unittest](https://docs.python.org/3/library/unittest.html): test discovery and assertions.
- [Streamlit number inputs](https://docs.streamlit.io/develop/api-reference/widgets/st.number_input): widget arguments and numeric values.
- [Streamlit columns](https://docs.streamlit.io/develop/api-reference/layout/st.columns): arranging inputs and results.
- [GitHub Actions workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax): steps and conditions.
- [Render deploy hooks](https://render.com/docs/deploy-hooks): deployment requests and repository-secret setup.

This is an editing guide. Your application files remain unchanged by creating this document. Its Python snippets were extracted and applied to a temporary copy on 2026-09-30 using Python 3.10.11 and Streamlit 1.64.0. Verified: step 1 produces the expected error; step 2 passes three tests; the completed changes pass five tests. A separate AppTest check confirmed all three default results and power-error recovery. Navigation anchors and source-file links were checked. GitHub Actions, hosted Python 3.12, and Render deployment were not executed during this verification.

[Back to navigation](#navigation)
