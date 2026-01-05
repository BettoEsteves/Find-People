"""
System Check Script for FaceAge Identity Analyzer
Verifica se todas as dependências estão instaladas corretamente
"""
import sys
from pathlib import Path

def print_header(text):
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def check_python_version():
    """Verificar versão do Python"""
    print_header("Verificando Python")
    version = sys.version_info
    print(f"Versão: {version.major}.{version.minor}.{version.micro}")

    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print("❌ ERRO: Python 3.10 ou superior é necessário!")
        return False
    else:
        print("✅ Versão do Python OK")
        return True

def check_dependencies():
    """Verificar dependências principais"""
    print_header("Verificando Dependências")

    dependencies = {
        'streamlit': 'Interface Web',
        'cv2': 'OpenCV - Processamento de Imagens',
        'torch': 'PyTorch - Deep Learning',
        'numpy': 'NumPy - Computação Numérica',
        'PIL': 'Pillow - Manipulação de Imagens',
        'sklearn': 'Scikit-learn - Machine Learning',
        'yaml': 'PyYAML - Configurações',
        'loguru': 'Loguru - Sistema de Logs'
    }

    all_ok = True
    for module, description in dependencies.items():
        try:
            __import__(module)
            print(f"✅ {description:40} OK")
        except ImportError:
            print(f"❌ {description:40} NÃO INSTALADO")
            all_ok = False

    return all_ok

def check_optional_dependencies():
    """Verificar dependências opcionais"""
    print_header("Verificando Dependências Opcionais")

    optional = {
        'insightface': 'InsightFace - Reconhecimento Facial',
        'facenet_pytorch': 'FaceNet - Reconhecimento Facial (alternativo)'
    }

    for module, description in optional.items():
        try:
            __import__(module)
            print(f"✅ {description:50} OK")
        except ImportError:
            print(f"⚠️  {description:50} NÃO INSTALADO")

def check_directories():
    """Verificar estrutura de diretórios"""
    print_header("Verificando Estrutura de Diretórios")

    required_dirs = [
        'config',
        'src/core',
        'src/utils',
        'data/uploads',
        'data/results',
        'models',
        'logs'
    ]

    all_ok = True
    for dir_path in required_dirs:
        full_path = Path(dir_path)
        if full_path.exists():
            print(f"✅ {dir_path:30} OK")
        else:
            print(f"❌ {dir_path:30} NÃO ENCONTRADO")
            all_ok = False

    return all_ok

def check_config():
    """Verificar arquivos de configuração"""
    print_header("Verificando Configuração")

    config_files = [
        'config/config.yaml',
        'requirements.txt',
        'app.py'
    ]

    all_ok = True
    for file_path in config_files:
        full_path = Path(file_path)
        if full_path.exists():
            size = full_path.stat().st_size
            print(f"✅ {file_path:30} OK ({size} bytes)")
        else:
            print(f"❌ {file_path:30} NÃO ENCONTRADO")
            all_ok = False

    return all_ok

def check_gpu():
    """Verificar disponibilidade de GPU"""
    print_header("Verificando GPU")

    try:
        import torch
        if torch.cuda.is_available():
            print(f"✅ GPU NVIDIA Disponível")
            print(f"   Dispositivo: {torch.cuda.get_device_name(0)}")
            print(f"   CUDA Versão: {torch.version.cuda}")
            print(f"   Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
        else:
            print("⚠️  GPU NVIDIA não disponível - usando CPU")
            print("   (GPU é opcional, mas acelera o processamento)")
    except:
        print("⚠️  PyTorch não instalado - não foi possível verificar GPU")

def main():
    """Executar todas as verificações"""
    print("\n" + "=" * 60)
    print("  FACEAGE IDENTITY ANALYZER - VERIFICAÇÃO DO SISTEMA")
    print("=" * 60)

    results = []

    results.append(("Python", check_python_version()))
    results.append(("Dependências", check_dependencies()))
    check_optional_dependencies()
    results.append(("Diretórios", check_directories()))
    results.append(("Configuração", check_config()))
    check_gpu()

    # Resumo
    print_header("RESUMO")

    all_passed = all(result[1] for result in results)

    for name, passed in results:
        status = "✅ OK" if passed else "❌ FALHOU"
        print(f"{name:20} {status}")

    print("\n" + "=" * 60)

    if all_passed:
        print("✅ SISTEMA PRONTO PARA EXECUÇÃO!")
        print("\nPara iniciar o aplicativo, execute:")
        print("  python run_app.bat")
        print("  OU")
        print("  streamlit run app.py")
    else:
        print("❌ PROBLEMAS ENCONTRADOS!")
        print("\nPara instalar dependências, execute:")
        print("  python install_dependencies.bat")
        print("  OU")
        print("  pip install -r requirements.txt")

    print("=" * 60 + "\n")

if __name__ == "__main__":
    main()
