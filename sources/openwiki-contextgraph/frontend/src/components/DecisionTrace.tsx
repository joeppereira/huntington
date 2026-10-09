import type { ChatTurn } from '../api'

interface DecisionTraceProps {
  turn: ChatTurn
}

/** Observed tool calls (from the backend's callback handler) plus the agent's self-reported reasoning. */
export function DecisionTrace({ turn }: DecisionTraceProps) {
  const { steps, latency_ms, input_tokens, output_tokens, model } = turn.trace
  const seconds = (latency_ms / 1000).toFixed(1)
  return (
    <details className="trace">
      <summary>
        Decision trace ({steps.length} step{steps.length === 1 ? '' : 's'}, {seconds} s)
      </summary>
      <div className="trace__body">
        <table className="trace__table">
          <thead>
            <tr>
              <th>#</th>
              <th>Tool</th>
              <th>Input</th>
              <th>Result</th>
              <th>ms</th>
            </tr>
          </thead>
          <tbody>
            {steps.map((step) => (
              <tr key={step.step}>
                <td>{step.step}</td>
                <td>
                  <code>{step.tool}</code>
                </td>
                <td>{step.input}</td>
                <td>{step.result}</td>
                <td>{step.ms}</td>
              </tr>
            ))}
          </tbody>
        </table>
        <p className="trace__meta">
          {model} · {input_tokens.toLocaleString()} input / {output_tokens.toLocaleString()} output tokens
        </p>
        <p className="trace__reasoning">
          <span className="trace__label">Reasoning (agent self-report):</span> {turn.reasoning_summary}
        </p>
      </div>
    </details>
  )
}
