@echo off
REM Script para instalar dependencias do FaceAge Identity Analyzer

echo ========================================
echo  Instalacao de Dependencias
echo  FaceAge Identity Analyzer
echo ========================================
echo.

cd /d "%~dp0"

REM Verificar se Python esta instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    echo Instale Python 3.10 ou superior primeiro.
    echo Download: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Python encontrado:
python --version
echo.

REM Criar ambiente virtual se nao existir
if not exist "venv_findp" (
    echo Criando ambiente virtual...
    python -m venv venv_findp
    if errorlevel 1 (
        echo ERRO ao criar ambiente virtual!
        pause
        exit /b 1
    )
    echo Ambiente virtual criado com sucesso!
    echo.
)

REM Ativar ambiente virtual
echo Ativando ambiente virtual...
call venv_findp\Scripts\activate.bat

REM Atualizar pip
echo.
echo Atualizando pip...
python -m pip install --upgrade pip

REM Instalar dependencias
echo.
echo Instalando dependencias...
echo Isso pode levar 5-10 minutos...
echo.

pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERRO durante instalacao!
    echo.
    echo Tente instalar manualmente:
    echo   venv_findp\Scripts\activate
    echo   pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo  Instalacao Concluida!
echo ========================================
echo.
echo Para executar o aplicativo, use:
echo   run_app.bat
echo.
echo Ou manualmente:
echo   venv_findp\Scripts\activate
echo   streamlit run app.py
echo.
pause
