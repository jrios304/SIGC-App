/**
 * SIGC — Pruebas unitarias: validaciones.js
 * 40 casos de prueba cubriendo todas las funciones del módulo
 */
const SIGCValidaciones = require('../app/js/validaciones');

describe('esEmailValido', () => {
  test('acepta correo con formato estándar', () => {
    expect(SIGCValidaciones.esEmailValido('admin@medical.com')).toBe(true);
  });
  test('acepta correo con subdominio', () => {
    expect(SIGCValidaciones.esEmailValido('user@mail.sigc.co')).toBe(true);
  });
  test('rechaza correo sin @', () => {
    expect(SIGCValidaciones.esEmailValido('adminmedical.com')).toBe(false);
  });
  test('rechaza correo sin dominio', () => {
    expect(SIGCValidaciones.esEmailValido('admin@')).toBe(false);
  });
  test('rechaza correo sin TLD', () => {
    expect(SIGCValidaciones.esEmailValido('admin@medical')).toBe(false);
  });
  test('rechaza string vacío', () => {
    expect(SIGCValidaciones.esEmailValido('')).toBe(false);
  });
});

describe('esPasswordSegura', () => {
  test('acepta contraseña fuerte', () => {
    expect(SIGCValidaciones.esPasswordSegura('Sistemas2026*')).toBe(true);
  });
  test('rechaza contraseña sin mayúscula', () => {
    expect(SIGCValidaciones.esPasswordSegura('sistemas2026*')).toBe(false);
  });
  test('rechaza contraseña sin símbolo', () => {
    expect(SIGCValidaciones.esPasswordSegura('Sistemas2026')).toBe(false);
  });
  test('rechaza contraseña con menos de 8 caracteres', () => {
    expect(SIGCValidaciones.esPasswordSegura('Sys*1')).toBe(false);
  });
  test('rechaza contraseña vacía', () => {
    expect(SIGCValidaciones.esPasswordSegura('')).toBe(false);
  });
  test('acepta contraseña con múltiples símbolos', () => {
    expect(SIGCValidaciones.esPasswordSegura('Admin@#2026!')).toBe(true);
  });
});

describe('evaluarFortaleza', () => {
  test('contraseña solo minúsculas retorna score 1', () => {
    expect(SIGCValidaciones.evaluarFortaleza('abcdefgh').score).toBe(1);
  });
  test('contraseña con mayúscula retorna score 2', () => {
    expect(SIGCValidaciones.evaluarFortaleza('Abcdefgh').score).toBe(2);
  });
  test('contraseña fuerte retorna score 4', () => {
    expect(SIGCValidaciones.evaluarFortaleza('Admin@2026').score).toBe(4);
  });
  test('retorna label y color no vacíos', () => {
    const r = SIGCValidaciones.evaluarFortaleza('Admin@2026');
    expect(r.label).toBeTruthy();
    expect(r.color).toBeTruthy();
  });
  test('contraseña vacía retorna score 0', () => {
    expect(SIGCValidaciones.evaluarFortaleza('').score).toBe(0);
  });
});

describe('esTarjetaProfesionalValida', () => {
  test('acepta formato TP-8877', () => {
    expect(SIGCValidaciones.esTarjetaProfesionalValida('TP-8877')).toBe(true);
  });
  test('acepta formato TP-AB12', () => {
    expect(SIGCValidaciones.esTarjetaProfesionalValida('TP-AB12')).toBe(true);
  });
  test('rechaza sin prefijo TP-', () => {
    expect(SIGCValidaciones.esTarjetaProfesionalValida('8877')).toBe(false);
  });
  test('rechaza prefijo diferente', () => {
    expect(SIGCValidaciones.esTarjetaProfesionalValida('MP-8877')).toBe(false);
  });
  test('rechaza sufijo muy corto', () => {
    expect(SIGCValidaciones.esTarjetaProfesionalValida('TP-1')).toBe(false);
  });
  test('rechaza string vacío', () => {
    expect(SIGCValidaciones.esTarjetaProfesionalValida('')).toBe(false);
  });
});

describe('esTelefonoValido', () => {
  test('acepta 10 dígitos', () => {
    expect(SIGCValidaciones.esTelefonoValido('3001234567')).toBe(true);
  });
  test('acepta 7 dígitos', () => {
    expect(SIGCValidaciones.esTelefonoValido('3001234')).toBe(true);
  });
  test('rechaza con letras', () => {
    expect(SIGCValidaciones.esTelefonoValido('300abc1234')).toBe(false);
  });
  test('rechaza menos de 7 dígitos', () => {
    expect(SIGCValidaciones.esTelefonoValido('300123')).toBe(false);
  });
  test('rechaza vacío', () => {
    expect(SIGCValidaciones.esTelefonoValido('')).toBe(false);
  });
});

