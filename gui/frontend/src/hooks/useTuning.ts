import { useCallback, useState } from 'react'
import type { StudyConfig, TrialResult } from '@/lib/types'
import { api } from '@/lib/api'
import { useTuningStore } from '@/stores/tuningStore'
import { useWebSocket } from './useWebSocket'

export function useTuning() {
  const { activeStudyId, startStudy, addTrial, completeStudy } = useTuningStore()
  const [wsUrl, setWsUrl] = useState<string | null>(null)

  const onMessage = useCallback(
    (data: unknown) => {
      const msg = data as { type: string; data?: TrialResult; study?: Record<string, unknown> }
      if (msg.type === 'trial' && msg.data) {
        addTrial(msg.data)
      } else if (msg.type === 'complete' && msg.study) {
        completeStudy(msg.study as never)
      }
    },
    [addTrial, completeStudy]
  )

  const { connected } = useWebSocket(wsUrl, { onMessage })

  const launch = useCallback(
    async (config: StudyConfig) => {
      const study = await api.createStudy(config)
      startStudy(study.id)
      setWsUrl(`/ws/study/${study.id}`)
      return study
    },
    [startStudy]
  )

  return { launch, connected, activeStudyId }
}
