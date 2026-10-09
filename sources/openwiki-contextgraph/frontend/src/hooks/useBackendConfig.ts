import { useEffect, useState } from 'react'
import { fetchConfig, type BackendConfig } from '../api'

interface ConfigState {
  config: BackendConfig | null
  error: string | null
}

/** Loads /api/config, retrying until the backend answers (it may start after the frontend). */
export function useBackendConfig(retryMs = 2000): ConfigState {
  const [state, setState] = useState<ConfigState>({ config: null, error: null })

  useEffect(() => {
    const controller = new AbortController()
    let timer: ReturnType<typeof setTimeout> | undefined

    const load = async () => {
      try {
        const config = await fetchConfig(controller.signal)
        setState({ config, error: null })
      } catch (err) {
        if (controller.signal.aborted) return
        setState({ config: null, error: err instanceof Error ? err.message : String(err) })
        timer = setTimeout(load, retryMs)
      }
    }
    void load()

    return () => {
      controller.abort()
      clearTimeout(timer)
    }
  }, [retryMs])

  return state
}
