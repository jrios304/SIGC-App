/**
 * SIGC — Módulo de validaciones
 * Lógica de validación de formularios separada de la vista
 */

const SIGCValidaciones = (() => {

  // ── Validadores básicos ────────────────────────────────────────────────────

  /**
   * Valida formato de correo electrónico
   * @param {string} email
   * @returns {boolean}
   */
  function esEmailValido(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.trim());
  }

  /**
   * Valida fortaleza de contraseña
   * Requiere: mínimo 8 caracteres, una mayúscula, un símbolo
   * @param {string} password
   * @returns {boolean}
   */
  function esPasswordSegura(password) {
    return password.length >= 8 &&
           /[A-Z]/.test(password) &&
           /[^A-Za-z0-9]/.test(password);
  }

  /**
   * Evalúa la fortaleza de una contraseña (0-4)
   * @param {string} password
   * @returns {{score: number, label: string, color: string}}
   */
  function evaluarFortaleza(password) {
    let score = 0;
    if (password.length >= 8)        score++;
    if (/[A-Z]/.test(password))      score++;
    if (/[0-9]/.test(password))      score++;
    if (/[^A-Za-z0-9]/.test(password)) score++;
    const labels = ['Muy débil', 'Débil', 'Moderada', 'Fuerte'];
    const colors = ['#e74c3c', '#e67e22', '#f1c40f', '#2ecc71'];
    return {
      score,
      label: labels[score - 1] || labels[0],
      color: colors[score - 1] || colors[0],
    };
  }

  /**
   * Valida formato de tarjeta profesional (TP-XXXX)
   * @param {string} tarjeta
   * @returns {boolean}
   */
  function esTarjetaProfesionalValida(tarjeta) {
    return /^TP-[A-Za-z0-9]{2,8}$/.test(tarjeta);
  }

  /**
   * Valida formato de número telefónico (7-10 dígitos)
   * @param {string} telefono
   * @returns {boolean}
   */
  function esTelefonoValido(telefono) {
    return /^\d{7,10}$/.test(telefono);
  }

  /**
   * Verifica si un string está vacío o solo tiene espacios
   * @param {string} valor
   * @returns {boolean}
   */
  function estaVacio(valor) {
    return !valor || valor.trim() === '';
  }

  // ── Validadores de formularios completos ──────────────────────────────────

  /**
   * Valida el formulario de login
   * @param {string} email
   * @param {string} password
   * @returns {{valido: boolean, errores: Object}}
   */
  function validarLogin(email, password) {
    const errores = {};
    if (!esEmailValido(email)) errores.email = 'Ingresa un correo electrónico válido.';
    if (estaVacio(password))   errores.password = 'La contraseña es requerida.';
    return { valido: Object.keys(errores).length === 0, errores };
  }

  /**
   * Valida el formulario de registro de administrador
   * @param {Object} datos - {nombre, email, password, confirmPassword}
   * @returns {{valido: boolean, errores: Object}}
   */
  function validarRegistroAdmin(datos) {
    const errores = {};
    if (estaVacio(datos.nombre))         errores.nombre = 'El nombre es requerido.';
    if (!esEmailValido(datos.email))     errores.email  = 'Ingresa un correo válido.';
    if (!esPasswordSegura(datos.password))
      errores.password = 'La contraseña debe tener mínimo 8 caracteres, una mayúscula y un símbolo.';
    if (datos.password !== datos.confirmPassword)
      errores.confirmPassword = 'Las contraseñas no coinciden.';
    return { valido: Object.keys(errores).length === 0, errores };
  }

  /**
   * Valida el formulario de registro de médico
   * @param {Object} datos - {nombre, apellido, correo, especialidad, tarjeta}
   * @returns {{valido: boolean, errores: Object}}
   */
  function validarRegistroMedico(datos) {
    const errores = {};
    if (estaVacio(datos.nombre))       errores.nombre      = 'El nombre es requerido.';
    if (estaVacio(datos.apellido))     errores.apellido    = 'El apellido es requerido.';
    if (!esEmailValido(datos.correo))  errores.correo      = 'Ingresa un correo válido.';
    if (estaVacio(datos.especialidad)) errores.especialidad = 'La especialidad es requerida.';
    if (!esTarjetaProfesionalValida(datos.tarjeta))
      errores.tarjeta = 'Formato inválido. Usa el formato TP-XXXX.';
    return { valido: Object.keys(errores).length === 0, errores };
  }

  /**
   * Valida el formulario de registro de paciente
   * @param {Object} datos
   * @returns {{valido: boolean, errores: Object}}
   */
  function validarRegistroPaciente(datos) {
    const errores = {};
    if (estaVacio(datos.nombre))    errores.nombre    = 'Este campo es obligatorio.';
    if (estaVacio(datos.apellido))  errores.apellido  = 'Este campo es obligatorio.';
    if (estaVacio(datos.tipoId))    errores.tipoId    = 'Selecciona un tipo de ID.';
    if (estaVacio(datos.id))        errores.id        = 'El número de identificación es requerido.';
    if (estaVacio(datos.fecha))     errores.fecha     = 'La fecha de nacimiento es requerida.';
    if (!esTelefonoValido(datos.telefono))
      errores.telefono = 'Ingresa un número de teléfono válido (10 dígitos).';
    if (datos.email && !esEmailValido(datos.email))
      errores.email = 'Formato de correo inválido.';
    if (estaVacio(datos.eps))       errores.eps       = 'Selecciona una EPS.';
    if (estaVacio(datos.direccion)) errores.direccion = 'La dirección es requerida.';
    return { valido: Object.keys(errores).length === 0, errores };
  }

  return {
    esEmailValido, esPasswordSegura, evaluarFortaleza,
    esTarjetaProfesionalValida, esTelefonoValido, estaVacio,
    validarLogin, validarRegistroAdmin, validarRegistroMedico, validarRegistroPaciente,
  };
})();

// Exportar para entorno Node.js / Jest
if (typeof module !== 'undefined') module.exports = SIGCValidaciones;

if (typeof module !== 'undefined') module.exports = SIGCValidaciones;
