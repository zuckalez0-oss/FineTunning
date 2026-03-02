# Prompt Master 🤖✨

O **Prompt Master** é uma ferramenta de linha de comando (CLI) desenvolvida em Python que utiliza a inteligência artificial do Google Gemini para transformar ideias brutas em prompts profissionais, estruturados e otimizados para diferentes contextos.

## 🚀 Funcionalidades

O sistema atua como um "Engenheiro de Prompts Automatizado", oferecendo 5 modos especializados:

1.  **Construção Geral:** Transforma solicitações vagas em instruções claras e organizadas.
2.  **Análise de Dados:** Gera prompts técnicos para estatística, visualização e insights de dados.
3.  **Machine Learning:** Cria especificações detalhadas para definição de datasets, modelos e métricas de avaliação.
4.  **Texto Criativo:** Estrutura prompts para narrativas, roteiros e escrita artística com foco em estilo e emoção.
5.  **Criação de Conteúdo:** Focado em marketing, SEO, copywriting e engajamento de público.

## 🛠️ Pré-requisitos

*   Python 3.x instalado.
*   Uma chave de API do Google Gemini (Google AI Studio).

## 📦 Instalação

1.  Baixe o arquivo `promptMaster.py`.
2.  Instale as dependências necessárias via pip:

```bash
pip install google-genai python-dotenv
```

## ⚙️ Configuração

Antes de executar, é necessário configurar a autenticação:

1.  Crie um arquivo chamado `.env` no mesmo diretório do script.
2.  Adicione sua chave de API do Gemini neste arquivo:

```env
GEMINI_API_KEY=sua_chave_api_aqui
```

## ▶️ Como Utilizar

1.  Abra o terminal na pasta do projeto e execute o script:

```bash
python promptMaster.py
```

2.  O menu interativo será exibido. Escolha uma opção numérica (1-5) baseada no seu objetivo:

```text
Sistema de Geração de Prompts Profissionais:
Digite a opcao para o tipo de prompt que deseja gerar:
1. Prompt para construção de conteúdo
2. Prompt para análise de dados
3. Prompt para aprendizado de máquina
4. Gerar texto criativo
5. Gerar prompt para criação de conteúdo
0. Sair
```

3.  **Digite sua ideia** quando solicitado (ex: *"Quero analisar vendas de um supermercado para encontrar padrões de compra"*).
4.  O sistema retornará um **prompt estruturado em Markdown** no terminal, pronto para ser copiado e utilizado em LLMs.

## 📂 Estrutura do Projeto

*   `promptMaster.py`: Código fonte principal contendo a lógica e os templates de sistema (System Prompts).
*   `.env`: Arquivo para armazenar a `GEMINI_API_KEY` de forma segura.
*   `.gitignore`: Configurado para ignorar arquivos sensíveis como o `.env`.
