import { TestResult } from '../../types/api'

interface TestResultsListProps {
  testResults: TestResult[]
}

/**
 * Test Results List Component
 *
 * Displays detailed test results with public and hidden tests.
 */
export function TestResultsList({ testResults }: TestResultsListProps) {
  const publicTests = testResults.filter(t => t.visibility === 'public')
  const hasHiddenTests = testResults.some(t => t.visibility === 'hidden')

  return (
    <div className="test-results">
      <h4>Detalle de tests:</h4>

      {/* Public Tests */}
      {publicTests.map((test, idx) => (
        <div key={idx} className={`test-item ${test.outcome}`}>
          <div className="test-name">
            {test.outcome === 'passed' && '✅ '}
            {test.outcome === 'failed' && '❌ '}
            {test.outcome === 'error' && '⚠️ '}
            {test.test_name} ({test.points}/{test.max_points} pts)
          </div>
          {test.message && (
            <div className="test-message">{test.message}</div>
          )}
        </div>
      ))}

      {/* Hidden Tests Indicator */}
      {hasHiddenTests && (
        <div className="test-item" style={{ borderLeftColor: '#94a3b8' }}>
          <div className="test-name">🔒 Tests ocultos ejecutados</div>
          <div className="test-message">
            Los detalles de los tests ocultos no son visibles
          </div>
        </div>
      )}
    </div>
  )
}
