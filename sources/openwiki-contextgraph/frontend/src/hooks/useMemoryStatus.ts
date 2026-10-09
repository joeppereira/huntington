import { useCallback, useEffect, useRef, useState } from 'react'
import { fetchMemoryStatus, requestMemorySync, type MemoryStatus } from '../api'

const IDLE_FACTOR = 5 // poll this many times slower while nothing is syncing

const isBusy = (s: MemoryStatus | null) => s !== null && (s.state === 'queued' || s.state === 'syncing')

/** Polls /api/memory/status: every `pollMs` while a sync is queued or running, slower otherwise. */
export function useMemoryStatus(pollMs = 3000) {
  const [status, setStatus] = useState<MemoryStatus | null>(null)
  const [unavailable, setUnavailable] = useState(false)
  const timer = useRef<ReturnType<typeof setTimeout> | undefined>(undefined)
  const controller = useRef<AbortController | null>(null)

  const refresh = useCallback(async () => {
    clearTimeout(timer.current)
    controller.current?.abort()
    const ctrl = new AbortController()
    controller.current = ctrl
    let next: MemoryStatus | null = null
    try {
      next = await fetchMemoryStatus(ctrl.signal)
      setStatus(next)
      setUnavailable(false)
    } catch {
      if (ctrl.signal.aborted) return
      setUnavailable(true)
    }
    timer.current = setTimeout(() => void refresh(), isBusy(next) ? pollMs : pollMs * IDLE_FACTOR)
  }, [pollMs])

  useEffect(() => {
    void refresh()
    return () => {
      clearTimeout(timer.current)
      controller.current?.abort()
    }
  }, [refresh])

  const syncNow = useCallback(async () => {
    try {
      setStatus(await requestMemorySync())
    } finally {
      void refresh()
    }
  }, [refresh])

  return { status, unavailable, refresh, syncNow }
}
