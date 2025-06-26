@echo off
setlocal

:: Prompt for version tag and description
set /p version=Enter version tag (e.g. v4.3): 
set /p description=Enter brief description of changes: 

:: Set paths
set app_src=C:\NorthPole\Bernard\WebPrototype\app.py
set html_src=C:\NorthPole\Bernard\WebPrototype\templates\index.html
set static_src=C:\NorthPole\Bernard\WebPrototype\static\festive-bg-v2.png

set backup_dir=C:\NorthPole\Bernard\Bernard_Backups
set app_backup=%backup_dir%\app_versions\app_%version%.py
set html_backup=%backup_dir%\html_versions\index_%version%.html
set static_backup=%backup_dir%\backgrounds\bg_%version%.png
set changelog=%backup_dir%\bernard_changelog.txt

:: Create folders if they don't exist
if not exist "%backup_dir%\app_versions" mkdir "%backup_dir%\app_versions"
if not exist "%backup_dir%\html_versions" mkdir "%backup_dir%\html_versions"
if not exist "%backup_dir%\backgrounds" mkdir "%backup_dir%\backgrounds"

:: Copy files
copy "%app_src%" "%app_backup%"
copy "%html_src%" "%html_backup%"
copy "%static_src%" "%static_backup%"

:: Append to changelog
>>"%changelog%" echo [%date% %time%] %version% - %description%

echo Backup complete and changelog updated!
pause

