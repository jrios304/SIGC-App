/**
 * SIGC — Pruebas unitarias: storage.js
 * 43 casos de prueba con mock de localStorage
 */

// Mock de localStorage para entorno Node.js
const localStorageMock = (() => {
  let store = {};
  return {
    getItem:    (k) => store[k] ?? null,
    setItem:    (k, v) => { store[k] = String(v); },
    removeItem: (k) => { delete store[k]; },
    clear:      () => { store = {}; },
  };
})();

const sessionStorageMock = (() => {
  let store = {};
  return {
    getItem:    (k) => store[k] ?? null,
    setItem:    (k, v) => { store[k] = String(v); },
    removeItem: (k) => { delete store[k]; },
    clear:      () => { store = {}; },
  };
})();

global.localStorage   = localStorageMock;
global.sessionStorage = sessionStorageMock;

const SIGCStorage = require('../app/js/storage');

beforeEach(() => {
  localStorage.clear();
  sessionStorage.clear();
  SIGCStorage.init();
});

// ── init ──────────────────────────────────────────────────────────────────
describe('init', () => {
  test('crea admin por defecto', () => {
    const admins = SIGCStorage.getAdmins();
    expect(admins.length).toBeGreaterThanOrEqual(1);
  });
  test('crea lista de médicos vacía', () => {
    expect(SIGCStorage.getMedicos()).toEqual([]);
  });
  test('crea lista de pacientes vacía', () => {
    expect(SIGCStorage.getPacientes()).toEqual([]);
  });
  test('admin por defecto tiene email correcto', () => {
    const admins = SIGCStorage.getAdmins();
    expect(admins[0].email).toBe('admin@medical.com');
  });
});

// ── registerAdmin ─────────────────────────────────────────────────────────
describe('registerAdmin', () => {
  test('registra un nuevo admin correctamente', () => {
    const r = SIGCStorage.registerAdmin({ email: 'nuevo@sigc.com', password: 'Pass@123', name: 'Nuevo' });
    expect(r).toBe(true);
  });
  test('rechaza admin con correo duplicado', () => {
    SIGCStorage.registerAdmin({ email: 'dup@sigc.com', password: 'Pass@123', name: 'Dup' });
    const r = SIGCStorage.registerAdmin({ email: 'dup@sigc.com', password: 'OtraPass', name: 'Dup2' });
    expect(r).toBe(false);
  });
  test('el admin queda almacenado correctamente', () => {
    SIGCStorage.registerAdmin({ email: 'test@sigc.com', password: 'Pass@123', name: 'Test' });
    const admins = SIGCStorage.getAdmins();
    expect(admins.some(a => a.email === 'test@sigc.com')).toBe(true);
  });
  test('rechaza el email del admin por defecto', () => {
    const r = SIGCStorage.registerAdmin({ email: 'admin@medical.com', password: 'Otra', name: 'Dup' });
    expect(r).toBe(false);
  });
});

// ── authenticateAdmin ─────────────────────────────────────────────────────
describe('authenticateAdmin', () => {
  test('autentica con credenciales correctas', () => {
    const r = SIGCStorage.authenticateAdmin('admin@medical.com', 'Sistemas2026*');
    expect(r).not.toBeNull();
  });
  test('rechaza password incorrecto', () => {
    const r = SIGCStorage.authenticateAdmin('admin@medical.com', 'claveIncorrecta');
    expect(r).toBeNull();
  });
  test('rechaza email inexistente', () => {
    const r = SIGCStorage.authenticateAdmin('noexiste@sigc.com', 'Sistemas2026*');
    expect(r).toBeNull();
  });
  test('retorna el objeto admin cuando es válido', () => {
    const r = SIGCStorage.authenticateAdmin('admin@medical.com', 'Sistemas2026*');
    expect(r.email).toBe('admin@medical.com');
  });
});

