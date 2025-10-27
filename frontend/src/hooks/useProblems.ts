import { useState, useEffect } from 'react'
import axios, { AxiosError } from 'axios'
import { Problem, ProblemsResponse } from '../types/api'

interface UseProblemsReturn {
  problems: Record<string, Problem>
  selectedProblemId: string
  setSelectedProblemId: (id: string) => void
  selectedProblem: Problem | undefined
  loading: boolean
  error: string | null
}

/**
 * Custom hook for managing problems based on subject and unit.
 *
 * Loads problems when subject or unit changes.
 * Auto-selects first problem when list updates.
 *
 * @param subjectId - Selected subject ID
 * @param unitId - Selected unit ID
 * @returns Object with problems, selected problem, and loading/error states
 */
export function useProblems(
  subjectId: string,
  unitId: string
): UseProblemsReturn {
  const [problems, setProblems] = useState<Record<string, Problem>>({})
  const [selectedProblemId, setSelectedProblemId] = useState<string>('')
  const [loading, setLoading] = useState<boolean>(false)
  const [error, setError] = useState<string | null>(null)

  // Load problems when subject/unit changes
  useEffect(() => {
    if (!subjectId || !unitId) {
      setProblems({})
      setSelectedProblemId('')
      return
    }

    setLoading(true)
    setError(null)

    axios.get<ProblemsResponse>(`/api/subjects/${subjectId}/units/${unitId}/problems`)
      .then(res => {
        const problemsData = res.data.problems || {}
        setProblems(problemsData)

        // Auto-select first problem
        const firstProblemId = Object.keys(problemsData)[0]
        if (firstProblemId) {
          setSelectedProblemId(firstProblemId)
        } else {
          setSelectedProblemId('')
        }
      })
      .catch((err: AxiosError) => {
        console.error('Error loading problems:', err)
        setError('Error al cargar ejercicios')
        setProblems({})
      })
      .finally(() => setLoading(false))
  }, [subjectId, unitId])

  const selectedProblem = problems[selectedProblemId]

  return {
    problems,
    selectedProblemId,
    setSelectedProblemId,
    selectedProblem,
    loading,
    error
  }
}
