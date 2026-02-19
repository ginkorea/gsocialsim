import { create } from 'zustand'
import type { StudyInfo, TrialResult } from '@/lib/types'

interface TuningState {
  activeStudyId: string | null
  studies: StudyInfo[]
  trials: TrialResult[]
  bestValue: number | null
  bestParams: Record<string, number>
  status: 'idle' | 'running' | 'completed' | 'failed'

  startStudy: (studyId: string) => void
  addTrial: (trial: TrialResult) => void
  completeStudy: (study: StudyInfo) => void
  reset: () => void
}

export const useTuningStore = create<TuningState>((set) => ({
  activeStudyId: null,
  studies: [],
  trials: [],
  bestValue: null,
  bestParams: {},
  status: 'idle',

  startStudy: (studyId) => {
    set({
      activeStudyId: studyId,
      trials: [],
      bestValue: null,
      bestParams: {},
      status: 'running',
    })
  },

  addTrial: (trial) => {
    set((state) => {
      const trials = [...state.trials, trial]
      const bestVal = trial.values[0]
      const isBetter = state.bestValue === null || bestVal < state.bestValue
      return {
        trials,
        bestValue: isBetter ? bestVal : state.bestValue,
        bestParams: isBetter ? trial.params : state.bestParams,
      }
    })
  },

  completeStudy: (study) => {
    set({
      status: 'completed',
      bestValue: study.best_value,
      bestParams: study.best_params,
    })
  },

  reset: () => {
    set({
      activeStudyId: null,
      trials: [],
      bestValue: null,
      bestParams: {},
      status: 'idle',
    })
  },
}))
