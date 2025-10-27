import { memo } from 'react'
import { Problem } from '../../types/api'

interface ProblemPromptProps {
  problem: Problem | undefined
}

/**
 * Problem Prompt Component
 *
 * Displays the problem statement/description.
 *
 * OPTIMIZATION: Memoized to prevent unnecessary re-renders.
 * Only re-renders when problem.prompt changes.
 */
export const ProblemPrompt = memo(({ problem }: ProblemPromptProps) => {
  return (
    <div className="panel">
      <h2>📝 Enunciado</h2>
      <div className="prompt">
        {problem?.prompt ? (
          <pre style={{ whiteSpace: 'pre-wrap', fontFamily: 'inherit' }}>
            {problem.prompt}
          </pre>
        ) : (
          <p>Selecciona un problema para comenzar</p>
        )}
      </div>
    </div>
  )
}, (prevProps, nextProps) => {
  // Custom comparison: only re-render if prompt actually changed
  return prevProps.problem?.prompt === nextProps.problem?.prompt
})
