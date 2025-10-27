import { Problem } from '../../types/api'

interface HintButtonProps {
  problem: Problem | undefined
  currentHintLevel: number
  onShowHint: () => void
}

/**
 * Hint Button Component
 *
 * Progressive hint system button with visual feedback.
 */
export function HintButton({
  problem,
  currentHintLevel,
  onShowHint
}: HintButtonProps) {
  const hints = problem?.metadata.hints || []
  const maxHints = hints.length
  const hintsExhausted = currentHintLevel >= maxHints && maxHints > 0

  return (
    <button
      onClick={onShowHint}
      style={{
        backgroundColor: hintsExhausted ? '#9E9E9E' : '#4CAF50',
        color: 'white',
        border: 'none',
        padding: '8px 16px',
        borderRadius: '4px',
        cursor: !problem ? 'not-allowed' : 'pointer',
        fontSize: '14px',
        fontWeight: '500',
        transition: 'background-color 0.3s',
        opacity: !problem ? 0.6 : 1
      }}
      onMouseEnter={(e) => {
        if (problem && !hintsExhausted) {
          e.currentTarget.style.backgroundColor = '#45a049'
        }
      }}
      onMouseLeave={(e) => {
        if (hintsExhausted) {
          e.currentTarget.style.backgroundColor = '#9E9E9E'
        } else {
          e.currentTarget.style.backgroundColor = '#4CAF50'
        }
      }}
      disabled={!problem}
      title={
        !problem
          ? 'Selecciona un problema primero'
          : hintsExhausted
            ? `Has visto todas las pistas (${currentHintLevel}/${maxHints})`
            : maxHints > 0
              ? `Pista ${currentHintLevel + 1} de ${maxHints}`
              : 'Ver pista'
      }
    >
      💡 Dame una pista {maxHints > 0 && currentHintLevel > 0 && `(${currentHintLevel}/${maxHints})`}
    </button>
  )
}
