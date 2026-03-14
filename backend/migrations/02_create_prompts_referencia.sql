create extension if not exists "pgcrypto";

create table if not exists public.prompts_referencia (
    id uuid primary key default gen_random_uuid(),
    nome text not null,
    descricao text,
    conteudo_prompt text not null,
    categoria text,
    data_criacao timestamptz not null default now()
);

create index if not exists idx_prompts_referencia_categoria
    on public.prompts_referencia (categoria);

create index if not exists idx_prompts_referencia_data_criacao
    on public.prompts_referencia (data_criacao desc);
