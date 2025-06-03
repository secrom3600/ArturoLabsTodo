@echo off

REM Ir a Frontend y levantar docker-compose
echo Starting Frontend...
cd /d "%~dp0ArturoLabs---Frontend\portal_gestion_carne"
if errorlevel 1 (
  echo Frontend folder not found!
  pause
  exit /b 1
)
docker-compose up -d

REM Volver a la carpeta base
cd /d "%~dp0"

REM Ir a Backend y levantar docker-compose
echo Starting Backend...
cd /d "%~dp0ArturoLabs---Backend"
if errorlevel 1 (
  echo Backend folder not found!
  pause
  exit /b 1
)
docker-compose up -d

REM Volver a la carpeta base
cd /d "%~dp0"

echo Both Frontend and Backend started!
pause