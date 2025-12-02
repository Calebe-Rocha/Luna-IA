import numpy as np
import time
import pyfiglet
import pygame
import json
import os
import hashlib
from datetime import datetime
import asyncio
import edge_tts
import requests


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
        """Cria contexto simples para a IA"""
        contexto = f"Você é Luna, assistente amigável conversando com {self.usuario}.\n"
        
        # Fatos importantes
        if self.memoria["fatos_importantes"]:
            contexto += "Fatos importantes:\n"
            for fato in self.memoria["fatos_importantes"][-2:]:
                contexto += f"- {fato['fato']}\n"
        
        # Preferências
        if self.memoria["preferencias"]:
            contexto += "Preferências:\n" 
            for chave, valor in self.memoria["preferencias"].items():
                contexto += f"- {chave}: {valor}\n"
        
        contexto += f"\nPergunta: {pergunta_atual}"
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
        """Limpa contexto quando fica muito grande"""
        if len(self.contexto_atual["sessao_atual"]) > 10:
            # Manter apenas as 5 conversas mais recentes
            self.contexto_atual["sessao_atual"] = self.contexto_atual["sessao_atual"][-5:]
            self.salvar_contexto()


class TTSRapido:
    def __init__(self):
        pygame.mixer.init()
        self.voz = "pt-BR-FranciscaNeural"
    
    async def _gerar_audio(self, texto, arquivo="temp.mp3"):
        communicate = edge_tts.Communicate(texto, self.voz)
        await communicate.save(arquivo)
    
    def falar(self, texto):
        arquivo = "temp_tts.mp3"
        asyncio.run(self._gerar_audio(texto, arquivo))
        
        pygame.mixer.music.load(arquivo)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        
        # Limpar arquivo temporário
        try:
            os.remove(arquivo)
        except:
            pass  # Se não conseguir deletar, ignora


