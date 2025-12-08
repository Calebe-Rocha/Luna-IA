import numpy as np
import time
import pygame
import json
import os
import hashlib
from datetime import datetime
import asyncio
import edge_tts
from groq import Groq
import sys
from pathlib import Path

# ==================== CONFIGURAÇÕES DE COR ====================
class Cores:
    RESET = '\033[0m'
    VERDE = '\033[92m'
    VERDE_ESCURO = '\033[32m'
    CIANO = '\033[96m'
    AMARELO = '\033[93m'
    VERMELHO = '\033[91m'
    ROXO = '\033[95m'
    BRANCO = '\033[97m'
    
    # Efeitos
    BOLD = '\033[1m'
    DIM = '\033[2m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    
    # Background
    BG_PRETO = '\033[40m'
    BG_VERDE = '\033[42m'

# ==================== ARTE ASCII ====================
ASCII_ART = {
    "logo": f"""{Cores.VERDE}{Cores.BOLD}
    ╦  ╦ ╦ ╔╗╔ ╔═╗   ╔═╗ ╦   
    ║  ║ ║ ║║║ ╠═╣   ╠═╣ ║   
    ╩═╝╚═╝ ╝╚╝ ╩ ╩   ╩ ╩ ╩   
    ═══════════════════════════
    [ NEURAL INTERFACE v3.0 ]
{Cores.RESET}""",
    
    "skull": f"""{Cores.VERDE_ESCURO}
        ___
       /   \\
      | O O |
       \\ _ /
        |||
{Cores.RESET}""",
    
    "matrix": f"""{Cores.VERDE}
    ▓▒░ MATRIX MODE ░▒▓
{Cores.RESET}""",
}

# ==================== EFEITOS VISUAIS ====================
def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{Cores.BG_PRETO}", end='')

def linha_hacker(tamanho=60, char="═"):
    return f"{Cores.VERDE_ESCURO}{char * tamanho}{Cores.RESET}"

def linha_neon(tamanho=60, char="─"):
    return f"{Cores.CIANO}{Cores.BOLD}{char * tamanho}{Cores.RESET}"

def titulo_secao(texto):
    print(f"\n{Cores.CIANO}{Cores.BOLD}╔{'═' * (len(texto) + 2)}╗")
    print(f"║ {texto} ║")
    print(f"╚{'═' * (len(texto) + 2)}╝{Cores.RESET}\n")

def print_hacker(texto, cor=Cores.VERDE):
    print(f"{cor}┃ {texto}{Cores.RESET}")

def animacao_typing(texto, cor=Cores.VERDE, delay=0.03):
    for char in texto:
        print(f"{cor}{char}{Cores.RESET}", end='', flush=True)
        time.sleep(delay)
    print()

def animacao_loading(texto="PROCESSANDO", duracao=2):
    frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    end_time = time.time() + duracao
    i = 0
    while time.time() < end_time:
        frame = frames[i % len(frames)]
        print(f"\r{Cores.CIANO}{frame} {texto}...{Cores.RESET}", end='', flush=True)
        time.sleep(0.1)
        i += 1
    print(f"\r{Cores.VERDE}✓ {texto} COMPLETO{Cores.RESET}" + " " * 20)

def banner_boot():
    limpar_tela()
    print(f"{Cores.VERDE_ESCURO}")
    print("█" * 70)
    print("█" + " " * 68 + "█")
    print(f"█{' ' * 15}{Cores.VERDE}{Cores.BOLD}INICIANDO SISTEMA LUNA AI{Cores.VERDE_ESCURO}{' ' * 15}█")
    print("█" + " " * 68 + "█")
    print("█" * 70)
    print(Cores.RESET)
    
    mensagens = [
        "Inicializando kernel neural...",
        "Carregando módulos de IA...",
        "Estabelecendo conexão segura...",
        "Sistema pronto.",
    ]
    
    for msg in mensagens:
        animacao_loading(msg, 0.8)
        time.sleep(0.3)
    
    time.sleep(0.5)

