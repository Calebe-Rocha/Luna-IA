# Luna-IA
**Logical Unified Neural Assistant**
Luna é uma assistente modular com duas versões distintas:
uma **IA Básica** (offline) e uma **IA Online** (avançada).
Escolha qual versão usar dependendo da necessidade de performance, privacidade ou integração.
---
# 1. Luna IA Básica (Offline)
Arquivo: `luna02.py`
A versão essencial da Luna — simples, rápida e voltada para privacidade total.
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
A versão completa da Luna — interface aprimorada, navegação de arquivos, leitura de PDFs e muito
mais.
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
## Como executar
```
python luna04.py
```
---
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
