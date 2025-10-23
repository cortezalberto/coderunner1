import { useState } from 'react'
import Playground from './components/Playground'
import AdminPanel from './components/AdminPanel'

function App() {
  const [activeTab, setActiveTab] = useState('playground')

  return (
    <div className="container">
      <h1>🐍 Python Playground</h1>

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

      {activeTab === 'playground' && <Playground />}
      {activeTab === 'admin' && <AdminPanel />}
    </div>
  )
}

export default App
