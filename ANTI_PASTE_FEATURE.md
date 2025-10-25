# 🚫 Anti-Paste Feature - Prevención de Copia de Código

## Descripción

Esta funcionalidad previene que los estudiantes peguen código generado por IA o copiado de otras fuentes en el editor Monaco, fomentando el aprendizaje activo y la práctica de escritura de código.

## Implementación

### Frontend (Playground.tsx)

La prevención de paste se implementa en tres niveles:

#### 1. Evento onDidPaste de Monaco
```typescript
editor.onDidPaste((e) => {
  e.preventDefault?.()
})
```
Previene el evento de paste nativo del editor Monaco.

#### 2. Comando de teclado (Ctrl/Cmd + V)
```typescript
editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.KeyV, () => {
  alert('⚠️ Pegar código está deshabilitado. Por favor, escribe tu solución.')
})
```
Bloquea el atajo de teclado más común para pegar.

#### 3. Evento DOM de paste
```typescript
const domNode = editor.getDomNode()
if (domNode) {
  domNode.addEventListener('paste', (e) => {
    e.preventDefault()
    alert('⚠️ Pegar código está deshabilitado. Por favor, escribe tu solución.')
  })
}
```
Previene paste a nivel del DOM, incluyendo click derecho → pegar.

### Advertencia Visual

Se muestra un mensaje informativo arriba del editor:

```
ℹ️ Nota: Pegar código está deshabilitado para fomentar el aprendizaje. Escribe tu solución.
```

Estilo visual:
- Fondo amarillo claro (#fff3cd)
- Texto marrón (#856404)
- Borde amarillo (#ffeaa7)

## Comportamiento

### Bloqueado:
- ✅ Ctrl + V / Cmd + V
- ✅ Click derecho → Pegar
- ✅ Menú Edit → Paste
- ✅ Paste programático

### Permitido:
- ✅ Tipeo manual
- ✅ Autocompletado de Monaco
- ✅ Snippets del editor
- ✅ Copy (copiar código propio)
- ✅ Cut (cortar código propio)

## Experiencia del Usuario

1. **Advertencia proactiva**: El usuario ve el mensaje informativo antes de intentar pegar
2. **Feedback inmediato**: Si intenta pegar, recibe un alert explicativo
3. **Mensaje educativo**: El mensaje enfatiza el propósito pedagógico

## Beneficios Educativos

### Para Estudiantes:
- 📝 Fomenta la escritura activa de código
- 🧠 Mejora la retención del aprendizaje
- 💪 Desarrolla memoria muscular de sintaxis
- 🎯 Reduce dependencia de copiar/pegar

### Para Instructores:
- ✅ Mayor certeza de autenticidad del código
- 📊 Resultados más representativos del conocimiento real
- 🎓 Evaluación más justa entre estudiantes
- 🚫 Reduce uso indebido de IA generativa

## Limitaciones Conocidas

### Tecnológicas:
- **DevTools**: Usuarios avanzados pueden desactivar JavaScript o modificar el DOM
- **Screenshots**: No previene que tomen captura y escriban manualmente
- **Otro editor**: Pueden escribir en otro editor y tipear aquí

### Pedagógicas:
- No impide consultar documentación (que es apropiado)
- No bloquea autocompletado (que ayuda al aprendizaje)
- No previene colaboración entre compañeros

## Consideraciones de Implementación

### No invasivo:
- No afecta otras funcionalidades del editor
- No rompe la experiencia de desarrollo normal
- No requiere cambios en backend

### Compatible:
- Funciona en todos los navegadores modernos
- Compatible con Monaco Editor v1.x
- No interfiere con React hot reload

### Mantenible:
- Código simple y directo
- Sin dependencias adicionales
- Fácil de modificar o remover si es necesario

## Configuración

### Habilitar/Deshabilitar

Para **deshabilitar** temporalmente (ej: para demostración):
```typescript
// Comentar el bloque onMount en Playground.tsx
onMount={(editor, monaco) => {
  // ... código de prevención de paste
}}
```

Para **personalizar el mensaje**:
```typescript
alert('Tu mensaje personalizado aquí')
```

### Mensaje más amigable (alternativa):
```typescript
alert('💡 Tip: Escribir el código tú mismo te ayuda a aprender mejor. ¡Inténtalo!')
```

## Testing

### Pruebas manuales recomendadas:
1. ✅ Intentar Ctrl+V con código copiado
2. ✅ Click derecho → Pegar
3. ✅ Verificar que tipeo manual funciona
4. ✅ Verificar que autocompletado funciona
5. ✅ Verificar que copy/cut funcionan
6. ✅ Verificar mensaje de advertencia visible

## Métricas de Éxito

**Indicadores para medir efectividad**:
- Reducción en código idéntico entre estudiantes
- Aumento en variedad de implementaciones
- Mejor correlación entre práctica y exámenes presenciales
- Feedback de estudiantes sobre aprendizaje

## Alternativas Consideradas

### No implementadas (y por qué):

1. **Bloqueo total de clipboard**: Demasiado invasivo, afecta copy/cut
2. **Watermarking de código**: Complejo, fácil de burlar
3. **Rate limiting de cambios**: Penaliza a escritores rápidos legítimos
4. **Análisis de similitud con IA**: Computacionalmente costoso, falsos positivos

## Mejoras Futuras (Opcional)

- [ ] Contador de intentos de paste para analytics
- [ ] Mensaje educativo rotativo (múltiples tips)
- [ ] Logging de intentos de paste (opcional, con consentimiento)
- [ ] Modo "instructor" para permitir paste temporalmente
- [ ] Integración con sistema de detección de plagio

## Referencias

- Monaco Editor API: https://microsoft.github.io/monaco-editor/api/
- Web Clipboard API: https://developer.mozilla.org/en-US/docs/Web/API/Clipboard_API
- Academic Integrity Best Practices: https://www.academicintegrity.org/

---

**Implementado**: 25 de Octubre, 2025
**Versión**: 1.0
**Mantenedor**: Python Playground Development Team
