@echo off
chcp 65001 >nul
title Đóng gói PrintMaster thành file EXE

cd /d "%~dp0"

echo =======================================================
echo    Đang đóng gói PrintMaster thành file EXE (Windows)
echo =======================================================

if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
)

echo [1/3] Cài đặt PyInstaller...
python -m pip install -q pyinstaller -r requirements.txt

echo [2/3] Xóa bản build cũ...
if exist "dist\PrintMaster" rmdir /s /q "dist\PrintMaster"
if exist "build" rmdir /s /q "build"

echo [3/3] Đang biên dịch thành file PrintMaster.exe...
python -m PyInstaller ^
    --name "PrintMaster" ^
    --windowed ^
    --noconfirm ^
    --clean ^
    --icon "assets/app_icon.ico" ^
    --add-data "ui;ui" ^
    --add-data "core;core" ^
    --add-data "assets;assets" ^
    main.py

echo =======================================================
echo [SUCCESS] DONG GOI HOAN TAT!
echo File chay PrintMaster.exe da duoc tao tai:
echo %~dp0dist\PrintMaster\PrintMaster.exe
echo =======================================================
pause
