# ⚡ Guia Rápido - FaceAge Identity Analyzer

## 🚀 Execução Rápida (3 passos)

### 1️⃣ Ativar Ambiente
```cmd
cd E:\Projetos\FindPeople
venv_findp\Scripts\activate
```

### 2️⃣ Instalar Dependências (primeira vez apenas)
```cmd
pip install -r requirements.txt
```
⏱️ Isso pode levar 5-10 minutos na primeira vez.

### 3️⃣ Executar
```cmd
streamlit run app.py
```
🌐 Abrirá automaticamente em: http://localhost:8501

---

## 📸 Como Usar

1. **Upload**: Envie uma foto clara com rosto frontal
2. **Dados**: Preencha nome, data de nascimento e idade na foto
3. **Analise**: Clique em "🚀 Analyze"
4. **Resultados**: Veja a comparação e score de similaridade

---

## ⚙️ Configurações Rápidas

Edite `config/config.yaml` se necessário:

```yaml
# Desabilitar GPU (se não tiver NVIDIA)
processing:
  enable_gpu: false

# Ajustar threshold de similaridade
models:
  face_recognition:
    similarity_threshold: 0.4  # Menor = mais restritivo
```

---

## 🔧 Troubleshooting Rápido

### Erro ao instalar
```cmd
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
```

### Streamlit não abre
Abra manualmente: http://localhost:8501

### Erro de memória
Reduza tamanho da imagem antes do upload

---

## 📂 Arquivos Importantes

- `app.py` - Aplicação principal
- `config/config.yaml` - Configurações
- `README.md` - Documentação completa
- `SETUP.md` - Instalação detalhada
- `logs/app.log` - Logs de execução

---

## ⚠️ Lembre-se

- ✅ Uso educacional/demonstrativo
- ❌ Não usar para fins legais
- 🔒 Obter consentimento para processar imagens
- 📊 Resultados são probabilísticos

---

## 📞 Ajuda

Precisa de mais detalhes? Veja:
- `README.md` - Documentação completa
- `SETUP.md` - Guia de instalação
- `PROJECT_SUMMARY.md` - Resumo técnico

---

**Versão**: 1.0.0 | **Status**: ✅ Pronto
