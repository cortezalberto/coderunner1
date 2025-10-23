import { useState, useEffect } from 'react'
import Editor from '@monaco-editor/react'
import axios from 'axios'

function Playground() {
  const [problems, setProblems] = useState({})
  const [selectedProblem, setSelectedProblem] = useState('')
  const [code, setCode] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [polling, setPolling] = useState(false)

  useEffect(() => {
    // Cargar lista de problemas
    axios.get('/api/problems')
      .then(res => {
        setProblems(res.data)
        const firstProblem = Object.keys(res.data)[0]
        if (firstProblem) {
          setSelectedProblem(firstProblem)
          setCode(res.data[firstProblem].starter || '')
        }
      })
      .catch(err => console.error('Error loading problems:', err))
  }, [])

  useEffect(() => {
    // Cambiar código cuando cambia el problema
    if (selectedProblem && problems[selectedProblem]) {
      setCode(problems[selectedProblem].starter || '')
      setResult(null)
    }
  }, [selectedProblem, problems])

  const handleSubmit = async () => {
    if (!selectedProblem || !code.trim()) return

    setLoading(true)
    setResult(null)

    try {
      // Enviar código
      const submitRes = await axios.post('/api/submit', {
        problem_id: selectedProblem,
        code: code,
        student_id: 'demo-student'
      })

      const jobId = submitRes.data.job_id

      // Polling del resultado
      setPolling(true)
      pollResult(jobId)

    } catch (err) {
      console.error('Error submitting:', err)
      setResult({
        status: 'error',
        error_message: err.response?.data?.detail || 'Error al enviar código'
      })
      setLoading(false)
    }
  }

  const pollResult = async (jobId) => {
    const maxAttempts = 30
    let attempts = 0

    const poll = async () => {
      try {
        const res = await axios.get(`/api/result/${jobId}`)
        const data = res.data

        if (data.status === 'completed' || data.status === 'failed' || data.status === 'timeout') {
          setResult(data)
          setLoading(false)
          setPolling(false)
        } else {
          attempts++
          if (attempts < maxAttempts) {
            setTimeout(poll, 1000)
          } else {
            setResult({
              status: 'error',
              error_message: 'Timeout esperando resultado'
            })
            setLoading(false)
            setPolling(false)
          }
        }
      } catch (err) {
        console.error('Error polling:', err)
        setResult({
          status: 'error',
          error_message: 'Error consultando resultado'
        })
        setLoading(false)
        setPolling(false)
      }
    }

    poll()
  }

  const currentProblem = problems[selectedProblem]

  return (
    <>
      <div className="problem-selector">
        <select
          value={selectedProblem}
          onChange={(e) => setSelectedProblem(e.target.value)}
        >
          {Object.keys(problems).map(key => (
            <option key={key} value={key}>
              {problems[key].metadata?.title || key}
            </option>
          ))}
        </select>
      </div>

      <div className="editor-container">
        <div className="panel">
          <h2>📝 Enunciado</h2>
          <div className="prompt">
            {currentProblem?.prompt ? (
              <pre style={{ whiteSpace: 'pre-wrap', fontFamily: 'inherit' }}>
                {currentProblem.prompt}
              </pre>
            ) : (
              <p>Selecciona un problema para comenzar</p>
            )}
          </div>
        </div>

        <div className="panel">
          <h2>💻 Editor</h2>
          <div className="editor-wrapper">
            <Editor
              height="400px"
              defaultLanguage="python"
              theme="vs-dark"
              value={code}
              onChange={(value) => setCode(value || '')}
              options={{
                minimap: { enabled: false },
                fontSize: 14,
                lineNumbers: 'on',
                scrollBeyondLastLine: false
              }}
            />
          </div>
          <button
            className="submit-btn"
            onClick={handleSubmit}
            disabled={loading || !code.trim()}
          >
            {loading ? '⏳ Ejecutando tests...' : '▶️ Ejecutar tests'}
          </button>
        </div>
      </div>

      {result && (
        <div className="results">
          <h3>📊 Resultados</h3>

          {result.status === 'completed' && (
            <>
              <div className={`status ${result.ok ? 'success' : 'error'}`}>
                {result.ok ? '✅ Todos los tests pasaron!' : '❌ Algunos tests fallaron'}
              </div>

              <div className="score">
                Puntaje: {result.score_total} / {result.score_max}
              </div>

              <div>
                <strong>Tests:</strong> {result.passed} pasados, {result.failed} fallados, {result.errors} errores
              </div>
              <div>
                <strong>Duración:</strong> {result.duration_sec}s
              </div>

              {result.test_results && result.test_results.length > 0 && (
                <div className="test-results">
                  <h4>Detalle de tests:</h4>
                  {result.test_results
                    .filter(t => t.visibility === 'public')
                    .map((test, idx) => (
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

                  {result.test_results.some(t => t.visibility === 'hidden') && (
                    <div className="test-item" style={{ borderLeftColor: '#94a3b8' }}>
                      <div className="test-name">🔒 Tests ocultos ejecutados</div>
                      <div className="test-message">
                        Los detalles de los tests ocultos no son visibles
                      </div>
                    </div>
                  )}
                </div>
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
      )}
    </>
  )
}

export default Playground
