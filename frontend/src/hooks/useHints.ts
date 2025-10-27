import { useState, useEffect } from 'react'

interface UseHintsReturn {
  currentHintLevel: number
  showHint: (hints?: string[]) => void
  resetHints: () => void
}

/**
 * Custom hook for managing progressive hint system.
 *
 * Tracks current hint level and provides function to show next hint.
 * Resets when problem changes.
 *
 * @returns Object with hint level and show/reset functions
 */
export function useHints(): UseHintsReturn {
  const [currentHintLevel, setCurrentHintLevel] = useState<number>(0)

  /**
   * Show next hint or generic message
   */
  const showHint = (hints?: string[]) => {
    if (!hints || hints.length === 0) {
      alert('💡 Pista: Lee cuidadosamente el enunciado del problema. Asegúrate de usar la función main() y leer la entrada con input().')
      return
    }

    const maxLevel = hints.length

    if (currentHintLevel >= maxLevel) {
      alert(`🎓 Ya has visto todas las pistas disponibles (${maxLevel}/${maxLevel}).\n\n¡Intenta resolver el problema con la información que tienes!`)
      return
    }

    const hintMessage = `💡 Pista ${currentHintLevel + 1} de ${maxLevel}:\n\n${hints[currentHintLevel]}`

    if (currentHintLevel === maxLevel - 1) {
      alert(`${hintMessage}\n\n⚠️ Esta es la última pista disponible.`)
    } else {
      alert(hintMessage)
    }

    setCurrentHintLevel(prev => prev + 1)
  }

  /**
   * Reset hint level to 0
   */
  const resetHints = () => {
    setCurrentHintLevel(0)
  }

  return {
    currentHintLevel,
    showHint,
    resetHints
  }
}
