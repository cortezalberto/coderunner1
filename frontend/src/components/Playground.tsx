import { useState, useEffect, useCallback, useRef } from 'react'
import Editor from '@monaco-editor/react'
import axios, { AxiosError } from 'axios'
import {
  Subject,
  Unit,
  Problem,
  ProblemsResponse,
  SubmissionResult,
  SubmitRequest,
  SubmitResponse,
  SubjectsResponse,
  UnitsResponse
} from '../types/api'

interface PlaygroundProps {
  onSubjectChange?: (subjectId: string) => void
}

function Playground({ onSubjectChange }: PlaygroundProps) {
  // Hierarchy state
  const [subjects, setSubjects] = useState<Subject[]>([])
  const [selectedSubjectId, setSelectedSubjectId] = useState<string>('')
  const [units, setUnits] = useState<Unit[]>([])
  const [selectedUnitId, setSelectedUnitId] = useState<string>('')

  // Problems state
  const [problems, setProblems] = useState<Record<string, Problem>>({})
  const [selectedProblemId, setSelectedProblemId] = useState<string>('')
  const [code, setCode] = useState<string>('')

  // Loading states
  const [subjectsLoading, setSubjectsLoading] = useState<boolean>(true)
  const [unitsLoading, setUnitsLoading] = useState<boolean>(false)
  const [problemsLoading, setProblemsLoading] = useState<boolean>(false)
  const [submitting, setSubmitting] = useState<boolean>(false)
  const [polling, setPolling] = useState<boolean>(false)

  // Result state
  const [result, setResult] = useState<SubmissionResult | null>(null)

  // Refs for cleanup
  const pollingControllerRef = useRef<AbortController | null>(null)
  const pollingTimeoutRef = useRef<number | null>(null)

  // Derived state
  const selectedProblem = problems[selectedProblemId]

  // Load subjects on mount
  useEffect(() => {
    setSubjectsLoading(true)
    axios.get<SubjectsResponse>('/api/subjects')
      .then(res => {
        const subjectsList = res.data.subjects || []
        setSubjects(subjectsList)
        if (subjectsList.length > 0) {
          setSelectedSubjectId(subjectsList[0].id)
        }
      })
      .catch((err: AxiosError) => {
        console.error('Error loading subjects:', err)
        setResult({
          status: 'error',
          error_message: 'Error al cargar materias. Por favor, recarga la página.'
        })
      })
      .finally(() => setSubjectsLoading(false))
  }, [])

  // Notify parent when subject changes
  useEffect(() => {
    if (selectedSubjectId && onSubjectChange) {
      onSubjectChange(selectedSubjectId)
    }
  }, [selectedSubjectId, onSubjectChange])

  // Load units when subject changes
  useEffect(() => {
    if (!selectedSubjectId) {
      setUnits([])
      setSelectedUnitId('')
      setProblems({})
      setSelectedProblemId('')
      return
    }

    setUnitsLoading(true)
    axios.get<UnitsResponse>(`/api/subjects/${selectedSubjectId}/units`)
      .then(res => {
        const unitsList = res.data.units || []
        setUnits(unitsList)
        if (unitsList.length > 0) {
          setSelectedUnitId(unitsList[0].id)
        } else {
          setSelectedUnitId('')
        }
      })
      .catch((err: AxiosError) => {
        console.error('Error loading units:', err)
        setUnits([])
        setResult({
          status: 'error',
          error_message: 'Error al cargar unidades temáticas'
        })
      })
      .finally(() => setUnitsLoading(false))
  }, [selectedSubjectId])

  // Load problems when unit changes
  useEffect(() => {
    if (!selectedSubjectId || !selectedUnitId) {
      setProblems({})
      setSelectedProblemId('')
      setCode('')
      return
    }

    setProblemsLoading(true)
    axios.get<ProblemsResponse>(`/api/subjects/${selectedSubjectId}/units/${selectedUnitId}/problems`)
      .then(res => {
        const problemsData = res.data.problems || {}
        setProblems(problemsData)
        const firstProblemId = Object.keys(problemsData)[0]
        if (firstProblemId) {
          setSelectedProblemId(firstProblemId)
        } else {
          setSelectedProblemId('')
          setCode('')
        }
      })
      .catch((err: AxiosError) => {
        console.error('Error loading problems:', err)
        setProblems({})
        setResult({
          status: 'error',
          error_message: 'Error al cargar ejercicios'
        })
      })
      .finally(() => setProblemsLoading(false))
  }, [selectedSubjectId, selectedUnitId])

  // Load starter code when problem changes
  useEffect(() => {
    if (selectedProblem) {
      // Store the server's starter code hash to detect changes
      const starterHash = `starter_${selectedProblemId}`
      const currentStarterHash = selectedProblem.starter ?
        selectedProblem.starter.substring(0, 50) : ''
      const savedStarterHash = localStorage.getItem(starterHash)

      // If starter code changed on server, clear saved code
      if (savedStarterHash && savedStarterHash !== currentStarterHash) {
        localStorage.removeItem(`code_${selectedProblemId}`)
      }

      // Save current starter hash
      localStorage.setItem(starterHash, currentStarterHash)

      // Try to load saved code from localStorage
      const savedCode = localStorage.getItem(`code_${selectedProblemId}`)
      setCode(savedCode || selectedProblem.starter || '')
      setResult(null)
    }
  }, [selectedProblemId, selectedProblem])

  // Save code to localStorage when it changes
  useEffect(() => {
    if (selectedProblemId && code) {
      localStorage.setItem(`code_${selectedProblemId}`, code)
    }
  }, [code, selectedProblemId])

  // Cleanup polling on unmount or when problem changes
  useEffect(() => {
    return () => {
      if (pollingControllerRef.current) {
        pollingControllerRef.current.abort()
      }
      if (pollingTimeoutRef.current) {
        clearTimeout(pollingTimeoutRef.current)
      }
    }
  }, [selectedProblemId])

  const pollResult = useCallback(async (jobId: string) => {
    // Create abort controller for this polling session
    const controller = new AbortController()
    pollingControllerRef.current = controller

    const maxAttempts = 30
    let attempts = 0

    const poll = async (): Promise<void> => {
      try {
        const res = await axios.get<SubmissionResult>(`/api/result/${jobId}`, {
          signal: controller.signal
        })
        const data = res.data

        if (data.status === 'completed' || data.status === 'failed' || data.status === 'timeout') {
          setResult(data)
          setPolling(false)
        } else {
          attempts++
          if (attempts < maxAttempts) {
            pollingTimeoutRef.current = window.setTimeout(poll, 1000)
          } else {
            setResult({
              status: 'error',
              error_message: 'Timeout esperando resultado (30 segundos). El trabajo puede seguir en ejecución.'
            })
            setPolling(false)
          }
        }
      } catch (err) {
        // Don't show error if polling was cancelled (user changed problem or resubmitted)
        if (axios.isCancel(err) || (err as Error).name === 'AbortError') {
          return
        }

        console.error('Error polling:', err)
        setResult({
          status: 'error',
          error_message: 'Error consultando resultado'
        })
        setPolling(false)
      }
    }

    poll()
  }, [])

  const handleSubmit = async () => {
    if (!selectedProblemId || !code.trim()) {
      setResult({
        status: 'error',
        error_message: 'Debes seleccionar un problema y escribir código'
      })
      return
    }

    // Cancel any ongoing polling
    if (pollingControllerRef.current) {
      pollingControllerRef.current.abort()
    }
    if (pollingTimeoutRef.current) {
      clearTimeout(pollingTimeoutRef.current)
    }

    setSubmitting(true)

    try {
      const submitData: SubmitRequest = {
        problem_id: selectedProblemId,
        code: code,
        student_id: 'demo-student'
      }

      const submitRes = await axios.post<SubmitResponse>('/api/submit', submitData)
      const jobId = submitRes.data.job_id

      // Clear previous result and start polling
      setResult(null)
      setSubmitting(false)
      setPolling(true)
      pollResult(jobId)

    } catch (err) {
      console.error('Error submitting:', err)

      let errorMessage = 'Error desconocido al enviar código'

      if (axios.isAxiosError(err)) {
        if (err.response) {
          // Server responded with error status
          errorMessage = err.response.data?.detail || `Error del servidor: ${err.response.status}`
        } else if (err.request) {
          // Request made but no response
          errorMessage = 'Error de conexión. Verifica tu conexión a internet.'
        }
      }

      setResult({
        status: 'error',
        error_message: errorMessage
      })
      setSubmitting(false)
      setPolling(false)
    }
  }

  const handleReset = () => {
    if (selectedProblem) {
      setCode(selectedProblem.starter || '')
      localStorage.removeItem(`code_${selectedProblemId}`)
      setResult(null)
    }
  }

  const loading = submitting || polling

  return (
    <>
      <div className="problem-selector">
        <div className="selector-group">
          <label htmlFor="subject-select">📚 Materia:</label>
          <select
            id="subject-select"
            value={selectedSubjectId}
            onChange={(e) => setSelectedSubjectId(e.target.value)}
            disabled={subjectsLoading}
          >
            {subjectsLoading ? (
              <option value="">Cargando materias...</option>
            ) : (
              <>
                <option value="">Selecciona una materia...</option>
                {subjects.map(subject => (
                  <option key={subject.id} value={subject.id}>
                    {subject.name}
                  </option>
                ))}
              </>
            )}
          </select>
        </div>

        <div className="selector-group">
          <label htmlFor="unit-select">📖 Unidad Temática:</label>
          <select
            id="unit-select"
            value={selectedUnitId}
            onChange={(e) => setSelectedUnitId(e.target.value)}
            disabled={!selectedSubjectId || unitsLoading}
          >
            {unitsLoading ? (
              <option value="">Cargando unidades...</option>
            ) : (
              <>
                <option value="">Selecciona una unidad...</option>
                {units.map(unit => (
                  <option key={unit.id} value={unit.id}>
                    {unit.name}
                  </option>
                ))}
              </>
            )}
          </select>
        </div>

        <div className="selector-group">
          <label htmlFor="problem-select">🎯 Ejercicio:</label>
          <select
            id="problem-select"
            value={selectedProblemId}
            onChange={(e) => setSelectedProblemId(e.target.value)}
            disabled={!selectedUnitId || problemsLoading}
          >
            {problemsLoading ? (
              <option value="">Cargando ejercicios...</option>
            ) : (
              <>
                <option value="">Selecciona un ejercicio...</option>
                {Object.keys(problems).map(key => (
                  <option key={key} value={key}>
                    {problems[key].metadata?.title || key}
                  </option>
                ))}
              </>
            )}
          </select>
        </div>
      </div>

      <div className="editor-container">
        <div className="panel">
          <h2>📝 Enunciado</h2>
          <div className="prompt">
            {selectedProblem?.prompt ? (
              <pre style={{ whiteSpace: 'pre-wrap', fontFamily: 'inherit' }}>
                {selectedProblem.prompt}
              </pre>
            ) : (
              <p>Selecciona un problema para comenzar</p>
            )}
          </div>
        </div>

        <div className="panel">
          <h2>💻 Editor</h2>
          <div className="paste-warning" style={{
            backgroundColor: '#fff3cd',
            color: '#856404',
            padding: '8px 12px',
            borderRadius: '4px',
            marginBottom: '10px',
            fontSize: '13px',
            border: '1px solid #ffeaa7'
          }}>
            ℹ️ <strong>Nota:</strong> Pegar código está deshabilitado para fomentar el aprendizaje. Escribe tu solución.
          </div>
          <div className="editor-wrapper">
            <Editor
              height="400px"
              defaultLanguage="python"
              theme="vs-dark"
              value={code}
              onChange={(value) => setCode(value || '')}
              onMount={(editor, monaco) => {
                // Prevent paste to avoid AI-generated code copying
                editor.onDidPaste((e) => {
                  e.preventDefault?.()
                })

                // Also prevent paste via keyboard shortcuts
                editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.KeyV, () => {
                  // Block paste command
                  alert('⚠️ Pegar código está deshabilitado. Por favor, escribe tu solución.')
                })

                // Prevent paste via context menu
                const domNode = editor.getDomNode()
                if (domNode) {
                  domNode.addEventListener('paste', (e) => {
                    e.preventDefault()
                    alert('⚠️ Pegar código está deshabilitado. Por favor, escribe tu solución.')
                  })
                }
              }}
              options={{
                minimap: { enabled: false },
                fontSize: 14,
                lineNumbers: 'on',
                scrollBeyondLastLine: false
              }}
            />
          </div>
          <div className="button-group">
            <button
              className="submit-btn"
              onClick={handleSubmit}
              disabled={loading || !code.trim()}
            >
              {submitting ? '📤 Enviando...' : polling ? '⏳ Ejecutando tests...' : '▶️ Ejecutar tests'}
            </button>
            <button
              className="reset-btn"
              onClick={handleReset}
              disabled={loading || !selectedProblem}
            >
              🔄 Reiniciar código
            </button>
          </div>
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
                Puntaje: {result.score_total || 0} / {result.score_max || 0}
              </div>

              <div>
                <strong>Tests:</strong> {result.passed || 0} pasados, {result.failed || 0} fallados, {result.errors || 0} errores
              </div>
              <div>
                <strong>Duración:</strong> {result.duration_sec || 0}s
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
