@echo off
title 拖入图片或文件夹原地转JPG

if "%~1" == "" (
    echo ==================================================
    echo 请将要转换的图片或文件夹，直接拖放到此 .bat 图标上。
    echo ==================================================
    pause
    exit /b
)

set SCRIPT_PATH=%~dp0convert_images.py
if not exist "%SCRIPT_PATH%" (
    set SCRIPT_PATH=c:\Users\dodo\Desktop\chillin07\convert_images.py
)

if not exist "%SCRIPT_PATH%" (
    echo [错误] 找不到转换脚本 convert_images.py，请确保它在 %~dp0 或 c:\Users\dodo\Desktop\chillin07 目录下。
    pause
    exit /b
)

python "%SCRIPT_PATH%" %*
