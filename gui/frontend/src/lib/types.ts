export interface ParamDef {
  name: string
  display_name: string
  group: string
  type: 'float' | 'int' | 'string' | 'bool'
  default: number | string | boolean
  min?: number
  max?: number
  step?: number
  description?: string
  choices?: string[]
}

export interface ParamSchema {
  groups: Record<string, ParamDef[]>
  defaults: Record<string, number | string | boolean>
}

export interface SimulationConfig {
  ticks: number
  agents: number
  seed: number
  network_mode: string
  avg_following: number
  analytics_mode: string
  influence_dynamics: Record<string, number>
  kernel: Record<string, number>
  feed_queue: Record<string, number>
  broadcast_feed: Record<string, number>
  media_diet: Record<string, number>
}

export interface RunInfo {
  id: string
  config: SimulationConfig
  status: 'pending' | 'running' | 'completed' | 'failed' | 'cancelled'
  created_at: string
  ticks_completed: number
  total_ticks: number
  metrics: Record<string, number>
}

export interface TickData {
  tick: number
  total: number
  impressions: number
  consumed: number
  belief_deltas: number
  leans: number[]
}

export interface WsMessage {
  type: 'tick' | 'complete' | 'error'
  data?: TickData
  metrics?: Record<string, number>
  status?: string
  message?: string
}

export interface Preset {
  id: string
  name: string
  config: SimulationConfig
}

export interface StudyConfig {
  name: string
  base_config: SimulationConfig
  search_space: Record<string, { type: string; low: number; high: number; step?: number }>
  objectives: { name: string; direction: string }[]
  sampler: string
  n_trials: number
  n_parallel: number
}

export interface TrialResult {
  trial_number: number
  params: Record<string, number>
  values: number[]
  objectives: string[]
}

export interface StudyInfo {
  id: string
  name: string
  status: 'running' | 'completed' | 'failed'
  n_trials: number
  completed_trials: number
  best_value: number | null
  best_params: Record<string, number>
  trials: TrialResult[]
}
