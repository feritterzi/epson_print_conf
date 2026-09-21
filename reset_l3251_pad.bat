@echo off
setlocal
cd /d "%~dp0"

if "%~1"=="" (
  echo Kullanim: reset_l3251_pad.bat YAZICI_IP
  echo Ornek:    reset_l3251_pad.bat 192.168.1.50
  exit /b 1
)

python reset_l3251_pad.py %*
exit /b %ERRORLEVEL%
