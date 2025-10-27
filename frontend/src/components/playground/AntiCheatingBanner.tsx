/**
 * Anti-Cheating Warning Banner
 *
 * Displays a prominent warning about academic integrity monitoring.
 */
export function AntiCheatingBanner() {
  return (
    <div style={{
      backgroundColor: '#ff4444',
      color: 'white',
      padding: '12px 20px',
      marginBottom: '20px',
      borderRadius: '8px',
      fontSize: '14px',
      fontWeight: 'bold',
      textAlign: 'center',
      border: '2px solid #cc0000',
      boxShadow: '0 2px 8px rgba(255,68,68,0.3)'
    }}>
      🚨 <strong>ADVERTENCIA DE INTEGRIDAD ACADÉMICA</strong> 🚨
      <div style={{ fontSize: '13px', marginTop: '8px', fontWeight: 'normal' }}>
        Esta sesión está siendo monitoreada. Si cambias de pestaña o minimizas la ventana, recibirás advertencias.
        Después de 2 advertencias, la sesión se cerrará automáticamente. ¡No intentes copiar!
      </div>
    </div>
  )
}