// ── registerMedico ────────────────────────────────────────────────────────
describe('registerMedico', () => {
  const medico = { nombre: 'Javier', apellido: 'Sanjuanelo', correo: 'javier@sigc.com', especialidad: 'Urología', tarjeta: 'TP-8877' };

  test('registra médico correctamente', () => {
    const r = SIGCStorage.registerMedico(medico);
    expect(r.success).toBe(true);
  });
  test('rechaza tarjeta profesional duplicada', () => {
    SIGCStorage.registerMedico(medico);
    const r = SIGCStorage.registerMedico({ ...medico, correo: 'otro@sigc.com' });
    expect(r.success).toBe(false);
    expect(r.error).toBe('tarjeta');
  });
  test('rechaza correo duplicado', () => {
    SIGCStorage.registerMedico(medico);
    const r = SIGCStorage.registerMedico({ ...medico, tarjeta: 'TP-9999' });
    expect(r.success).toBe(false);
    expect(r.error).toBe('correo');
  });
  test('el médico queda en la lista', () => {
    SIGCStorage.registerMedico(medico);
    expect(SIGCStorage.getMedicos().length).toBe(1);
  });
  test('permite registrar múltiples médicos únicos', () => {
    SIGCStorage.registerMedico(medico);
    SIGCStorage.registerMedico({ ...medico, correo: 'william@sigc.com', tarjeta: 'TP-1234' });
    expect(SIGCStorage.getMedicos().length).toBe(2);
  });
});

// ── registerPaciente ──────────────────────────────────────────────────────
describe('registerPaciente', () => {
  const paciente = { nombre: 'María', apellido: 'García', id: '123456', eps: 'Sanitas' };

  test('registra paciente correctamente', () => {
    const r = SIGCStorage.registerPaciente(paciente);
    expect(r.success).toBe(true);
  });
  test('rechaza ID duplicado', () => {
    SIGCStorage.registerPaciente(paciente);
    const r = SIGCStorage.registerPaciente({ ...paciente, nombre: 'Otro' });
    expect(r.success).toBe(false);
    expect(r.error).toBe('id_duplicado');
  });
  test('el paciente queda en la lista', () => {
    SIGCStorage.registerPaciente(paciente);
    expect(SIGCStorage.getPacientes().length).toBe(1);
  });
  test('permite registrar múltiples pacientes con IDs únicos', () => {
    SIGCStorage.registerPaciente(paciente);
    SIGCStorage.registerPaciente({ ...paciente, id: '654321' });
    expect(SIGCStorage.getPacientes().length).toBe(2);
  });
});

// ── Sesión ────────────────────────────────────────────────────────────────
describe('sesión', () => {
  test('getSession retorna null cuando no hay sesión', () => {
    expect(SIGCStorage.getSession()).toBeNull();
  });
  test('setSession guarda el usuario correctamente', () => {
    SIGCStorage.setSession({ name: 'Admin' });
    expect(SIGCStorage.getSession()).not.toBeNull();
  });
  test('clearSession elimina la sesión', () => {
    SIGCStorage.setSession({ name: 'Admin' });
    SIGCStorage.clearSession();
    expect(SIGCStorage.getSession()).toBeNull();
  });
  test('getSession retorna el usuario guardado', () => {
    SIGCStorage.setSession({ name: 'Jefferson', email: 'j@sigc.com' });
    expect(SIGCStorage.getSession().name).toBe('Jefferson');
  });
});

// ── Control de intentos ───────────────────────────────────────────────────
describe('control de intentos fallidos', () => {
  test('getFailedAttempts retorna 0 inicialmente', () => {
    expect(SIGCStorage.getFailedAttempts()).toBe(0);
  });
  test('setFailedAttempts actualiza el contador', () => {
    SIGCStorage.setFailedAttempts(2);
    expect(SIGCStorage.getFailedAttempts()).toBe(2);
  });
  test('isBlocked retorna false sin bloqueo activo', () => {
    expect(SIGCStorage.isBlocked()).toBe(false);
  });
  test('setBlock activa el bloqueo', () => {
    SIGCStorage.setBlock(60000);
    expect(SIGCStorage.isBlocked()).toBe(true);
  });
  test('clearBlock limpia el bloqueo', () => {
    SIGCStorage.setBlock(60000);
    SIGCStorage.clearBlock();
    expect(SIGCStorage.isBlocked()).toBe(false);
  });
  test('clearBlock resetea el contador de intentos', () => {
    SIGCStorage.setFailedAttempts(3);
    SIGCStorage.clearBlock();
    expect(SIGCStorage.getFailedAttempts()).toBe(0);
  });
  test('getBlockEnd retorna timestamp futuro cuando bloqueado', () => {
    SIGCStorage.setBlock(60000);
    expect(SIGCStorage.getBlockEnd()).toBeGreaterThan(Date.now());
  });
  test('bloqueo expirado retorna isBlocked false', () => {
    SIGCStorage.setBlock(-1000); // ya expiró
    expect(SIGCStorage.isBlocked()).toBe(false);
  });
});
