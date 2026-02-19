import { useCallback, useEffect, useRef, useState } from 'react'

interface UseWebSocketOptions {
  onMessage: (data: unknown) => void
  onClose?: () => void
}

export function useWebSocket(url: string | null, options: UseWebSocketOptions) {
  const wsRef = useRef<WebSocket | null>(null)
  const [connected, setConnected] = useState(false)

  const connect = useCallback(() => {
    if (!url) return
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    const wsUrl = `${protocol}//${window.location.host}${url}`
    const ws = new WebSocket(wsUrl)

    ws.onopen = () => setConnected(true)
    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        options.onMessage(data)
      } catch {
        // ignore
      }
    }
    ws.onclose = () => {
      setConnected(false)
      options.onClose?.()
    }
    ws.onerror = () => {
      setConnected(false)
    }
    wsRef.current = ws
  }, [url, options.onMessage, options.onClose])

  useEffect(() => {
    connect()
    return () => {
      wsRef.current?.close()
    }
  }, [connect])

  const close = useCallback(() => {
    wsRef.current?.close()
  }, [])

  return { connected, close }
}
