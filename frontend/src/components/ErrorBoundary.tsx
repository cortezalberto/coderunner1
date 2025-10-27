import { Component, ReactNode, ErrorInfo } from 'react'

interface Props {
  children: ReactNode
  fallback?: ReactNode
}

interface State {
  hasError: boolean
  error: Error | null
  errorInfo: ErrorInfo | null
}

/**
 * Error Boundary component for catching React errors.
 *
 * Catches errors in child components and displays a fallback UI
 * instead of crashing the entire application.
 *
 * Usage:
 * ```tsx
 * <ErrorBoundary>
 *   <YourComponent />
 * </ErrorBoundary>
 * ```
 */
export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props)
    this.state = {
      hasError: false,
      error: null,
      errorInfo: null
    }
  }

  static getDerivedStateFromError(error: Error): Partial<State> {
    // Update state so the next render will show the fallback UI
    return { hasError: true, error }
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    // Log error to console
    console.error('ErrorBoundary caught error:', error, errorInfo)

    // TODO: Log to monitoring service (e.g., Sentry, LogRocket)
    if (import.meta.env.PROD) {
      // Example: logErrorToService(error, errorInfo)
    }

    this.setState({
      error,
      errorInfo
    })
  }

  render() {
    if (this.state.hasError) {
      // Custom fallback UI if provided
      if (this.props.fallback) {
        return this.props.fallback
      }

      // Default fallback UI
      return (
        <div style={{
          padding: '40px',
          textAlign: 'center',
          backgroundColor: '#fff3cd',
          border: '2px solid #ffc107',
          borderRadius: '8px',
          margin: '20px',
          maxWidth: '800px',
          marginLeft: 'auto',
          marginRight: 'auto'
        }}>
          <h2 style={{ color: '#856404', marginBottom: '16px' }}>
            ⚠️ Algo salió mal
          </h2>
          <p style={{ color: '#856404', marginBottom: '24px' }}>
            Ha ocurrido un error inesperado. Por favor, recarga la página.
          </p>
          <button
            onClick={() => window.location.reload()}
            style={{
              padding: '10px 20px',
              backgroundColor: '#2563eb',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer',
              fontSize: '16px',
              fontWeight: '500'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.backgroundColor = '#1d4ed8'
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.backgroundColor = '#2563eb'
            }}
          >
            🔄 Recargar página
          </button>

          {/* Show error details in development mode */}
          {import.meta.env.DEV && this.state.error && (
            <details style={{ marginTop: '20px', textAlign: 'left' }}>
              <summary style={{
                cursor: 'pointer',
                color: '#dc3545',
                fontWeight: '600',
                marginBottom: '10px'
              }}>
                Ver detalles del error (solo en desarrollo)
              </summary>
              <pre style={{
                padding: '15px',
                backgroundColor: '#f8f9fa',
                borderRadius: '4px',
                overflow: 'auto',
                fontSize: '12px',
                fontFamily: 'monospace',
                color: '#212529',
                border: '1px solid #dee2e6'
              }}>
                <strong>Error:</strong> {this.state.error.toString()}
                {'\n\n'}
                <strong>Component Stack:</strong>
                {this.state.errorInfo?.componentStack}
              </pre>
            </details>
          )}
        </div>
      )
    }

    return this.props.children
  }
}
