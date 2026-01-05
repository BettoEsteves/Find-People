# 👤 FaceAge Identity Analyzer

**Face Aging Simulation & Identity Verification System**

Um aplicativo web avançado que simula o envelhecimento facial e verifica a probabilidade de identidade entre imagens de diferentes idades, usando Deep Learning e Computer Vision.

---

## 🎯 Funcionalidades

- **Detecção Facial Automática**: Detecta e alinha faces em imagens
- **Simulação de Envelhecimento**: Gera aparência estimada da pessoa na idade atual
- **Comparação Facial**: Calcula similaridade entre imagem original e envelhecida
- **Análise de Confiança**: Fornece métricas de confiança para cada análise
- **Interface Web Intuitiva**: Interface Streamlit fácil de usar
- **Visualizações Detalhadas**: Comparações lado a lado com métricas visuais

---

## 📋 Requisitos

### Sistema
- Windows (obrigatório)
- Python 3.10 ou superior
- 4GB RAM mínimo (8GB recomendado)
- GPU NVIDIA (opcional, para melhor performance)

### Dependências Principais
- Streamlit (interface web)
- OpenCV (processamento de imagens)
- InsightFace / FaceNet (reconhecimento facial)
- PyTorch (deep learning)
- Scikit-learn (métricas de similaridade)

---

## 🚀 Instalação

### 1. Clone o Repositório
```bash
git clone https://github.com/BettoEsteves/Find-People.git
cd Find-People
```

### 2. Crie o Ambiente Virtual (Windows)
```bash
python -m venv venv_findp
venv_findp\Scripts\activate
```

### 3. Instale as Dependências
```bash
pip install -r requirements.txt
```

### 4. Configuração
Edite `config/config.yaml` se necessário para ajustar:
- Backend de detecção facial
- Threshold de similaridade
- Configurações de GPU
- Outros parâmetros

---

## 💻 Como Usar

### Iniciar o Aplicativo
```bash
streamlit run app.py
```

O aplicativo abrirá automaticamente no navegador em `http://localhost:8501`

### Passo a Passo

1. **Upload da Foto**
   - Clique em "Upload Person's Photo"
   - Selecione uma foto clara com rosto frontal
   - Formatos aceitos: JPG, PNG

2. **Preencha os Dados**
   - Nome da pessoa
   - Data de nascimento
   - Idade aproximada na foto

3. **Analise**
   - Clique em "🚀 Analyze"
   - Aguarde o processamento (pode levar 10-30 segundos)

4. **Visualize os Resultados**
   - Imagem original vs. imagem envelhecida
   - Score de similaridade (%)
   - Nível de confiança
   - Métricas detalhadas

---

## 🏗️ Arquitetura do Sistema

```
┌─────────────────┐
│  Upload Imagem  │
└────────┬────────┘
         │
         ▼
┌─────────────────────┐
│ Detecção Facial     │ ◄── RetinaFace / OpenCV
│ (FaceDetector)      │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│ Alinhamento         │
│ (FaceAligner)       │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│ Envelhecimento      │ ◄── Style Transfer
│ (FaceAging)         │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│ Extração Embeddings │ ◄── InsightFace / FaceNet
│ (FaceEmbeddings)    │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│ Comparação Facial   │ ◄── Cosine Similarity
│ (FaceComparator)    │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Resultados + UI    │
└─────────────────────┘
```

---

## 📁 Estrutura do Projeto

```
FindPeople/
│
├── app.py                     # Aplicativo principal Streamlit
├── requirements.txt           # Dependências
├── README.md                 # Este arquivo
├── .gitignore               # Arquivos ignorados pelo Git
│
├── config/                   # Configurações
│   ├── __init__.py
│   ├── config.yaml          # Arquivo de configuração
│   └── settings.py          # Carregador de configurações
│
├── src/                     # Código fonte
│   ├── __init__.py
│   │
│   ├── core/                # Módulos principais
│   │   ├── __init__.py
│   │   ├── face_detector.py      # Detecção facial
│   │   ├── face_aligner.py       # Alinhamento
│   │   ├── face_aging.py         # Envelhecimento
│   │   ├── face_embeddings.py    # Extração de features
│   │   └── face_comparator.py    # Comparação
│   │
│   └── utils/              # Utilitários
│       ├── __init__.py
│       ├── image_utils.py       # Processamento de imagens
│       ├── date_utils.py        # Cálculos de data/idade
│       └── visualization.py     # Visualizações
│
├── data/                   # Dados
│   ├── uploads/           # Imagens enviadas
│   └── results/           # Resultados salvos
│
├── models/                # Modelos baixados (criado automaticamente)
│
├── logs/                  # Logs de execução
│
└── tests/                 # Testes (opcional)
```

