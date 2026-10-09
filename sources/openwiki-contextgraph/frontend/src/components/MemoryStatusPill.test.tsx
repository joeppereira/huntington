import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import type { MemoryStatus } from '../api'
import { idleMemory } from '../test/fixtures'
import { MemoryStatusPill } from './MemoryStatusPill'

const status = (overrides: Partial<MemoryStatus>) => ({ ...(idleMemory as MemoryStatus), ...overrides })

describe('MemoryStatusPill', () => {
  it.each([
    [{ state: 'idle', initialized: false }, 'Memory: empty'],
    [{ state: 'idle', initialized: true, last_duration_s: 72.4 }, 'Memory: up to date (last sync 72 s)'],
    [{ state: 'queued', pending_turns: 1 }, 'Memory: queued (1 turn pending)'],
    [{ state: 'syncing', pending_turns: 2 }, 'Memory: syncing (2 turns pending)'],
    [{ state: 'idle', mode: 'manual', pending_turns: 3, initialized: true }, 'Memory: 3 turns not synced'],
    [{ state: 'error', pending_turns: 1, last_error: 'openwiki exited with code 1' }, 'Memory: sync failed (1 turn pending)'],
  ] as const)('%o -> %s', (overrides, text) => {
    render(<MemoryStatusPill status={status(overrides as Partial<MemoryStatus>)} />)
    expect(screen.getByRole('status')).toHaveTextContent(text)
  })

  it('shows the error tail as a tooltip', () => {
    render(<MemoryStatusPill status={status({ state: 'error', last_error: 'boom: provider error' })} />)
    expect(screen.getByRole('status')).toHaveAttribute('title', 'boom: provider error')
  })

  it('renders nothing useful before the first status arrives', () => {
    render(<MemoryStatusPill status={null} />)
    expect(screen.getByRole('status')).toHaveTextContent('Memory: …')
  })
})
