@echo off
set REPO=https://dl-cdn.alpinelinux.org/alpine/v3.20/main/x86_64
echo === 1. Running all unit tests ===
python -m unittest discover -s tests
echo.
echo === 2. Load order: simple graph (DAG) ===
python -m src.cli --package A --repo test_repos/repo_simple.txt --test-mode --output graph.svg
echo.
echo === 3. Load order: cyclic graph ===
python -m src.cli --package A --repo test_repos/repo_cycle.txt --test-mode --output graph.svg
echo.
echo === 4. Load order: real Alpine package 'curl' ===
python -m src.cli --package curl --repo %REPO% --output graph.svg