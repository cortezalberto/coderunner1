import { Component, ReactNode } from 'react'

interface ErrorBoundaryProps {
  children: ReactNode
  fallback?: ReactNode
  section?: string
}

interface ErrorBoundaryState {
  hasError: boolean
  error: Error | null
}

/**
 * Section Error Boundary
 *
 * Granular error boundary for specific playground sections.
 * Prevents errors in one section from crashing the entire UI.
 *
 * OPTIMIZATION: Granular error boundaries improve UX.
 * If CodeEditor crashes, other sections remain functional.
 */
class SectionErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props)
    this.state = { hasError: false, error: null }
  }

  static getDerivedStateFromError(error: Error): Partial<ErrorBoundaryState> {
    return { hasError: true, error }
  }

  componentDidCatch(error: Error, errorInfo: any) {
    const section = this.props.section || 'Unknown'
    console.error(`[${section} Error Boundary] Caught error:`, error, errorInfo)

    // TODO: Send to error tracking service (Sentry)
    // Sentry.captureException(error, {
    //   tags: { section: this.props.section },
    //   extra: errorInfo
    // })
  }

  render() {
    if (this.state.hasError) {
      // Use custom fallback if provided
      if (this.props.fallback) {
        return this.props.fallback
      }

      // Default fallback UI
      return (
        <div style={{
          padding: '20px',
          backgroundColor: '#fff3cd',
          border: '1px solid #ffeaa7',
          borderRadius: '8px',
          margin: '10px 0'
        }}>
          <h4 style={{ color: '#856404', margin: '0 0 10px 0' }}>
            ⚠️ Error en {this.props.section || 'esta sección'}
          </h4>
          <p style={{ color: '#856404', fontSize: '14px', margin: '0 0 10px 0' }}>
            Ocurrió un error inesperado. La aplicación sigue funcionando, pero esta sección no se puede mostrar.
          </p>
          <button
            onClick={() => {
              this.setState({ hasError: false, error: null })
              window.location.reload()
            }}
            style={{
              padding: '8px 16px',
              backgroundColor: '#856404',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer',
              fontSize: '14px'
            }}
          >
            Recargar página
          </button>
          {process.env.NODE_ENV === 'development' && this.state.error && (
            <details style={{ marginTop: '15px' }}>
              <summary style={{ cursor: 'pointer', color: '#856404', fontWeight: 'bold' }}>
                Detalles técnicos (desarrollo)
              </summary>
              <pre style={{
                backgroundColor: '#f8f9fa',
                padding: '10px',
                borderRadius: '4px',
                fontSize: '12px',
                overflow: 'auto',
                marginTop: '10px'
              }}>
                {this.state.error.toString()}
                {'\n\n'}
                {this.state.error.stack}
              </pre>
            </details>
          )}
        </div>
      )
    }

    return this.props.children
  }
}

/**
 * Specific fallback components for different sections
 */

export const ProblemSelectorFallback = () => (
  <div className="panel" style={{
    padding: '20px',
    backgroundColor: '#f8d7da',
    border: '1px solid #f5c6cb',
    borderRadius: '8px'
  }}>
    <h3 style={{ color: '#721c24', margin: '0 0 10px 0' }}>
      ⚠️ Error en selector de problemas
    </h3>
    <p style={{ color: '#721c24', fontSize: '14px' }}>
      No se pudo cargar el selector de problemas. Intenta recargar la página.
    </p>
  </div>
)

export const CodeEditorFallback = () => (
  <div className="panel" style={{
    padding: '20px',
    backgroundColor: '#f8d7da',
    border: '1px solid #f5c6cb',
    borderRadius: '8px'
  }}>
    <h3 style={{ color: '#721c24', margin: '0 0 10px 0' }}>
      ⚠️ Error en editor de código
    </h3>
    <p style={{ color: '#721c24', fontSize: '14px' }}>
      El editor de código no se pudo cargar. Intenta recargar la página.
    </p>
    <p style={{ color: '#721c24', fontSize: '12px', marginTop: '10px' }}>
      Si el problema persiste, verifica tu conexión a internet.
    </p>
  </div>
)

export const ResultsPanelFallback = () => (
  <div className="results" style={{
    padding: '20px',
    backgroundColor: '#f8d7da',
    border: '1px solid #f5c6cb',
    borderRadius: '8px'
  }}>
    <h3 style={{ color: '#721c24', margin: '0 0 10px 0' }}>
      ⚠️ Error mostrando resultados
    </h3>
    <p style={{ color: '#721c24', fontSize: '14px' }}>
      No se pudieron mostrar los resultados. Tu código fue ejecutado correctamente, pero hubo un error al mostrar los resultados.
    </p>
  </div>
)

// Named exports for specific sections
export const ProblemSelectorBoundary = ({ children }: { children: ReactNode }) => (
  <SectionErrorBoundary section="Selector de Problemas" fallback={<ProblemSelectorFallback />}>
    {children}
  </SectionErrorBoundary>
)

export const CodeEditorBoundary = ({ children }: { children: ReactNode }) => (
  <SectionErrorBoundary section="Editor de Código" fallback={<CodeEditorFallback />}>
    {children}
  </SectionErrorBoundary>
)

export const ResultsPanelBoundary = ({ children }: { children: ReactNode }) => (
  <SectionErrorBoundary section="Panel de Resultados" fallback={<ResultsPanelFallback />}>
    {children}
  </SectionErrorBoundary>
)

export default SectionErrorBoundary
