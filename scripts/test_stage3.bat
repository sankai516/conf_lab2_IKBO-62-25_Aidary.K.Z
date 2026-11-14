@echo off
echo === 1. Running all unit tests ===
python -m unittest discover -s tests
echo.
echo === 2. Test mode: simple graph (DAG) ===
python -m src.cli --package A --repo test_repos/repo_simple.txt --test-mode --output graph.svg
echo.
echo === 3. Test mode: cyclic dependency ===
python -m src.cli --package A --repo test_repos/repo_cycle.txt --test-mode --output graph.svg
echo.
echo === 4. Remote mode: real Alpine package 'curl' ===
set REPO=https://dl-cdn.alpinelinux.org/alpine/v3.20/main/x86_64
python -m src.cli --package curl --repo %REPO% --output graph.svg