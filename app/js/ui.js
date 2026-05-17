/**
 * SIGC — Módulo de utilidades de UI
 * Funciones reutilizables para manipulación del DOM
 */

const SIGCUI = (() => {

  /**
   * Muestra un mensaje de alerta en el DOM
   * @param {string} id - ID del elemento de alerta
   */
  function mostrarAlerta(id) {
    const el = document.getElementById(id);
    if (el) el.classList.add('show');
  }

  /**
   * Oculta un mensaje de alerta en el DOM
   * @param {string} id - ID del elemento de alerta
   */
  function ocultarAlerta(id) {
    const el = document.getElementById(id);
    if (el) el.classList.remove('show');
  }

  /**
   * Oculta múltiples alertas
   * @param {string[]} ids - Array de IDs de alertas
   */
  function ocultarAlertas(ids) {
    ids.forEach(ocultarAlerta);
  }

  /**
   * Marca un campo de formulario como inválido
   * @param {string} inputId - ID del input
   * @param {string} errorId - ID del elemento de error
   * @param {string} [mensaje] - Mensaje de error personalizado
   */
  function marcarError(inputId, errorId, mensaje) {
    const input = document.getElementById(inputId);
    const error = document.getElementById(errorId);
    if (input) input.classList.add('err');
    if (error) {
      if (mensaje) error.textContent = mensaje;
      error.classList.add('show');
    }
  }

  /**
   * Limpia el estado de error de un campo de formulario
   * @param {string} inputId - ID del input
   * @param {string} errorId - ID del elemento de error
   */
  function limpiarError(inputId, errorId) {
    const input = document.getElementById(inputId);
    const error = document.getElementById(errorId);
    if (input) input.classList.remove('err');
    if (error) error.classList.remove('show');
  }

  /**
   * Limpia múltiples errores de formulario
   * @param {Array<[string, string]>} pares - Array de [inputId, errorId]
   */
  function limpiarErrores(pares) {
    pares.forEach(([inputId, errorId]) => limpiarError(inputId, errorId));
  }

  /**
   * Aplica errores de validación a múltiples campos
   * @param {Object} errores - {campo: mensaje}
   * @param {Object} mapa - {campo: [inputId, errorId]}
   */
  function aplicarErrores(errores, mapa) {
    for (const [campo, mensaje] of Object.entries(errores)) {
      if (mapa[campo]) {
        const [inputId, errorId] = mapa[campo];
        marcarError(inputId, errorId, mensaje);
      }
    }
  }

  /**
   * Redirige a otra página después de un delay
   * @param {string} url - URL de destino
   * @param {number} [delay=1800] - Delay en milisegundos
   */
  function redirigirDespues(url, delay = 1800) {
    setTimeout(() => { window.location.href = url; }, delay);
  }

  /**
   * Obtiene el valor de un input por ID
   * @param {string} id
   * @returns {string}
   */
  function getVal(id) {
    const el = document.getElementById(id);
    return el ? el.value.trim() : '';
  }

  /**
   * Actualiza el nombre y avatar del usuario en el sidebar
   * @param {Object} user - {name}
   */
  function actualizarSidebar(user) {
    const nameEl   = document.getElementById('user-name');
    const avatarEl = document.getElementById('user-avatar');
    if (nameEl)   nameEl.textContent   = user?.name || 'Admin';
    if (avatarEl) avatarEl.textContent = (user?.name || 'A')[0].toUpperCase();
  }

  /**
   * Configura el botón de logout
   * @param {string} btnId - ID del botón de logout
   */
  function configurarLogout(btnId) {
    const btn = document.getElementById(btnId);
    if (btn) {
      btn.addEventListener('click', () => {
        SIGCStorage.clearSession();
        window.location.href = 'index.html';
      });
    }
  }

  /**
   * Renderiza una lista de items en un contenedor
   * @param {string} containerId - ID del contenedor
   * @param {Array} items - Array de items a renderizar
   * @param {Function} templateFn - Función que genera el HTML de cada item
   * @param {string} emptyMsg - Mensaje cuando no hay items
   */
  function renderizarLista(containerId, items, templateFn, emptyMsg = 'No hay registros aún.') {
    const container = document.getElementById(containerId);
    if (!container) return;
    if (items.length === 0) {
      container.innerHTML = `<div class="empty-list">${emptyMsg}</div>`;
      return;
    }
    container.innerHTML = items.slice().reverse().map(templateFn).join('');
  }

  return {
    mostrarAlerta, ocultarAlerta, ocultarAlertas,
    marcarError, limpiarError, limpiarErrores, aplicarErrores,
    redirigirDespues, getVal, actualizarSidebar,
    configurarLogout, renderizarLista,
  };
})();
