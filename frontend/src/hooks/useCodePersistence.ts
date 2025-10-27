import { useState, useEffect, useCallback } from 'react'

interface UseCodePersistenceReturn {
  code: string
  setCode: (code: string) => void
  resetCode: () => void
}

/**
 * Custom hook for persisting code to localStorage.
 *
 * Automatically saves code changes and restores saved code on mount.
 * Handles starter code hash to detect server-side changes.
 *
 * @param problemId - Current problem ID
 * @param starterCode - Default starter code from server
 * @returns Object with code state and reset function
 */
export function useCodePersistence(
  problemId: string,
  starterCode: string
): UseCodePersistenceReturn {
  const [code, setCode] = useState<string>('')

  // Load code when problem changes
  useEffect(() => {
    if (!problemId) {
      setCode('')
      return
    }

    // Store the server's starter code hash to detect changes
    const starterHash = `starter_${problemId}`
    const currentStarterHash = starterCode ? starterCode.substring(0, 50) : ''
    const savedStarterHash = localStorage.getItem(starterHash)

    // If starter code changed on server, clear saved code
    if (savedStarterHash && savedStarterHash !== currentStarterHash) {
      localStorage.removeItem(`code_${problemId}`)
    }

    // Save current starter hash
    localStorage.setItem(starterHash, currentStarterHash)

    // Try to load saved code from localStorage
    const savedCode = localStorage.getItem(`code_${problemId}`)
    setCode(savedCode || starterCode || '')
  }, [problemId, starterCode])

  // Save code to localStorage when it changes
  useEffect(() => {
    if (problemId && code) {
      localStorage.setItem(`code_${problemId}`, code)
    }
  }, [code, problemId])

  // Reset code to starter and clear localStorage
  const resetCode = useCallback(() => {
    setCode(starterCode || '')
    if (problemId) {
      localStorage.removeItem(`code_${problemId}`)
    }
  }, [problemId, starterCode])

  return {
    code,
    setCode,
    resetCode
  }
}
