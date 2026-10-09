import { renderHook, waitFor } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import { mockFetchJson, readyConfig } from '../test/fixtures'
import { useBackendConfig } from './useBackendConfig'

describe('useBackendConfig', () => {
  it('loads /api/config', async () => {
    const fetchMock = mockFetchJson(readyConfig)
    const { result } = renderHook(() => useBackendConfig(10))
    await waitFor(() => expect(result.current.config).toEqual(readyConfig))
    expect(fetchMock).toHaveBeenCalledWith('/api/config', expect.anything())
    expect(result.current.error).toBeNull()
  })

  it('retries until the backend answers, reporting the error meanwhile', async () => {
    const fetchMock = mockFetchJson(new Error('ECONNREFUSED'), new Error('ECONNREFUSED'), readyConfig)
    const { result } = renderHook(() => useBackendConfig(10))
    await waitFor(() => expect(result.current.config).toEqual(readyConfig))
    expect(fetchMock).toHaveBeenCalledTimes(3)
    expect(result.current.error).toBeNull()
  })

  it('rejects a malformed config response', async () => {
    mockFetchJson({ semantic_ready: 'yes' })
    const { result } = renderHook(() => useBackendConfig(10_000))
    await waitFor(() => expect(result.current.error).not.toBeNull())
    expect(result.current.config).toBeNull()
  })
})
