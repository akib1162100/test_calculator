# Student lab: add power and protect deployment with tests

**Before this extension:** complete the simple zero-division lesson at the top of the README. Restore the backend guard and uncomment the preserved additional tests and `AppTest` import. This extension assumes that restored five-test baseline; the initial beginner version has only two active tests.

Start from the working multiplication/division project and complete the steps in order. Keep the original two operations working. This lab adds a third operation to the same application and extends the existing workflow; it does not need a new server or a new deployment service.

**Prerequisites:** finish README sections 1–8, run the five baseline tests, and understand functions, `if`, imports, and exceptions. **Time:** 60–90 minutes. **Deliverables:** a feature branch and pull request containing the new function, third UI row, new tests, and updated workflow; screenshots or links showing failed and passing checks; and a short explanation of the live verification.

All exercise IDs below have matching answers in the separate instructor guide. Try each task before consulting that guide.

## P0 — Establish the baseline and branch (easy, 5 minutes)

1. Run the starter and verify both operations, including division by zero.
2. Run the five tests:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s . -p "test_*.py" -v
```

3. Create a branch for your changes:

```powershell
git switch -c feature/power
```

`switch` changes branches; `-c` creates the named branch first. A branch lets you propose and check a change before merging it into the deployed `main` branch. It is not a separate Python environment or a separately running application.

**Acceptance:** baseline tests pass and `git branch --show-current` reports `feature/power`.

## P1 — Define the behavior before implementing it (easy, 5 minutes)

Write down the contract for `power(base: float, exponent: int) -> float`:

- Return the base raised to an integer exponent.
- Support positive, zero, and negative exponents.
- A negative exponent means a reciprocal: `2` raised to `-2` is `0.25`.
- Reject a zero base with a negative exponent using `ValueError("Zero cannot have a negative exponent.")`.
- For this exercise, use Python's convention that `0 ** 0` is `1`; this is an explicit application decision, not a claim that all mathematical contexts use that convention.
- The UI accepts a base from -100 to 100 and an integer exponent from -10 to 10. Fractional exponents and complex outputs are outside this lesson.

Complete the expected-result column before coding:

| Base | Exponent | Expected result |
|---:|---:|---|
| 2 | 3 | ? |
| -2 | 3 | ? |
| -2 | 2 | ? |
| 5 | 0 | ? |
| 2 | -2 | ? |
| 0 | 4 | ? |
| 0 | 0 | ? |
| 0 | -1 | ? |

**Hint:** an exponent counts repeated multiplication only for positive integers. For zero and negative exponents, use the stated rules. **Acceptance:** predictions match the contract, especially the two different zero cases.

## P2 — Add the backend function (easy, 10 minutes)

1. Open `calculator.py`.
2. Add `power` beneath `divide` with the signature from P1.
3. Check the invalid zero/negative combination before evaluating the expression.
4. Raise the specified `ValueError` in that case.
5. Return the power result otherwise.

Use Python's `**` operator. Do not use `^`: in Python that means bitwise exclusive OR, not exponentiation. Do not write a multiplication loop; it handles negative exponents poorly and repeats a language feature.

Type hints describe your intended callers; they do not enforce integer-only input. This project obtains the exponent from an integer widget. If you later expose this function through a public API, enforce the numeric contract at that new input boundary.

Quick check from the terminal:

```powershell
.\.venv\Scripts\python.exe -c "from calculator import power; print(power(2, 3))"
```

`-c` executes the quoted Python snippet. `from ... import ...` loads your function; `print` makes its return value visible. Expect `8` or `8.0`. This quick check is useful feedback but does not replace the tests in P4.

**Acceptance:** all P1 cases behave as specified; no Streamlit import is needed in `calculator.py`.

## P3 — Add the frontend row (moderate, 15 minutes)

1. Open `app.py` and add `power` to the existing import from `calculator`.
2. At the bottom, after the division error handler has ended, add a `Power` subheading. Start it at the left margin so it is not accidentally inside `except`.
3. Create three columns, following the multiplication/division pattern.
4. In the left column, create a number input labeled `Base`, with minimum `-100.0`, maximum `100.0`, default `2.0`, and key `power_base`.
5. In the middle column, create a number input labeled `Exponent`, with minimum `-10`, maximum `10`, default `3`, step `1`, and key `power_exponent`. Integer arguments make it an integer input.
6. In the right column, display a metric labeled `Power result`. Call the backend function, and use the same `:g` display format as the existing rows.
7. Surround the call with `try`/`except ValueError` and display the exception message in the right column.
8. Update the caption so it accurately distinguishes the multiplication/division input range from the power ranges.
9. In `test_calculator.py`, update the default metric-list expectation in `test_rows_and_changed_inputs` from `["24", "4"]` to `["24", "4", "8"]`. The new row intentionally changes this output. Keep the other baseline assertions. P5 explains this assertion further.

**Hint:** use separate, unique keys, and pass actual widget values to the function. A constant `power(2, 3)` would show 8 but would not respond to the user.

Restart or refresh the local app if necessary. Confirm:

```text
Power
Base [2]             Exponent [3]          Power result 8
```

Try `2, -2`, then `0, -1`, then change the exponent to `2`. Expect `0.25`, the specified error, and `0` with no lingering error. Check the original division result as well. Keep visible labels and try keyboard navigation between the inputs.

**Acceptance:** three distinct operation rows work; the invalid power case renders a readable error and recovers after correction; multiplication and division still behave correctly.

## P4 — Add backend test cases (moderate, 15 minutes)

1. In `test_calculator.py`, add `power` to the backend import.
2. Inside `CalculatorTests`, add `test_power_values`. Use the valid rows from P1 as `(base, exponent, expected)` examples and compare results with `assertAlmostEqual`.
3. Add `test_power_zero_negative`. Use `assertRaisesRegex` to check the specified `ValueError` and its message for `power(0, -1)`.
4. Run discovery again. There should now be **7 tests**: five existing methods plus two new methods. Multiple examples inside one method are subtests, so they do not each increase this total.

**Hint:** tests need independently chosen expected answers. Comparing `power(a, b)` with another call to `power(a, b)` cannot detect a wrong implementation.

**Acceptance:** all valid examples and the invalid case are tested, the baseline tests remain, and discovery ends with `OK`.

## P5 — Add interface tests and update an affected assertion (moderate, 15 minutes)

Adding a row changes a legitimate baseline expectation: the initial list of displayed metrics now includes the default power result. Confirm the P3 update in `test_rows_and_changed_inputs`: its expected list should be `["24", "4", "8"]`. Keep all its existing assertions. This is updating an expectation to match a requested feature, not weakening a test to conceal a bug.

Inside `InterfaceTests`, add two methods:

**`test_power_input`:**

1. Create a fresh `AppTest` and run it.
2. Set `power_base` to `3.0` and `power_exponent` to `4`, then call `.run()`.
3. Assert that `app.exception` is empty.
4. Assert that the third metric (`app.metric[2]`) is `"81"`.

**`test_power_error_and_recovery`:**

1. Start another fresh `AppTest` session.
2. Set the base to `0.0` and exponent to `-1`, then run.
3. Assert there is no unhandled exception and the displayed error matches the contract.
4. Change the exponent to `2` and run again.
5. Assert the error has disappeared and the third metric reads `"0"`.

Use the existing division recovery test as a worked pattern. In AppTest, `.set_value()` changes test state; `.run()` executes the updated app. Displayed metrics are strings, so compare with `"81"`, not the integer `81`.

**Acceptance:** discovery now runs **9 tests** and all pass. The UI tests fail if the new widgets are not connected to `power`. The test methods must be inside the appropriate class, above the final `if __name__ ...` block.

## P6 — Add the CI test gate (moderate, 10 minutes)

Open `.github/workflows/deploy.yml`. Find the student-task comment between the syntax check and deployment request. Replace that comment with:

```yaml
      - name: Run tests
        run: python -m unittest discover -s . -p "test_*.py" -v
