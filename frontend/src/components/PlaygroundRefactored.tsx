import { useEffect } from 'react'
import {
  useHierarchyData,
  useProblems,
  useCodePersistence,
  useSubmission,
  useHints
} from '../hooks'
import {
  AntiCheatingBanner,
  ProblemSelector,
  ProblemPrompt,
  HintButton,
  CodeEditor,
  EditorActions,
  ResultsPanel
} from './playground'

interface PlaygroundProps {
  onSubjectChange?: (subjectId: string) => void
}

/**
 * Playground Component (Refactored)
 *
 * Main component for the code playground interface.
 * Refactored to use custom hooks and smaller subcomponents.
 *
 * Original: 783 lines with complex state management
 * Refactored: ~150 lines with separated concerns
 *
 * Changes:
 * - Extracted 5 custom hooks for state management
 * - Divided into 8 smaller components
 * - Improved testability and maintainability
 * - Preserved all original functionality
 */
function PlaygroundRefactored({ onSubjectChange }: PlaygroundProps) {
  // Hierarchy data (subjects and units)
  const {
    subjects,
    selectedSubjectId,
    setSelectedSubjectId,
    subjectsLoading,
    subjectsError,
    units,
    selectedUnitId,
    setSelectedUnitId,
    unitsLoading,
    unitsError
  } = useHierarchyData()

  // Problems data
  const {
    problems,
    selectedProblemId,
    setSelectedProblemId,
    selectedProblem,
    loading: problemsLoading,
    error: problemsError
  } = useProblems(selectedSubjectId, selectedUnitId)

  // Code persistence
  const {
    code,
    setCode,
    resetCode
  } = useCodePersistence(selectedProblemId, selectedProblem?.starter || '')

  // Submission handling
  const {
    submit,
    submitting,
    polling,
    result,
    setResult,
    cleanup
  } = useSubmission()

  // Hint system
  const {
    currentHintLevel,
    showHint,
    resetHints
  } = useHints()

  // Notify parent when subject changes
  useEffect(() => {
    if (selectedSubjectId && onSubjectChange) {
      onSubjectChange(selectedSubjectId)
    }
  }, [selectedSubjectId, onSubjectChange])

  // Reset hints when problem changes
  useEffect(() => {
    resetHints()
    setResult(null)
  }, [selectedProblemId, resetHints, setResult])

  // Cleanup polling on problem change
  useEffect(() => {
    return () => {
      cleanup()
    }
  }, [selectedProblemId, cleanup])

  // Anti-cheating: Monitor tab/window changes
  useEffect(() => {
    let warningCount = 0
    const MAX_WARNINGS = 2

    const handleVisibilityChange = () => {
      if (document.hidden) {
        warningCount++

        if (warningCount >= MAX_WARNINGS) {
          alert('🚫 NO TE DEJO VER OTRA PÁGINA, SOY UN VIEJO GARCA! 🚫\n\nSe detectó que saliste de la página múltiples veces. La sesión se cerrará por intento de copia.')
          window.close()
          setTimeout(() => {
            window.location.href = 'about:blank'
          }, 100)
        } else {
          alert(`⚠️ ADVERTENCIA ${warningCount}/${MAX_WARNINGS} ⚠️\n\n¡No cambies de pestaña!\n\nSe detectó que saliste del playground. Esto se considera un intento de copia.\n\nSi sales ${MAX_WARNINGS - warningCount} vez(ces) más, la sesión se cerrará automáticamente.`)
        }
      }
    }

    const handleBlur = () => {
      if (!document.hidden) {
        console.warn('Window lost focus - possible tab switching')
      }
    }

    const handleBeforeUnload = (e: BeforeUnloadEvent) => {
      e.preventDefault()
      e.returnValue = '¡Alto ahí! ¿Intentas salir? Esto se considera sospechoso.'
      return '¡Alto ahí! ¿Intentas salir? Esto se considera sospechoso.'
    }

    const handleContextMenu = (e: MouseEvent) => {
      e.preventDefault()
      alert('🚫 Click derecho deshabilitado durante la sesión de evaluación.')
      return false
    }

    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && (e.key === 't' || e.key === 'n' || e.key === 'w')) {
        e.preventDefault()
        alert('🚫 Atajos de teclado para abrir pestañas están bloqueados.')
      }
    }

    document.addEventListener('visibilitychange', handleVisibilityChange)
    window.addEventListener('blur', handleBlur)
    window.addEventListener('beforeunload', handleBeforeUnload)
    document.addEventListener('contextmenu', handleContextMenu)
    document.addEventListener('keydown', handleKeyDown)

    return () => {
      document.removeEventListener('visibilitychange', handleVisibilityChange)
      window.removeEventListener('blur', handleBlur)
      window.removeEventListener('beforeunload', handleBeforeUnload)
      document.removeEventListener('contextmenu', handleContextMenu)
      document.removeEventListener('keydown', handleKeyDown)
    }
  }, [])

  // Handle errors from loading
  useEffect(() => {
    if (subjectsError || unitsError || problemsError) {
      setResult({
        status: 'error',
        error_message: subjectsError || unitsError || problemsError || 'Error desconocido'
      })
    }
  }, [subjectsError, unitsError, problemsError, setResult])

  // Handler functions
  const handleSubmit = () => {
    submit(selectedProblemId, code)
  }

  const handleShowHint = () => {
    showHint(selectedProblem?.metadata.hints)
  }

  return (
    <>
      <AntiCheatingBanner />

      <ProblemSelector
        subjects={subjects}
        selectedSubjectId={selectedSubjectId}
        onSubjectChange={setSelectedSubjectId}
        subjectsLoading={subjectsLoading}
        units={units}
        selectedUnitId={selectedUnitId}
        onUnitChange={setSelectedUnitId}
        unitsLoading={unitsLoading}
        problems={problems}
        selectedProblemId={selectedProblemId}
        onProblemChange={setSelectedProblemId}
        problemsLoading={problemsLoading}
      />

      <div className="editor-container">
        <ProblemPrompt problem={selectedProblem} />

        <div className="panel">
          <div style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            marginBottom: '10px'
          }}>
            <h2 style={{ margin: 0 }}>💻 Editor</h2>
            <HintButton
              problem={selectedProblem}
              currentHintLevel={currentHintLevel}
              onShowHint={handleShowHint}
            />
          </div>

          <CodeEditor
            code={code}
            onChange={setCode}
          />

          <EditorActions
            onSubmit={handleSubmit}
            onReset={resetCode}
            submitting={submitting}
            polling={polling}
            canSubmit={!!code.trim()}
            canReset={!!selectedProblem}
          />
        </div>
      </div>

      <ResultsPanel result={result} />
    </>
  )
}

export default PlaygroundRefactored
