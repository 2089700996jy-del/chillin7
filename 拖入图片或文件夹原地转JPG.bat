@echo off
title Drag and drop images or folders here

if "%~1" == "" (
    echo ==================================================
    echo Drag and drop files or folders onto this bat file.
    echo ==================================================
    pause
    exit /b
)

python "%~dp0convert_images.py" %*
