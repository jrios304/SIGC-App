/**
 * SIGC — Módulo de validaciones (v2 — refactorizado)
 * Lógica de validación de formularios separada de la vista.
 *
 * Refactorización Act.5:
 * - Reglas extraídas a constantes de módulo (elimina condiciones inline)
 * - Motor aplicarReglas() reemplaza ifs individuales en cada validador
 * - Complexity reducida de 29 → ~12 manteniendo 100% de cobertura Jest
 */

const SIGCValidaciones = (() => {

  // ── Constantes de validación ───────────────────────────────────────────────
  const RE_EMAIL    = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  const RE_PASSWORD = /^(?=.*[A-Z])(?=.*[^A-Za-z0-9]).{8,}$/;
  const RE_TARJETA  = /^TP-[A-Za-z0-9]{2,8}$/;
  const RE_TELEFONO = /^\d{7,10}$/;
  const RE_DIGIT    = /[0-9]/;
  const RE_UPPER    = /[A-Z]/;
  const RE_SYMBOL   = /[^A-Za-z0-9]/;

  const FORTALEZA_LABELS = ['Muy débil', 'Débil', 'Moderada', 'Fuerte'];
  const FORTALEZA_COLORS = ['#e74c3c', '#e67e22', '#f1c40f', '#2ecc71'];

  // ── Validadores básicos ────────────────────────────────────────────────────

  /**
   * Valida formato de correo electrónico.
   * @param {string} email
   * @returns {boolean}
   */
  function esEmailValido(email) {
    return RE_EMAIL.test((email || '').trim());
  }

  /**
   * Valida fortaleza de contraseña.
   * Requiere: mínimo 8 caracteres, una mayúscula y un símbolo.
   * @param {string} password
   * @returns {boolean}
   */
  function esPasswordSegura(password) {
    return RE_PASSWORD.test(password || '');
  }

  /**
   * Evalúa la fortaleza de una contraseña en escala 0-4.
   * Usa tabla de criterios para reducir complejidad ciclomática.
   * @param {string} password
   * @returns {{score: number, label: string, color: string}}
   */
  function evaluarFortaleza(password) {
    const criterios = [
      pwd => pwd.length >= 8,
      pwd => RE_UPPER.test(pwd),
      pwd => RE_DIGIT.test(pwd),
      pwd => RE_SYMBOL.test(pwd),
    ];
    const score = criterios.filter(fn => fn(password || '')).length;
    return {
      score,
      label: FORTALEZA_LABELS[score - 1] || FORTALEZA_LABELS[0],
      color: FORTALEZA_COLORS[score - 1] || FORTALEZA_COLORS[0],
    };
  }

  /**
   * Valida formato de tarjeta profesional médica (TP-XXXX).
   * @param {string} tarjeta
   * @returns {boolean}
   */
  function esTarjetaProfesionalValida(tarjeta) {
    return RE_TARJETA.test(tarjeta || '');
  }

  /**
   * Valida formato de número telefónico (7 a 10 dígitos).
   * @param {string} telefono
   * @returns {boolean}
   */
  function esTelefonoValido(telefono) {
    return RE_TELEFONO.test(telefono || '');
  }

  /**
   * Verifica si un valor está vacío o solo contiene espacios.
   * @param {string} valor
   * @returns {boolean}
   */
  function estaVacio(valor) {
    return !valor || String(valor).trim() === '';
  }

  // ── Motor de validación por tabla de reglas ────────────────────────────────

  /**
   * Aplica una tabla de reglas sobre un objeto de datos.
   * Elimina la necesidad de ifs individuales en cada validador de formulario,
   * reduciendo la complejidad ciclomática de O(n) condiciones a O(1).
   *
   * @param {Object} datos  - Datos del formulario a validar
   * @param {Array}  reglas - Array de [campo, fnError, mensaje]
   * @returns {{valido: boolean, errores: Object}}
   */
  function aplicarReglas(datos, reglas) {
    const errores = {};
    reglas.forEach(([campo, fnError, mensaje]) => {
      if (!errores[campo] && fnError(datos)) {
        errores[campo] = mensaje;
      }
    });
    return { valido: Object.keys(errores).length === 0, errores };
  }

  // ── Tablas de reglas por formulario ───────────────────────────────────────
  const REGLAS_LOGIN = [
    ['email',    d => !esEmailValido(d.email),   'Ingresa un correo electrónico válido.'],
    ['password', d => estaVacio(d.password),      'La contraseña es requerida.'],
  ];

  const REGLAS_ADMIN = [
    ['nombre',          d => estaVacio(d.nombre),              'El nombre es requerido.'],
    ['email',           d => !esEmailValido(d.email),          'Ingresa un correo válido.'],
    ['password',        d => !esPasswordSegura(d.password),    'La contraseña debe tener mínimo 8 caracteres, una mayúscula y un símbolo.'],
    ['confirmPassword', d => d.password !== d.confirmPassword, 'Las contraseñas no coinciden.'],
  ];

  const REGLAS_MEDICO = [
    ['nombre',       d => estaVacio(d.nombre),                     'El nombre es requerido.'],
    ['apellido',     d => estaVacio(d.apellido),                   'El apellido es requerido.'],
    ['correo',       d => !esEmailValido(d.correo),                'Ingresa un correo válido.'],
    ['especialidad', d => estaVacio(d.especialidad),               'La especialidad es requerida.'],
    ['tarjeta',      d => !esTarjetaProfesionalValida(d.tarjeta), 'Formato inválido. Usa el formato TP-XXXX.'],
  ];

  const REGLAS_PACIENTE = [
    ['nombre',    d => estaVacio(d.nombre),              'Este campo es obligatorio.'],
    ['apellido',  d => estaVacio(d.apellido),            'Este campo es obligatorio.'],
    ['tipoId',    d => estaVacio(d.tipoId),              'Selecciona un tipo de ID.'],
    ['id',        d => estaVacio(d.id),                  'El número de identificación es requerido.'],
    ['fecha',     d => estaVacio(d.fecha),               'La fecha de nacimiento es requerida.'],
    ['telefono',  d => !esTelefonoValido(d.telefono),   'Ingresa un número de teléfono válido (10 dígitos).'],
    ['email',     d => d.email && !esEmailValido(d.email), 'Formato de correo inválido.'],
    ['eps',       d => estaVacio(d.eps),                 'Selecciona una EPS.'],
    ['direccion', d => estaVacio(d.direccion),           'La dirección es requerida.'],
  ];

  // ── Validadores de formularios ─────────────────────────────────────────────

  /**
   * Valida el formulario de login.
   * @param {string} email
   * @param {string} password
   * @returns {{valido: boolean, errores: Object}}
   */
  function validarLogin(email, password) {
    return aplicarReglas({ email, password }, REGLAS_LOGIN);
  }

  /**
   * Valida el formulario de registro de administrador.
   * @param {Object} datos - {nombre, email, password, confirmPassword}
   * @returns {{valido: boolean, errores: Object}}
   */
  function validarRegistroAdmin(datos) {
    return aplicarReglas(datos, REGLAS_ADMIN);
  }

  /**
   * Valida el formulario de registro de médico.
   * @param {Object} datos - {nombre, apellido, correo, especialidad, tarjeta}
   * @returns {{valido: boolean, errores: Object}}
   */
  function validarRegistroMedico(datos) {
    return aplicarReglas(datos, REGLAS_MEDICO);
  }

  /**
   * Valida el formulario de registro de paciente.
   * @param {Object} datos
   * @returns {{valido: boolean, errores: Object}}
   */
  function validarRegistroPaciente(datos) {
    return aplicarReglas(datos, REGLAS_PACIENTE);
  }

  return {
    esEmailValido, esPasswordSegura, evaluarFortaleza,
    esTarjetaProfesionalValida, esTelefonoValido, estaVacio,
    validarLogin, validarRegistroAdmin, validarRegistroMedico, validarRegistroPaciente,
  };
})();

if (typeof module !== 'undefined') module.exports = SIGCValidaciones;
