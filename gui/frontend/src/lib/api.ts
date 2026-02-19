import type { ParamSchema, RunInfo, SimulationConfig, Preset, StudyConfig, StudyInfo } from './types'

const BASE = ''

async function fetchJson<T>(url: string, init?: RequestInit): Promise<T> {
  const res = await fetch(BASE + url, {
    headers: { 'Content-Type': 'application/json' },
    ...init,
  })
  if (!res.ok) {
    const text = await res.text()
    throw new Error(`${res.status}: ${text}`)
  }
  return res.json()
}

export const api = {
  // Health
  health: () => fetchJson<{ status: string }>('/api/health'),

  // Params
  getSchema: () => fetchJson<ParamSchema>('/api/params/schema'),

  // Presets
  listPresets: () => fetchJson<Preset[]>('/api/presets'),
  createPreset: (name: string, config: SimulationConfig) =>
    fetchJson<{ id: string; name: string }>('/api/presets', {
      method: 'POST',
      body: JSON.stringify({ name, config }),
    }),
  getPreset: (id: string) => fetchJson<Preset>(`/api/presets/${id}`),

  // Runs
  createRun: (config: SimulationConfig) =>
    fetchJson<RunInfo>('/api/runs', {
      method: 'POST',
      body: JSON.stringify(config),
    }),
  listRuns: () => fetchJson<RunInfo[]>('/api/runs'),
  getRun: (id: string) => fetchJson<RunInfo>(`/api/runs/${id}`),
  getResults: (id: string) => fetchJson<Record<string, unknown>>(`/api/runs/${id}/results`),
  cancelRun: (id: string) => fetchJson<{ status: string }>(`/api/runs/${id}`, { method: 'DELETE' }),

  // Studies
  createStudy: (config: StudyConfig) =>
    fetchJson<StudyInfo>('/api/studies', {
      method: 'POST',
      body: JSON.stringify(config),
    }),
  listStudies: () => fetchJson<StudyInfo[]>('/api/studies'),
  getStudy: (id: string) => fetchJson<StudyInfo>(`/api/studies/${id}`),
}