# ==================== NAVEGADOR DE ARQUIVOS ====================
class NavegadorArquivos:
    def __init__(self):
        self.dir_atual = Path.cwd()
        self.historico = []
        
        # Extensões suportadas
        self.text_ext = {".txt", ".md", ".json", ".csv", ".log", ".py", ".js", ".html", ".css"}
        self.doc_ext = {".pdf", ".docx"}
        self.all_ext = self.text_ext | self.doc_ext
    
    def listar_conteudo(self):
        """Lista diretórios e arquivos do diretório atual"""
        try:
            itens = list(self.dir_atual.iterdir())
            
            # Separar diretórios e arquivos
            diretorios = sorted([i for i in itens if i.is_dir()], key=lambda x: x.name.lower())
            arquivos = sorted([i for i in itens if i.is_file()], key=lambda x: x.name.lower())
            
            return diretorios, arquivos
        except PermissionError:
            return [], []
    
    def formatar_tamanho(self, caminho):
        """Retorna tamanho formatado do arquivo"""
        try:
            tamanho = caminho.stat().st_size
            if tamanho < 1024:
                return f"{tamanho}B"
            elif tamanho < 1024 * 1024:
                return f"{tamanho / 1024:.1f}KB"
            else:
                return f"{tamanho / (1024 * 1024):.1f}MB"
        except:
            return "?"
    
    def eh_suportado(self, arquivo):
        """Verifica se arquivo é suportado"""
        return arquivo.suffix.lower() in self.all_ext
    
    def navegar(self):
        """Interface interativa de navegação"""
        while True:
            limpar_tela()
            
            # Cabeçalho
            print(ASCII_ART["logo"])
            titulo_secao("NAVEGADOR DE ARQUIVOS")
            
            # Caminho atual
            print(f"{Cores.CIANO}{Cores.BOLD}📂 LOCAL:{Cores.RESET} {Cores.VERDE}{self.dir_atual}{Cores.RESET}")
            print(linha_neon(70))
            
            diretorios, arquivos = self.listar_conteudo()
            
            # Opções de navegação
            opcoes = []
            
            # Voltar diretório
            if self.dir_atual.parent != self.dir_atual:
                opcoes.append(("↩", "..", "Voltar", "DIR"))
            
            # Drives (Windows) ou raiz (Linux)
            if sys.platform == 'win32':
                opcoes.append(("🖥", "DRIVES", "Listar drives", "SPECIAL"))
            else:
                opcoes.append(("🖥", "/", "Ir para raiz", "SPECIAL"))
            
            # Adicionar diretórios
            for d in diretorios[:15]:  # Limitar visualização
                opcoes.append(("📁", d.name, "", "DIR"))
            
            # Adicionar arquivos suportados
            arquivos_suportados = [a for a in arquivos if self.eh_suportado(a)][:15]
            for a in arquivos_suportados:
                tamanho = self.formatar_tamanho(a)
                opcoes.append(("📄", a.name, tamanho, "FILE"))
            
            # Mostrar opções
            print(f"\n{Cores.VERDE}{Cores.BOLD}OPÇÕES:{Cores.RESET}")
            for idx, (icone, nome, info, tipo) in enumerate(opcoes, 1):
                if tipo == "DIR":
                    cor = Cores.CIANO
                elif tipo == "FILE":
                    cor = Cores.VERDE
                else:
                    cor = Cores.AMARELO
                
                info_str = f" ({info})" if info else ""
                print(f"{cor}  {idx:2d}. {icone} {nome}{info_str}{Cores.RESET}")
            
            # Comandos
            print(f"\n{linha_hacker(70, '─')}")
            print(f"{Cores.AMARELO}[0]{Cores.RESET} Cancelar  |  {Cores.AMARELO}[PATH]{Cores.RESET} Digitar caminho direto")
            print(linha_hacker(70, '─'))
            
            # Input
            escolha = input(f"\n{Cores.VERDE}{Cores.BOLD}>{Cores.RESET} ").strip()
            
            if not escolha or escolha == '0':
                return None
            
            # Caminho direto
            if os.path.exists(escolha):
                caminho = Path(escolha)
                if caminho.is_file() and self.eh_suportado(caminho):
                    return str(caminho)
                elif caminho.is_dir():
                    self.historico.append(self.dir_atual)
                    self.dir_atual = caminho
                    continue
                else:
                    print(f"{Cores.VERMELHO}✗ Arquivo não suportado{Cores.RESET}")
                    time.sleep(1)
                    continue
            
            # Seleção por número
            if escolha.isdigit():
                idx = int(escolha)
                if 1 <= idx <= len(opcoes):
                    icone, nome, info, tipo = opcoes[idx - 1]
                    
                    if nome == "..":
                        self.historico.append(self.dir_atual)
                        self.dir_atual = self.dir_atual.parent
                    elif nome == "DRIVES":
                        self.selecionar_drive()
                    elif nome == "/":
                        self.historico.append(self.dir_atual)
                        self.dir_atual = Path("/")
                    elif tipo == "DIR":
                        self.historico.append(self.dir_atual)
                        self.dir_atual = self.dir_atual / nome
                    elif tipo == "FILE":
                        return str(self.dir_atual / nome)
                else:
                    print(f"{Cores.VERMELHO}✗ Opção inválida{Cores.RESET}")
                    time.sleep(1)
            else:
                print(f"{Cores.VERMELHO}✗ Entrada inválida{Cores.RESET}")
                time.sleep(1)
    
    def selecionar_drive(self):
        """Seleção de drive no Windows"""
        if sys.platform != 'win32':
            return
        
        import string
        drives = [f"{d}:\\" for d in string.ascii_uppercase if os.path.exists(f"{d}:\\")]
        
        limpar_tela()
        titulo_secao("SELECIONAR DRIVE")
        
        for idx, drive in enumerate(drives, 1):
            print(f"{Cores.CIANO}  {idx}. {drive}{Cores.RESET}")
        
        escolha = input(f"\n{Cores.VERDE}Escolha (Enter para cancelar):{Cores.RESET} ").strip()
        
        if escolha.isdigit():
            idx = int(escolha)
            if 1 <= idx <= len(drives):
                self.historico.append(self.dir_atual)
                self.dir_atual = Path(drives[idx - 1])