---

## 🔬 Detalhes Técnicos

### Detecção Facial
- **Backend Primário**: RetinaFace (alta precisão)
- **Fallback**: OpenCV Haar Cascade
- **Confiança Mínima**: 90%

### Alinhamento
- Alinhamento baseado em landmarks oculares
- Normalização de pose e escala
- Target size: 256x256 pixels

### Envelhecimento Facial
- **Método**: Style Transfer + Image Processing
- **Técnicas**:
  - Ajuste de tom de pele
  - Adição de rugas e texturas
  - Simulação de flacidez
  - Age spots (para idades avançadas)
- **Confiança**: Decresce com delta de idade maior

### Reconhecimento Facial
- **Backend**: InsightFace (buffalo_l) ou FaceNet
- **Embedding Size**: 512 dimensões
- **Normalização**: L2 normalization

### Comparação
- **Métrica Principal**: Cosine Similarity
- **Threshold**: 0.4 (configurável)
- **Escala**: 0-100%

---

## ⚠️ Limitações e Avisos

### Limitações Técnicas
1. **Envelhecimento é Estimativo**
   - Não considera genética individual
   - Não modela estilo de vida ou saúde
   - Resultados variam com qualidade da imagem

2. **Dependência de Imagem**
   - Requer foto frontal clara
   - Iluminação adequada
   - Sem oclusões faciais

3. **Precisão da Comparação**
   - Score alto não garante identidade
   - Fatores ambientais afetam resultado
   - Não é método forense

### Avisos Éticos e Legais

⚠️ **IMPORTANTE**:
- Este sistema é **demonstrativo e educacional**
- Resultados são **probabilísticos**, não determinísticos
- **NÃO deve ser usado** para fins legais ou forenses
- **NÃO substitui** métodos oficiais de identificação
- Respeite privacidade e obtenha consentimento antes de usar

---

## 🐛 Solução de Problemas

### Erro ao Instalar InsightFace
```bash
# Tente instalar manualmente
pip install onnxruntime
pip install insightface
```

### GPU não Detectada
- Verifique instalação do CUDA
- Ajuste `enable_gpu: false` em `config/config.yaml`

### Modelo Não Baixa
- Verifique conexão de internet
- Modelos são baixados automaticamente na primeira execução
- Podem ocupar ~500MB

### Streamlit não Inicia
```bash
# Reinstale Streamlit
pip uninstall streamlit
pip install streamlit
```

---

## 🧪 Testes

### Executar Testes Unitários (Opcional)
```bash
pytest tests/ -v
```

### Testar Módulo Específico
```bash
python -m pytest tests/test_face_detector.py
```

---

## 📊 Performance

### Tempo Médio de Processamento
- Detecção facial: ~0.5-2s
- Alinhamento: ~0.1s
- Envelhecimento: ~1-3s
- Embeddings: ~1-2s
- Comparação: ~0.1s
- **Total**: ~3-8 segundos por análise

### Requisitos de Memória
- RAM: ~500MB-2GB (depende do modelo)
- GPU VRAM: ~1-2GB (se habilitado)

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Faça fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

---

## 📝 Licença

Este projeto é open source e está disponível sob a [MIT License](LICENSE).

---

## 👨‍💻 Autor

**Betto Esteves**
- GitHub: [@BettoEsteves](https://github.com/BettoEsteves)

---

## 🙏 Agradecimentos

- **InsightFace**: Framework de reconhecimento facial
- **Streamlit**: Framework de interface web
- **OpenCV**: Biblioteca de Computer Vision
- **PyTorch**: Framework de Deep Learning

---

## 📚 Referências

- [InsightFace Documentation](https://github.com/deepinsight/insightface)
- [RetinaFace Paper](https://arxiv.org/abs/1905.00641)
- [FaceNet Paper](https://arxiv.org/abs/1503.03832)
- [Face Aging Survey](https://arxiv.org/abs/2010.01265)

---

## 📞 Suporte

Para questões e suporte:
- Abra uma [Issue no GitHub](https://github.com/BettoEsteves/Find-People/issues)
- Consulte a documentação em `docs/`

---

**⭐ Se este projeto foi útil, considere dar uma estrela no GitHub!**