describe('estaVacio', () => {
  test('retorna true para string vacío', () => {
    expect(SIGCValidaciones.estaVacio('')).toBe(true);
  });
  test('retorna true para solo espacios', () => {
    expect(SIGCValidaciones.estaVacio('   ')).toBe(true);
  });
  test('retorna false para texto con contenido', () => {
    expect(SIGCValidaciones.estaVacio('hola')).toBe(false);
  });
  test('retorna true para null', () => {
    expect(SIGCValidaciones.estaVacio(null)).toBe(true);
  });
});

describe('validarLogin', () => {
  test('valida correctamente con datos válidos', () => {
    const r = SIGCValidaciones.validarLogin('admin@medical.com', 'pass123');
    expect(r.valido).toBe(true);
  });
  test('retorna error de email con correo inválido', () => {
    const r = SIGCValidaciones.validarLogin('correo-invalido', 'pass123');
    expect(r.valido).toBe(false);
    expect(r.errores.email).toBeDefined();
  });
  test('retorna error de password cuando está vacío', () => {
    const r = SIGCValidaciones.validarLogin('admin@medical.com', '');
    expect(r.valido).toBe(false);
    expect(r.errores.password).toBeDefined();
  });
  test('retorna múltiples errores cuando ambos campos son inválidos', () => {
    const r = SIGCValidaciones.validarLogin('', '');
    expect(Object.keys(r.errores).length).toBeGreaterThanOrEqual(2);
  });
});

describe('validarRegistroAdmin', () => {
  const base = { nombre: 'Jefferson Ríos', email: 'jrios@medical.com', password: 'Admin@2026', confirmPassword: 'Admin@2026' };
  test('valida formulario completo y correcto', () => {
    expect(SIGCValidaciones.validarRegistroAdmin(base).valido).toBe(true);
  });
  test('rechaza nombre vacío', () => {
    const r = SIGCValidaciones.validarRegistroAdmin({ ...base, nombre: '' });
    expect(r.errores.nombre).toBeDefined();
  });
  test('rechaza contraseña débil', () => {
    const r = SIGCValidaciones.validarRegistroAdmin({ ...base, password: '1234', confirmPassword: '1234' });
    expect(r.errores.password).toBeDefined();
  });
  test('rechaza contraseñas que no coinciden', () => {
    const r = SIGCValidaciones.validarRegistroAdmin({ ...base, confirmPassword: 'otra' });
    expect(r.errores.confirmPassword).toBeDefined();
  });
});

describe('validarRegistroMedico', () => {
  const base = { nombre: 'Javier', apellido: 'Sanjuanelo', correo: 'javier@sigc.com', especialidad: 'Urología', tarjeta: 'TP-8877' };
  test('valida médico con datos completos', () => {
    expect(SIGCValidaciones.validarRegistroMedico(base).valido).toBe(true);
  });
  test('rechaza especialidad vacía', () => {
    const r = SIGCValidaciones.validarRegistroMedico({ ...base, especialidad: '' });
    expect(r.errores.especialidad).toBeDefined();
  });
  test('rechaza tarjeta con formato inválido', () => {
    const r = SIGCValidaciones.validarRegistroMedico({ ...base, tarjeta: '8877' });
    expect(r.errores.tarjeta).toBeDefined();
  });
  test('rechaza correo inválido', () => {
    const r = SIGCValidaciones.validarRegistroMedico({ ...base, correo: 'no-valido' });
    expect(r.errores.correo).toBeDefined();
  });
});

describe('validarRegistroPaciente', () => {
  const base = { nombre: 'María', apellido: 'García', tipoId: 'Cédula', id: '123456', fecha: '1990-01-01', telefono: '3001234567', email: '', eps: 'Sanitas', direccion: 'Calle 45' };
  test('valida paciente con datos completos', () => {
    expect(SIGCValidaciones.validarRegistroPaciente(base).valido).toBe(true);
  });
  test('rechaza nombre vacío', () => {
    const r = SIGCValidaciones.validarRegistroPaciente({ ...base, nombre: '' });
    expect(r.errores.nombre).toBeDefined();
  });
  test('rechaza teléfono inválido', () => {
    const r = SIGCValidaciones.validarRegistroPaciente({ ...base, telefono: '123' });
    expect(r.errores.telefono).toBeDefined();
  });
  test('rechaza EPS vacía', () => {
    const r = SIGCValidaciones.validarRegistroPaciente({ ...base, eps: '' });
    expect(r.errores.eps).toBeDefined();
  });
  test('acepta email vacío (campo opcional)', () => {
    expect(SIGCValidaciones.validarRegistroPaciente({ ...base, email: '' }).valido).toBe(true);
  });
  test('rechaza email inválido si no está vacío', () => {
    const r = SIGCValidaciones.validarRegistroPaciente({ ...base, email: 'no-valido' });
    expect(r.errores.email).toBeDefined();
  });
});
