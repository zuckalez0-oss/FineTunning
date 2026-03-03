import os
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from colorama import Fore, Style, init
from google import genai
from supabase import create_client, Client
import datetime




import typer

load_dotenv()
init(autoreset=True)
console = Console()
app = typer.Typer() # verify
#===== inicializando gemini ======
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
##===== Inicializa Supabase ======
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
supabase:Client=create_client(SUPABASE_URL,SUPABASE_KEY)

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

def iniciar_sessao_banco():
    """Cria um usuario falso (para CLI) e inicia um novo projeto/sessao"""
    email_cli="cli@promptmaster.local"

    user_res = supabase.table("users").select("id").eq("email", email_cli).execute()
    if not user_res.data:
        user_res=supabase.table("users").insert({"email":email_cli}).execute()
    user_id=user_res.data[0]["id"]

    titulo = f"Sessão CLI - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    proj_res = supabase.table("projects").insert({
        "user_id":user_id,
        "title":titulo,
        "memory_sumary":"Nenhum resumo ainda"
    }).execute()

    project_id=proj_res.data[0]["id"]
    console.print(f"[bold green]Sessão iniciada com sucesso![/bold green] (ID: {project_id[:8]}...)")
    return project_id, proj_res.data[0]["memory_sumary"]
def salvar_mensagem(project_id:str, role:str, content:str):
    """Salva a mensagem no banco de dados"""
    supabase.table("promppts").insert({
        "project_id":project_id,
        "role":role,
        "content":content
    }).execute()
def buscar_ultima_mensagem(project_id:str):
    """Busca apenas a ultima troca de mensagens (User + Assistant) para economizar tokens e manter contexto recente"""
    res = supabase.table("prompts").select("*").eq("project_id",project_id).order("created_at", desc=True).limit(2).execute()

    if not res.data:
        return "nenhuma interação anterior"
    #inverter a ordem para ficar cronológica, (User --> Assistant)
    mensagens = reversed(res.data)
    contexto=""
    for msg in mensagens:
        papel = "Usuario" if msg["role"] == "user" else "IA"
        contexto += f"{papel}: {msg['content']}\n"

    return contexto
def gerar_resposta_com_contexto(project_id, memory_sumary,system_prompt, ideia_usuario):
    """
    Aplica a regra da imagem:
    1. Persona (System)
    2. Memory Summary
    3. Última interação
    4. Nova instrução
    """
    ultima_interacao = buscar_ultima_mensagem(project_id)
    prompt_final = f"""
    [PERSONA ATIVA]
    {system_prompt}

    [RESUMO DA MEMÓRIA]
    {memory_sumary}

    [ÚLTIMA INTERAÇÃO RELEVANTE]
    {ultima_interacao}

    [NOVA INSTRUÇÃO]
    {ideia_usuario}
    """
    resposta = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt_final
    )
    salvar_mensagem(project_id, "user", ideia_usuario)
    salvar_mensagem(project_id, "assistant", resposta.text)
    return resposta.text
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
    table = Table(title="🎯 PromptMaster (Conectado ao DB)")
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
        persona=""
        if opcao == "1":
            persona=SISTEM_PROMPT_BUILD
        elif opcao == "2":
            persona=PROMPT_ANALISE_DADOS
        elif opcao == "3":
            persona=PROMPT_ESPECIALISTA_SHEETS
        elif opcao == "4":
            persona=PROMPT_PROFESSOR_PROGRAMACAO
        elif opcao == "5":
            persona=PROMPT_CONTEUDO
        elif opcao == "0":
            console.print("[bold green]Encerrando o programa.[/bold green]")
            break
        else:
            console.print("[bold red]Opção inválida. Por favor, escolha uma opção entre 0 e 5.[/bold red]")
            continue
        ideia = input("Digite sua ideia: ")
        


        # match opcao:
        #     case "1":
        #         ideia=input("Digite sua ideia para construção: ")
        #         prompt_gerado = gerar_prompt_build(ideia)
        #         console.print("\nPrompt Gerado:\n")
        #         console.print(prompt_gerado)
        #     case "2":
        #         ideia=input("Digite sua ideia para análise de dados: ")
        #         prompt_gerado = gerar_prompt_analise_dados(ideia)
        #         console.print("\nPrompt Gerado:\n")
        #         console.print(prompt_gerado)
        #     case "3":
        #         ideia=input("Digite sua ideia para aprendizado de máquina: ")
        #         prompt_gerado = gerar_prompt_sheetmaster(ideia)
        #         console.print("\nPrompt Gerado:\n")
        #         console.print(prompt_gerado)
        #     case "4":
        #         ideia=input("Digite sua ideia para professor de programação: ")
        #         prompt_gerado = gerar_prompt_professor_programacao(ideia)
        #         console.print("\nPrompt Gerado:\n")
        #         console.print(prompt_gerado)
        #     case "5":
        #         ideia=input("Digite sua ideia para criação de conteúdo: ")
        #         prompt_gerado = gerar_prompt_conteudo(ideia)
        #         console.print("\nPrompt Gerado:\n")
        #         console.print(prompt_gerado)
        #     case "0":
        #         console.print("[bold green]Encerrando o programa.[/bold green]")
        #         break
        #     case _:
        #         console.print("[bold red]Opção inválida. Por favor, escolha uma opção entre 0 e 5.[/bold red]")

        
 