import datetime
import os
from typing import Any

from dotenv import load_dotenv
from google import genai
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from supabase import Client, create_client

#====Configs iniciais====
load_dotenv()
console = Console()
#====verifica se a pasta de prompts existe, se não, cria====
PASTA_PROMPTS="meus_prompts"
if not os.path.exists(PASTA_PROMPTS):
    os.makedirs(PASTA_PROMPTS)
##==============================
##===== Iniciando Clients ======
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
PERSONA_TABLE = "persona_profiles"

THEME = {
    "navy": "#143a57",
    "navy_alt": "#1c4b69",
    "cyan": "#2ed6dc",
    "white": "#f6fbff",
    "muted": "#a9c0d0",
    "soft": "#dceaf2",
    "danger": "#ff8c8c",
    "success": "#7ee0a3",
}

_client: genai.Client | None = None
_supabase: Client | None = None
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
PROMPT_FRONTEND_SENIOR = """
Você é um engenheiro Frontend Sênior com experiência em construção de aplicações web modernas e escaláveis.

Possui domínio em:
- Arquitetura de Frontend
- React / Next.js
- Componentização
- Design Systems
- UX/UI
- Performance Web
- Acessibilidade (a11y)
- State management
- Integração com APIs
- Organização de código escalável

Sua função é transformar ideias em PROMPTS PROFISSIONAIS para desenvolvimento de interfaces frontend.

Sempre responda em Markdown estruturado seguindo este modelo:

# 🎯 Objetivo da Interface
Explique claramente o que a interface deve fazer e qual problema resolve.

# 👤 Usuário e Contexto
Descreva:
- tipo de usuário
- cenário de uso
- dispositivo principal (desktop, mobile ou ambos)

# 🧠 Estratégia de UX
Defina:
- fluxo principal do usuário
- ações principais
- simplicidade de uso
- feedback visual

# 🏗 Arquitetura Frontend
Sugira:
- framework (React, Next.js, Vue etc.)
- organização de pastas
- separação de componentes
- gerenciamento de estado

# 🧩 Componentes Principais
Liste os principais componentes da interface.

Exemplo:
- Navbar
- Sidebar
- Dashboard
- Cards
- Forms
- Modais

Explique a função de cada componente.

# 🎨 Diretrizes de UI
Defina:
- estilo visual
- tipografia
- espaçamento
- cores
- responsividade

Se aplicável, sugerir uso de:
- Tailwind
- Material UI
- Shadcn UI
- Design System próprio

# ⚡ Performance
Incluir recomendações como:
- lazy loading
- memoização
- divisão de componentes
- otimização de renderização

# ♿ Acessibilidade
Garantir:
- navegação por teclado
- contraste adequado
- uso correto de aria-labels

# 🔗 Integração com Backend
Definir como a interface deve consumir APIs.

Exemplo:
- REST
- GraphQL
- autenticação
- tratamento de erros

# 📄 Estrutura do Projeto
Forneça uma sugestão de estrutura de diretórios.

# 🚀 Melhorias Futuras
Sugira possíveis evoluções da interface.

Responda apenas em Markdown.
Não explique nada fora da estrutura.
Produza prompts claros, técnicos e prontos para serem usados em IAs de geração de código.
"""
PROMPT_OPTIONS = {
    "2": {
        "label": "Construção de Aplicação",
        "description": "Prompt técnico para software",
        "system_prompt": SISTEM_PROMPT_BUILD,
    },
    "3": {
        "label": "Análise de Dados",
        "description": "Prompt para análise e interpretação",
        "system_prompt": PROMPT_ANALISE_DADOS,
    },
    "4": {
        "label": "SheetMaster",
        "description": "Prompt para automação em planilhas",
        "system_prompt": PROMPT_ESPECIALISTA_SHEETS,
    },
    "5": {
        "label": "Professor de Programação",
        "description": "Prompt didático e técnico",
        "system_prompt": PROMPT_PROFESSOR_PROGRAMACAO,
    },
    "6": {
        "label": "Criação de Conteúdo",
        "description": "Prompt para conteúdo informativo",
        "system_prompt": PROMPT_CONTEUDO,
    },
    "7": {
        "label": "Geração de FrontEnd",
        "description": "Prompt para UI e frontend",
        "system_prompt": PROMPT_FRONTEND_SENIOR,
    },
}


