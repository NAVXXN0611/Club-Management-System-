import { createClient } from '@supabase/supabase-js'

const normalizeSupabaseUrl = (url: string | undefined) => {
  if (!url) return ''

  return url
    .trim()
    .replace(/\/+$/, '')
    .replace(/\/(?:rest|auth)\/v1$/, '')
}

const supabaseUrl = normalizeSupabaseUrl(import.meta.env.VITE_SUPABASE_URL)
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_PUBLISHABLE_KEY

if (!supabaseUrl || !supabaseAnonKey) {
  console.warn('Supabase URL or Anon Key is missing. Please check your .env.local file.')
}

export const supabase = createClient(
  supabaseUrl || 'https://placeholder.supabase.co',
  supabaseAnonKey || 'placeholder'
)
