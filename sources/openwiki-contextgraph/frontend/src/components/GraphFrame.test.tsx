import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import { GraphFrame } from './GraphFrame'

describe('GraphFrame', () => {
  it('embeds the visualizer URL and offers a new-tab link', () => {
    render(<GraphFrame title="Semantic graph" url="http://127.0.0.1:4321" emptyMessage="not built" />)
    const iframe = screen.getByTitle('Semantic graph')
    expect(iframe).toHaveAttribute('src', 'http://127.0.0.1:4321')
    // Visualizer needs scripts + its own origin (fetch /api/graph, SSE) but must not navigate our tab.
    expect(iframe.getAttribute('sandbox')?.split(' ').sort()).toEqual(
      ['allow-popups', 'allow-popups-to-escape-sandbox', 'allow-same-origin', 'allow-scripts'],
    )
    const link = screen.getByRole('link', { name: /open in new tab/i })
    expect(link).toHaveAttribute('href', 'http://127.0.0.1:4321')
    expect(link).toHaveAttribute('target', '_blank')
  })

  it('shows the empty message instead of an iframe when there is no URL', () => {
    render(<GraphFrame title="Semantic graph" url={null} emptyMessage="Run scripts/build-semantic.ps1" />)
    expect(screen.queryByTitle('Semantic graph')).not.toBeInTheDocument()
    expect(screen.getByText('Run scripts/build-semantic.ps1')).toBeInTheDocument()
  })

  it('shows a loading message while the URL is unknown', () => {
    render(<GraphFrame title="Semantic graph" url={undefined} emptyMessage="x" />)
    expect(screen.getByText(/connecting to backend/i)).toBeInTheDocument()
  })
})

describe('GraphFrame reloadKey', () => {
  it('remounts the iframe when the reload key changes, and only then', () => {
    const { rerender } = render(<GraphFrame title="Memory" url="http://127.0.0.1:4322" emptyMessage="x" reloadKey="a" />)
    const first = screen.getByTitle('Memory')
    rerender(<GraphFrame title="Memory" url="http://127.0.0.1:4322" emptyMessage="x" reloadKey="a" />)
    expect(screen.getByTitle('Memory')).toBe(first)
    rerender(<GraphFrame title="Memory" url="http://127.0.0.1:4322" emptyMessage="x" reloadKey="b" />)
    expect(screen.getByTitle('Memory')).not.toBe(first)
  })
})
