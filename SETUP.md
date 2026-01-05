# Guia de Instalação - FaceAge Identity Analyzer

## Pré-requisitos

- Windows 10 ou superior
- Python 3.10 ou 3.11
- Git instalado
- 4GB RAM mínimo (8GB recomendado)

## Instalação Passo a Passo (Windows)

### 1. Verifique a Versão do Python

```cmd
python --version
```

Deve mostrar Python 3.10.x ou 3.11.x

### 2. Clone o Repositório

```cmd
cd E:\Projetos
git clone https://github.com/BettoEsteves/Find-People.git
cd Find-People
```

### 3. Crie o Ambiente Virtual

```cmd
python -m venv venv_findp
```

### 4. Ative o Ambiente Virtual

```cmd
venv_findp\Scripts\activate
```

Você verá `(venv_findp)` no início da linha de comando.

### 5. Atualize pip

```cmd
python -m pip install --upgrade pip
```

### 6. Instale as Dependências

```cmd
pip install -r requirements.txt
```

Este processo pode levar 5-10 minutos dependendo da sua conexão.

### 7. Verifique a Instalação

```cmd
python -c "import streamlit; import cv2; import numpy; print('Instalação OK!')"
```

### 8. Execute o Aplicativo

```cmd
streamlit run app.py
```

O navegador deve abrir automaticamente em `http://localhost:8501`

## Solução de Problemas

### Erro: "Python não é reconhecido"

Adicione Python ao PATH:
1. Painel de Controle > Sistema > Configurações Avançadas
2. Variáveis de Ambiente
3. Adicione o caminho do Python ao PATH

### Erro ao Instalar Pacotes

Tente instalar individualmente:

```cmd
pip install streamlit
pip install opencv-python
pip install torch torchvision
pip install insightface
```

### InsightFace Não Instala

```cmd
pip install onnxruntime
pip install insightface --no-cache-dir
```

### Streamlit Não Abre no Navegador

Abra manualmente: `http://localhost:8501`

## GPU (Opcional)

Para usar GPU NVIDIA:

1. Instale CUDA Toolkit 11.8 ou 12.1
2. Instale cuDNN
3. Reinstale PyTorch com suporte CUDA:

```cmd
pip uninstall torch torchvision
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

4. Ajuste `config/config.yaml`:
```yaml
processing:
  enable_gpu: true
```

## Desativar Ambiente Virtual

```cmd
deactivate
```

## Executar Novamente

Sempre ative o ambiente antes de executar:

```cmd
cd E:\Projetos\FindPeople
venv_findp\Scripts\activate
streamlit run app.py
```

## Atualizações

Para atualizar o projeto:

```cmd
git pull origin main
pip install -r requirements.txt --upgrade
```

## Verificar Logs

Se houver problemas, verifique:
```
logs/app.log
```

## Suporte

- Issues: https://github.com/BettoEsteves/Find-People/issues
- Documentação: README.md
