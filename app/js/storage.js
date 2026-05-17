/**
 * SIGC — Módulo de almacenamiento
 * Abstracción sobre localStorage para gestión de datos del sistema
 */

const SIGCStorage = (() => {

  const KEYS = {
    ADMINS:    'sigc_admins',
    MEDICOS:   'sigc_medicos',
    PACIENTES: 'sigc_pacientes',
    SESSION:   'sigc_session',
    FAILS:     'sigc_fails',
    BLOCKED:   'sigc_blocked',
    BLOCK_END: 'sigc_block_end',
  };

  /** Inicializa los datos por defecto si no existen */
  function init() {
    if (!localStorage.getItem(KEYS.ADMINS)) {
      localStorage.setItem(KEYS.ADMINS, JSON.stringify([
        { email: 'admin@medical.com', password: 'Sistemas2026*', name: 'Super Admin' }
      ]));
    }
    if (!localStorage.getItem(KEYS.MEDICOS))   localStorage.setItem(KEYS.MEDICOS, JSON.stringify([]));
    if (!localStorage.getItem(KEYS.PACIENTES))  localStorage.setItem(KEYS.PACIENTES, JSON.stringify([]));
  }

  // ── Admins ──────────────────────────────────────────────────────────────────

  /** @returns {Array} Lista de administradores */
  function getAdmins() {
    return JSON.parse(localStorage.getItem(KEYS.ADMINS) || '[]');
  }

  /**
   * Registra un nuevo administrador
   * @param {Object} admin - {email, password, name}
   * @returns {boolean} true si fue registrado, false si el correo ya existe
   */
  function registerAdmin(admin) {
    const admins = getAdmins();
    if (admins.find(a => a.email === admin.email)) return false;
    admins.push(admin);
    localStorage.setItem(KEYS.ADMINS, JSON.stringify(admins));
    return true;
  }

  /**
   * Autentica un administrador
   * @param {string} email
   * @param {string} password
   * @returns {Object|null} El admin si es válido, null si no
   */
  function authenticateAdmin(email, password) {
    const admins = getAdmins();
    return admins.find(a => a.email === email && a.password === password) || null;
  }

  // ── Médicos ─────────────────────────────────────────────────────────────────

  /** @returns {Array} Lista de médicos */
  function getMedicos() {
    return JSON.parse(localStorage.getItem(KEYS.MEDICOS) || '[]');
  }

  /**
   * Registra un nuevo médico
   * @param {Object} medico
   * @returns {{success: boolean, error: string|null}}
   */
  function registerMedico(medico) {
    const medicos = getMedicos();
    if (medicos.find(m => m.tarjeta.toLowerCase() === medico.tarjeta.toLowerCase())) {
      return { success: false, error: 'tarjeta' };
    }
    if (medicos.find(m => m.correo.toLowerCase() === medico.correo.toLowerCase())) {
      return { success: false, error: 'correo' };
    }
    medicos.push(medico);
    localStorage.setItem(KEYS.MEDICOS, JSON.stringify(medicos));
    return { success: true, error: null };
  }

  // ── Pacientes ───────────────────────────────────────────────────────────────

  /** @returns {Array} Lista de pacientes */
  function getPacientes() {
    return JSON.parse(localStorage.getItem(KEYS.PACIENTES) || '[]');
  }

  /**
   * Registra un nuevo paciente
   * @param {Object} paciente
   * @returns {{success: boolean, error: string|null}}
   */
  function registerPaciente(paciente) {
    const pacientes = getPacientes();
    if (pacientes.find(p => p.id === paciente.id)) {
      return { success: false, error: 'id_duplicado' };
    }
    pacientes.push(paciente);
    localStorage.setItem(KEYS.PACIENTES, JSON.stringify(pacientes));
    return { success: true, error: null };
  }

  // ── Sesión ──────────────────────────────────────────────────────────────────

  /** @returns {Object|null} Usuario de sesión actual */
  function getSession() {
    const s = localStorage.getItem(KEYS.SESSION) || sessionStorage.getItem('sigc_user');
    return s ? JSON.parse(s) : null;
  }

  /** @param {Object} user - Guarda la sesión activa */
  function setSession(user) {
    localStorage.setItem(KEYS.SESSION, JSON.stringify(user));
    sessionStorage.setItem('sigc_user', JSON.stringify(user));
  }

  /** Cierra la sesión activa */
  function clearSession() {
    localStorage.removeItem(KEYS.SESSION);
    sessionStorage.clear();
  }

  // ── Control de intentos fallidos ────────────────────────────────────────────

  /** @returns {number} Número de intentos fallidos actuales */
  function getFailedAttempts() {
    return parseInt(sessionStorage.getItem(KEYS.FAILS) || '0');
  }

  /** @param {number} n - Actualiza el contador de intentos fallidos */
  function setFailedAttempts(n) {
    sessionStorage.setItem(KEYS.FAILS, String(n));
  }

  /** @returns {boolean} Si la cuenta está bloqueada actualmente */
  function isBlocked() {
    const blocked  = sessionStorage.getItem(KEYS.BLOCKED) === 'true';
    const blockEnd = parseInt(sessionStorage.getItem(KEYS.BLOCK_END) || '0');
    return blocked && blockEnd > Date.now();
  }

  /** @returns {number} Timestamp de fin del bloqueo */
  function getBlockEnd() {
    return parseInt(sessionStorage.getItem(KEYS.BLOCK_END) || '0');
  }

  /**
   * Activa el bloqueo de cuenta
   * @param {number} durationMs - Duración del bloqueo en milisegundos
   */
  function setBlock(durationMs) {
    const end = Date.now() + durationMs;
    sessionStorage.setItem(KEYS.BLOCKED, 'true');
    sessionStorage.setItem(KEYS.BLOCK_END, String(end));
  }

  /** Limpia el estado de bloqueo */
  function clearBlock() {
    sessionStorage.removeItem(KEYS.BLOCKED);
    sessionStorage.removeItem(KEYS.BLOCK_END);
    setFailedAttempts(0);
  }

  return {
    init, getAdmins, registerAdmin, authenticateAdmin,
    getMedicos, registerMedico, getPacientes, registerPaciente,
    getSession, setSession, clearSession,
    getFailedAttempts, setFailedAttempts, isBlocked, getBlockEnd, setBlock, clearBlock,
  };
})();

// Exportar para entorno Node.js / Jest
if (typeof module !== 'undefined') module.exports = SIGCStorage;

if (typeof module !== 'undefined') module.exports = SIGCStorage;
