@echo off
color 0A
title Strivon Game Booster
echo ==========================================
echo       Strivon Game Booster v1.0
echo ==========================================
echo.
echo Optimizing system for peak gaming performance...
echo.

echo [1/4] Clearing temporary files...
del /q /f /s %TEMP%\* >nul 2>&1

echo [2/4] Stopping non-essential background services...
:: Requires Administrator privileges to stop services
net stop "SysMain" >nul 2>&1
net stop "WSearch" >nul 2>&1

echo [3/4] Setting power plan to High Performance...
powercfg -setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c >nul 2>&1

echo [4/4] Freeing up RAM (Closing known background browsers/apps)...
:: Note: This will forcefully close these applications if they are running.
taskkill /F /IM "msedge.exe" /T >nul 2>&1
taskkill /F /IM "chrome.exe" /T >nul 2>&1
taskkill /F /IM "Spotify.exe" /T >nul 2>&1

echo.
echo ==========================================
echo    Optimization Complete!
echo    Your system is now optimized for gaming.
echo ==========================================
pause
