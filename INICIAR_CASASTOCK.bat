@echo off
setlocal
title Iniciar CasaStock

rem Sempre executar a partir da pasta onde este arquivo esta salvo.
cd /d "%~dp0"

echo ==========================================
echo              CASASTOCK
echo ==========================================
echo.

if not exist "app.py" (
    echo ERRO: Nao encontrei o arquivo app.py.
    echo Verifique se este arquivo .bat esta na pasta principal do CasaStock.
    goto erro
)

if not exist "requirements.txt" (
    echo ERRO: Nao encontrei o arquivo requirements.txt.
    goto erro
)

rem Localiza uma instalacao do Python 3.
set "PYTHON_LAUNCHER="
py -3 --version >nul 2>&1
if not errorlevel 1 set "PYTHON_LAUNCHER=py -3"

if not defined PYTHON_LAUNCHER (
    python --version >nul 2>&1
    if not errorlevel 1 set "PYTHON_LAUNCHER=python"
)

if not defined PYTHON_LAUNCHER (
    echo ERRO: Python 3 nao foi encontrado neste computador.
    echo Instale o Python 3 em https://www.python.org/downloads/
    echo Durante a instalacao, marque a opcao "Add Python to PATH".
    goto erro
)

rem Cria o ambiente virtual automaticamente na primeira execucao.
if not exist ".venv\Scripts\python.exe" (
    echo Preparando o ambiente do CasaStock...
    %PYTHON_LAUNCHER% -m venv .venv
    if errorlevel 1 (
        echo ERRO: Nao foi possivel criar o ambiente virtual.
        goto erro
    )
)

rem Instala as dependencias apenas quando o Flask ainda nao estiver instalado.
".venv\Scripts\python.exe" -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo Instalando as dependencias. Isso pode levar alguns instantes...
    ".venv\Scripts\python.exe" -m pip install -r requirements.txt
    if errorlevel 1 (
        echo ERRO: Falha ao instalar as dependencias.
        echo Confira sua conexao com a internet e tente novamente.
        goto erro
    )
)

echo.
echo Iniciando o servidor do CasaStock...
start "CasaStock - Servidor" /D "%CD%" "%CD%\.venv\Scripts\python.exe" app.py

echo Aguardando o servidor iniciar...
timeout /t 3 /nobreak >nul
start "" "http://127.0.0.1:5000"

echo.
echo O navegador deve abrir o CasaStock.
echo Mantenha aberta a janela "CasaStock - Servidor" enquanto estiver usando o sistema.
echo Para desligar o CasaStock, feche a janela do servidor ou pressione Ctrl+C nela.
echo.
pause
exit /b 0

:erro
echo.
echo O CasaStock nao conseguiu iniciar.
pause
exit /b 1
