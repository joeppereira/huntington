import { expect, test } from '@playwright/test'

test('semantic graph page embeds the OpenWiki visualizer', async ({ page }) => {
  await page.goto('/')
  await expect(page).toHaveURL(/\/semantic$/)
  const iframe = page.getByTitle('Semantic knowledge graph')
  await expect(iframe).toHaveAttribute('src', 'http://127.0.0.1:4321')

  const frame = page.frameLocator('iframe[title="Semantic knowledge graph"]')
  await expect(frame.locator('.topbar')).toBeVisible({ timeout: 30_000 })
  await expect(frame.locator('canvas').first()).toBeVisible({ timeout: 30_000 })

  // The visualizer's same-origin requests must still work inside the sandboxed iframe.
  const visFrame = page.frames().find((f) => f.url().startsWith('http://127.0.0.1:4321'))
  expect(visFrame).toBeDefined()
  const graph = await visFrame!.evaluate(async () => {
    const res = await fetch('/api/graph')
    return (await res.json()) as { nodes: unknown[]; edges: unknown[] }
  })
  expect(graph.nodes.length).toBeGreaterThanOrEqual(90)
  expect(graph.edges.length).toBeGreaterThan(500)
})

test('agent page shows the context visualizer next to the chat', async ({ page }) => {
  await page.goto('/agent')
  const iframe = page.getByTitle('Agent memory graph')
  await expect(iframe).toHaveAttribute('src', 'http://127.0.0.1:4322')
  const frame = page.frameLocator('iframe[title="Agent memory graph"]')
  await expect(frame.locator('.topbar')).toBeVisible({ timeout: 30_000 })
  await expect(page.getByRole('textbox', { name: 'Ask a question' })).toBeEnabled()
})

test('switching pages does not reload the visualizers', async ({ page }) => {
  await page.goto('/semantic')
  const frameLocator = page.frameLocator('iframe[title="Semantic knowledge graph"]')
  await expect(frameLocator.locator('canvas').first()).toBeVisible({ timeout: 30_000 })

  const frame = page.frames().find((f) => f.url().startsWith('http://127.0.0.1:4321'))
  expect(frame).toBeDefined()
  await frame!.evaluate(() => {
    ;(window as unknown as { __pocMarker: number }).__pocMarker = 42
  })

  await page.getByRole('link', { name: 'Agent & Memory' }).click()
  await expect(page.getByTitle('Agent memory graph')).toBeVisible()
  await page.getByRole('link', { name: 'Semantic Graph' }).click()
  await expect(page.getByTitle('Semantic knowledge graph')).toBeVisible()

  const marker = await frame!.evaluate(() => (window as unknown as { __pocMarker?: number }).__pocMarker)
  expect(marker).toBe(42)
})
