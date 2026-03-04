import os
import datetime

import typer
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from colorama import Fore, Style, init
from google import genai
from supabase import create_client, Client

#====Configs iniciais====
load_dotenv()
init(autoreset=True)
console = Console()
app = typer.Typer() 
#====verifica se a pasta de prompts existe, se não, cria====
PASTA_PROMPTS="meus_prompts"
if not os.path.exists(PASTA_PROMPTS):
    os.makedirs(PASTA_PROMPTS)
##==============================
##===== Iniciando Clients ======
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
supabase:Client=create_client(SUPABASE_URL,SUPABASE_KEY)
##==============================
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
    #1. verifica ou cria user
    user_res = supabase.table("users").select("id").eq("email", email_cli).execute()
    if not user_res.data:
        user_res=supabase.table("users").insert({"email":email_cli}).execute()

    user_id=user_res.data[0]["id"]
    titulo = f"Sessão CLI - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    #2. cria o projeto/sessao
    proj_res = supabase.table("projects").insert({
        "user_id":user_id,
        "title":titulo,
        "memory_summary":"Inicio da conversa"
    }).execute()
    project_id=proj_res.data[0]["id"]
    memory_summary=proj_res.data[0]["memory_summary"]
    console.print(f"[bold green]Sessão iniciada com sucesso![/bold green] (ID: {project_id[:8]})")
    return project_id, memory_summary

def salvar_mensagem(project_id:str, role:str, content:str): 
    """Salva a mensagem no banco de dados (tabela prompts)"""
    supabase.table("prompts").insert({
        "project_id":project_id,
        "role":role,
        "content":content
    }).execute()
    
def buscar_ultima_mensagem(project_id:str):
    """Busca as últimas interações para dar contexto à IA"""
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

def buscar_ultimo_resultado_ia(project_id:str):
    """Busca a ultima mensagem onde o papel era assistant (resposta da IA)"""
    res=supabase.table("prompts") \
        .select("content") \
        .eq("project_id", project_id) \
        .eq("role", "assistant") \
        .order("created_at", desc=True) \
        .limit(1) \
        .execute()
    return res.data[0]["content"] if res.data else None

def gerar_incremento(project_id,ideia_usuario):
    """Gera o incremento para memória sumária baseada na ultima resposta da ia."""
    contexto_anterior=buscar_ultimo_resultado_ia(project_id)
    if not contexto_anterior:
        return"Nenhum contexto anterior encontrado para gerar incremento."
    
    prompt_refinamento=f"""
    Você é um especialista em evolução de projetos.
    
    [CONTEXTO ANTERIOR]
    {contexto_anterior}
    
    [NOVA INSTRUÇÃO DE INCREMENTO]
    {ideia_usuario}
    
    Pegue o contexto anterior e aplique as melhorias ou expansões solicitadas, 
    mantendo a coerência técnica.
    """

def gerar_resposta_com_contexto(project_id, memory_summary,system_prompt, ideia_usuario):
    """Executa a lógica de IA com histórico do Banco de Dados"""
    ultima_interacao = buscar_ultima_mensagem(project_id)
    prompt_final = f"""
    [PERSONA ATIVA]
    {system_prompt}

    [RESUMO DA MEMÓRIA]
    {memory_summary}

    [ÚLTIMA INTERAÇÃO RELEVANTE]
    {ultima_interacao}

    [NOVA INSTRUÇÃO]
    {ideia_usuario}
    """
    resposta = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt_final
    )
    texto_resposta = resposta.text
    #Atualiza a memória sumária do projeto (pode ser melhorado com técnicas de resumo ou filtragem de informações relevantes)
    salvar_mensagem(project_id, "user", ideia_usuario)
    salvar_mensagem(project_id, "assistant", resposta.text)

    return texto_resposta

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
    table = Table(title="🎯 PromptMaster - Hub de Inteligência")
    table.add_column("Opção", style="cyan")
    table.add_column("Tipo", style="yellow")
    table.add_column("Descrição", style="magenta")
    table.add_row("1", "Construção de Aplicação", "Transforme uma ideia em um prompt técnico para desenvolvimento de software")
    table.add_row("2", "Análise de Dados", "Gere prompts para análise e interpretação de dados")
    table.add_row("3", "SheetMaster", "Crie prompts para automação e análise em planilhas")
    table.add_row("4", "Professor de Programação", "Desenvolva prompts para ensino e aprendizado de programação")
    table.add_row("5", "Criação de Conteúdo", "Gere prompts para criação de conteúdo informativo e educativo")
    #table.add_row("1-5", "Persona", "Criar algo do zero com uma Persona")
    table.add_row("6", "INCREMENTAR", "Melhorar/Evoluir o último resultado gerado"),
    table.add_row("7", "Histórico", "Exibir histórico de interações desta sessão")
    table.add_row("0", "Sair", "Encerrar sessão")
    console.print(table)
