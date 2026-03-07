@echo off
set "key=HKEY_CURRENT_USER\Software\Microsoft\ColorFiltering"
:: Check if filtering is currently on (Active=1) or off (Active=0)
for /f "tokens=3" %%a in ('reg query "%key%" /v Active 2^>nul') do set "current=%%a"

if "%current%"=="0x1" (
    :: Turn it off
    reg add "%key%" /v Active /t REG_DWORD /d 0 /f
) else (
    :: Set filter to 'Inverted' (1) and turn it on
    reg add "%key%" /v FilterType /t REG_DWORD /d 1 /f
    reg add "%key%" /v Active /t REG_DWORD /d 1 /f
)
:: Force Windows to refresh the accessibility settings
taskkill /f /im explorer.exe && start explorer.exe