```

Line 1 adds a named step to the existing ordered list. Line 2 executes exactly the test discovery command used locally, using the runner's configured Python. The six leading spaces before `- name` match the adjacent steps. Do not create another workflow file for this exercise: editing the existing workflow ensures deployment depends on the tests.

The final sequence must be:

```text
Checkout → Set up Python → Install → Syntax check → Run tests → Request deployment
```

A nonzero test exit code stops the job before the deployment step. Keep the deployment step's push-to-main condition. Do not add `continue-on-error`, `|| true`, or `if: always()` to bypass failures. Confirm Render Auto-Deploy is still Off; otherwise it could deploy independently of this workflow.

**Acceptance:** pull requests run all nine tests but do not deploy; pushes to `main` request deployment only after the tests pass.

## P7 — Prove the gate and deploy (moderate, 15 minutes plus hosting time)

First run the tests locally. Then deliberately change the backend power calculation to `base * exponent` on your feature branch. This expression has valid Python syntax but wrong behavior, so it demonstrates why syntax checking is insufficient. Keep the invalid-input guard unchanged.

```powershell
git add app.py calculator.py test_calculator.py .github/workflows/deploy.yml
git commit -m "Demonstrate failing power tests"
git push -u origin feature/power
```

These lines stage the four edited files, save the demonstration revision, and upload the feature branch. On GitHub, open a pull request from `feature/power` into `main`. The pull-request event starts CI; a plain feature-branch push without an open pull request does not match this workflow's triggers.

1. Confirm that syntax checking passes but `Run tests` fails. Record the failing assertion and the skipped deployment step. A pull request is also excluded by the deployment condition, so this proves CI catches the bug, not by itself that a `main` push was blocked.
2. Restore the correct power expression. Run all nine tests locally.
3. Commit the correction and push again:

```powershell
git add calculator.py
git commit -m "Fix power calculation"
git push
```

4. Confirm the updated pull-request run passes nine tests, while deployment remains skipped.
5. If your repository supports it, configure a branch rule/ruleset requiring the `check-and-deploy` status check before merging to `main`. Without this rule, a failing check is visible but does not necessarily prevent a merge. The workflow itself still stops before the hook when tests fail on a `main` push.
6. Merge only the corrected, passing change. The merge creates a push to `main`, causing a new workflow run.
7. Verify that the new run tests the merged revision and then requests its deployment. Check Render for the same commit, wait for Live, and try all three operations at the public URL.

**Optional instructor-supervised proof:** in a disposable classroom deployment, push a deliberately failing test to `main`, verify that `Request Render deployment` is skipped and Render receives no new deployment, then correct the test. Do not perform this experiment on a shared live application.

**Acceptance:** provide failed and passing CI evidence, a passing `main` run, the matching Render commit/status, and manual results for `3^4`, `0^-1`, and recovery. Do not include secrets in evidence. If hosting is unavailable, label deployment unverified and submit the locally passing implementation and configured workflow instead of claiming a live release.

## P8 — Explain and reflect (easy, 5 minutes)

Answer in your own words:

1. Why does adding a backend function alone not add a visible row?
2. What kind of defect can a backend test miss that an interface test can catch?
3. Why must the tests run before the deploy hook?
4. Why can a green Actions job still be followed by a failed Render deployment?
5. What does `ref=${GITHUB_SHA}` protect against?
6. How would this structure change if a mobile app needed the same calculations through an HTTP API?

If functions and exceptions are unclear, repeat README section 4 with `divide(12, 0)`. If widget wiring is unclear, trace README section 5 with different inputs. If CI is unclear, compare the deliberately wrong but syntactically valid power expression with the failing test output.

## Assessment map

| Concept | Exercise / evidence | Points |
|---|---|---:|
| Defined behavior and correct backend | P1–P2, valid and invalid power cases | 20 |
| Working, labeled interface and recovery | P3, three rows and corrected-input behavior | 20 |
| Backend tests and regression preservation | P4, independent expected outputs | 15 |
| Interface tests | P5, changed inputs and error recovery | 15 |
| CI/CD dependency and evidence | P6–P7, failing/passing checks and deployment verification | 20 |
| Explanation and reflection | P8, clear separation of roles and limitations | 10 |

Optional future extensions: add square root with domain validation, strengthen numeric display precision, or expose an API for an independent client. None is required for this lab.
