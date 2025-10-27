import { useState, useRef, useCallback, useEffect } from 'react'
import axios from 'axios'
import { SubmissionResult, SubmitRequest, SubmitResponse } from '../types/api'

interface UseSubmissionReturn {
  submit: (problemId: string, code: string, studentId?: string) => Promise<void>
  submitting: boolean
  polling: boolean
  result: SubmissionResult | null
  setResult: (result: SubmissionResult | null) => void
  cleanup: () => void
}

/**
 * Custom hook for handling code submissions and result polling.
 *
 * Manages submission lifecycle:
 * 1. Submit code to backend
 * 2. Poll for results with exponential backoff
 * 3. Handle timeouts and errors
 * 4. Cleanup on unmount or problem change
 *
 * @returns Object with submit function, loading states, and result
 */
export function useSubmission(): UseSubmissionReturn {
  const [submitting, setSubmitting] = useState(false)
  const [polling, setPolling] = useState(false)
  const [result, setResult] = useState<SubmissionResult | null>(null)

  const pollingControllerRef = useRef<AbortController | null>(null)
  const pollingTimeoutRef = useRef<number | null>(null)

  /**
   * Poll for submission result with exponential backoff
   */
  const pollResult = useCallback(async (jobId: string) => {
    // Create abort controller for this polling session
    const controller = new AbortController()
    pollingControllerRef.current = controller

    const maxAttempts = 20  // ~40 seconds total
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
            // Exponential backoff: 2s → 4s → 6s → 8s → 10s (max)
            const baseDelay = 2000
            const delay = Math.min(baseDelay * Math.min(attempts, 5), 10000)

            pollingTimeoutRef.current = window.setTimeout(poll, delay)
          } else {
            setResult({
              status: 'error',
              error_message: 'Timeout esperando resultado (40 segundos). El trabajo puede seguir en ejecución.'
            })
            setPolling(false)
          }
        }
      } catch (err) {
        // Don't show error if polling was cancelled
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

  /**
   * Submit code for evaluation
   */
  const submit = useCallback(async (
    problemId: string,
    code: string,
    studentId: string = 'demo-student'
  ) => {
    if (!problemId || !code.trim()) {
      setResult({
        status: 'error',
        error_message: 'Debes seleccionar un problema y escribir código'
      })
      return
    }

    // Cancel any ongoing polling
    cleanup()

    setSubmitting(true)

    try {
      const submitData: SubmitRequest = {
        problem_id: problemId,
        code: code,
        student_id: studentId
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
          errorMessage = err.response.data?.detail || `Error del servidor: ${err.response.status}`
        } else if (err.request) {
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
  }, [pollResult])

  /**
   * Cleanup polling resources
   */
  const cleanup = useCallback(() => {
    if (pollingControllerRef.current) {
      pollingControllerRef.current.abort()
      pollingControllerRef.current = null
    }
    if (pollingTimeoutRef.current) {
      clearTimeout(pollingTimeoutRef.current)
      pollingTimeoutRef.current = null
    }
  }, [])

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      cleanup()
    }
  }, [cleanup])

  return {
    submit,
    submitting,
    polling,
    result,
    setResult,
    cleanup
  }
}
