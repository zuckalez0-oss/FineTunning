from google import genai
import os
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from colorama import Fore, Style, init


load_dotenv()
init(autoreset=True)
console = Console()

#=====Configuração do cliente Gemini======
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


SISTEM_PROMPT_BUILD = """
Você é um especialista em engenharia de prompts.

Sua função é transformar ideias brutas em prompts profissionais,
claros, estruturados e otimizados para IA.

Sempre responda em Markdown estruturado seguindo este modelo:

# 🎯 Objetivo
(explicação clara)

# 🧠 Contexto
(contexto expandido)

# 📌 Instruções
(lista clara de instruções)

# 📄 Formato de Saída
(especificar formato esperado)

# ⚠️ Restrições
(limitações e regras)

Não explique nada fora do Markdown.
"""
PROMPT_ANALISE_DADOS = """
Você é um especialista em prompts para análise de dados e inteligência analítica.

Transforme a ideia do usuário em um prompt técnico e estruturado.

Responda apenas em Markdown:

# 🎯 Objetivo da Análise
Defina claramente o problema analítico.

# 📊 Tipo de Dados Esperados
- Estruturados ou não estruturados
- Volume estimado
- Fonte

# 🔍 Metodologia Sugerida
- Estatística descritiva
- Correlação
- Regressão
- Clusterização
- Machine Learning (se aplicável)

# 🛠 Ferramentas ou Linguagem
Sugira Python, Pandas, SQL, Power BI, etc.

# 📈 Formato da Saída
- Tabelas
- Gráficos
- Insights estratégicos

# ⚠️ Restrições
Limitações técnicas ou premissas.

Não adicione explicações fora do Markdown.
"""
PROMPT_MACHINE_LEARNING = """
Você é um engenheiro de prompts especialista em Machine Learning.

Transforme a ideia do usuário em um prompt técnico detalhado.

Responda exclusivamente em Markdown:

# 🎯 Problema de ML
Classificação, regressão, clusterização, NLP etc.

# 📦 Definição do Dataset
- Tipo de dados
- Variáveis independentes
- Variável alvo

# 🔎 Pré-processamento Necessário
- Limpeza
- Normalização
- Encoding
- Balanceamento

# 🤖 Modelo Sugerido
Explique qual modelo usar e por quê.

# ⚙️ Métricas de Avaliação
Accuracy, F1-Score, RMSE, AUC etc.

# 🚀 Estratégia de Otimização
Validação cruzada, tuning de hiperparâmetros.

# 📄 Formato de Saída
Código estruturado + explicação técnica.

# ⚠️ Restrições
Limitações computacionais ou de dados.

Sem explicações fora do Markdown.
"""
PROMPT_TEXTO_CRIATIVO = """
Você é um especialista em prompts para geração criativa.

Transforme a ideia do usuário em um prompt artístico e detalhado.

Responda somente em Markdown:

# 🎨 Conceito Central
Explique a ideia principal.

# 🌍 Ambientação
Descreva cenário, época e atmosfera.

# 👤 Personagens (se houver)
Detalhes psicológicos e físicos.

# ✍️ Estilo Literário
Indique referências de estilo (ex: poético, épico, minimalista).

# 🎭 Emoção Dominante
Qual sentimento deve prevalecer.

# 📖 Estrutura Narrativa
Início, desenvolvimento e clímax.

# 📏 Limitações
Tamanho, formato ou restrições criativas.

Não escreva nada fora do Markdown.
"""
PROMPT_CONTEUDO = """
Você é um especialista em engenharia de prompts focado em criação de conteúdo.

Transforme a ideia do usuário em um prompt profissional altamente estruturado.

Responda EXCLUSIVAMENTE em Markdown seguindo este modelo:

# 🎯 Objetivo
Defina claramente o que deve ser criado.

# 👥 Público-Alvo
Descreva o público ideal.

# 🧠 Contexto
Explique cenário, nicho, plataforma e tom de voz.

# ✍️ Diretrizes de Escrita
- Estilo
- Emoção
- Estratégia (storytelling, persuasão, autoridade etc.)

# 📄 Estrutura do Conteúdo
Defina como o conteúdo deve ser organizado.

# 🚀 Elementos de Performance
- SEO (se aplicável)
- Gatilhos mentais
- CTA estratégico

# ⚠️ Restrições
Limitações de tamanho, linguagem ou regras específicas.

Não explique nada fora do Markdown.
"""

def gerar_prompt_build(ideia_usuario):
    resposta = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"{SISTEM_PROMPT_BUILD}\n\nIdeia do usuário:{ideia_usuario}"
    )
    return resposta.text
def gerar_prompt_analise_dados(ideia_usuario):
    resposta = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"{PROMPT_ANALISE_DADOS}\n\nIdeia do usuário:{ideia_usuario}"
    )
    return resposta.text
def gerar_prompt_machine_learning(ideia_usuario):
    resposta = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"{PROMPT_MACHINE_LEARNING}\n\nIdeia do usuário:{ideia_usuario}"
    )
    return resposta.text
def gerar_prompt_texto_criativo(ideia_usuario):
    resposta = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"{PROMPT_TEXTO_CRIATIVO}\n\nIdeia do usuário:{ideia_usuario}"
    )
    return resposta.text
def gerar_prompt_conteudo(ideia_usuario):
    resposta = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"{PROMPT_CONTEUDO}\n\nIdeia do usuário:{ideia_usuario}"
    )
    return resposta.text
def mostrar_menu():
    table = Table(title="🎯 PromptMaster")
    table.add_column("Opção",style="cyan")
    table.add_column("Descrição", style="magenta")
    table.add_row("1", "Prompt para construção de conteúdo")
    table.add_row("2", "Prompt para análise de dados")
    table.add_row("3", "Prompt para aprendizado de máquina")
    table.add_row("4", "Gerar texto criativo")
    table.add_row("5", "Gerar prompt para criação de conteúdo")
    table.add_row("0", "Sair")
    console.print(table)

print("Programa iniciado")
if __name__ =="__main__":
    while True:
        mostrar_menu()

        opcao = input("Escolha uma opção (1-5): ")
        match opcao:
            case "1":
                ideia=input("Digite sua ideia para construção: ")
                prompt_gerado = gerar_prompt_build(ideia)
                console.print("\nPrompt Gerado:\n")
                console.print(prompt_gerado)
            case "2":
                ideia=input("Digite sua ideia para análise de dados: ")
                prompt_gerado = gerar_prompt_analise_dados(ideia)
                console.print("\nPrompt Gerado:\n")
                console.print(prompt_gerado)
            case "3":
                ideia=input("Digite sua ideia para aprendizado de máquina: ")
                prompt_gerado = gerar_prompt_machine_learning(ideia)
                console.print("\nPrompt Gerado:\n")
                console.print(prompt_gerado)
            case "4":
                ideia=input("Digite sua ideia para texto criativo: ")
                prompt_gerado = gerar_prompt_texto_criativo(ideia)
                console.print("\nPrompt Gerado:\n")
                console.print(prompt_gerado)
            case "5":
                ideia=input("Digite sua ideia para criação de conteúdo: ")
                prompt_gerado = gerar_prompt_conteudo(ideia)
                console.print("\nPrompt Gerado:\n")
                console.print(prompt_gerado)
            case "0":
                console.print("[bold green]Encerrando o programa.[/bold green]")
                break
            case _:
                console.print("[bold red]Opção inválida. Por favor, escolha uma opção entre 0 e 5.[/bold red]")

        
 