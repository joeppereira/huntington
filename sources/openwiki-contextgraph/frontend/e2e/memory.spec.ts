import { expect, test } from '@playwright/test'

const status = (overrides: Record<string, unknown>) => ({
  state: 'idle',
  mode: 'per_turn',
  pending_turns: 0,
  last_success_at: null,
  last_duration_s: null,
  last_error: null,
  initialized: false,
  ...overrides,
})

test('memory pane shows sync status, overlay and manual sync (mocked status)', async ({ page }) => {
  let current = status({})
  let syncRequests = 0
  await page.route('**/api/memory/status', (route) => route.fulfill({ json: current }))
  await page.route('**/api/memory/sync', async (route) => {
    syncRequests += 1
    current = status({ state: 'syncing', pending_turns: 1 })
    await route.fulfill({ status: 202, json: current })
  })

  await page.goto('/agent')
  await expect(page.getByRole('status')).toHaveText('Memory: empty')
  await expect(page.getByText('Memory graph appears after the first synced turn.')).toBeVisible()

  await page.getByRole('button', { name: 'Sync memory now' }).click()
  await expect(page.getByRole('status')).toHaveText('Memory: syncing (1 turn pending)')
  await expect(page.getByRole('button', { name: 'Sync memory now' })).toBeDisabled()
  expect(syncRequests).toBe(1)

  current = status({ initialized: true, last_duration_s: 64.2, last_success_at: '2026-10-05T07:00:00Z' })
  await expect(page.getByRole('status')).toHaveText('Memory: up to date (last sync 64 s)', { timeout: 10_000 })
  await expect(page.getByText('Memory graph appears after the first synced turn.')).toBeHidden()
})

test('reset demo wipes memory and starts a new session (real backend)', async ({ page }) => {
  await page.goto('/agent')
  const session = page.locator('.chat__session')
  await expect(session).toHaveText(/Session \d{8}-\d{6}-[0-9a-f]{4}/)
  const before = await session.textContent()

  await page.getByRole('button', { name: 'Reset demo' }).click()
  await expect(page.getByText(/wipe the agent's memory/i)).toBeVisible()
  await page.getByRole('button', { name: 'Wipe memory' }).click()

  await expect(session).not.toHaveText(before ?? '', { timeout: 20_000 })
  await expect(session).toHaveText(/Session \d{8}-\d{6}-[0-9a-f]{4}/)
  await expect(page.getByRole('alert')).toHaveCount(0)
  await expect(page.getByRole('status')).toHaveText('Memory: empty')
  const frame = page.frameLocator('iframe[title="Agent memory graph"]')
  await expect(frame.locator('.topbar')).toBeVisible({ timeout: 30_000 })
})
