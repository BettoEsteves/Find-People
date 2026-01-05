# Como Conectar ao GitHub

O repositório Git local foi inicializado com sucesso. Siga os passos abaixo para criar o repositório no GitHub e fazer o push.

## Opção 1: Via GitHub CLI (gh)

Se você tem o GitHub CLI instalado:

```bash
cd E:\Projetos\FindPeople
gh auth login
gh repo create Find-People --public --source=. --description "Face Aging Simulation & Identity Verification System using Deep Learning and Computer Vision" --push
```

## Opção 2: Via Navegador (Recomendado)

### Passo 1: Criar Repositório no GitHub

1. Acesse: https://github.com/new
2. Preencha:
   - **Repository name**: `Find-People`
   - **Description**: `Face Aging Simulation & Identity Verification System using Deep Learning and Computer Vision`
   - **Visibility**: Public
   - **NÃO** marque "Initialize this repository with:"
     - Não adicione README
     - Não adicione .gitignore
     - Não adicione license
3. Clique em **Create repository**

### Passo 2: Conectar e Push

Após criar o repositório, o GitHub mostrará instruções. Execute:

```bash
cd E:\Projetos\FindPeople
git remote add origin https://github.com/BettoEsteves/Find-People.git
git push -u origin main
```

**OU** se você usa SSH:

```bash
cd E:\Projetos\FindPeople
git remote add origin git@github.com:BettoEsteves/Find-People.git
git push -u origin main
```

## Verificar

Após o push, acesse:
https://github.com/BettoEsteves/Find-People

Você deve ver todos os arquivos do projeto.

## Próximos Commits

Depois de configurado, para futuros commits:

```bash
cd E:\Projetos\FindPeople
git add .
git commit -m "Sua mensagem de commit"
git push
```

## Problemas de Autenticação

### Token de Acesso Pessoal (PAT)

Se você não configurou autenticação, precisará criar um Personal Access Token:

1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token (classic)
3. Selecione escopos: `repo`, `workflow`
4. Copie o token (você não verá novamente!)
5. Use o token como senha quando fazer git push

### SSH (Alternativa)

1. Gere chave SSH: `ssh-keygen -t ed25519 -C "seu-email@example.com"`
2. Copie a chave pública: `cat ~/.ssh/id_ed25519.pub`
3. GitHub → Settings → SSH and GPG keys → New SSH key
4. Cole a chave pública

## Status Atual

✅ Repositório Git inicializado
✅ Todos os arquivos commitados
✅ Branch main criado
⏳ Aguardando conexão com GitHub remoto

Execute os comandos acima para completar o setup!
