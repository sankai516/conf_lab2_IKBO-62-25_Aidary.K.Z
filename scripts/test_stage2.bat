@echo off
set REPO=https://dl-cdn.alpinelinux.org/alpine/v3.20/main/x86_64
echo === 1. Running unit tests ===
python -m unittest discover -s tests
echo.
echo === 2. Fetching direct dependencies for 'curl' from Alpine repo ===
python -m src.cli --package curl --repo %REPO% --output graph.svg