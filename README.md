# Luna-IA
**Logical Unified Neural Assistant**

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Status](https://img.shields.io/badge/Status-Active-success)
![License](https://img.shields.io/badge/License-MIT-green)

### Luna é uma assistente modular com duas versões distintas:
Uma **IA Básica** (offline) e uma **IA Online** (avançada).

Escolha qual versão usar dependendo da necessidade de performance, privacidade ou integração.

---

# 1. Luna IA Básica (Offline)
Arquivo: `luna02.py`

**A versão essencial da Luna — simples, rápida e voltada para privacidade total.**

## Recursos
- 100% local, sem internet
- Usa modelos do Ollama (LLaMA, Gemma, Qwen, Phi, etc.)
- Memória simples: fatos, preferências, estatísticas
- TTS integrado usando **edge-tts + pygame**
- Interface minimalista em terminal
- Baixo consumo de recursos

## Como executar
### 1. Inicie o Ollama
```
ollama serve
```
### 2. Baixe ou carregue o modelo desejado
```
ollama run llama3
```
### 3. Execute a Luna Básica
```
python luna02.py
```
---
# 2. Luna IA Online (Avançada + Groq)
Arquivo: `luna04.py`

**A versão completa da Luna — interface aprimorada, navegação de arquivos, leitura de PDFs e muito
mais.**

## Recursos
- Modelos Groq ultrarrápidos (LLaMA 3.3, Mixtral, Gemma, etc.)
- Memória profunda por usuário
- Perfis múltiplos
- Navegador de arquivos integrado
- Leitura de arquivos: TXT, MD, JSON, CSV, LOG, PY, JS, HTML, CSS, PDF, DOCX
- Sistema avançado de contexto
- Anexos durante a conversa
- Troca dinâmica de modelos
- TTS integrado
- Boot animado estilo *neural terminal*

# Dependências
Arquivo: `requirements.txt`
```
numpy
pyfiglet
pygame
edge-tts
requests
PyPDF2
python-docx
```
---
## Como executar
Luna04.py é a versão Online da Luna, que usa a API da Groq.
Então você precisa:
✔ Python instalado
✔ Dependências instaladas
✔ Uma Groq API Key
✔ Executar o script corretamente

Vamos lá:

## 1. Instalar o Python (se ainda não tiver)
#### Windows

Baixar: https://www.python.org/downloads/

Muito importante: marcar Add Python to PATH

Concluir instalação

#### Linux (Ubuntu / Pop!_OS / Debian)
```
sudo apt update
sudo apt install python3 python3-pip -y
```
## 2. Baixar/entrar na pasta do projeto

Se você baixou o ZIP:

Windows:
```
cd C:\Users\SEU_NOME_DE_USUARIO\Downloads\Luna
```
**Lembre-se de substituir o SEU_NOME_DE_USUARIO**

Linux:
```
cd ~/Downloads/Luna
```

Verifique se os arquivos estão lá:
```
ls
```

Deve aparecer:

luna04.py
prompt.txt
requirements.txt

## 3. Instalar as dependências

No terminal (Windows CMD, PowerShell, ou Linux):
```
pip install -r requirements.txt
```

Isso instala:

```
numpy

pygame

edge-tts

requests

PyPDF2

python-docx

pyfiglet
```

⚠ Se der erro no pygame no Linux, instale:
```
sudo apt install python3-dev libasound2-dev libportaudio2 libportaudiocpp0 ffmpeg -y
```

## 4. Criar sua API KEY da Groq

Acesse:
🔗 https://console.groq.com/keys

Clique em Create API Key

Copie a chave (ex: gsk_abcd1234...)

Você vai colar essa chave quando abrir o Luna04.py, no menu:

Configurações → API Key

## 5. Executar o Luna04.py

No terminal dentro da pasta do projeto:

#### Windows
python luna04.py

#### Linux
python3 luna04.py

## 6. Primeira execução — o Luna vai pedir isso:
✔ 1. Seu nome de usuário

Aparece:
```
>>> Digite seu nome de usuário:
```
✔ 2. Configurar API KEY

No menu principal:
```
2 → Configurações
1 → Configurar API Key
```

**Cole sua chave da Groq.**

Depois disso, a IA já funciona.

## 7. Usando o menu da IA

Menu inicial:
```
1. Iniciar IA
2. Configurações
0. Sair
```

Dentro de Iniciar IA:
```
1. Conversar
2. Histórico
3. Comandos
4. Trocar Modelo
5. Toggle TTS
```
Para conversar:
```
>>> /lembrar algo importante
>>> /preferencia tema = futurista
>>> /anexar
```

## 🛠️ 8. Problemas comuns e soluções rápidas
### ❌ Erro: No module named pygame

→ Instalar:

pip install pygame

### ❌ Erro com TTS

→ Instalar FFmpeg:
#### Linux:

sudo apt install ffmpeg


#### Windows:
https://www.gyan.dev/ffmpeg/builds/

### ❌ Erro: Invalid Groq Key

→ Verifique:

Sem espaços extras

Sem aspas

Key ativa na sua conta Groq

### ❌ Tela do Luna sem cores no Windows PowerShell

Use o CMD tradicional ou o terminal do VSCode.

### 9. Teste rápido para confirmar que tudo está OK

Digite na IA:
```
Olá Luna, o sistema está funcionando?
```

Se ela te responder fluido e rápido → Setup concluído com sucesso.

---

# Comandos disponíveis
| Comando | Função |
|--------|--------|
| `/lembrar [texto]` | Salva fato importante |
| `/preferencia chave = valor` | Define preferências |
| `/stats` | Estatísticas do usuário |
| `/anexar` | Abre o navegador de arquivos (IA Online) |
| `/limpar_anexos` | Remove todos os anexos |
| `sair` | Volta ao menu |
---
# Estrutura do Projeto
```
Luna/
 luna04.py # IA Online (Groq)
 luna02.py # IA Básica Offline
 prompt.txt
 requirements.txt
 README.md
```
---
# Filosofia

**Controle total. Código claro. Zero enrolação.**

---
# Desenvolvido por
**Calebe Andrade (Calebe Dev)**
 caleberandradep@gmail.com