def get_genai_client() -> genai.Client:
    global _client
    if _client is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY não configurada.")
        _client = genai.Client(api_key=api_key)
    return _client


def get_supabase() -> Client:
    global _supabase
    if _supabase is None:
        if not SUPABASE_URL or not SUPABASE_KEY:
            raise RuntimeError("Credenciais do Supabase não configuradas.")
        _supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    return _supabase


def combinar_prompt_com_persona(prompt_base: str, persona_ativa: dict[str, Any] | None) -> str:
    if not persona_ativa:
        return prompt_base
    return f"""
{persona_ativa['system_prompt']}

[DIRETRIZ DE CONTEXTO]
Execute a tarefa abaixo mantendo a persona ativa acima.

[TAREFA]
{prompt_base}
"""


def listar_personas_db() -> list[dict[str, Any]]:
    response = (
        get_supabase()
        .table(PERSONA_TABLE)
        .select("id,name,description,category,system_prompt")
        .order("name")
        .execute()
    )
    return response.data or []


def resolver_persona(personas: list[dict[str, Any]], escolha: str) -> dict[str, Any] | None:
    escolha_limpa = escolha.strip()
    if not escolha_limpa:
        return None

    if escolha_limpa.isdigit():
        indice = int(escolha_limpa) - 1
        if 0 <= indice < len(personas):
            return personas[indice]

    escolha_normalizada = escolha_limpa.casefold()
    for persona in personas:
        nome = str(persona.get("name", "")).strip().casefold()
        if nome == escolha_normalizada:
            return persona
    return None


def selecionar_persona() -> dict[str, Any] | None:
    try:
        personas = listar_personas_db()
    except Exception as exc:
        console.print(f"[{THEME['danger']}]Erro ao listar personas: {exc}[/]")
        return None

    if not personas:
        console.print(f"[{THEME['muted']}]Nenhuma persona encontrada.[/]")
        return None

    tabela = Table(
        box=box.SIMPLE_HEAVY,
        border_style=THEME["cyan"],
        header_style=f"bold {THEME['cyan']}",
        style=f"{THEME['white']} on {THEME['navy']}",
        padding=(0, 1),
    )
    tabela.add_column("#", justify="right", width=3)
    tabela.add_column("Persona", min_width=18)
    tabela.add_column("Categoria", min_width=12)
    for indice, persona in enumerate(personas, start=1):
        tabela.add_row(
            str(indice),
            str(persona.get("name", "-")),
            str(persona.get("category") or "-"),
        )

    console.print(
        Panel.fit(
            tabela,
            title=f"[{THEME['cyan']}]Personas Disponíveis[/]",
            border_style=THEME["cyan"],
            style=f"{THEME['white']} on {THEME['navy']}",
        )
    )
    escolha = input("Persona: ")
    persona = resolver_persona(personas, escolha)
    if not persona:
        console.print(f"[{THEME['danger']}]Persona inválida.[/]")
        return None

    console.print(f"[{THEME['success']}]Persona ativada: {persona['name']}[/]")
    return persona


