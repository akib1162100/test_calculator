# Verification record

The starter was subsequently simplified for the beginner lesson: two ordinary tests remain active, and the additional tests plus zero-division guard are preserved as comments. The table below records the original, fully enabled version; it does not describe the intentionally disabled current checks.

Verified the revised lesson: **2 active tests passed**; enabling the preserved zero-division test in a temporary copy produced **3 tests with 1 error (`ZeroDivisionError`)**; restoring the preserved backend guard produced **3 passing tests**. The delivered source retains the comments so students can perform these steps themselves.

Verified locally on **2026-09-30**, using **Windows, Python 3.10.11, and Streamlit 1.64.0** in the project's isolated `.venv` environment. The supplied cloud configuration targets Python 3.12; that interpreter and GitHub's Linux runner were not executed here.

| Check | Observed result |
|---|---|
| Install `requirements.txt` in a fresh virtual environment | Succeeded |
| Starter `unittest discover` | 5 tests passed |
| Starter syntax check (`compileall`) | Passed |
| Instructor solution | Extracted the eight Python solution blocks from the answer key, applied them to a temporary copy, and ran 9 tests successfully |
| Deliberately wrong power implementation | `base * exponent` still compiled, but the test runner returned exit code 1 and reported 8 assertion/subtest failures |
| Local server startup | Streamlit started on `127.0.0.1:8501` |
| HTTP `/` | 200, HTML |
| HTTP `/_stcore/health` | 200, `ok` |
| Documentation links | Local file targets checked |

AppTest verified default results, changed inputs, expected error messages, and recovery after correcting invalid inputs. It simulates the interface; it does not prove browser layout. Browser automation was unavailable because the Windows sandbox helper failed to initialize, so no visual browser inspection or screenshot is claimed. A local preview was requested in Codex.

The GitHub workflow was reviewed against the linked official documentation. GitHub Actions execution, secrets setup, Render builds, public deployment, branch protection, and hosted Python 3.12 compatibility remain **unverified in this environment**. Follow the README setup and student lab to collect that evidence in your own repository.

The starter intentionally has no test step in CI: adding that step is part of the student assignment. Keep Render Auto-Deploy Off so the completed exercise's CI test gate controls deployment requests. A successful hook call alone does not confirm a successful hosted deployment.

No GitHub repository, external account, hosting service, or secret was created or modified. The downloadable package contains source and documentation only; it excludes the local environment and generated caches.
