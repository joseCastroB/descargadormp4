@echo off
title Descargador Local
echo =========================================
echo   Iniciando Descargador...
echo   Por favor, no cierres esta ventana.
echo =========================================

:: Abre el navegador web automáticamente
start http://127.0.0.1:8000

:: Ejecuta el servidor portable que acabamos de compilar
main.exe