import { useCallback, useState } from 'react'
import type { SimulationConfig, WsMessage } from '@/lib/types'
import { api } from '@/lib/api'
import { useRunStore } from '@/stores/runStore'
import { useWebSocket } from './useWebSocket'

export function useSimulation() {
  const { activeRunId, startRun, addTick, addLog, complete } = useRunStore()
  const [wsUrl, setWsUrl] = useState<string | null>(null)

  const onMessage = useCallback(
    (data: unknown) => {
      const msg = data as WsMessage
      if (msg.type === 'tick' && msg.data) {
        addTick(msg.data)
      } else if (msg.type === 'log' && msg.message) {
        addLog(msg.message)
      } else if (msg.type === 'complete' && msg.metrics) {
        addLog(`Simulation complete`)
        complete(msg.metrics)
      } else if (msg.type === 'error' && msg.message) {
        addLog(`ERROR: ${msg.message}`)
      }
    },
    [addTick, addLog, complete]
  )

  const onOpen = useCallback(() => {
    addLog('WebSocket connected')
  }, [addLog])

  const onClose = useCallback(() => {
    addLog('WebSocket disconnected')
  }, [addLog])

  const onError = useCallback(() => {
    addLog('WebSocket error')
  }, [addLog])

  const { connected } = useWebSocket(wsUrl, { onMessage, onOpen, onClose, onError })

  const launch = useCallback(
    async (config: SimulationConfig) => {
      const run = await api.createRun(config)
      startRun(run.id)
      addLog(`Run created: ${run.id} (${config.ticks} ticks, ${config.agents} agents)`)
      addLog(`Connecting WebSocket to /ws/run/${run.id}...`)
      setWsUrl(`/ws/run/${run.id}`)
      return run
    },
    [startRun, addLog]
  )

  const cancel = useCallback(async () => {
    if (activeRunId) {
      addLog('Cancelling simulation...')
      await api.cancelRun(activeRunId)
    }
  }, [activeRunId, addLog])

  return { launch, cancel, connected, activeRunId }
}