# ==================== CLASSES PRINCIPAIS ====================
TEXT_EXTENSOES_SUPORTADAS = {".txt", ".md", ".json", ".csv", ".log"}
DOC_EXTENSOES_SUPORTADAS = {".pdf", ".docx"}

class GerenciadorConfig:
    def __init__(self, arquivo="config_luna.json"):
        self.arquivo = arquivo
        self.config = self.carregar_config()
    
    def _config_padrao(self):
        return {"perfil_ativo": None, "perfis": {}}
    
    def carregar_config(self):
        if os.path.exists(self.arquivo):
            try:
                with open(self.arquivo, "r", encoding="utf-8") as arquivo:
                    dados = json.load(arquivo)
                    if "perfil_ativo" in dados and "perfis" in dados:
                        return dados
            except Exception as e:
                print_hacker(f"Aviso: Não foi possível ler {self.arquivo}: {e}", Cores.AMARELO)
        return self._config_padrao()
    
    def salvar_config(self):
        try:
            with open(self.arquivo, "w", encoding="utf-8") as arquivo:
                json.dump(self.config, arquivo, indent=2, ensure_ascii=False)
        except Exception as e:
            print_hacker(f"Aviso: Não foi possível salvar {self.arquivo}: {e}", Cores.AMARELO)
    
    def garantir_perfil(self, nome):
        perfis = self.config.setdefault("perfis", {})
        if nome not in perfis:
            perfis[nome] = {"api_key": None, "tts_ativo": True}
            self.salvar_config()
        return perfis[nome]
    
    def definir_perfil_ativo(self, nome):
        self.config["perfil_ativo"] = nome
        self.garantir_perfil(nome)
        self.salvar_config()
    
    def obter_perfil(self, nome):
        return self.config.get("perfis", {}).get(nome)
    
    def listar_perfis(self):
        return sorted(self.config.get("perfis", {}).keys())
    
    def atualizar_api_key(self, nome, api_key):
        perfil = self.garantir_perfil(nome)
        perfil["api_key"] = api_key
        self.salvar_config()
    
    def atualizar_status_tts(self, nome, ativo):
        perfil = self.garantir_perfil(nome)
        perfil["tts_ativo"] = ativo
        self.salvar_config()

