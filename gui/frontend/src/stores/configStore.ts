import { create } from 'zustand'
import type { ParamSchema, SimulationConfig } from '@/lib/types'
import { api } from '@/lib/api'

interface ConfigState {
  schema: ParamSchema | null
  config: SimulationConfig
  dirty: boolean
  loading: boolean

  fetchSchema: () => Promise<void>
  updateParam: (name: string, value: number | string | boolean) => void
  setConfig: (config: SimulationConfig) => void
  resetToDefaults: () => void
}

const DEFAULT_CONFIG: SimulationConfig = {
  ticks: 96,
  agents: 100,
  seed: 123,
  network_mode: 'groups',
  avg_following: 12,
  analytics_mode: 'summary',
  influence_dynamics: {},
  kernel: {},
  feed_queue: {},
  broadcast_feed: {},
  media_diet: {},
}

// Map param names to their config group
const PARAM_GROUP: Record<string, keyof SimulationConfig> = {
  inertia_rho: 'influence_dynamics',
  learning_rate_base: 'influence_dynamics',
  rebound_k: 'influence_dynamics',
  critical_velocity_threshold: 'influence_dynamics',
  critical_kappa: 'influence_dynamics',
  evidence_decay_lambda: 'influence_dynamics',
  evidence_threshold: 'influence_dynamics',
  trust_exponent_gamma: 'influence_dynamics',
  habituation_alpha: 'influence_dynamics',
  bounded_confidence_tau: 'influence_dynamics',
  mutual_trust_weight: 'kernel',
  offline_contacts_per_tick: 'kernel',
  offline_base_prob: 'kernel',
  discovery_min_per_tick: 'kernel',
  discovery_max_per_tick: 'kernel',
  discovery_pool_size: 'kernel',
  recency_weight: 'feed_queue',
  engagement_weight: 'feed_queue',
  proximity_weight: 'feed_queue',
  mutual_weight: 'feed_queue',
  candidate_window_ticks: 'broadcast_feed',
  max_candidates: 'broadcast_feed',
  max_shown: 'broadcast_feed',
  saturation_k: 'media_diet',
}

export const useConfigStore = create<ConfigState>((set, get) => ({
  schema: null,
  config: { ...DEFAULT_CONFIG },
  dirty: false,
  loading: false,

  fetchSchema: async () => {
    set({ loading: true })
    try {
      const schema = await api.getSchema()
      set({ schema, loading: false })
    } catch {
      set({ loading: false })
    }
  },

  updateParam: (name, value) => {
    const config = { ...get().config }
    const group = PARAM_GROUP[name]

    if (group && typeof value === 'number') {
      const sub = { ...(config[group] as Record<string, number>) }
      sub[name] = value
      ;(config as Record<string, unknown>)[group] = sub
    } else if (name in config) {
      ;(config as Record<string, unknown>)[name] = value
    }

    set({ config, dirty: true })
  },

  setConfig: (config) => set({ config, dirty: false }),

  resetToDefaults: () => {
    set({ config: { ...DEFAULT_CONFIG }, dirty: true })
  },
}))
