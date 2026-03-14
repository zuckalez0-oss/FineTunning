-- 1. Add missing fields to 'prompts' to match Frontend DTO
ALTER TABLE public.prompts 
ADD COLUMN IF NOT EXISTS title text,
ADD COLUMN IF NOT EXISTS tags text[],
ADD COLUMN IF NOT EXISTS category text;

-- 2. Create 'prompt_versions' table
CREATE TABLE IF NOT EXISTS public.prompt_versions (
    id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
    prompt_id uuid REFERENCES public.prompts(id) ON DELETE CASCADE,
    content text NOT NULL,
    source text CHECK (source IN ('original', 'refinement')) NOT NULL,
    created_at timestamptz DEFAULT now()
);

-- 3. In persona_profiles, verify we have the fields requested: name, system_prompt, auto_detect_tags, description, category
-- Let's add description and category as requested
ALTER TABLE public.persona_profiles
ADD COLUMN IF NOT EXISTS description text,
ADD COLUMN IF NOT EXISTS category text;
