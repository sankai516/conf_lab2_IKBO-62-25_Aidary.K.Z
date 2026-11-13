@echo off
set REPO=https://dl-cdn.alpinelinux.org/alpine/v3.20/main/x86_64
echo === 1. Running unit tests ===
python -m unittest discover -s tests
echo.
echo === 2. Valid configuration output ===
python -m src.cli --package curl --repo %REPO% --output graph.svg
echo.
echo === 3. Error: invalid output extension ===
python -m src.cli --package curl --repo %REPO% --output graph.png
echo.
echo === 4. Error: missing test repo file ===
python -m src.cli --package A --repo missing.txt --test-mode --output g.svg