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

  // Store callbacks in refs so `connect` never changes identity
  const onMessageRef = useRef(options.onMessage)
  onMessageRef.current = options.onMessage
  const onOpenRef = useRef(options.onOpen)
  onOpenRef.current = options.onOpen
  const onCloseRef = useRef(options.onClose)
  onCloseRef.current = options.onClose
  const onErrorRef = useRef(options.onError)
  onErrorRef.current = options.onError

  const reconnect = options.reconnect ?? true
  const reconnectInterval = options.reconnectInterval ?? 3000
  const reconnectRef = useRef(reconnect)
  reconnectRef.current = reconnect
  const reconnectIntervalRef = useRef(reconnectInterval)
  reconnectIntervalRef.current = reconnectInterval

  const connect = useCallback(() => {
    if (!urlRef.current) return

    // Clean up existing connection
    if (wsRef.current) {
      wsRef.current.onclose = null
      wsRef.current.close()
    }

    // Connect directly to backend (bypass Vite proxy which breaks WS upgrades)
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    const backendPort = import.meta.env.VITE_BACKEND_PORT || '8000'
    const wsUrl = `${protocol}//${window.location.hostname}:${backendPort}${urlRef.current}`
    const ws = new WebSocket(wsUrl)

    ws.onopen = () => {
      setConnected(true)
      onOpenRef.current?.()
    }
    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        onMessageRef.current(data)
      } catch {
        // ignore
      }
    }
    ws.onclose = () => {
      setConnected(false)
      onCloseRef.current?.()
      // Auto-reconnect if enabled and URL is still set
      if (reconnectRef.current && urlRef.current) {
        reconnectTimer.current = setTimeout(() => {
          if (urlRef.current) {
            connect()
          }
        }, reconnectIntervalRef.current)
      }
    }
    ws.onerror = () => {
      setConnected(false)
      onErrorRef.current?.()
    }
    wsRef.current = ws
  }, []) // stable — no dependencies, all values read from refs

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
