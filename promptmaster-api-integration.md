# 1. Visão Geral do Projeto
A integração visa conectar a aplicação frontend construída em React/TypeScript (Next.js/Vite) ao serviço de backend "Prompt Master". O objetivo é permitir que o frontend realize operações CRUD completas (Criar, Ler, Atualizar, Excluir) em prompts gerados e gerenciados pela plataforma, garantindo uma interface fluida, responsiva e com feedback em tempo real para o usuário, utilizando as melhores práticas de comunicação assíncrona.

# 2. Pré-requisitos
*   **Conhecimentos:** TypeScript avançado, React Hooks (`useState`, `useEffect`), chamadas HTTP assíncronas (Promises, async/await).
*   **Ferramentas:** Node.js, Gerenciador de pacotes (npm, pnpm ou yarn).
*   **Bibliotecas:** `axios` (ou `fetch` nativo com wrappers), `@tanstack/react-query` (recomendado) ou `swr` para gerenciamento de estado do servidor, `zod` para validação de esquemas (opcional, mas recomendado).
*   **Configurações:** Ambiente de backend rodando (ou mocks configurados), e URL base da API (ex: `http://localhost:8000/api`) definida em um arquivo `.env.local`.

# 3. Definição da API do Prompt Master (Esquema Proposto)

Assumindo que o "Prompt Master" expõe uma API RESTful padrão, propomos a seguinte estrutura:

### 3.1. Endpoints Principais

| Método   | Endpoint                  | Descrição                                         | Autenticação   |
| :------- | :------------------------ | :------------------------------------------------ | :------------- |
| `GET`    | `/api/prompts`            | Retorna uma lista paginada/filtrada de prompts.   | Necessária     |
| `GET`    | `/api/prompts/{id}`       | Retorna os detalhes de um prompt específico.      | Necessária     |
| `POST`   | `/api/prompts`            | Cria um novo prompt.                              | Necessária     |
| `PUT`    | `/api/prompts/{id}`       | Atualiza (substitui) os dados de um prompt.       | Necessária     |
| `DELETE` | `/api/prompts/{id}`       | Remove um prompt específico.                      | Necessária     |

*(Nota: Caso a API utilize Supabase diretamente e não um middleware customizado, as rotas serão chamadas via SDK do Supabase, que encapsula esses endpoints REST).*

### 3.2. Interfaces TypeScript para Dados

```typescript
// src/types/prompt.ts

export interface Prompt {
  id: string; // UUID
  project_id?: string; // Relacionamento com projeto (se aplicável)
  role: 'user' | 'assistant' | 'system'; 
  content: string;
  created_at: string; // ISO 8601 Date string
  updated_at?: string;
}

export interface PromptInput {
  role: 'user' | 'assistant' | 'system';
  content: string;
  project_id?: string;
}

export interface ApiResponse<T> {
  data: T;
  message?: string;
  error?: string;
}
```

# 4. Etapas de Implementação Detalhadas

### 4.1. Configuração do Frontend para a API

**1. Variáveis de Ambiente:**
Crie ou atualize o `.env.local` na raiz do projeto:
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api
# Ou se for Supabase direto:
# NEXT_PUBLIC_SUPABASE_URL=...
# NEXT_PUBLIC_SUPABASE_ANON_KEY=...
```

**2. Instalação de Bibliotecas:**
```bash
npm install axios @tanstack/react-query
```

**3. Instância do Axios Interceptor:**
Crie `src/services/api.ts` para centralizar a configuração:
```typescript
import axios from 'axios';

export const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para injetar token de auth, se aplicável
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token && config.headers) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
```

### 4.2. Camada de Comunicação com a API

Crie um serviço dedicado `src/services/promptService.ts`:

```typescript
import { api } from './api';
import { Prompt, PromptInput, ApiResponse } from '../types/prompt';

export const promptService = {
  getPrompts: async (): Promise<Prompt[]> => {
    const { data } = await api.get<ApiResponse<Prompt[]>>('/prompts');
    return data.data; // Assumindo o wrapper ApiResponse
  },

  getPromptById: async (id: string): Promise<Prompt> => {
    const { data } = await api.get<ApiResponse<Prompt>>(`/prompts/${id}`);
    return data.data;
  },

  createPrompt: async (promptData: PromptInput): Promise<Prompt> => {
    const { data } = await api.post<ApiResponse<Prompt>>('/prompts', promptData);
    return data.data;
  },

  updatePrompt: async (id: string, promptData: Partial<PromptInput>): Promise<Prompt> => {
    const { data } = await api.put<ApiResponse<Prompt>>(`/prompts/${id}`, promptData);
    return data.data;
  },

  deletePrompt: async (id: string): Promise<void> => {
    await api.delete(`/prompts/${id}`);
  }
};
```

### 4.3. Integração com Componentes TSX

Recomenda-se o uso do `@tanstack/react-query` via custom hooks para lidar de forma nativa com cache, loading states e erros.

**Criando hooks customizados em `src/hooks/usePrompts.ts`:**
```typescript
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { promptService } from '../services/promptService';
import { PromptInput } from '../types/prompt';

