import type { BackendConfig } from '../api'
import { GraphFrame } from '../components/GraphFrame'

interface SemanticGraphPageProps {
  config: BackendConfig | null
  hidden: boolean
}

export function SemanticGraphPage({ config, hidden }: SemanticGraphPageProps) {
  return (
    <main className="page page--semantic" hidden={hidden}>
      <GraphFrame
        title="Semantic knowledge graph"
        url={config ? config.semantic_vis_url : undefined}
        emptyMessage={
          <>
            The semantic wiki has not been built yet. Run <code>scripts\build-semantic.ps1</code>, then restart
            the backend.
          </>
        }
      />
    </main>
  )
}
