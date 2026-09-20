@echo off
title Enviando Nova Stellaris para o GitHub...
echo ===================================================
echo       Enviando alteracoes para o GitHub
echo ===================================================
"C:\Users\marce\.gemini\antigravity\scratch\tools\mingit\cmd\git.exe" push origin main
echo.
if %errorlevel% equ 0 (
    echo [SUCESSO] Projeto enviado com exito para o GitHub!
) else (
    echo [ERRO] Falha no envio. Se solicitar login, autorize no navegador.
)
echo.
pause
