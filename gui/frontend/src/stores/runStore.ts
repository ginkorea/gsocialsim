import { create } from 'zustand'
import type { RunInfo, TickData } from '@/lib/types'
import { api } from '@/lib/api'

interface RunState {
  runs: RunInfo[]
  activeRunId: string | null
  tickHistory: TickData[]
  currentTick: TickData | null
  status: 'idle' | 'running' | 'completed' | 'failed'
  logs: string[]

  fetchRuns: () => Promise<void>
  startRun: (runId: string) => void
  addTick: (data: TickData) => void
  addLog: (message: string) => void
  complete: (metrics: Record<string, number>) => void
  reset: () => void
}

export const useRunStore = create<RunState>((set, get) => ({
  runs: [],
  activeRunId: null,
  tickHistory: [],
  currentTick: null,
  status: 'idle',
  logs: [],

  fetchRuns: async () => {
    try {
      const runs = await api.listRuns()
      set({ runs })
    } catch {
      // ignore
    }
  },

  startRun: (runId) => {
    set({
      activeRunId: runId,
      tickHistory: [],
      currentTick: null,
      status: 'running',
      logs: [`[${new Date().toLocaleTimeString()}] Starting run ${runId}...`],
    })
  },

  addTick: (data) => {
    set((state) => ({
      tickHistory: [...state.tickHistory, data],
      currentTick: data,
    }))
  },

  addLog: (message) => {
    set((state) => ({
      logs: [...state.logs, `[${new Date().toLocaleTimeString()}] ${message}`],
    }))
  },

  complete: (metrics) => {
    set((state) => ({
      status: 'completed',
      runs: state.runs.map((r) =>
        r.id === state.activeRunId ? { ...r, status: 'completed' as const, metrics } : r
      ),
    }))
  },

  reset: () => {
    set({
      activeRunId: null,
      tickHistory: [],
      currentTick: null,
      status: 'idle',
    })
  },
}))
