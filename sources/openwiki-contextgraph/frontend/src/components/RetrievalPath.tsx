import type { RetrievalNode, RetrievalPath as Path } from '../api'

interface RetrievalPathProps {
  path: Path
}

const plural = (n: number, word: string) => `${n} ${word}${n === 1 ? '' : 's'}`

function stepLabel(tool: string, input: string, titles: string[]): string {
  const names = titles.join(', ')
  return tool === 'semantic_search' ? `Searched ${input} → ${names || 'no nodes'}` : `Opened ${names || input}`
}

function discovery(node: RetrievalNode): string {
  if (node.found_in_step === null) return 'not returned by a tool'
  return node.best_rank === null ? `step ${node.found_in_step}` : `step ${node.found_in_step}, #${node.best_rank}`
}

/**
 * Which semantic-graph nodes (wiki pages) the agent found, opened and cited for one answer.
 * OpenWiki search ranks page sections by keyword; it does not walk graph edges, so links are shown
 * separately as context for where the evidence sits in the graph.
 */
export function RetrievalPath({ path }: RetrievalPathProps) {
  if (path.nodes.length === 0) return null
  const title = new Map(path.nodes.map((n) => [n.id, n.title]))
  const opened = path.nodes.filter((n) => n.opened).length
  const cited = path.nodes.filter((n) => n.cited).length

  return (
    <details className="path">
      <summary>
        How the answer was found: {plural(path.nodes.length, 'graph node')} ({opened} opened, {cited} cited)
      </summary>
      <div className="path__body">
        <p className="path__note">
          OpenWiki search ranks every section of the semantic graph by keyword match (titles and headings weigh
          most). The agent then opens the sections it needs. Each node below is a page in the Semantic Graph tab.
        </p>

        <ol className="path__steps" aria-label="Retrieval steps">
          {path.steps.map((s) => (
            <li key={s.step}>
              Step {s.step} · {stepLabel(s.tool, s.input, s.node_ids.map((id) => title.get(id) ?? id))}
            </li>
          ))}
        </ol>

        <div className="path__table-wrap">
          <table className="path__table">
            <thead>
              <tr>
                <th>Node</th>
                <th>Type</th>
                <th>Found</th>
                <th>Sections</th>
                <th>Role</th>
              </tr>
            </thead>
            <tbody>
              {path.nodes.map((n) => (
                <tr key={n.id}>
                  <td>
                    <span className="path__title">{n.title}</span>
                    <code className="path__id">{n.id}</code>
                  </td>
                  <td>{n.type ?? '-'}</td>
                  <td>{discovery(n)}</td>
                  <td>
                    {n.sections.map((s) => (
                      <code key={s} className="path__section">
                        {s}
                      </code>
                    ))}
                  </td>
                  <td className="path__roles">
                    {n.opened ? <span className="role role--opened">opened</span> : null}
                    {n.cited ? <span className="role role--cited">cited</span> : null}
                    {!n.opened && !n.cited ? <span className="role">found only</span> : null}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <p className="path__label">Links between these nodes in the graph</p>
        {!path.graph_available ? (
          <p className="path__note">The semantic graph could not be loaded, so links are not shown.</p>
        ) : path.links.length === 0 ? (
          <p className="path__note">None of these nodes link to each other directly.</p>
        ) : (
          <ul className="path__links" aria-label="Links between these nodes">
            {path.links.map((l) => (
              <li key={`${l.source}>${l.target}`}>
                {title.get(l.source) ?? l.source} → {title.get(l.target) ?? l.target}
              </li>
            ))}
          </ul>
        )}
      </div>
    </details>
  )
}
