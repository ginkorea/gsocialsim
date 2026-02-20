import { createContext, useContext, type ReactNode } from 'react'
import { useSimulation } from '@/hooks/useSimulation'

type SimulationContextValue = ReturnType<typeof useSimulation>

const SimulationContext = createContext<SimulationContextValue | null>(null)

export function SimulationProvider({ children }: { children: ReactNode }) {
  const simulation = useSimulation()
  return (
    <SimulationContext.Provider value={simulation}>
      {children}
    </SimulationContext.Provider>
  )
}

export function useSimulationContext() {
  const ctx = useContext(SimulationContext)
  if (!ctx) {
    throw new Error('useSimulationContext must be used within SimulationProvider')
  }
  return ctx
}
