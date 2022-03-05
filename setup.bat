@echo off
cls

if exist .venv (
    echo already has .venv
) else (
    python -m venv .venv
    echo created new venv
)
start "".venv\Scripts\activate""

echo installing packages

pip install pygame
pip install numpy
pip install pillow

if not errorlevel 1(
    echo "finished"
) else (
    echo "an error occured"
)
