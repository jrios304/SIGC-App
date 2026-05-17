/**
 * SIGC — Módulo de seguridad
 * Funciones de sanitización y detección de amenazas
 * Alineado con OWASP A03:2021 — Injection (XSS)
 */

const SIGCSeguridad = (() => {

  /** Mapa de caracteres peligrosos a entidades HTML */
  const CHAR_MAP = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#x27;',
    '`': '&#x60;',
  };

  /** Patrón de detección de payloads XSS comunes */
  const XSS_PATTERN = /[<>"'`]|script|javascript|onerror|onload|onclick|eval\(/i;

  /**
   * Sanitiza un string reemplazando caracteres peligrosos por entidades HTML
   * Previene la ejecución de scripts inyectados en el DOM
   * @param {string} str - Cadena de texto a sanitizar
   * @returns {string} Cadena sanitizada segura para renderizar en HTML
   */
  function sanitizar(str) {
    if (!str) return '';
    return String(str).replace(/[&<>"'`]/g, m => CHAR_MAP[m]);
  }

  /**
   * Detecta si un string contiene patrones de inyección XSS
   * @param {string} str - Cadena de texto a analizar
   * @returns {boolean} true si se detecta un posible payload XSS
   */
  function contieneXSS(str) {
    if (!str) return false;
    return XSS_PATTERN.test(str);
  }

  /**
   * Sanitiza y detecta XSS en un objeto de datos de formulario
   * Itera sobre todos los campos de tipo string y aplica sanitización
   * @param {Object} datos - Objeto con los datos del formulario
   * @returns {{datos: Object, xssDetectado: boolean, camposAfectados: string[]}}
   */
  function procesarFormulario(datos) {
    const resultado = {};
    let xssDetectado = false;
    const camposAfectados = [];

    for (const [key, value] of Object.entries(datos)) {
      if (typeof value === 'string') {
        if (contieneXSS(value)) {
          xssDetectado = true;
          camposAfectados.push(key);
          resultado[key] = sanitizar(value);
        } else {
          resultado[key] = value.trim();
        }
      } else {
        resultado[key] = value;
      }
    }

    return { datos: resultado, xssDetectado, camposAfectados };
  }

  return { sanitizar, contieneXSS, procesarFormulario };
})();

// Exportar para entorno Node.js / Jest
if (typeof module !== 'undefined') module.exports = SIGCSeguridad;

if (typeof module !== 'undefined') module.exports = SIGCSeguridad;
