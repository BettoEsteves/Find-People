# 🔧 Guia de Solução de Problemas

## Problemas de Instalação

### Erro: "Python não encontrado" ou "python não é reconhecido"

**Solução**:
1. Instale Python 3.10 ou superior: https://www.python.org/downloads/
2. Durante instalação, marque: ✅ "Add Python to PATH"
3. Reinicie o terminal/CMD após instalação
4. Verifique: `python --version`

---

### Erro ao Instalar Dependências

**Solução 1 - Limpar cache do pip**:
```cmd
venv_findp\Scripts\activate
python -m pip cache purge
pip install -r requirements.txt
```

**Solução 2 - Instalar sem cache**:
```cmd
venv_findp\Scripts\activate
pip install -r requirements.txt --no-cache-dir
```

**Solução 3 - Atualizar pip**:
```cmd
venv_findp\Scripts\activate
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

---

### Erro: "Microsoft Visual C++ 14.0 is required"

**Solução**:
1. Baixe: https://visualstudio.microsoft.com/visual-cpp-build-tools/
2. Instale "Visual C++ Build Tools"
3. Reinicie e tente novamente

---

### Erro com InsightFace

**Solução**:
```cmd
venv_findp\Scripts\activate
pip install onnxruntime
pip install insightface --no-cache-dir
```

Se persistir, o aplicativo usará FaceNet como alternativa automaticamente.

---

### Erro com PyTorch

**Solução - CPU Only**:
```cmd
venv_findp\Scripts\activate
pip uninstall torch torchvision
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

**Solução - GPU (NVIDIA)**:
```cmd
pip uninstall torch torchvision
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
```

---

## Problemas de Execução

### Streamlit não inicia

**Solução 1**:
```cmd
venv_findp\Scripts\activate
python -m streamlit run app.py
```

**Solução 2 - Porta ocupada**:
```cmd
streamlit run app.py --server.port 8502
```

---

### Erro: "No module named 'streamlit'"

**Solução**:
```cmd
venv_findp\Scripts\activate
pip install streamlit
```

---

### Navegador não abre automaticamente

**Solução**: Abra manualmente:
```
http://localhost:8501
```

---

### Erro: "Address already in use"

**Solução - Matar processo na porta 8501**:
```cmd
netstat -ano | findstr :8501
taskkill /PID [número_do_PID] /F
```

Ou use porta diferente:
```cmd
streamlit run app.py --server.port 8502
```

---

## Problemas durante Análise

### "No face detected"

**Causas**:
- Foto sem rosto visível
- Rosto muito pequeno
- Má iluminação
- Rosto de perfil

**Soluções**:
- Use foto frontal clara
- Boa iluminação
- Rosto ocupando pelo menos 30% da imagem
- Sem óculos escuros ou máscaras

---

### "Failed to extract features"

**Causa**: Modelo não conseguiu processar o rosto

**Solução**:
1. Tente foto diferente
2. Verifique se InsightFace instalou corretamente:
```cmd
venv_findp\Scripts\activate
python -c "import insightface; print('OK')"
```

---

### Processamento muito lento

**Soluções**:

**1. Reduzir tamanho da imagem**:
- Antes de upload, redimensione para max 1024x1024px

**2. Habilitar GPU (NVIDIA)**:
- Instale CUDA Toolkit: https://developer.nvidia.com/cuda-downloads
- Instale cuDNN
- Em `config/config.yaml`:
```yaml
processing:
  enable_gpu: true
```

**3. Usar CPU mais eficiente**:
```cmd
set OMP_NUM_THREADS=4
streamlit run app.py
```

---

### Erro: "CUDA out of memory"

**Solução - Desabilitar GPU**:

Em `config/config.yaml`:
```yaml
processing:
  enable_gpu: false
```

---

## Problemas com GPU

### GPU não detectada

**Verificar**:
```cmd
venv_findp\Scripts\activate
python -c "import torch; print(torch.cuda.is_available())"
```

**Se retornar False**:
1. Verifique drivers NVIDIA atualizados
2. Instale CUDA Toolkit compatível
3. Reinstale PyTorch com suporte CUDA:
```cmd
pip uninstall torch torchvision
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
```

---

## Problemas com Arquivos

### Erro: "Permission denied"

**Solução Windows**:
1. Execute terminal como Administrador
2. Ou mude permissões da pasta FindPeople

---

### Logs não aparecem

**Solução**:
Verifique pasta `logs/`:
```cmd
type logs\app.log
```

Se não existir:
```cmd
mkdir logs
```

---

## Verificação do Sistema

Execute verificação completa:
```cmd
venv_findp\Scripts\activate
python check_system.py
```

Isso mostrará:
- ✅ O que está OK
- ❌ O que precisa ser corrigido
- ⚠️ Avisos

---

## Problemas com Git/GitHub

### Erro ao fazer push

**Solução - Configurar credenciais**:
```cmd
git config --global user.name "Seu Nome"
git config --global user.email "seu@email.com"
```

**Autenticação**:
1. GitHub → Settings → Developer settings
2. Personal access tokens → Generate new token
3. Copie o token
4. Use como senha no git push

---

### Conflitos de merge

**Solução**:
```cmd
git pull origin main
# Resolva conflitos manualmente
git add .
git commit -m "Resolve conflicts"
git push origin main
```

---

## Limpeza e Reset

### Reinstalar ambiente virtual

```cmd
rmdir /S /Q venv_findp
python -m venv venv_findp
venv_findp\Scripts\activate
pip install -r requirements.txt
```

---

### Limpar cache Python

```cmd
# Remover __pycache__
for /d /r . %d in (__pycache__) do @if exist "%d" rd /s /q "%d"

# Limpar cache pip
pip cache purge
```

---

## Informações de Debug

### Coletar informações para Issue

```cmd
venv_findp\Scripts\activate
python --version
pip list
python check_system.py > system_info.txt
type logs\app.log >> system_info.txt
```

Envie `system_info.txt` com sua Issue no GitHub.

---

## Logs e Diagnóstico

### Verificar logs de execução
```cmd
type logs\app.log | more
```

### Ativar modo debug

Em `config/config.yaml`:
```yaml
app:
  debug: true

logging:
  level: DEBUG
```

---

## Contato e Suporte

Se nenhuma solução funcionou:

1. **Verifique Issues existentes**:
   https://github.com/BettoEsteves/Find-People/issues

2. **Crie nova Issue** com:
   - Descrição do problema
   - Mensagem de erro completa
   - Output de `python check_system.py`
   - Sistema operacional e versão Python

3. **Logs**: Anexe `logs/app.log` (remova dados sensíveis primeiro)

---

## Perguntas Frequentes (FAQ)

### Preciso de GPU?
**Não.** GPU acelera, mas não é obrigatória.

### Funciona no Linux/Mac?
**Sim**, mas alguns scripts (.bat) são Windows. Use equivalentes .sh no Linux.

### Quanto tempo demora uma análise?
**3-8 segundos** em CPU moderna, 1-3s com GPU.

### Posso processar múltiplas fotos?
**Não implementado ainda**. Processo uma de cada vez.

### É preciso internet?
**Sim, na primeira execução** para baixar modelos (~500MB).
Depois funciona offline.

### Resultados são precisos?
**Probabilísticos**. Não use para fins legais/forenses.

---

**Última atualização**: 2026-01-05
