import { expect, test } from '@playwright/test'

const mockedTurn = (sessionId: string, turn: number, question: string) => ({
  session_id: sessionId,
  turn,
  answer: `Answer to: ${question}. The CET1 ratio was **15.1%**.`,
  sources: [{ ref: 'openwiki/metrics/cet1-ratio.md#requirement-stack-and-management-target', why: 'requirement stack' }],
  confidence: 'high',
  follow_up_questions: ['What drives the stress capital buffer?'],
  reasoning_summary: 'Searched the wiki for CET1.',
  trace: {
    steps: [{ step: 1, tool: 'semantic_search', input: '"CET1"', result: '8 hits: openwiki/metrics/cet1-ratio.md#x', ms: 40 }],
    latency_ms: 1200,
    input_tokens: 5000,
    output_tokens: 300,
    model: 'claude-sonnet-5-5',
  },
})

test('chat UI renders answers, trace and follow-ups (mocked /api/chat)', async ({ page }) => {
  let turn = 0
  const bodies: Array<{ session_id: string; message: string }> = []
  await page.route('**/api/chat', async (route) => {
    const body = route.request().postDataJSON() as { session_id: string; message: string }
    bodies.push(body)
    turn += 1
    await route.fulfill({ json: mockedTurn(body.session_id, turn, body.message) })
  })

  await page.goto('/agent')
  const input = page.getByRole('textbox', { name: 'Ask a question' })
  await expect(input).toBeEnabled()
  const sessionLabel = await page.locator('.chat__session').textContent()
  expect(sessionLabel).toMatch(/Session \d{8}-\d{6}-[0-9a-f]{4}/)

  await input.fill('What was the CET1 ratio?')
  await input.press('Enter')
  const card = page.locator('.turn').first()
  await expect(card.getByText('15.1%')).toBeVisible()
  await expect(card.getByText('Confidence: high')).toBeVisible()
  await expect(card.getByText('openwiki/metrics/cet1-ratio.md#requirement-stack-and-management-target')).toBeVisible()

  await card.getByText(/Decision trace \(1 step/).click()
  await expect(card.getByRole('table')).toContainText('semantic_search')
  await expect(card.getByText(/agent self-report/i)).toBeVisible()

  await card.getByRole('button', { name: 'What drives the stress capital buffer?' }).click()
  await expect(page.locator('.turn')).toHaveCount(2)
  expect(bodies.map((b) => b.message)).toEqual(['What was the CET1 ratio?', 'What drives the stress capital buffer?'])
  expect(new Set(bodies.map((b) => b.session_id)).size).toBe(1)
})

test('real agent answers through the whole stack', async ({ page }) => {
  test.skip(process.env.RUN_LIVE !== '1', 'set RUN_LIVE=1 to call the Anthropic API')
  test.setTimeout(180_000)
  await page.goto('/agent')
  const input = page.getByRole('textbox', { name: 'Ask a question' })
  await expect(input).toBeEnabled()
  await input.fill("What was Meridian Harbor's CET1 ratio at year-end 2025?")
  await input.press('Enter')
  const card = page.locator('.turn').first()
  await expect(card).toBeVisible({ timeout: 150_000 })
  await expect(card.locator('.turn__answer')).toContainText(/15\.1|15\.08/)
  await expect(card.locator('.turn__sources')).toContainText('openwiki/')
  await page.screenshot({ path: 'test-results/agent-page-live.png', fullPage: true })
})