export const usePrompts = () => {
  return useQuery({
    queryKey: ['prompts'],
    queryFn: promptService.getPrompts,
  });
};

export const useCreatePrompt = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: PromptInput) => promptService.createPrompt(data),
    onSuccess: () => {
      // Invalida o cache para refetch automático
      queryClient.invalidateQueries({ queryKey: ['prompts'] });
    },
  });
};
```

**Uso no Componente TSX (`PromptList.tsx`):**
```tsx
import { usePrompts } from '../hooks/usePrompts';

export function PromptList() {
  const { data: prompts, isLoading, isError, error } = usePrompts();

  if (isLoading) return <div>Carregando prompts...</div>;
  if (isError) return <div>Erro ao carregar: {(error as Error).message}</div>;

  return (
    <ul>
      {prompts?.map(prompt => (
        <li key={prompt.id}>{prompt.content}</li>
      ))}
    </ul>
  );
}
```

### 4.4. Gerenciamento de Estado da Aplicação

Ao invés de usar `useState` e `useEffect` para persistir dados do servidor no frontend redundante, adotaremos a abordagem de **Server State vs Client State**:
- **Server State:** Gerenciado 100% pelo `React Query`. Ele cria um cache em memória.
- **Client State (ex: Modal aberto, filtros locais):** Gerenciado via Zustand (`zustand`) ou `useState` localmente nos componentes.

**Exemplo com Zustand para filtros (opcional):**
```typescript
import { create } from 'zustand';

interface PromptState {
  searchQuery: string;
  setSearchQuery: (query: string) => void;
}

export const usePromptStore = create<PromptState>((set) => ({
  searchQuery: '',
  setSearchQuery: (query) => set({ searchQuery: query }),
}));
```

### 4.5. Autenticação e Autorização (Se Aplicável)

Se o "Prompt Master" exige auth, a estratégia sugerida é o uso de JWT ou Cookies HttpOnly (para maior segurança em SSR como Next.js):
1. Usuário faz login -> Frontend recebe JWT.
2. Token é armazenado (ex: `localStorage` no SPA, ou `cookies` no Next.js Server Actions).
3. O Interceptor Axios (mostrado no item 4.1) lê e anexa o token enviando no cabeçalho `Authorization`.
4. Tratamento de **Erro 401 (Não autorizado)** no interceptor axios para forçar um "Logout" automático e redirecionar para `/login`.

### 4.6. Tratamento de Erros e Feedback ao Usuário

- **Mensagens Globais (Toast):** Utilize bibliotecas como `sonner` ou `react-hot-toast`.
- **Interceptors de Resposta:** Identificar padrões de erro (400, 500) globalmente:
```typescript
api.interceptors.response.use(
  (response) => response,
  (error) => {
    const errorMsg = error.response?.data?.message || "Ocorreu um erro inesperado na API.";
    toast.error(errorMsg); // Exibe feedback na UI automagicamente
    return Promise.reject(error);
  }
);
```

# 5. Estratégias de Teste

1. **Testes Unitários:** O foco deve recair nas partes da lógica pura, ou seja, testar utils de validação e se os `services` de API estão realizando a request correta. Usar `Vitest` ou `Jest` + `msw` (Mock Service Worker) para interceptar rotas.
2. **Testes de Integração (Componentes):** Testar componentes usando `@testing-library/react`. Mockar o React Query Provider ou usar o `msw` para que, ao renderizar o `PromptList`, os dados de teste apareçam corretamente sem chamar a API real de fato, atestando que os estados de `loading`, `error` e `success` aparecem no DOM.

# 6. Otimizações e Boas Práticas

- **Cache e Stale Time:** Utilize o recurso de *staleTime* do React Query (ex: `staleTime: 1000 * 60 * 5` -> 5 minutos) em listagens de prompts que não mudam frequentemente, zerando as requisições HTTP redundantes e economizando tráfego de banda.
- **Mutations Otimistas (Optimistic Updates):** Ao criar ou deletar um prompt, atualize manualmente o cache do `useQueryClient` de forma imediata na UI, revertendo a tela apenas se a requisição de backend falhar, criando uma interface *Zero Latency* para o usuário.
- **Memoização (`useMemo` e `useCallback`):** Empregado somente caso arrays grandes necessitem ser filtrados ou transformados no frontend de forma custosa, prevenindo gargalos no JavaScript thread local.

# 7. Ferramentas e Tecnologias Sugeridas

*   **Comunicação API:** `Axios` ou o nativo `fetch` api com wrapper inteligente;
*   **Gerenciamento do Estado Servidor/Cache:** `@tanstack/react-query` (Fortemente sugerido ao invés de Context API/Redux para chamadas HTTP).
*   **Gerenciamento de Estado Cliente:** `Zustand`.
*   **Feedback Modal/Toast:** `sonner` ou `react-toastify`.
*   **Validação de Formulários & Esquema (Tipagem Strict):** `React Hook Form` + `Zod`. (Excelente parceria para as tipagens do DTO de prompt ao enviá-las no `createPrompt()`).
*   **Testes:** `Vitest` + `React Testing Library` + `MSW (Mock Service Worker)`.
