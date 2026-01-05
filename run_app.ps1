# FaceAge Identity Analyzer - PowerShell Startup Script
# Este script ativa o ambiente virtual e executa o aplicativo

Write-Host "========================================"
Write-Host " FaceAge Identity Analyzer"
Write-Host " Iniciando aplicacao..."
Write-Host "========================================"
Write-Host ""

# Mudar para o diretório do script
Set-Location $PSScriptRoot

# Verificar se o ambiente virtual existe
if (-not (Test-Path "venv_findp\Scripts\Activate.ps1")) {
    Write-Host "ERRO: Ambiente virtual nao encontrado!" -ForegroundColor Red
    Write-Host "Execute: python -m venv venv_findp"
    Read-Host "Pressione Enter para sair"
    exit 1
}

# Ativar ambiente virtual
Write-Host "Ativando ambiente virtual..." -ForegroundColor Cyan
& "venv_findp\Scripts\Activate.ps1"

# Verificar se as dependencias estao instaladas
Write-Host "Verificando dependencias..." -ForegroundColor Cyan
try {
    python -c "import streamlit" 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "Streamlit nao instalado"
    }
} catch {
    Write-Host ""
    Write-Host "Instalando dependencias..." -ForegroundColor Yellow
    Write-Host "Isso pode levar alguns minutos..."
    Write-Host ""

    pip install -r requirements.txt

    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "ERRO: Falha ao instalar dependencias!" -ForegroundColor Red
        Read-Host "Pressione Enter para sair"
        exit 1
    }
}

# Executar aplicacao Streamlit
Write-Host ""
Write-Host "Iniciando Streamlit..." -ForegroundColor Green
Write-Host "O navegador abrira automaticamente em http://localhost:8501"
Write-Host ""
Write-Host "Pressione Ctrl+C para parar o servidor" -ForegroundColor Yellow
Write-Host ""

streamlit run app.py

# Manter janela aberta se houver erro
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERRO ao executar o aplicativo!" -ForegroundColor Red
    Read-Host "Pressione Enter para sair"
}