def mostrar_menu(persona_ativa: dict[str, Any] | None):
    console.clear()
    persona_nome = persona_ativa["name"] if persona_ativa else "Nenhuma"
    cabecalho = (
        f"[bold {THEME['white']}]Prompt Master[/bold {THEME['white']}]\n"
        f"[{THEME['muted']}]Automação para prompts[/]\n"
        f"[{THEME['cyan']}]Persona ativa:[/] [{THEME['white']}] {persona_nome}[/]"
    )
    console.print(
        Panel.fit(
            cabecalho,
            border_style=THEME["cyan"],
            style=f"{THEME['white']} on {THEME['navy']}",
            subtitle=f"[{THEME['muted']}]Lypsyos palette[/]",
        )
    )

    tabela = Table(
        box=box.SIMPLE_HEAVY,
        border_style=THEME["navy_alt"],
        header_style=f"bold {THEME['cyan']}",
        style=f"{THEME['white']} on {THEME['navy']}",
        padding=(0, 1),
    )
    tabela.add_column("Opção", width=6, justify="right")
    tabela.add_column("Ação", min_width=22)
    tabela.add_column("Resumo", min_width=26, style=THEME["muted"])
    tabela.add_row("1", "Selecionar Persona", "Ativar persona do banco")
    for chave, dados in PROMPT_OPTIONS.items():
        tabela.add_row(chave, dados["label"], dados["description"])
    tabela.add_row("8", "Incrementar", "Refinar último resultado")
    tabela.add_row("9", "Histórico", "Ver sessão")
    tabela.add_row("0", "Sair", "Encerrar")
    console.print(tabela)
def iniciar_sessao_banco(): 
    """Cria um usuario falso (para CLI) e inicia um novo projeto/sessao"""
    email_cli="cli@promptmaster.local"
    #1. verifica ou cria user
    supabase = get_supabase()
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
    get_supabase().table("prompts").insert({
        "project_id":project_id,
        "role":role,
        "content":content
    }).execute()
    
def buscar_ultima_mensagem(project_id:str):
    """Busca as últimas interações para dar contexto à IA"""
    res = get_supabase().table("prompts").select("*").eq("project_id",project_id).order("created_at", desc=True).limit(2).execute()

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
    res=get_supabase().table("prompts") \
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
    resposta = get_genai_client().models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt_final
    )
    texto_resposta = resposta.text
    #Atualiza a memória sumária do projeto (pode ser melhorado com técnicas de resumo ou filtragem de informações relevantes)
    salvar_mensagem(project_id, "user", ideia_usuario)
    salvar_mensagem(project_id, "assistant", resposta.text)

    return texto_resposta

def gerar_prompt_build(ideia_usuario):
    resposta = get_genai_client().models.generate_content(
        model="gemini-2.5-flash",
        contents=f"{SISTEM_PROMPT_BUILD}\n\nIdeia do usuário:{ideia_usuario}"
    )
    return resposta.text
def gerar_prompt_analise_dados(ideia_usuario):
    resposta = get_genai_client().models.generate_content(
        model="gemini-2.5-flash",
        contents=f"{PROMPT_ANALISE_DADOS}\n\nIdeia do usuário:{ideia_usuario}"
    )
    return resposta.text
def gerar_prompt_sheetmaster(ideia_usuario):
    resposta = get_genai_client().models.generate_content(
        model="gemini-2.5-flash",
        contents=f"{PROMPT_ESPECIALISTA_SHEETS}\n\nIdeia do usuário:{ideia_usuario}"
    )
    return resposta.text
def gerar_prompt_professor_programacao(ideia_usuario):
    resposta = get_genai_client().models.generate_content(
        model="gemini-2.5-flash",
        contents=f"{PROMPT_PROFESSOR_PROGRAMACAO}\n\nIdeia do usuário:{ideia_usuario}"
    )
    return resposta.text
def gerar_prompt_conteudo(ideia_usuario):
    resposta = get_genai_client().models.generate_content(
        model="gemini-2.5-flash",
        contents=f"{PROMPT_CONTEUDO}\n\nIdeia do usuário:{ideia_usuario}"
    )
    return resposta.text