def listar_historico(project_id:str):
        """Busca todas as mensagens do projeto atual no banco e exibe formatado"""
        res=supabase.table("prompts").select("*").eq("project_id", project_id).order("created_at", desc=False).execute()
        if not res.data:
            console.print("[yellow]Nenhuma mensagem encontrada nesta sessão.[/yellow]")
            return
        table=Table(title="📜 Histórico de Interações")
        table.add_column("Papel", style="bold cyan")
        table.add_column("Mensagem", style="white")
        for msg in res.data:
            papel = "👤 Você" if msg["role"] == "user" else "🤖 IA"
            conteudo=msg["content"][:100] + "..." if len(msg["content"])>100 else msg["content"]
            table.add_row(papel,conteudo)
        console.print(table)

def salvar_ou_incrementar_md(nome_arquivo,conteudo,incrementar=False):
    """Salva o conteúdo em um arquivo Markdown. Se incrementar=True, adiciona ao final do arquivo existente."""
    caminho=os.path.join(PASTA_PROMPTS,nome_arquivo)
    modo="a" if incrementar else "w"
    with open(caminho,modo,encoding="utf-8") as f:
        if incrementar:
            f.write("\n\n==============================\n")
            f.write(f"Incremento em {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("==============================\n\n")
        f.write(conteudo)
        console.print(f"[bold green]✅ Arquivo {nome_arquivo} atualizado com sucesso![/bold green]")
    
def listar_e_ler_md():
    arquivos=[f for f in os.listdir(PASTA_PROMPTS) if f.endswith(".md")]
    if not arquivos:
        return None, None
    console.print("📂 [bold cyan]Arquivos Markdown disponíveis:[/bold cyan]")
    for i, arq in enumerate(arquivos,1):
        console.print(f"{i}. {arq}")    

    escolha=int(input("\nEscolha o número do arquivo: ")) - 1
    nome_escolhido=arquivos[escolha]
    with open(os.path.join(PASTA_PROMPTS,nome_escolhido), "r", encoding="utf-8") as f:
        return nome_escolhido, f.read()
           
if __name__ =="__main__":
    id_project, memory_summary = iniciar_sessao_banco()

while True:
    mostrar_menu()
    opcao = input("Escolha uma opção (0-6): ")

    match opcao:
        case "0":
            console.print("[bold green]Encerrando...[/bold green]")
            break

        case "1" | "2" | "3" | "4" | "5":
            # TUDO isso aqui deve estar indentado para dentro deste case
            personas = {
                "1": SISTEM_PROMPT_BUILD,
                "2": PROMPT_ANALISE_DADOS,
                "3": PROMPT_ESPECIALISTA_SHEETS,
                "4": PROMPT_PROFESSOR_PROGRAMACAO,
                "5": PROMPT_CONTEUDO
            }
            persona_escolhida = personas[opcao]
            ideia = input("\n💡 Digite sua ideia inicial: ")
            
            with console.status("[bold yellow]Gerando prompt...[/bold yellow]"):
                resultado = gerar_resposta_com_contexto(id_project, memory_summary, persona_escolhida, ideia)
            console.print(f"\n[bold cyan]✨ Resultado:[/bold cyan]\n{resultado}")

        case "6":
            # Remova o 'pass' e coloque a lógica da PONTE aqui
            ultimo_contexto = buscar_ultimo_resultado_ia(id_project)
            
            if not ultimo_contexto:
                console.print("[bold red]❌ Nada para incrementar ainda![/bold red]")
                continue # Volta para o início do while

            ideia_incremento = input("\n🔄 O que deseja mudar no resultado anterior? ")
            prompt_ponte = f"Você é um especialista em refinamento...\n[ANTERIOR]\n{ultimo_contexto}"

            with console.status("[bold blue]Incrementando...[/bold blue]"):
                resultado = gerar_resposta_com_contexto(id_project, memory_summary, prompt_ponte, ideia_incremento)
            console.print(f"\n[bold green]🚀 Resultado Incrementado:[/bold green]\n{resultado}")
        case "7":
            listar_historico(id_project)

        case _: # O 'default' (opção inválida)
            console.print("[bold red]Opção inválida![/bold red]")
            
            
            

        

            

        


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

        
 