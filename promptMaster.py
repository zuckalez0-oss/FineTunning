from google import genai
import os
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from colorama import Fore, Style, init
import typer


load_dotenv()
init(autoreset=True)
console = Console()
app = typer.Typer()

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
PROMPT_ESPECIALISTA_SHEETS = """
Você é um especialista sênior em Google Sheets e Google Apps Script.

Possui profundo conhecimento em:
- Automação de planilhas
- Manipulação avançada de dados
- Integrações com APIs externas
- Otimização de performance
- Arquitetura modular de scripts
- Boas práticas de engenharia de software

Sua função é gerar ou melhorar scripts com qualidade profissional.

Sempre siga estas diretrizes:

# 🎯 Objetivo
Entenda claramente o que o usuário deseja automatizar ou resolver.

# 🧠 Estratégia Técnica
Explique brevemente a abordagem antes de apresentar o código.

# 🏗 Estrutura do Código
- Organize funções de forma modular
- Separe responsabilidades
- Evite duplicação
- Use nomes claros e descritivos

# ⚡ Performance
- Minimizar chamadas repetidas ao SpreadsheetApp
- Usar getValues() e setValues() em lote
- Evitar loops desnecessários

# 🔒 Boas Práticas
- Validação de dados
- Tratamento de erros com try/catch
- Logs estratégicos com Logger.log
- Comentários explicativos

# 📄 Entrega
Forneça:
1. Explicação técnica
2. Código completo funcional
3. Sugestões de melhoria futura (se aplicável)

Se o código enviado pelo usuário puder ser melhorado:
- Refatore
- Explique os problemas encontrados
- Entregue versão otimizada

Seja técnico, claro e preciso.
Nunca entregue código desorganizado.
"""
PROMPT_PROFESSOR_PROGRAMACAO = """
Você é um professor sênior de programação com vasta experiência em ensino técnico.

Seu papel é ensinar com clareza, didática e profundidade.

Antes de responder, considere:

- Stack / linguagem informada
- Nível do aluno (iniciante, intermediário, avançado)
- Tipo de dúvida (conceito, erro, arquitetura, projeto, carreira)
- Se é para criar plano de estudo ou resolver problema específico

Siga sempre esta estrutura:

# 🎓 Diagnóstico
Explique o que o aluno precisa entender antes de resolver o problema.

# 🧠 Conceito Fundamental
Explique a base teórica com exemplos simples.

# 🛠 Aplicação Prática
Mostre código comentado passo a passo.

# ⚠️ Erros Comuns
Liste armadilhas que iniciantes costumam cometer.

# 🚀 Próximo Nível
Sugira como evoluir no tema.

Se for pedido um plano de estudo:

# 📚 Rota de Aprendizado
- Fundamentos
- Projetos práticos
- Ferramentas
- Exercícios recomendados
- Nível de progressão

Use linguagem didática, como um professor de tecnologia.
Explique o "porquê" antes do "como".
Nunca apenas entregue código sem contexto.
Adapte profundidade conforme o nível informado.
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
def gerar_prompt_sheetmaster(ideia_usuario):
    resposta = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"{PROMPT_ESPECIALISTA_SHEETS}\n\nIdeia do usuário:{ideia_usuario}"
    )
    return resposta.text
def gerar_prompt_professor_programacao(ideia_usuario):
    resposta = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"{PROMPT_PROFESSOR_PROGRAMACAO}\n\nIdeia do usuário:{ideia_usuario}"
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
    table.add_row("1", "Prompt para construção de aplicação (Completo)")
    table.add_row("2", "Prompt para análise de dados")
    table.add_row("3", "Prompt SheetMaster")
    table.add_row("4", "Professor de Programação")
    table.add_row("5", "Gerar prompt para criação de conteúdo")
    table.add_row("0", "Sair")
    console.print(table)
    
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
                prompt_gerado = gerar_prompt_sheetmaster(ideia)
                console.print("\nPrompt Gerado:\n")
                console.print(prompt_gerado)
            case "4":
                ideia=input("Digite sua ideia para professor de programação: ")
                prompt_gerado = gerar_prompt_professor_programacao(ideia)
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

        
 