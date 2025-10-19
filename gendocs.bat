@echo off
REM ==========================================
REM Generar documentación con pdoc en Windows
REM ==========================================

REM Cambia "src" por el nombre del paquete o carpeta de tu proyecto
set PROJECT_DIR=FallSimulator/src/fall_simulator/
set OUTPUT_DIR=docs

echo Generando documentación de %PROJECT_DIR%...
REM Crear carpeta docs si no existe
if not exist "%OUTPUT_DIR%" mkdir "%OUTPUT_DIR%"

REM Generar documentación HTML con pdoc
python -m pdoc "%PROJECT_DIR%" -o "%OUTPUT_DIR%"

echo Documentación generada en %OUTPUT_DIR%\%PROJECT_DIR%
pause