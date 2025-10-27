import { useState, useEffect } from 'react'
import axios, { AxiosError } from 'axios'
import { Subject, Unit, SubjectsResponse, UnitsResponse } from '../types/api'

interface UseHierarchyDataReturn {
  // Subjects
  subjects: Subject[]
  selectedSubjectId: string
  setSelectedSubjectId: (id: string) => void
  subjectsLoading: boolean
  subjectsError: string | null

  // Units
  units: Unit[]
  selectedUnitId: string
  setSelectedUnitId: (id: string) => void
  unitsLoading: boolean
  unitsError: string | null
}

/**
 * Custom hook for managing hierarchical data (subjects and units).
 *
 * Handles loading subjects on mount and units when subject changes.
 * Provides loading and error states for better UX.
 *
 * @returns Object with subjects, units, selected IDs, and loading/error states
 */
export function useHierarchyData(): UseHierarchyDataReturn {
  // Subjects state
  const [subjects, setSubjects] = useState<Subject[]>([])
  const [selectedSubjectId, setSelectedSubjectId] = useState<string>('')
  const [subjectsLoading, setSubjectsLoading] = useState<boolean>(true)
  const [subjectsError, setSubjectsError] = useState<string | null>(null)

  // Units state
  const [units, setUnits] = useState<Unit[]>([])
  const [selectedUnitId, setSelectedUnitId] = useState<string>('')
  const [unitsLoading, setUnitsLoading] = useState<boolean>(false)
  const [unitsError, setUnitsError] = useState<string | null>(null)

  // Load subjects on mount
  useEffect(() => {
    setSubjectsLoading(true)
    setSubjectsError(null)

    axios.get<SubjectsResponse>('/api/subjects')
      .then(res => {
        const subjectsList = res.data.subjects || []
        setSubjects(subjectsList)

        // Auto-select first subject
        if (subjectsList.length > 0) {
          setSelectedSubjectId(subjectsList[0].id)
        }
      })
      .catch((err: AxiosError) => {
        console.error('Error loading subjects:', err)
        setSubjectsError('Error al cargar materias. Por favor, recarga la página.')
      })
      .finally(() => setSubjectsLoading(false))
  }, [])

  // Load units when subject changes
  useEffect(() => {
    if (!selectedSubjectId) {
      setUnits([])
      setSelectedUnitId('')
      return
    }

    setUnitsLoading(true)
    setUnitsError(null)

    axios.get<UnitsResponse>(`/api/subjects/${selectedSubjectId}/units`)
      .then(res => {
        const unitsList = res.data.units || []
        setUnits(unitsList)

        // Auto-select first unit
        if (unitsList.length > 0) {
          setSelectedUnitId(unitsList[0].id)
        } else {
          setSelectedUnitId('')
        }
      })
      .catch((err: AxiosError) => {
        console.error('Error loading units:', err)
        setUnitsError('Error al cargar unidades temáticas')
        setUnits([])
      })
      .finally(() => setUnitsLoading(false))
  }, [selectedSubjectId])

  return {
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
  }
}
