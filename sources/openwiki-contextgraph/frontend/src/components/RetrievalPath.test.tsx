import { render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it } from 'vitest'
import type { RetrievalPath as Path } from '../api'
import { RetrievalPath } from './RetrievalPath'

const path: Path = {
  graph_available: true,
  steps: [
    { step: 2, tool: 'semantic_search', input: '"CET1 requirement"', node_ids: ['metrics/cet1-ratio', 'concepts/stress-capital-buffer'] },
    { step: 3, tool: 'semantic_read', input: 'openwiki/metrics/cet1-ratio.md [requirement-stack]', node_ids: ['metrics/cet1-ratio'] },
  ],
  nodes: [
    { id: 'metrics/cet1-ratio', title: 'CET1 Ratio', type: 'FinancialMetric', sections: ['requirement-stack'], found_in_step: 2, best_rank: 1, opened: true, cited: true },
    { id: 'concepts/stress-capital-buffer', title: 'Stress Capital Buffer', type: 'RiskConcept', sections: ['definition'], found_in_step: 2, best_rank: 2, opened: false, cited: false },
  ],
  links: [{ source: 'metrics/cet1-ratio', target: 'concepts/stress-capital-buffer' }],
}

async function open(p: Path = path) {
  render(<RetrievalPath path={p} />)
  await userEvent.click(screen.getByText(/how the answer was found/i))
}

describe('RetrievalPath', () => {
  it('summarises node counts in the toggle', () => {
    render(<RetrievalPath path={path} />)
    expect(screen.getByText('How the answer was found: 2 graph nodes (1 opened, 1 cited)')).toBeInTheDocument()
  })

  it('lists each step with the nodes it reached, by title', async () => {
    await open()
    const steps = screen.getByRole('list', { name: /retrieval steps/i })
    const [search, read] = within(steps).getAllByRole('listitem')
    expect(search).toHaveTextContent('Step 2 · Searched "CET1 requirement" → CET1 Ratio, Stress Capital Buffer')
    expect(read).toHaveTextContent('Step 3 · Opened CET1 Ratio')
  })

  it('shows one row per node with type, discovery, sections and roles', async () => {
    await open()
    const rows = within(screen.getByRole('table')).getAllByRole('row')
    expect(rows).toHaveLength(3)
    expect(rows[1]).toHaveTextContent('CET1 Ratio')
    expect(rows[1]).toHaveTextContent('metrics/cet1-ratio')
    expect(rows[1]).toHaveTextContent('FinancialMetric')
    expect(rows[1]).toHaveTextContent('step 2, #1')
    expect(rows[1]).toHaveTextContent('requirement-stack')
    expect(within(rows[1]).getByText('opened')).toBeInTheDocument()
    expect(within(rows[1]).getByText('cited')).toBeInTheDocument()
    expect(within(rows[2]).queryByText('opened')).not.toBeInTheDocument()
    expect(within(rows[2]).getByText('found only')).toBeInTheDocument()
  })

  it('shows graph links between the visited nodes', async () => {
    await open()
    expect(screen.getByRole('list', { name: /links between these nodes/i })).toHaveTextContent('CET1 Ratio → Stress Capital Buffer')
  })

  it('says when visited nodes are not linked, and when the graph was unavailable', async () => {
    await open({ ...path, links: [] })
    expect(screen.getByText(/none of these nodes link to each other directly/i)).toBeInTheDocument()
  })

  it('marks a node that was cited without being returned by a tool', async () => {
    const node = { ...path.nodes[0], id: 'overview', title: 'Overview', found_in_step: null, best_rank: null, opened: false }
    await open({ ...path, nodes: [node] })
    expect(within(screen.getByRole('table')).getAllByRole('row')[1]).toHaveTextContent('not returned by a tool')
  })

  it('renders nothing when the agent did not use the semantic graph', () => {
    const { container } = render(<RetrievalPath path={{ graph_available: true, steps: [], nodes: [], links: [] }} />)
    expect(container).toBeEmptyDOMElement()
  })
})
