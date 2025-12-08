# Luna-IA

### Logical Unified Neural Assistant

Luna é uma assistente de IA modular desenvolvida para rodar localmente, com suporte a memória, TTS, integração com modelos Groq ou Ollama, histórico, anexos de arquivos e navegação via terminal.

O foco é ser leve, direta e fácil de integrar em projetos pessoais, bots e ferramentas automáticas.

📦 Arquitetura Atual do Projeto

O projeto possui duas versões da Luna, cada uma com objetivos diferentes:

## 1️⃣ luna04.py — Versão Avançada (Groq + TTS + Memória + Navegador)

#### 📌 Arquivo: luna04.py


Principais recursos

Interface estilo neural terminal animada

Integração com Groq API (LLama 3.3, Mixtral etc.)

Memória persistente por usuário

Contexto inteligente

Sistema de perfis

Navegador de arquivos interno (com leitura de PDFs, DOCX e textos)

TTS por edge-tts + pygame

Suporte a múltiplos modelos

Histórico navegável

Sistema de prompts via arquivo externo (prompt.txt)

Ideal para quem quer uma IA local avançada, mas ainda leve.

## 2️⃣ luna02.py — Versão Simples (Ollama Local + TTS)

#### 📌 Arquivo: luna02.py


Principais recursos

Conexão direta com Ollama (modelos locais como LLaMA, Gemma, Qwen etc.)

Memória simples (fatos, preferências, estatísticas)

Sistema básico de TTS

Interface minimalista em terminal

Sem dependência de API externa

Ideal para uso offline com modelos locais.

## ⚙️ Requisitos

### 📌 Arquivo: requirements.txt


Dependências
numpy
pyfiglet
pygame
edge-tts
requests
PyPDF2
python-docx

🔧 Instalação
1. Instalar dependências
pip install -r requirements.txt

## ▶️ Como Executar
Versão Avançada (Groq)

Requer chave da Groq:

Pegue em: https://console.groq.com/keys

No programa, vá em Configurações → API Key

python luna04.py

Versão Simples (Ollama)

Certifique-se de ter o Ollama rodando:

ollama serve
ollama run llama3


Execute:

python luna02.py

## 🧠 Como a Luna funciona (Resumo Técnico)
Memória

Ambas versões criam arquivos como:

memoria_usuario.json

contexto_usuario.json

Armazenam:

fatos importantes

preferências

estatísticas

últimas conversas

TTS

Usa:

edge-tts para gerar o áudio

pygame para tocar

Raciocínio da IA

luna04.py usa prompt-base em prompt.txt


luna02.py monta seu próprio contexto interno.

## 🗂️ Comandos Disponíveis
Em ambos os sistemas:
Comando	Função
/lembrar [texto]	Salva um fato importante
/preferencia chave = valor	Registra preferências
/stats	Estatísticas do usuário
/anexar (somente luna04)	Abre navegador de arquivos
/limpar_anexos	Remove anexos
sair	Volta ao menu
## 🌐 Modelos Suportados
Luna04 (via Groq):

llama-3.3-70b-versatile

llama-3.1-8b-instant

mixtral-8x7b

gemma2

Luna02 (via Ollama):

Qualquer modelo instalado localmente:

llama3

qwen2

gemma2

phi3

modelos personalizados

## 📁 Estrutura do Projeto
Luna/
├── luna04.py
├── luna02.py
├── prompt.txt
├── requirements.txt
└── README.md

## 🚀 Filosofia do Projeto

Simplicidade, velocidade e autonomia.
A Luna foi criada para ser uma assistente local, personalizada, com memória real e capacidade de operar sem depender da nuvem — a menos que você deseje.

## Desenvolvido por

Calebe Andrade (Calebe Dev)
📧 caleberandradep@gmail.com

🗓️ Desde 2025
