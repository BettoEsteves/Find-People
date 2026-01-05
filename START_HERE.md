# 🚀 COMECE AQUI - FaceAge Identity Analyzer

## ⚡ Execução Rápida (Windows)

### Opção 1: Duplo Clique (Mais Fácil)

1. **Duplo clique** em: `run_app.bat`
2. Aguarde o navegador abrir automaticamente
3. Pronto! Use o aplicativo

### Opção 2: PowerShell

```powershell
# Clique direito em run_app.ps1 > "Executar com PowerShell"
# OU abra PowerShell e execute:
.\run_app.ps1
```

### Opção 3: Terminal/CMD

```cmd
cd E:\Projetos\FindPeople
venv_findp\Scripts\activate
streamlit run app.py
```

---

## 📦 Primeira Instalação

Se for a primeira vez executando:

1. **Duplo clique** em: `install_dependencies.bat`
2. Aguarde a instalação (5-10 minutos)
3. Depois execute: `run_app.bat`

---

## ✅ Verificar Sistema

Para verificar se tudo está instalado corretamente:

```cmd
venv_findp\Scripts\activate
python check_system.py
```

---

## 🎯 Como Usar o Aplicativo

1. **Upload**: Clique em "Upload Person's Photo"
   - Envie uma foto clara com rosto frontal
   - Formatos: JPG, PNG

2. **Dados**: Preencha no menu lateral
   - Nome da pessoa
   - Data de nascimento
   - Idade aproximada na foto

3. **Analise**: Clique no botão "🚀 Analyze"

4. **Resultados**: Veja:
   - Comparação lado a lado
   - Score de similaridade (%)
   - Nível de confiança
   - Métricas detalhadas

---

## 📂 Estrutura Rápida

```
FindPeople/
├── run_app.bat              ← EXECUTE ESTE!
├── run_app.ps1              ← OU ESTE (PowerShell)
├── install_dependencies.bat ← Primeira instalação
├── check_system.py          ← Verificar sistema
├── app.py                   ← Aplicação principal
└── README.md                ← Documentação completa
```

---

## 🔧 Problemas Comuns

### Erro: "Python não encontrado"
- Instale Python 3.10+: https://www.python.org/downloads/
- Marque "Add Python to PATH" durante instalação

### Erro: "Módulo não encontrado"
- Execute: `install_dependencies.bat`

### Aplicativo não abre
- Abra manualmente: http://localhost:8501

### GPU não detectada
- Normal! O aplicativo funciona sem GPU (apenas mais lento)
- Para usar GPU: Instale CUDA Toolkit

---

## 📚 Documentação Completa

- `README.md` - Documentação técnica detalhada
- `SETUP.md` - Guia de instalação completo
- `QUICKSTART.md` - Guia rápido
- `PROJECT_SUMMARY.md` - Resumo do projeto

---

## ⚠️ IMPORTANTE

- ✅ Uso educacional/demonstrativo
- ❌ Não usar para fins legais
- 🔒 Obter consentimento antes de processar imagens
- 📊 Resultados são probabilísticos, não garantias

---

## 🆘 Precisa de Ajuda?

1. Verifique os logs: `logs/app.log`
2. Execute: `python check_system.py`
3. Consulte: `README.md`
4. Issues: https://github.com/BettoEsteves/Find-People/issues

---

**Desenvolvido com Python, Deep Learning e Computer Vision**

**Versão**: 1.0.0 | **Status**: ✅ Pronto para uso
