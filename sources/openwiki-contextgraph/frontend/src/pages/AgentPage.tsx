import { useState } from 'react'
import { resetDemo, type BackendConfig } from '../api'
import { ChatPanel } from '../components/ChatPanel'
import { GraphFrame } from '../components/GraphFrame'
import { MemoryStatusPill } from '../components/MemoryStatusPill'
import { useMemoryStatus } from '../hooks/useMemoryStatus'

interface AgentPageProps {
  config: BackendConfig | null
  hidden: boolean
  memoryPollMs?: number
}

interface ResetState {
  count: number // bumps on each reset: remounts the chat and the memory iframe
  sessionId?: string // session the backend created during the reset
  confirming: boolean
  running: boolean
  error: string | null
}

export function AgentPage({ config, hidden, memoryPollMs = 3000 }: AgentPageProps) {
  const { status, unavailable, refresh, syncNow } = useMemoryStatus(memoryPollMs)
  const [reset, setReset] = useState<ResetState>({ count: 0, confirming: false, running: false, error: null })
  const busy = status?.state === 'queued' || status?.state === 'syncing'

  const runReset = async () => {
    setReset((r) => ({ ...r, confirming: false, running: true, error: null }))
    try {
      const result = await resetDemo()
      setReset((r) => ({ count: r.count + 1, sessionId: result.session_id, confirming: false, running: false, error: null }))
    } catch (err) {
      const message = err instanceof Error ? err.message : String(err)
      setReset((r) => ({ ...r, running: false, error: `Reset failed: ${message}` }))
    } finally {
      void refresh()
    }
  }

  return (
    <main className="page page--agent" hidden={hidden}>
      <section className="agent__memory">
        <div className="memory__bar">
          <MemoryStatusPill status={status} unavailable={unavailable} />
          <div className="memory__actions">
            <button type="button" className="button button--secondary" disabled={busy} onClick={() => void syncNow()}>
              Sync memory now
            </button>
            <button
              type="button"
              className="button button--secondary button--danger"
              disabled={reset.running}
              onClick={() => setReset((r) => ({ ...r, confirming: true, error: null }))}
            >
              {reset.running ? 'Resetting…' : 'Reset demo'}
            </button>
          </div>
        </div>
        {reset.confirming ? (
          <div className="memory__confirm">
            <span>Wipe the agent's memory and start a new chat? This deletes all turns and the memory graph.</span>
            <button type="button" className="button button--danger-solid" onClick={() => void runReset()}>
              Wipe memory
            </button>
            <button type="button" className="button button--secondary" onClick={() => setReset((r) => ({ ...r, confirming: false }))}>
              Cancel
            </button>
          </div>
        ) : null}
        {reset.error ? (
          <p className="memory__error" role="alert">
            {reset.error}
          </p>
        ) : null}
        <div className="memory__graph">
          <GraphFrame
            title="Agent memory graph"
            url={config ? config.context_vis_url : undefined}
            emptyMessage="The context visualizer is not running; check the backend log."
            overlay={status && !status.initialized ? 'Memory graph appears after the first synced turn.' : undefined}
            reloadKey={`${reset.count}:${status?.last_success_at ?? ''}`}
          />
        </div>
      </section>
      <section className="agent__chat">
        <ChatPanel key={reset.count} initialSessionId={reset.sessionId} onTurnCompleted={() => void refresh()} />
      </section>
    </main>
  )
}
