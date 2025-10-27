import { useState } from 'react'
import { ErrorBoundary } from './components/ErrorBoundary'
import PlaygroundRefactored from './components/PlaygroundRefactored'
import AdminPanel from './components/AdminPanel'
import LanguageLogo from './components/LanguageLogo'

type TabType = 'playground' | 'admin'

/**
 * App Component (Updated with Error Boundary)
 *
 * Main application component with:
 * - Error boundary for graceful error handling
 * - Tab navigation (Playground / Admin Panel)
 * - Dynamic logo system based on selected subject
 *
 * Updated to use:
 * - PlaygroundRefactored (new version with hooks and components)
 * - ErrorBoundary wrapper for crash prevention
 */
function App() {
  const [activeTab, setActiveTab] = useState<TabType>('playground')
  const [selectedSubjectId, setSelectedSubjectId] = useState<string>('programacion-1')

  return (
    <ErrorBoundary>
      <div className="container">
        <div className="header-with-logo">
          <LanguageLogo subjectId={selectedSubjectId} size={50} />
          <h1 style={{ marginLeft: '15px' }}>Code Playground</h1>
        </div>

        <div className="nav-tabs">
          <button
            className={`nav-tab ${activeTab === 'playground' ? 'active' : ''}`}
            onClick={() => setActiveTab('playground')}
          >
            Ejercicios
          </button>
          <button
            className={`nav-tab ${activeTab === 'admin' ? 'active' : ''}`}
            onClick={() => setActiveTab('admin')}
          >
            Panel Docente
          </button>
        </div>

        {activeTab === 'playground' && (
          <ErrorBoundary>
            <PlaygroundRefactored onSubjectChange={setSelectedSubjectId} />
          </ErrorBoundary>
        )}
        {activeTab === 'admin' && (
          <ErrorBoundary>
            <AdminPanel />
          </ErrorBoundary>
        )}
      </div>
    </ErrorBoundary>
  )
}

export default App
