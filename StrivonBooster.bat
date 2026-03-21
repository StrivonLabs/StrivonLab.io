@echo off
title STRIVON BOOSTER - Ultimate Performance Alpha
color 0b

echo.
echo    .oooooo..o oooooooooooo oooooooooo.  ooooo ooooooo..o  .oooooo.   ooooo      ooo 
echo   d8P'    `Y8 `888'     `8 `888'   `Y8b `888' d8P'    `Y8 d8P'  `Y8b  `888b.     `8' 
echo   Y88bo.       888          888      888 888  Y88bo.     888      888  8 `88b.    8  
echo    `"Y8888o.   888oooo8     888      888 888   `"Y8888o. 888      888  8   `88b.  8  
echo        `"Y88b  888    "     888      888 888       `"Y88b 888      888  8     `88b.8  
echo   oo     .d8P  888       o  888     d88' 888  oo     .d8P 88b.  .d8P  8       `8888  
echo   8""88888P'  o888ooooood8 o888bood8P'  o888o 8""88888P'   `Y8bood8P'  o8          8  
echo.
echo ======================================================================================
echo    STRIVON BOOSTER - SYSTEM OPTIMIZER [v4.0 ALPHA]
echo ======================================================================================
echo.

echo [*] Cleaning system temp files...
del /q /s /f %temp%\* >nul 2>&1
del /q /s /f C:\Windows\Temp\* >nul 2>&1

echo [*] Optimizing Power Plan...
powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c >nul 2>&1

echo [*] High-Priority Processes...
wmic process where name="RobloxPlayerBeta.exe" CALL setpriority "high priority" >nul 2>&1

echo [*] Flushing DNS Cache...
ipconfig /flushdns >nul 2>&1

echo [*] RAM Purge (Closing Latency Hogs)...
taskkill /f /im "msedge.exe" >nul 2>&1
taskkill /f /im "chrome.exe" >nul 2>&1
taskkill /f /im "spotify.exe" >nul 2>&1
taskkill /f /im "discord.exe" >nul 2>&1

echo.
echo ======================================================================================
echo    SYSTEM OPTIMIZED - STRIVON LABS [VERIFIED]
echo ======================================================================================
echo [*] Press any key to exit.
pause >nul
