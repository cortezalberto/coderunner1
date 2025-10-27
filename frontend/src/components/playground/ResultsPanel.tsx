import { memo } from 'react'
import { SubmissionResult } from '../../types/api'
import { TestResultsList } from './TestResultsList'

interface ResultsPanelProps {
  result: SubmissionResult | null
}

/**
 * Results Panel Component
 *
 * Displays submission results including:
 * - Success/failure status
 * - Score
 * - Test results
 * - Stdout/stderr
 *
 * OPTIMIZATION: Memoized to prevent re-renders when result hasn't changed.
 * Results can be large (test_results array), memoization improves performance.
 */
export const ResultsPanel = memo(({ result }: ResultsPanelProps) => {
  if (!result) {
    return null
  }

  return (
    <div className="results">
      <h3>📊 Resultados</h3>

      {result.status === 'completed' && (
        <>
          <div className={`status ${result.ok ? 'success' : 'error'}`}>
            {result.ok ? '✅ Todos los tests pasaron!' : '❌ Algunos tests fallaron'}
          </div>

          <div className="score">
            Puntaje: {result.score_total || 0} / {result.score_max || 0}
          </div>

          <div>
            <strong>Tests:</strong> {result.passed || 0} pasados, {result.failed || 0} fallados, {result.errors || 0} errores
          </div>
          <div>
            <strong>Duración:</strong> {result.duration_sec || 0}s
          </div>

          {result.test_results && result.test_results.length > 0 && (
            <TestResultsList testResults={result.test_results} />
          )}

          {result.stdout && (
            <div className="output-section">
              <h4>Salida estándar:</h4>
              <pre className="output-pre">{result.stdout}</pre>
            </div>
          )}

          {result.stderr && (
            <div className="output-section">
              <h4>Errores:</h4>
              <pre className="output-pre">{result.stderr}</pre>
            </div>
          )}
        </>
      )}

      {result.status === 'timeout' && (
        <div className="status error">
          ⏱️ Timeout: {result.error_message}
        </div>
      )}

      {result.status === 'failed' && (
        <div className="status error">
          ❌ Error: {result.error_message}
        </div>
      )}

      {result.status === 'error' && (
        <div className="status error">
          ❌ {result.error_message}
        </div>
      )}
    </div>
  )
}, (prevProps, nextProps) => {
  // Deep comparison: only re-render if result actually changed
  // Compare job_id and status as proxy for result equality
  if (!prevProps.result && !nextProps.result) return true
  if (!prevProps.result || !nextProps.result) return false
  return prevProps.result.job_id === nextProps.result.job_id &&
         prevProps.result.status === nextProps.result.status
})
