@echo off
echo ===================================================
echo ⚡ PulseKit - Reddit Lead Finder ⚡
echo ===================================================
echo.
echo Running python script to scan for active leads...
python reddit_lead_finder.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [!] Error running python script. Make sure python is in your PATH.
    pause
    exit /b
)
echo.
echo [+] Done! Opening leads.md in your editor...
if exist leads.md (
    start leads.md
) else (
    echo [!] leads.md was not generated.
)
echo ===================================================
pause
