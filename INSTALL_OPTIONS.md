# Opções de Instalação - FaceAge Identity Analyzer

## ⚠️ Problema com Python 3.13

**Python 3.13 é muito novo!** Alguns pacotes (InsightFace, ml_dtypes) não têm wheels pré-compilados e requerem compilação, o que necessita de Microsoft Visual C++ Build Tools.

---

## 📦 Três Opções de Instalação

### Opção 1: Instalação Simplificada (RECOMENDADO para Windows)

**Mais fácil e rápida - Funciona sem compilação!**

```cmd
venv_findp\Scripts\activate
pip install -r requirements_simple.txt
```

**Funcionalidades**:
- ✅ Interface Streamlit completa
- ✅ Processamento de imagens (OpenCV)
- ✅ Envelhecimento facial (algoritmos de imagem)
- ✅ Reconhecimento facial (FaceNet)
- ✅ Todas as visualizações
- ❌ InsightFace (substituído por FaceNet)

**Vantagens**:
- Instalação rápida (2-5 minutos)
- Sem necessidade de Visual Studio
- Funciona imediatamente

---

### Opção 2: Instalação Completa com Build Tools

**Para quem quer usar InsightFace (melhor precisão)**

#### Passo 1: Instalar Visual Studio Build Tools

1. Baixe: https://visualstudio.microsoft.com/visual-cpp-build-tools/
2. Execute o instalador
3. Selecione: "Desktop development with C++"
4. Instale (pode levar 30-60 minutos)
5. Reinicie o computador

#### Passo 2: Instalar Dependências

```cmd
venv_findp\Scripts\activate
pip install -r requirements.txt
```

**Funcionalidades Adicionais**:
- ✅ InsightFace (maior precisão)
- ✅ Mais opções de backends
- ✅ GPU support otimizado

---

### Opção 3: Usar Python 3.11 (RECOMENDADO para máxima compatibilidade)

**Python 3.11 tem wheels pré-compilados para todos os pacotes!**

#### Passo 1: Instalar Python 3.11

1. Baixe Python 3.11.x: https://www.python.org/downloads/release/python-3118/
2. Instale (marque "Add Python to PATH")
3. Verifique: `python --version` (deve mostrar 3.11.x)

#### Passo 2: Recriar Ambiente Virtual

```cmd
cd E:\Projetos\FindPeople
rmdir /S /Q venv_findp
python -m venv venv_findp
venv_findp\Scripts\activate
pip install -r requirements.txt
```

**Esta é a melhor opção para instalação completa sem complicações!**

---

## 🎯 Qual Opção Escolher?

### Use Opção 1 (Simplificada) se:
- Quer instalar rapidamente ✅
- Não quer instalar Visual Studio ✅
- Python 3.13 ✅
- Aceita FaceNet em vez de InsightFace ✅

### Use Opção 2 (Build Tools) se:
- Quer máxima precisão (InsightFace) ✅
- Não se importa em instalar Build Tools ✅
- Python 3.13 ✅
- Tem tempo para instalação longa ⏱️

### Use Opção 3 (Python 3.11) se:
- Quer instalação completa SEM Build Tools ✅✅
- Aceita trocar versão do Python ✅
- Quer máxima compatibilidade ✅
- **RECOMENDADO!** ⭐

---

## 📊 Comparação de Funcionalidades

| Funcionalidade | Simplificada | Build Tools | Python 3.11 |
|----------------|-------------|-------------|-------------|
| Interface Streamlit | ✅ | ✅ | ✅ |
| Envelhecimento Facial | ✅ | ✅ | ✅ |
| Reconhecimento (FaceNet) | ✅ | ✅ | ✅ |
| Reconhecimento (InsightFace) | ❌ | ✅ | ✅ |
| Instalação Rápida | ✅ | ❌ | ✅ |
| Sem Build Tools | ✅ | ❌ | ✅ |
| Tempo de Instalação | 2-5 min | 30-90 min | 5-10 min |

---

## 🔍 Verificar Instalação

Após instalar, verifique:

```cmd
venv_findp\Scripts\activate
python check_system.py
```

Isso mostrará o que está funcionando e o que falta.

---

## ⚡ Testar Rapidamente

Após instalação:

```cmd
venv_findp\Scripts\activate
streamlit run app.py
```

Se abrir no navegador, está funcionando!

---

## 🆘 Problemas?

### Erro: "cl.exe not found" ou "Visual C++ required"
- **Solução**: Use Opção 1 (Simplificada) ou Opção 3 (Python 3.11)

### Erro: "No module named 'insightface'"
- **Se Opção 1**: Normal, use FaceNet
- **Se Opção 2/3**: Reinstale com Build Tools

### Erro: "torch not found"
- **Solução**:
```cmd
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

---

## 💡 Recomendação Final

**Para a melhor experiência:**
1. **Instale Python 3.11** (não 3.13)
2. **Use `requirements.txt` completo**
3. **Tenha toda a funcionalidade sem problemas!**

OU

Se preferir Python 3.13:
1. **Use `requirements_simple.txt`**
2. **Instalação rápida e funcional**
3. **Troque InsightFace por FaceNet (pequena diferença)**

---

**Versão**: 1.0.0
**Atualizado**: 2026-01-05
