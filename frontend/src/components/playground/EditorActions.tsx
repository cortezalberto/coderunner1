interface EditorActionsProps {
  onSubmit: () => void
  onReset: () => void
  submitting: boolean
  polling: boolean
  canSubmit: boolean
  canReset: boolean
}

/**
 * Editor Action Buttons Component
 *
 * Submit and reset buttons with loading states.
 */
export function EditorActions({
  onSubmit,
  onReset,
  submitting,
  polling,
  canSubmit,
  canReset
}: EditorActionsProps) {
  const loading = submitting || polling

  return (
    <div className="button-group">
      <button
        className="submit-btn"
        onClick={onSubmit}
        disabled={loading || !canSubmit}
      >
        {submitting ? '📤 Enviando...' : polling ? '⏳ Ejecutando tests...' : '▶️ Ejecutar tests'}
      </button>
      <button
        className="reset-btn"
        onClick={onReset}
        disabled={loading || !canReset}
      >
        🔄 Reiniciar código
      </button>
    </div>
  )
}