def gerar_prompt_frontend(ideia_usuario):
    resposta = get_genai_client().models.generate_content(
        model="gemini-2.5-flash",
        contents=f"{PROMPT_FRONTEND_SENIOR}\n\nIdeia do usuário:{ideia_usuario}"
    )
    return resposta.text
def listar_historico(project_id:str):
        """Busca todas as mensagens do projeto atual no banco e exibe formatado"""
        res=get_supabase().table("prompts").select("*").eq("project_id", project_id).order("created_at", desc=False).execute()
        if not res.data:
            console.print(f"[{THEME['muted']}]Nenhuma mensagem nesta sessão.[/]")
            return
        table=Table(
            title="Histórico",
            box=box.SIMPLE_HEAVY,
            border_style=THEME["cyan"],
            header_style=f"bold {THEME['cyan']}",
            style=f"{THEME['white']} on {THEME['navy']}",
        )
        table.add_column("Papel", style=f"bold {THEME['cyan']}")
        table.add_column("Mensagem", style=THEME["white"])
        for msg in res.data:
            papel = "Você" if msg["role"] == "user" else "IA"
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


def executar_menu() -> None:
    id_project, memory_summary = iniciar_sessao_banco()
    persona_ativa: dict[str, Any] | None = None

    while True:
        mostrar_menu(persona_ativa)
        opcao = input("Escolha: ").strip()

        match opcao:
            case "0":
                console.print(f"[{THEME['success']}]Encerrando.[/]")
                break

            case "1":
                persona_selecionada = selecionar_persona()
                if persona_selecionada:
                    persona_ativa = persona_selecionada

            case "2" | "3" | "4" | "5" | "6" | "7":
                ideia = input("Ideia: ").strip()
                if not ideia:
                    console.print(f"[{THEME['danger']}]Ideia vazia.[/]")
                    continue

                prompt_base = PROMPT_OPTIONS[opcao]["system_prompt"]
                prompt_ativo = combinar_prompt_com_persona(prompt_base, persona_ativa)
                with console.status(f"[{THEME['cyan']}]Gerando...[/]"):
                    resultado = gerar_resposta_com_contexto(
                        id_project,
                        memory_summary,
                        prompt_ativo,
                        ideia,
                    )

                console.print(
                    Panel(
                        resultado,
                        title=f"[{THEME['cyan']}]Resultado[/]",
                        border_style=THEME["cyan"],
                        style=f"{THEME['white']} on {THEME['navy']}",
                    )
                )

            case "8":
                ultimo_contexto = buscar_ultimo_resultado_ia(id_project)
                if not ultimo_contexto:
                    console.print(f"[{THEME['danger']}]Nada para incrementar.[/]")
                    continue

                ideia_incremento = input("Ajuste: ").strip()
                if not ideia_incremento:
                    console.print(f"[{THEME['danger']}]Ajuste vazio.[/]")
                    continue

                prompt_ponte = (
                    "Você é um especialista em refinamento de prompts. "
                    "Melhore a resposta anterior sem perder clareza.\n\n"
                    f"[ANTERIOR]\n{ultimo_contexto}"
                )
                prompt_ativo = combinar_prompt_com_persona(prompt_ponte, persona_ativa)
                with console.status(f"[{THEME['cyan']}]Incrementando...[/]"):
                    resultado = gerar_resposta_com_contexto(
                        id_project,
                        memory_summary,
                        prompt_ativo,
                        ideia_incremento,
                    )

                console.print(
                    Panel(
                        resultado,
                        title=f"[{THEME['cyan']}]Incremento[/]",
                        border_style=THEME["cyan"],
                        style=f"{THEME['white']} on {THEME['navy']}",
                    )
                )

            case "9":
                listar_historico(id_project)

            case _:
                console.print(f"[{THEME['danger']}]Opção inválida.[/]")


if __name__ =="__main__":
    try:
        executar_menu()
    except RuntimeError as exc:
        console.print(f"[{THEME['danger']}]Erro: {exc}[/]")

