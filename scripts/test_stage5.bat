@echo off
set REPO=https://dl-cdn.alpinelinux.org/alpine/v3.20/main/x86_64
echo === 1. Running all unit tests ===
python -m unittest discover -s tests
echo.
echo === 2. Visualizing package 1: tree ===
python -m src.cli --package tree --repo %REPO% --output tree.svg
echo.
echo === 3. Visualizing package 2: zlib ===
python -m src.cli --package zlib --repo %REPO% --output zlib.svg
echo.
echo === 4. Visualizing package 3: curl ===
python -m src.cli --package curl --repo %REPO% --output curl.svg