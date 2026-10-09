import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter } from 'react-router'
import { describe, expect, it } from 'vitest'
import App from './App'
import { readyConfig, stubRoutes } from './test/fixtures'

function renderAt(path: string) {
  return render(
    <MemoryRouter initialEntries={[path]}>
      <App />
    </MemoryRouter>,
  )
}

describe('App', () => {
  it('redirects / to the semantic graph page', async () => {
    stubRoutes({ '/api/config': readyConfig, '/api/sessions': { session_id: 's1' } })
    renderAt('/')
    expect(await screen.findByRole('link', { name: 'Semantic Graph' })).toHaveAttribute('aria-current', 'page')
  })

  it('keeps both iframes mounted when switching pages', async () => {
    stubRoutes({ '/api/config': readyConfig, '/api/sessions': { session_id: 's1' } })
    renderAt('/semantic')
    const semantic = await screen.findByTitle('Semantic knowledge graph')
    const context = await screen.findByTitle('Agent memory graph')
    expect(semantic).toBeVisible()
    expect(context).not.toBeVisible()

    await userEvent.click(screen.getByRole('link', { name: 'Agent & Memory' }))
    await waitFor(() => expect(context).toBeVisible())
    expect(semantic).not.toBeVisible()
    // Same DOM nodes: the visualizers were not reloaded.
    expect(screen.getByTitle('Semantic knowledge graph')).toBe(semantic)
    expect(screen.getByTitle('Agent memory graph')).toBe(context)
  })

  it('tells the user to build the semantic wiki when it is missing', async () => {
    stubRoutes({ '/api/config': { ...readyConfig, semantic_vis_url: null, semantic_ready: false } })
    renderAt('/semantic')
    expect(await screen.findByText(/scripts\\build-semantic\.ps1/)).toBeInTheDocument()
  })

  it('shows a backend-unreachable banner while config fails', async () => {
    stubRoutes({ '/api/config': new Error('down') })
    renderAt('/semantic')
    expect(await screen.findByText(/backend not reachable/i)).toBeInTheDocument()
  })
})
