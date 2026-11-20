@echo off
set REPO=https://dl-cdn.alpinelinux.org/alpine/v3.20/main/x86_64
set PKG=%1
if "%PKG%"=="" set PKG=curl
python -m src.cli --package %PKG% --repo %REPO% --output %PKG%.svg
