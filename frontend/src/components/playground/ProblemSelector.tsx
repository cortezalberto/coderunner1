import { Subject, Unit, Problem } from '../../types/api'

interface ProblemSelectorProps {
  // Subjects
  subjects: Subject[]
  selectedSubjectId: string
  onSubjectChange: (id: string) => void
  subjectsLoading: boolean

  // Units
  units: Unit[]
  selectedUnitId: string
  onUnitChange: (id: string) => void
  unitsLoading: boolean

  // Problems
  problems: Record<string, Problem>
  selectedProblemId: string
  onProblemChange: (id: string) => void
  problemsLoading: boolean
}

/**
 * Problem Selector Component
 *
 * Three-level cascading dropdown for selecting:
 * 1. Subject (Materia)
 * 2. Unit (Unidad Temática)
 * 3. Problem (Ejercicio)
 */
export function ProblemSelector({
  subjects,
  selectedSubjectId,
  onSubjectChange,
  subjectsLoading,
  units,
  selectedUnitId,
  onUnitChange,
  unitsLoading,
  problems,
  selectedProblemId,
  onProblemChange,
  problemsLoading
}: ProblemSelectorProps) {
  return (
    <div className="problem-selector">
      {/* Subject Selector */}
      <div className="selector-group">
        <label htmlFor="subject-select">📚 Materia:</label>
        <select
          id="subject-select"
          value={selectedSubjectId}
          onChange={(e) => onSubjectChange(e.target.value)}
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

      {/* Unit Selector */}
      <div className="selector-group">
        <label htmlFor="unit-select">📖 Unidad Temática:</label>
        <select
          id="unit-select"
          value={selectedUnitId}
          onChange={(e) => onUnitChange(e.target.value)}
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

      {/* Problem Selector */}
      <div className="selector-group">
        <label htmlFor="problem-select">🎯 Ejercicio:</label>
        <select
          id="problem-select"
          value={selectedProblemId}
          onChange={(e) => onProblemChange(e.target.value)}
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
  )
}
