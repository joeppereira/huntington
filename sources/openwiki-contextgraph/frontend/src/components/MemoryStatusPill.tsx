import type { MemoryStatus } from '../api'

const turns = (n: number) => `${n} turn${n === 1 ? '' : 's'}`

export function memoryLabel(status: MemoryStatus | null, unavailable = false): string {
  if (unavailable) return 'Memory: status unavailable'
  if (status === null) return 'Memory: …'
  const pending = turns(status.pending_turns)
  switch (status.state) {
    case 'error':
      return status.pending_turns > 0 ? `Memory: sync failed (${pending} pending)` : 'Memory: sync failed'
    case 'queued':
    case 'syncing':
      return `Memory: ${status.state} (${pending} pending)`
    default:
      if (status.pending_turns > 0) return `Memory: ${pending} not synced`
      if (!status.initialized) return 'Memory: empty'
      return status.last_duration_s === null
        ? 'Memory: up to date'
        : `Memory: up to date (last sync ${Math.round(status.last_duration_s)} s)`
  }
}

/** Memory lags the chat: each sync is a full OpenWiki run, so the pill makes the lag explicit. */
export function MemoryStatusPill({ status, unavailable = false }: { status: MemoryStatus | null; unavailable?: boolean }) {
  const tone = unavailable ? 'error' : (status?.state ?? 'idle')
  const title = unavailable ? 'The backend did not answer; retrying.' : (status?.last_error ?? undefined)
  return (
    <span role="status" className={`pill pill--${tone}`} title={title}>
      {memoryLabel(status, unavailable)}
    </span>
  )
}