class MemoriaLuna:
    def __init__(self, usuario=""):
        self.usuario = usuario
        self.arquivo_memoria = f"memoria_{usuario}.json" if usuario else "memoria_global.json"
        self.arquivo_contexto = f"contexto_{usuario}.json" if usuario else "contexto_global.json"
        self.memoria = self.carregar_memoria()
        self.contexto_atual = self.carregar_contexto()
        
    def carregar_memoria(self):
        if os.path.exists(self.arquivo_memoria):
            try:
                with open(self.arquivo_memoria, "r", encoding="utf-8") as arquivo:
                    return json.load(arquivo)
            except:
                return self.criar_memoria_vazia()
        else:
            return self.criar_memoria_vazia()
    
    def criar_memoria_vazia(self):
        return {
            "conversas": [],
            "preferencias": {},
            "fatos_importantes": [],
            "contexto_longo_prazo": {},
            "personalidade": {
                "tom": "amigável e prestativo",
                "estilo": "direto e claro",
                "restricoes": []
            },
            "estatisticas": {
                "total_conversas": 0,
                "primeira_interacao": None,
                "ultima_interacao": None,
                "temas_frequentes": {}
            }
        }
    
    def salvar_memoria(self):
        try:
            with open(self.arquivo_memoria, "w", encoding="utf-8") as arquivo:
                json.dump(self.memoria, arquivo, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao salvar memória: {e}")
    
    def carregar_contexto(self):
        if os.path.exists(self.arquivo_contexto):
            try:
                with open(self.arquivo_contexto, "r", encoding="utf-8") as arquivo:
                    return json.load(arquivo)
            except:
                return self.criar_contexto_vazio()
        else:
            return self.criar_contexto_vazio()
    
    def criar_contexto_vazio(self):
        return {
            "sessao_atual": [],
            "inicio_sessao": datetime.now().isoformat(),
            "temas_sessao": []
        }
    
    def salvar_contexto(self):
        try:
            with open(self.arquivo_contexto, "w", encoding="utf-8") as arquivo:
                json.dump(self.contexto_atual, arquivo, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao salvar contexto: {e}")

    def apagar_memoria_e_contexto(self):
        removidos = []
        for caminho in [self.arquivo_memoria, self.arquivo_contexto]:
            if os.path.exists(caminho):
                try:
                    os.remove(caminho)
                    removidos.append(caminho)
                except Exception as e:
                    print(f"Erro ao excluir {caminho}: {e}")
        self.memoria = self.criar_memoria_vazia()
        self.contexto_atual = self.criar_contexto_vazio()
        return removidos
    
    def adicionar_conversa(self, pergunta, resposta, categoria="geral"):
        conversa = {
            "id": self.gerar_id_conversa(pergunta),
            "timestamp": datetime.now().isoformat(),
            "usuario": self.usuario,
            "pergunta": pergunta,
            "resposta": resposta,
            "categoria": categoria,
            "importancia": self.calcular_importancia(pergunta, resposta)
        }
        
        self.memoria["conversas"].append(conversa)
        self.contexto_atual["sessao_atual"].append(conversa)
        self.atualizar_estatisticas(categoria)
        self.salvar_memoria()
        self.salvar_contexto()
        self.limpar_contexto_sessao()
        return conversa["id"]
    
    def gerar_id_conversa(self, pergunta):
        timestamp = str(time.time())
        texto = f"{pergunta}_{timestamp}_{self.usuario}"
        return hashlib.md5(texto.encode()).hexdigest()[:8]
    
    def calcular_importancia(self, pergunta, resposta):
        palavras_importantes = ["lembrar", "importante", "não esquecer", "sempre", "nunca", 
                              "prefiro", "gosto", "amo", "odeio", "família", "trabalho"]
        
        texto_completo = f"{pergunta} {resposta}".lower()
        importancia = 1
        
        for palavra in palavras_importantes:
            if palavra in texto_completo:
                importancia += 1
        
        return min(importancia, 10)
    
    def atualizar_estatisticas(self, categoria):
        stats = self.memoria["estatisticas"]
        stats["total_conversas"] += 1
        stats["ultima_interacao"] = datetime.now().isoformat()
        
        if stats["primeira_interacao"] is None:
            stats["primeira_interacao"] = datetime.now().isoformat()
        
        if categoria in stats["temas_frequentes"]:
            stats["temas_frequentes"][categoria] += 1
        else:
            stats["temas_frequentes"][categoria] = 1
    
    def buscar_conversas_relacionadas(self, pergunta, limite=3):
        palavras_chave = pergunta.lower().split()
        conversas_relacionadas = []
        
        for conversa in self.memoria["conversas"]:
            pontuacao = 0
            texto_conversa = f"{conversa['pergunta']} {conversa['resposta']}".lower()
            
            for palavra in palavras_chave:
                if len(palavra) > 2:
                    pontuacao += texto_conversa.count(palavra) * conversa["importancia"]
            
            if pontuacao > 0:
                conversas_relacionadas.append((conversa, pontuacao))
        
        conversas_relacionadas.sort(key=lambda x: x[1], reverse=True)
        return [conv[0] for conv in conversas_relacionadas[:limite]]
    
    def obter_contexto_para_ia(self, pergunta_atual):
        personalidade = self.memoria["personalidade"]
        
        contexto = f"""Você é Luna, uma assistente de IA {personalidade['tom']} conversando com {self.usuario}.
Estilo de comunicação: {personalidade['estilo']}

"""
        
        if self.contexto_atual["sessao_atual"]:
            contexto += "Histórico da conversa atual:\n"
            for conv in self.contexto_atual["sessao_atual"][-3:]:
                contexto += f"Usuário: {conv['pergunta']}\nVocê: {conv['resposta']}\n\n"
        
        if self.memoria["fatos_importantes"]:
            contexto += "Fatos importantes sobre o usuário:\n"
            for fato in self.memoria["fatos_importantes"][-3:]:
                contexto += f"- {fato['fato']}\n"
            contexto += "\n"
        
        if self.memoria["preferencias"]:
            contexto += "Preferências do usuário:\n" 
            for chave, valor in self.memoria["preferencias"].items():
                contexto += f"- {chave}: {valor}\n"
            contexto += "\n"
        
        relacionadas = self.buscar_conversas_relacionadas(pergunta_atual, 2)
        if relacionadas:
            contexto += "Conversas anteriores relevantes:\n"
            for conv in relacionadas:
                contexto += f"P: {conv['pergunta'][:80]}\nR: {conv['resposta'][:100]}\n\n"
        
        contexto += f"Pergunta atual: {pergunta_atual}"
        return contexto
    
    def adicionar_fato_importante(self, fato):
        fato_obj = {
            "fato": fato,
            "timestamp": datetime.now().isoformat(),
            "usuario": self.usuario
        }
        self.memoria["fatos_importantes"].append(fato_obj)
        self.salvar_memoria()
    
    def definir_preferencia(self, chave, valor):
        self.memoria["preferencias"][chave] = valor
        self.salvar_memoria()
    
    def obter_estatisticas(self):
        return self.memoria["estatisticas"]
    
    def limpar_contexto_sessao(self):
        if len(self.contexto_atual["sessao_atual"]) > 10:
            self.contexto_atual["sessao_atual"] = self.contexto_atual["sessao_atual"][-5:]
            self.salvar_contexto()

class TTSRapido:
    def __init__(self, habilitado=True):
        pygame.mixer.init()
        self.voz = "pt-BR-FranciscaNeural"
        self.habilitado = habilitado
    
    async def _gerar_audio(self, texto, arquivo="temp.mp3"):
        communicate = edge_tts.Communicate(texto, self.voz)
        await communicate.save(arquivo)
    
    def falar(self, texto):
        if not self.habilitado:
            return
            
        arquivo = "temp_tts.mp3"
        asyncio.run(self._gerar_audio(texto, arquivo))
        
        pygame.mixer.music.load(arquivo)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        
        try:
            os.remove(arquivo)
        except:
            pass
    
    def toggle(self):
        self.habilitado = not self.habilitado
        return self.habilitado

class IAGroq:
    def __init__(self, api_key=None, prompt_path="prompt.txt"):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        self.prompt_path = prompt_path
        self.prompt_text = self._carregar_prompt()
        
        if not self.api_key:
            print_hacker("⚠️  AVISO: Chave API do Groq não encontrada!", Cores.AMARELO)
            print_hacker("Configure a variável de ambiente GROQ_API_KEY", Cores.AMARELO)
            print_hacker("Obtenha em: https://console.groq.com/keys", Cores.CIANO)
        
        self.client = Groq(api_key=self.api_key) if self.api_key else None
        
        self.modelos = {
            "1": {"nome": "llama-3.3-70b-versatile", "desc": "Llama 3.3 70B - Mais inteligente"},
            "2": {"nome": "llama-3.1-8b-instant", "desc": "Llama 3.1 8B - Rápido"},
            "3": {"nome": "mixtral-8x7b-32768", "desc": "Mixtral 8x7B - Contexto grande"},
            "4": {"nome": "gemma2-9b-it", "desc": "Gemma 2 9B - Equilibrado"}
        }
        self.modelo_atual = "llama-3.3-70b-versatile"
    
    def _carregar_prompt(self):
        try:
            with open(self.prompt_path, "r", encoding="utf-8") as arquivo:
                conteudo = arquivo.read().strip()
                if conteudo:
                    return conteudo
        except:
            pass
        return "Você é Luna, uma assistente de IA inteligente e prestativa."
    
    def selecionar_modelo(self):
        limpar_tela()
        titulo_secao("SELEÇÃO DE MODELO")
        
        for key, modelo in self.modelos.items():
            marca = "►" if self.modelo_atual == modelo["nome"] else " "
            cor = Cores.CIANO if self.modelo_atual == modelo["nome"] else Cores.VERDE
            print(f"{cor}{marca} {key}. {modelo['desc']}{Cores.RESET}")
        
        print(f"\n{linha_hacker(60)}")
        escolha = input(f"{Cores.VERDE}Escolha (Enter para manter):{Cores.RESET} ").strip()
        
        if escolha in self.modelos:
            self.modelo_atual = self.modelos[escolha]["nome"]
            print(f"{Cores.VERDE}✓ Modelo alterado!{Cores.RESET}")
        
        time.sleep(1)
    
    def gerar_resposta(self, contexto, temperatura=0.7, max_tokens=2048):
        if not self.client:
            return "Erro: Cliente Groq não configurado."
        
        try:
            completion = self.client.chat.completions.create(
                model=self.modelo_atual,
                messages=[
                    {"role": "system", "content": self.prompt_text},
                    {"role": "user", "content": contexto}
                ],
                temperature=temperatura,
                max_tokens=max_tokens,
                top_p=0.95,
                stream=False
            )
            
            return completion.choices[0].message.content.strip()
            
        except Exception as e:
            return f"Erro: {e}"

def ler_anexo(caminho, limite_chars=4000):
    caminho = caminho.strip().strip('"').strip("'")
    if not caminho or not os.path.isfile(caminho):
        return False, "Arquivo não encontrado.", None

    _, ext = os.path.splitext(caminho)
    ext = ext.lower()

    if ext in TEXT_EXTENSOES_SUPORTADAS:
        try:
            with open(caminho, "r", encoding="utf-8", errors="ignore") as arquivo:
                conteudo = arquivo.read(limite_chars + 1)
        except Exception as e:
            return False, f"Erro: {e}", None

    elif ext == ".pdf":
        try:
            import PyPDF2
            leitor = PyPDF2.PdfReader(caminho)
            paginas = []
            for pagina in leitor.pages:
                paginas.append(pagina.extract_text() or "")
                if len("".join(paginas)) > limite_chars:
                    break
            conteudo = "".join(paginas)
        except ImportError:
            return False, "Instale PyPDF2: pip install PyPDF2", None
        except Exception as e:
            return False, f"Erro ao ler PDF: {e}", None

    elif ext == ".docx":
        try:
            import docx
            documento = docx.Document(caminho)
            conteudo = "\n".join(paragrafo.text for paragrafo in documento.paragraphs)
        except ImportError:
            return False, "Instale python-docx: pip install python-docx", None
        except Exception as e:
            return False, f"Erro: {e}", None
    else:
        return False, "Formato não suportado.", None

    if not conteudo or not conteudo.strip():
        return False, "Arquivo vazio.", None

    if len(conteudo) > limite_chars:
        conteudo = conteudo[:limite_chars] + "\n[Conteúdo truncado]"

    nome = os.path.basename(caminho)
    return True, f"Arquivo anexado: {nome}", {"nome": nome, "conteudo": conteudo}



# ==================== MAIN ====================
def main():
    # Boot sequence
    banner_boot()
    
    limpar_tela()
    print(ASCII_ART["logo"])
    titulo_secao("INICIALIZAÇÃO")
    
    config = GerenciadorConfig()
    pessoa = config.config.get("perfil_ativo")
    
    if pessoa:
        print_hacker(f"Perfil detectado: {pessoa}", Cores.CIANO)
        time.sleep(1)
    else:
        animacao_typing("\n>>> Digite seu nome de usuário: ", Cores.CIANO, 0.02)
        pessoa = input().strip() or "Anon"
        config.definir_perfil_ativo(pessoa)
    
    dados_perfil = config.garantir_perfil(pessoa)
    animacao_loading(f"Carregando perfil {pessoa}", 1.5)
    
    # Inicialização
    tts = TTSRapido(habilitado=dados_perfil.get("tts_ativo", True))
    ia = IAGroq(api_key=dados_perfil.get("api_key"))
    navegador = NavegadorArquivos()

    # Loop principal
    while True:
        limpar_tela()
        print(ASCII_ART["logo"])
        
        print(f"{Cores.CIANO}╔{'═' * 58}╗")
        print(f"║ USER: {pessoa:<50} ║")
        print(f"╚{'═' * 58}╝{Cores.RESET}\n")
        
        print(f"{Cores.VERDE}{Cores.BOLD}MENU PRINCIPAL{Cores.RESET}")
        print(linha_hacker(60))
        print(f"{Cores.VERDE}  [1]{Cores.RESET} Iniciar IA")
        print(f"{Cores.VERDE}  [2]{Cores.RESET} Configurações")
        print(f"{Cores.VERMELHO}  [0]{Cores.RESET} Sair")
        print(linha_hacker(60))
        
        escolha = input(f"\n{Cores.CIANO}>>> {Cores.RESET}").strip()

        # IA
        if escolha == "1":
            if not ia.client:
                limpar_tela()
                print(f"{Cores.VERMELHO}{Cores.BOLD}⚠️  ACESSO NEGADO{Cores.RESET}")
                print_hacker("Configure a API Key em Configurações (opção 2 → 1)", Cores.AMARELO)
                time.sleep(3)
                continue
            
            while True:
                limpar_tela()
                
                # Cabeçalho IA
                print(f"{Cores.VERDE}{Cores.BOLD}")
                print("╔════════════════════════════════════════════════════════╗")
                print("║              LUNA AI - NEURAL INTERFACE               ║")
                print("╚════════════════════════════════════════════════════════╝")
                print(Cores.RESET)
                
                print(f"{Cores.CIANO}┌─[{pessoa}@LUNA]")
                print(f"├─[Modelo: {ia.modelo_atual}]")
                print(f"└─[TTS: {'ON' if tts.habilitado else 'OFF'}]{Cores.RESET}\n")
                
                print(f"{Cores.VERDE}{Cores.BOLD}OPÇÕES:{Cores.RESET}")
                print(f"{Cores.VERDE}  [1]{Cores.RESET} Conversar")
                print(f"{Cores.VERDE}  [2]{Cores.RESET} Histórico")
                print(f"{Cores.VERDE}  [3]{Cores.RESET} Comandos")
                print(f"{Cores.VERDE}  [4]{Cores.RESET} Trocar Modelo")
                print(f"{Cores.VERDE}  [5]{Cores.RESET} Toggle TTS")
                print(f"{Cores.VERMELHO}  [0]{Cores.RESET} Voltar")
                print(linha_hacker(60))
                
                menu_escolha = input(f"\n{Cores.CIANO}>>> {Cores.RESET}").strip()
                
                if menu_escolha == "0":
                    break
                
                # Conversar
                elif menu_escolha == "1":
                    limpar_tela()
                    print(ASCII_ART["matrix"])
                    print(f"\n{Cores.VERDE}{Cores.BOLD}[MODO CONVERSA]{Cores.RESET}")
                    print(linha_neon(60))
                    print(f"{Cores.DIM}Comandos: /lembrar /preferencia /anexar /stats /sair{Cores.RESET}")
                    print(linha_neon(60))
                    
                    anexos_sessao = []
                    while True:
                        if anexos_sessao:
                            nomes = ", ".join(anexo["nome"] for anexo in anexos_sessao)
                            print(f"{Cores.AMARELO}[📎 {nomes}]{Cores.RESET}")

                        user_input = input(f"\n{Cores.CIANO}{pessoa}>{Cores.RESET} ").strip()
                        
                        if not user_input:
                            continue
                        
                        if user_input.lower() in ['/sair', 'sair', 'exit']:
                            break
                        
                        # Comandos especiais
                        if user_input.lower().startswith('/lembrar '):
                            fato = user_input[9:]
                            memoria = MemoriaLuna(pessoa)
                            memoria.adicionar_fato_importante(fato)
                            print(f"{Cores.VERDE}Luna> Memória atualizada!{Cores.RESET}")
                            continue
                        
                        elif user_input.lower().startswith('/preferencia '):
                            try:
                                partes = user_input[13:].split(' = ')
                                if len(partes) == 2:
                                    chave, valor = partes[0].strip(), partes[1].strip()
                                    memoria = MemoriaLuna(pessoa)
                                    memoria.definir_preferencia(chave, valor)
                                    print(f"{Cores.VERDE}Luna> Preferência salva: {chave} = {valor}{Cores.RESET}")
                                else:
                                    print(f"{Cores.AMARELO}Luna> Use: /preferencia chave = valor{Cores.RESET}")
                            except:
                                print(f"{Cores.AMARELO}Luna> Formato inválido{Cores.RESET}")
                            continue
                        
                        elif user_input.lower() == '/stats':
                            memoria = MemoriaLuna(pessoa)
                            stats = memoria.obter_estatisticas()
                            print(f"\n{Cores.CIANO}╔═══ ESTATÍSTICAS ═══╗{Cores.RESET}")
                            print(f"{Cores.VERDE}├─ Conversas: {stats['total_conversas']}")
                            if stats['primeira_interacao']:
                                print(f"├─ Primeira: {stats['primeira_interacao'][:10]}")
                            if stats['temas_frequentes']:
                                print(f"└─ Temas: {list(stats['temas_frequentes'].keys())}{Cores.RESET}")
                            continue

                        elif user_input.lower() == '/anexar':
                            caminho = navegador.navegar()
                            if caminho:
                                animacao_loading("Processando arquivo")
                                sucesso, mensagem, anexo = ler_anexo(caminho)
                                print(f"{Cores.VERDE}Luna> {mensagem}{Cores.RESET}")
                                if sucesso and anexo:
                                    anexos_sessao.append(anexo)
                            continue

                        elif user_input.lower() == '/limpar_anexos':
                            anexos_sessao.clear()
                            print(f"{Cores.VERDE}Luna> Anexos removidos{Cores.RESET}")
                            continue
                        
                        # Pergunta normal
                        memoria = MemoriaLuna(pessoa)
                        contexto_completo = memoria.obter_contexto_para_ia(user_input)
                        
                        if anexos_sessao:
                            contexto_completo += "\n\nArquivos anexados:\n"
                            for anexo in anexos_sessao:
                                contexto_completo += f"[{anexo['nome']}]\n{anexo['conteudo']}\n---\n"
                        
                        try:
                            animacao_loading("Processando", 0.5)
                            resposta = ia.gerar_resposta(contexto_completo)
                            memoria.adicionar_conversa(user_input, resposta)
                            
                            print(f"\n{Cores.VERDE}{Cores.BOLD}Luna>{Cores.RESET} ", end='')
                            animacao_typing(resposta, Cores.VERDE, 0.01)
                            print()
                            
                            try:
                                tts.falar(resposta)
                            except:
                                pass
                                
                        except Exception as e:
                            print(f"{Cores.VERMELHO}✗ Erro: {e}{Cores.RESET}")
                
                # Histórico
                elif menu_escolha == "2":
                    limpar_tela()
                    titulo_secao("HISTÓRICO DE CONVERSAS")
                    
                    memoria = MemoriaLuna(pessoa)
                    conversas = memoria.memoria["conversas"]
                    
                    if conversas:
                        for conv in conversas[-10:]:
                            data = conv['timestamp'][:16].replace('T', ' ')
                            print(f"{Cores.CIANO}[{data}]{Cores.RESET}")
                            print(f"{Cores.VERDE}Você: {conv['pergunta'][:70]}{Cores.RESET}")
                            print(f"{Cores.VERDE}Luna: {conv['resposta'][:100]}...{Cores.RESET}")
                            print(linha_hacker(60, '─'))
                    else:
                        print_hacker("Nenhuma conversa encontrada", Cores.AMARELO)
                    
                    input(f"\n{Cores.VERDE}[Enter para continuar]{Cores.RESET}")

                # Comandos
                elif menu_escolha == "3":
                    limpar_tela()
                    titulo_secao("COMANDOS DISPONÍVEIS")
                    
                    comandos = [
                        ("/lembrar [fato]", "Salva fato importante"),
                        ("/preferencia [chave] = [valor]", "Define preferência"),
                        ("/anexar", "Navegador de arquivos"),
                        ("/limpar_anexos", "Remove anexos"),
                        ("/stats", "Estatísticas"),
                        ("/sair", "Sair da conversa"),
                    ]
                    
                    for cmd, desc in comandos:
                        print(f"{Cores.CIANO}{cmd:<35}{Cores.RESET} {Cores.VERDE}{desc}{Cores.RESET}")
                    
                    print(f"\n{linha_hacker(60)}")
                    input(f"{Cores.VERDE}[Enter para continuar]{Cores.RESET}")
                
                # Trocar modelo
                elif menu_escolha == "4":
                    ia.selecionar_modelo()
                
                # Toggle TTS
                elif menu_escolha == "5":
                    status = tts.toggle()
                    config.atualizar_status_tts(pessoa, status)
                    print(f"\n{Cores.VERDE}✓ TTS {'Ativado' if status else 'Desativado'}{Cores.RESET}")
                    time.sleep(1)
                    
                else:
                    print(f"{Cores.VERMELHO}✗ Opção inválida{Cores.RESET}")
                    time.sleep(1)
        
        # Configurações
        elif escolha == "2":
            while True:
                limpar_tela()
                titulo_secao("CONFIGURAÇÕES")
                print_hacker(f"Perfil ativo: {pessoa}", Cores.CIANO)
                print(linha_hacker(60))
                print(f"{Cores.VERDE}  [1]{Cores.RESET} Configurar API Key")
                print(f"{Cores.VERDE}  [2]{Cores.RESET} Trocar Perfil")
                print(f"{Cores.VERMELHO}  [3]{Cores.RESET} Excluir memória/contexto do perfil")
                print(f"{Cores.VERMELHO}  [0]{Cores.RESET} Voltar")
                print(linha_hacker(60))
                
                sub_escolha = input(f"\n{Cores.CIANO}>>> {Cores.RESET}").strip()
                
                # Voltar
                if sub_escolha == "0":
                    break
                
                # Configurar API
                elif sub_escolha == "1":
                    limpar_tela()
                    titulo_secao("CONFIGURAÇÃO API GROQ")
                    print_hacker("Obtenha sua chave em: https://console.groq.com/keys", Cores.CIANO)
                    print(linha_hacker(60))
                    
                    nova_key = input(f"\n{Cores.VERDE}API Key (Enter para cancelar): {Cores.RESET}").strip()
                    if nova_key:
                        ia = IAGroq(api_key=nova_key)
                        config.atualizar_api_key(pessoa, nova_key)
                        animacao_loading("Salvando configuração", 1)
                        print(f"{Cores.VERDE}✓ API Key configurada!{Cores.RESET}")
                    else:
                        print(f"{Cores.AMARELO}✗ Cancelado{Cores.RESET}")
                    time.sleep(2)
                
                # Trocar perfil
                elif sub_escolha == "2":
                    limpar_tela()
                    titulo_secao("GERENCIAR PERFIS")
                    
                    perfis = config.listar_perfis()
                    if perfis:
                        for idx, nome in enumerate(perfis, 1):
                            ativo = " ◄ ATIVO" if nome == pessoa else ""
                            print(f"{Cores.VERDE}  {idx}. {nome}{ativo}{Cores.RESET}")
                    else:
                        print_hacker("Nenhum perfil encontrado", Cores.AMARELO)
                    
                    print(f"\n{linha_hacker(60)}")
                    novo = input(f"{Cores.VERDE}Nome do perfil (Enter cancela): {Cores.RESET}").strip()
                    
                    if novo:
                        pessoa = novo
                        config.definir_perfil_ativo(novo)
                        dados_perfil = config.garantir_perfil(novo)
                        tts = TTSRapido(habilitado=dados_perfil.get("tts_ativo", True))
                        ia = IAGroq(api_key=dados_perfil.get("api_key"))
                        animacao_loading(f"Carregando perfil {novo}", 1)
                
                # Excluir memória/contexto do perfil ativo
                elif sub_escolha == "3":
                    limpar_tela()
                    titulo_secao("LIMPAR MEMÓRIA E CONTEXTO")
                    print_hacker(f"Perfil ativo: {pessoa}", Cores.CIANO)
                    print_hacker("Apenas os dados deste perfil serão removidos.", Cores.AMARELO)
                    confirmacao = input(f"\n{Cores.VERMELHO}Tem certeza? (s/N): {Cores.RESET}").strip().lower()
                    
                    if confirmacao in ["s", "sim", "y", "yes"]:
                        memoria = MemoriaLuna(pessoa)
                        removidos = memoria.apagar_memoria_e_contexto()
                        animacao_loading("Removendo dados", 1)
                        
                        if removidos:
                            print_hacker("Arquivos excluídos:", Cores.VERDE)
                            for caminho in removidos:
                                print(f"{Cores.VERDE}- {caminho}{Cores.RESET}")
                        else:
                            print_hacker("Nenhum arquivo encontrado para excluir", Cores.AMARELO)
                    else:
                        print(f"{Cores.AMARELO}✗ Operação cancelada{Cores.RESET}")
                    
                    time.sleep(2)
                
                else:
                    print(f"{Cores.VERMELHO}✗ Opção inválida{Cores.RESET}")
                    time.sleep(1)
        
        elif escolha == "0":
            limpar_tela()
            print(f"{Cores.VERDE}{Cores.BOLD}")
            print("╔════════════════════════════════════╗")
            print("║    ENCERRANDO SISTEMA LUNA...     ║")
            print("╚════════════════════════════════════╝")
            print(Cores.RESET)
            animacao_loading("Desconectando", 1)
            print(f"\n{Cores.CIANO}Até logo, {pessoa}!{Cores.RESET}\n")
            break

        else:
            print(f"{Cores.VERMELHO}✗ Opção inválida{Cores.RESET}")
            time.sleep(1)


if __name__ == "__main__":
    main()
