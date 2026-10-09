import type { ReactNode } from 'react'

interface GraphFrameProps {
  title: string
  /** undefined: still loading config; null: graph not available */
  url: string | null | undefined
  emptyMessage: ReactNode
  /** Rendered over the iframe (e.g. "memory appears after the first sync"). */
  overlay?: ReactNode
  /** Changing this remounts the iframe (e.g. after the backend restarted the visualizer). */
  reloadKey?: string | null
}

/** Embeds an OpenWiki visualizer. The visualizer is never proxied: it is loaded from its own origin. */
export function GraphFrame({ title, url, emptyMessage, overlay, reloadKey }: GraphFrameProps) {
  if (url === undefined) {
    return <div className="graph-frame graph-frame--message">Connecting to backend…</div>
  }
  if (url === null) {
    return <div className="graph-frame graph-frame--message">{emptyMessage}</div>
  }
  return (
    <div className="graph-frame">
      <div className="graph-frame__bar">
        <span className="graph-frame__title">{title}</span>
        <a href={url} target="_blank" rel="noreferrer">
          Open in new tab ↗
        </a>
      </div>
      {/* allow-scripts + allow-same-origin is safe here: the visualizer runs on another origin
          (its own port), so it cannot reach this page; the sandbox still blocks top navigation. */}
      <iframe
        key={reloadKey ?? 'initial'}
        className="graph-frame__iframe"
        src={url}
        title={title}
        sandbox="allow-scripts allow-same-origin allow-popups allow-popups-to-escape-sandbox"
      />
      {overlay ? <div className="graph-frame__overlay">{overlay}</div> : null}
    </div>
  )
}