def main():
    # Solicita o nome do usuário no início
    print("=" * 60)
    print("Bem-vindo ao P.S.F.A - Luna AI Assistant")
    print("=" * 60)
    pessoa = input("\nPor favor, digite seu nome: ").strip()
    
    if not pessoa:
        pessoa = "Usuario"
    
    print(f"\nOlá, {pessoa}! Inicializando sistema...\n")
    time.sleep(1)
    
    # Inicializa TTS
    tts = TTSRapido()

    while True:
        # Limpa a tela (opcional)
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Define o titulo
        titulo = pyfiglet.figlet_format("P.S.F.A")

        # Printa o titulo
        print(titulo)
        print("=" * 60, "\n")

        # Printa as opções
        print("Opções: \n0. Sair\n1. Iniciar IA")

        # Cria a variavel escolha
        try:
            escolha = int(input("\nQual opção: "))
        except ValueError:
            print("Opção inválida! Digite apenas números.")
            time.sleep(2)
            continue

        # Se selecionar 1 vai para a ia
        if escolha == 1:
            
            while True:
                # Limpa a tela
                os.system('cls' if os.name == 'nt' else 'clear')
                
                # Printa e define o menu
                menu = pyfiglet.figlet_format("Luna")
                print(menu)
                print("=" * 60, "\n")
                
                # Printa a mensagem
                print(f"Você está no menu da IA (Usuário: {pessoa})\n")
                print("Opções:")
                print("0. Voltar ao menu principal")
                print("1. Conversar com a IA")
                print("2. Ver conversas anteriores")
                print("3. Comandos especiais")
                
                # Cria a variavel menu_escolha
                try:
                    menu_escolha = int(input("\nQual opção: "))
                except ValueError:
                    print("Opção inválida! Digite apenas números.")
                    time.sleep(2)
                    continue
                
                # Se selecionar 0 sai
                if menu_escolha == 0:
                    break
                
                elif menu_escolha == 1:
                    print("\n" + "=" * 60)
                    print("Digite 'sair' para voltar ao menu")
                    print("\nComandos especiais:")
                    print("  /lembrar [fato] - Salva um fato importante")
                    print("  /preferencia [chave] = [valor] - Define preferência")
                    print("  /stats - Mostra estatísticas")
                    print("=" * 60 + "\n")
                    
                    while True:
                        user_input = input("Você: ").strip()
                        
                        if not user_input:
                            continue
                        
                        if user_input.lower() in ['sair', 'exit', 'quit']:
                            break
                        
                        # Comandos especiais para memória
                        if user_input.lower().startswith('/lembrar '):
                            fato = user_input[9:]  # Remove '/lembrar '
                            memoria = MemoriaLuna(pessoa)
                            memoria.adicionar_fato_importante(fato)
                            print("Luna: Ok, vou lembrar disso!")
                            continue
                        
                        elif user_input.lower().startswith('/preferencia '):
                            try:
                                partes = user_input[13:].split(' = ')  # Remove '/preferencia '
                                if len(partes) == 2:
                                    chave, valor = partes[0].strip(), partes[1].strip()
                                    memoria = MemoriaLuna(pessoa)
                                    memoria.definir_preferencia(chave, valor)
                                    print(f"Luna: Anotado! {chave} = {valor}")
                                else:
                                    print("Luna: Use o formato /preferencia chave = valor")
                            except:
                                print("Luna: Use o formato /preferencia chave = valor")
                            continue
                        
                        elif user_input.lower() == '/stats':
                            memoria = MemoriaLuna(pessoa)
                            stats = memoria.obter_estatisticas()
                            print(f"\nEstatísticas de {pessoa}:")
                            print(f"- Total de conversas: {stats['total_conversas']}")
                            if stats['primeira_interacao']:
                                print(f"- Primeira interação: {stats['primeira_interacao'][:10]}")
                            if stats['temas_frequentes']:
                                print(f"- Temas mais frequentes: {list(stats['temas_frequentes'].keys())}")
                            print()
                            continue
                        
                        # Pergunta normal com memória
                        memoria = MemoriaLuna(pessoa)
                        contexto_completo = memoria.obter_contexto_para_ia(user_input)
                        
                        session = requests.Session()
                        url = 'http://localhost:11434/api/generate'
                        payload = {
                            'model': "Luna", 
                            'prompt': contexto_completo,
                            'stream': False,
                            'options': {
                                'temperature': 0.4,  # Controla criatividade
                                'top_p': 0.9,        # Controla foco
                                'repeat_penalty': 1.1 # Evita repetições
                            }
                        }

                        try:
                            response = session.post(url, json=payload, timeout=30)
                            if response.status_code == 200:
                                resposta = response.json()['response'].strip()
                                memoria.adicionar_conversa(user_input, resposta)
                                print(f"Luna: {resposta}\n")
                                
                                # Falar a resposta
                                try:
                                    tts.falar(resposta)
                                except Exception as e:
                                    print(f"[Aviso: Erro ao falar - {e}]")
                            else:
                                print(f"Erro: {response.status_code} - {response.text}")
                        except requests.exceptions.ConnectionError:
                            print("Erro: Não foi possível conectar ao Ollama. Verifique se está rodando.")
                        except requests.exceptions.Timeout:
                            print("Erro: Timeout na conexão com Ollama.")
                        except Exception as e:
                            print(f"Erro de conexão: {e}")
                        finally:
                            session.close()
            
                elif menu_escolha == 2:
                    memoria = MemoriaLuna(pessoa)
                    conversas = memoria.memoria["conversas"]
                    
                    print("\n" + "=" * 60)
                    if conversas:
                        print(f"Conversas Anteriores de {pessoa}:\n")
                        for conv in conversas[-10:]:  # Últimas 10 conversas
                            data = conv['timestamp'][:16].replace('T', ' ')
                            print(f"[{data}]")
                            print(f"Você: {conv['pergunta'][:70]}...")
                            print(f"Luna: {conv['resposta'][:100]}...")
                            print("-" * 60)
                    else:
                        print("Nenhuma conversa anterior encontrada.")
                    
                    print("=" * 60)
                    input("\nPressione Enter para voltar ao menu da IA...")

                elif menu_escolha == 3:
                    print("\n" + "=" * 60)
                    print("Comandos Especiais Disponíveis:")
                    print("-" * 60)
                    print("/lembrar [fato]")
                    print("  → Salva um fato importante sobre você")
                    print("\n/preferencia [chave] = [valor]")
                    print("  → Define uma preferência")
                    print("\n/stats")
                    print("  → Mostra suas estatísticas de uso")
                    print("\nEsses comandos funcionam durante a conversa com a IA.")
                    print("=" * 60)
                    input("\nPressione Enter para continuar...")
                    
                else:
                    print("Opção inválida!")
                    time.sleep(2)
                    
        elif escolha == 0:
            print("\nEncerrando sistema... Até logo!")
            break

        # Se não for nenhuma delas 
        else:
            print("Opção inválida. Escolha 0 ou 1.")
            time.sleep(2)


if __name__ == "__main__":
    main()