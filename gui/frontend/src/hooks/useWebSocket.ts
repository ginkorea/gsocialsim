import { useCallback, useEffect, useRef, useState } from 'react'

interface UseWebSocketOptions {
  onMessage: (data: unknown) => void
  onOpen?: () => void
  onClose?: () => void
  onError?: () => void
  reconnect?: boolean
  reconnectInterval?: number
}

export function useWebSocket(url: string | null, options: UseWebSocketOptions) {
  const wsRef = useRef<WebSocket | null>(null)
  const reconnectTimer = useRef<ReturnType<typeof setTimeout> | null>(null)
  const [connected, setConnected] = useState(false)
  const urlRef = useRef(url)
  urlRef.current = url

  const { reconnect = true, reconnectInterval = 3000 } = options

  const connect = useCallback(() => {
    if (!urlRef.current) return

    // Clean up existing connection
    if (wsRef.current) {
      wsRef.current.onclose = null
      wsRef.current.close()
    }

    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    const wsUrl = `${protocol}//${window.location.host}${urlRef.current}`
    const ws = new WebSocket(wsUrl)

    ws.onopen = () => {
      setConnected(true)
      options.onOpen?.()
    }
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
      // Auto-reconnect if enabled and URL is still set
      if (reconnect && urlRef.current) {
        reconnectTimer.current = setTimeout(() => {
          if (urlRef.current) {
            connect()
          }
        }, reconnectInterval)
      }
    }
    ws.onerror = () => {
      setConnected(false)
      options.onError?.()
    }
    wsRef.current = ws
  }, [options.onMessage, options.onOpen, options.onClose, options.onError, reconnect, reconnectInterval])

  useEffect(() => {
    if (url) {
      connect()
    }
    return () => {
      if (reconnectTimer.current) {
        clearTimeout(reconnectTimer.current)
      }
      if (wsRef.current) {
        wsRef.current.onclose = null  // prevent reconnect on cleanup
        wsRef.current.close()
      }
    }
  }, [url, connect])

  const close = useCallback(() => {
    if (reconnectTimer.current) {
      clearTimeout(reconnectTimer.current)
    }
    if (wsRef.current) {
      wsRef.current.onclose = null
      wsRef.current.close()
    }
  }, [])

  return { connected, close }
}
