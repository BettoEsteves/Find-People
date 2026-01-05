@echo off
REM FaceAge Identity Analyzer - Startup Script
REM Este script ativa o ambiente virtual e executa o aplicativo

echo ========================================
echo  FaceAge Identity Analyzer
echo  Iniciando aplicacao...
echo ========================================
echo.

cd /d "%~dp0"

REM Verificar se o ambiente virtual existe
if not exist "venv_findp\Scripts\activate.bat" (
    echo ERRO: Ambiente virtual nao encontrado!
    echo Execute: python -m venv venv_findp
    pause
    exit /b 1
)

REM Ativar ambiente virtual
call venv_findp\Scripts\activate.bat

REM Verificar se as dependencias estao instaladas
python -c "import streamlit" 2>nul
if errorlevel 1 (
    echo.
    echo Instalando dependencias...
    echo Isso pode levar alguns minutos...
    echo.
    pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo ERRO: Falha ao instalar dependencias!
        pause
        exit /b 1
    )
)

REM Executar aplicacao Streamlit
echo.
echo Iniciando Streamlit...
echo O navegador abrira automaticamente em http://localhost:8501
echo.
echo Pressione Ctrl+C para parar o servidor
echo.

streamlit run app.py

REM Manter janela aberta se houver erro
if errorlevel 1 (
    echo.
    echo ERRO ao executar o aplicativo!
    pause
)
