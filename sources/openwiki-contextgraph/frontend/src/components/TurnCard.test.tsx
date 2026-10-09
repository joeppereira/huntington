import { render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it, vi } from 'vitest'
import type { ChatTurn } from '../api'
import { chatTurn } from '../test/fixtures'
import { TurnCard } from './TurnCard'

const turn = chatTurn as ChatTurn

describe('TurnCard', () => {
  it('renders the answer as markdown with a confidence badge', () => {
    render(<TurnCard turn={turn} onAsk={vi.fn()} />)
    expect(screen.getByText('15.1%').tagName).toBe('STRONG')
    expect(screen.getByText(/confidence: high/i)).toBeInTheDocument()
  })

  it('does not render raw HTML from the model', () => {
    render(<TurnCard turn={{ ...turn, answer: 'hi <img src=x onerror="alert(1)">' }} onAsk={vi.fn()} />)
    expect(document.querySelector('img')).toBeNull()
  })

  it('lists sources with their reasons', () => {
    render(<TurnCard turn={turn} onAsk={vi.fn()} />)
    const sources = screen.getByRole('list', { name: /sources/i })
    expect(within(sources).getByText('openwiki/metrics/cet1-ratio.md#requirement-stack')).toBeInTheDocument()
    expect(within(sources).getByText(/lists the requirement stack/)).toBeInTheDocument()
  })

  it('asks a follow-up question when its chip is clicked', async () => {
    const onAsk = vi.fn()
    render(<TurnCard turn={turn} onAsk={onAsk} />)
    await userEvent.click(screen.getByRole('button', { name: 'What drives the stress capital buffer?' }))
    expect(onAsk).toHaveBeenCalledWith('What drives the stress capital buffer?')
  })

  it('disables follow-up chips while another question is pending', () => {
    render(<TurnCard turn={turn} onAsk={vi.fn()} disabled />)
    expect(screen.getByRole('button', { name: 'What drives the stress capital buffer?' })).toBeDisabled()
  })

  it('shows the observed decision trace and the self-reported reasoning on expand', async () => {
    render(<TurnCard turn={turn} onAsk={vi.fn()} />)
    const toggle = screen.getByText(/decision trace \(2 steps, 6\.3 s\)/i)
    expect(screen.queryByRole('table')).not.toBeVisible()
    await userEvent.click(toggle)
    const rows = within(screen.getByRole('table')).getAllByRole('row')
    expect(rows).toHaveLength(3)
    expect(rows[1]).toHaveTextContent('semantic_search')
    expect(rows[1]).toHaveTextContent('8 hits')
    expect(screen.getByText(/agent self-report/i)).toBeInTheDocument()
    expect(screen.getByText('Searched for CET1 and read the metric page.')).toBeInTheDocument()
  })
})
