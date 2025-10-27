import { memo } from 'react'
import Editor from '@monaco-editor/react'

interface CodeEditorProps {
  code: string
  onChange: (value: string) => void
}

/**
 * Code Editor Component with Anti-Paste Protection
 *
 * Monaco editor configured for Python with paste blocking
 * to prevent AI-generated code copying.
 *
 * OPTIMIZATION: Memoized to prevent expensive Monaco re-renders.
 * Only re-renders when code prop changes (not on parent re-renders).
 * Monaco is heavy (~2MB), avoiding unnecessary re-renders is critical.
 */
export const CodeEditor = memo(({ code, onChange }: CodeEditorProps) => {
  return (
    <>
      {/* Paste Warning Banner */}
      <div className="paste-warning" style={{
        backgroundColor: '#fff3cd',
        color: '#856404',
        padding: '10px 14px',
        borderRadius: '6px',
        marginBottom: '12px',
        fontSize: '14px',
        border: '1px solid #ffeaa7',
        display: 'flex',
        alignItems: 'center',
        gap: '8px'
      }}>
        <span style={{ fontSize: '18px' }}>ℹ️</span>
        <div>
          <strong>Modo aprendizaje activo:</strong> Pegar código está deshabilitado para fomentar tu desarrollo.
          Si necesitas ayuda, usa el botón "💡 Dame una pista".
        </div>
      </div>

      {/* Monaco Editor */}
      <div className="editor-wrapper">
        <Editor
          height="400px"
          defaultLanguage="python"
          theme="vs-dark"
          value={code}
          onChange={(value) => onChange(value || '')}
          onMount={(editor, monaco) => {
            let pasteAttempts = 0
            const maxAttempts = 3

            // Toast notification for paste blocking
            const showPasteBlockedNotification = () => {
              pasteAttempts++

              const notification = document.createElement('div')
              notification.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 16px 20px;
                border-radius: 8px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                z-index: 10000;
                font-size: 14px;
                font-weight: 500;
                max-width: 320px;
                animation: slideIn 0.3s ease-out;
              `

              if (pasteAttempts >= maxAttempts) {
                notification.innerHTML = `
                  <div style="display: flex; align-items: start; gap: 12px;">
                    <span style="font-size: 24px;">🎯</span>
                    <div>
                      <div style="font-weight: 600; margin-bottom: 4px;">¡Sigue intentando!</div>
                      <div style="opacity: 0.95; font-size: 13px;">
                        Escribir código a mano mejora tu retención y comprensión.
                        Usa el botón "💡 Pista" si necesitas orientación.
                      </div>
                    </div>
                  </div>
                `
              } else {
                notification.innerHTML = `
                  <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="font-size: 20px;">⚠️</span>
                    <div>Pegar código está deshabilitado. Escribe tu solución manualmente.</div>
                  </div>
                `
              }

              document.body.appendChild(notification)

              setTimeout(() => {
                notification.style.animation = 'slideOut 0.3s ease-in'
                setTimeout(() => notification.remove(), 300)
              }, 4000)
            }

            // Prevent paste to avoid AI-generated code copying
            editor.onDidPaste((e) => {
              e.preventDefault?.()
              showPasteBlockedNotification()
            })

            // Block paste via keyboard shortcuts
            editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.KeyV, () => {
              showPasteBlockedNotification()
            })

            // Block paste via context menu
            const domNode = editor.getDomNode()
            if (domNode) {
              domNode.addEventListener('paste', (e) => {
                e.preventDefault()
                showPasteBlockedNotification()
              })
            }
          }}
          options={{
            minimap: { enabled: false },
            fontSize: 14,
            lineNumbers: 'on',
            scrollBeyondLastLine: false
          }}
        />
      </div>
    </>
  )
}, (prevProps, nextProps) => {
  // Custom comparison: only re-render if code or onChange changed
  // This is critical for Monaco Editor performance
  return prevProps.code === nextProps.code && prevProps.onChange === nextProps.onChange
})
