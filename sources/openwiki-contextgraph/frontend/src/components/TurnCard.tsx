import Markdown from 'react-markdown'
import type { ChatTurn } from '../api'
import { DecisionTrace } from './DecisionTrace'
import { RetrievalPath } from './RetrievalPath'

interface TurnCardProps {
  turn: ChatTurn
  onAsk: (question: string) => void
  disabled?: boolean
}

export function TurnCard({ turn, onAsk, disabled = false }: TurnCardProps) {
  return (
    <article className="turn">
      <div className="turn__header">
        <span className="turn__number">Turn {turn.turn}</span>
        <span className={`badge badge--${turn.confidence}`}>Confidence: {turn.confidence}</span>
      </div>
      {/* react-markdown does not render raw HTML, so model output cannot inject markup. */}
      <div className="turn__answer">
        <Markdown>{turn.answer}</Markdown>
      </div>
      {turn.sources.length > 0 ? (
        <ul className="turn__sources" aria-label="Sources">
          {turn.sources.map((source) => (
            <li key={source.ref}>
              <code>{source.ref}</code>
              <span className="turn__why"> - {source.why}</span>
            </li>
          ))}
        </ul>
      ) : null}
      {turn.follow_up_questions.length > 0 ? (
        <div className="turn__followups">
          {turn.follow_up_questions.map((question) => (
            <button key={question} type="button" className="chip" disabled={disabled} onClick={() => onAsk(question)}>
              {question}
            </button>
          ))}
        </div>
      ) : null}
      {turn.retrieval ? <RetrievalPath path={turn.retrieval} /> : null}
      <DecisionTrace turn={turn} />
    </article>
  )
}
