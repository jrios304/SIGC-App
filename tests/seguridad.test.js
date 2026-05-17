/**
 * SIGC — Pruebas unitarias: seguridad.js
 * 28 casos de prueba cubriendo sanitización XSS y detección de amenazas
 */
const SIGCSeguridad = require('../app/js/seguridad');

describe('sanitizar', () => {
  test('escapa carácter <', () => {
    expect(SIGCSeguridad.sanitizar('<script>')).toContain('&lt;');
  });
  test('escapa carácter >', () => {
    expect(SIGCSeguridad.sanitizar('<div>')).toContain('&gt;');
  });
  test('escapa comillas dobles', () => {
    expect(SIGCSeguridad.sanitizar('"value"')).toContain('&quot;');
  });
  test('escapa comillas simples', () => {
    expect(SIGCSeguridad.sanitizar("'value'")).toContain('&#x27;');
  });
  test('escapa backtick', () => {
    expect(SIGCSeguridad.sanitizar('`value`')).toContain('&#x60;');
  });
  test('escapa ampersand', () => {
    expect(SIGCSeguridad.sanitizar('a&b')).toContain('&amp;');
  });
  test('no modifica texto seguro', () => {
    expect(SIGCSeguridad.sanitizar('María García')).toBe('María García');
  });
  test('retorna string vacío para null', () => {
    expect(SIGCSeguridad.sanitizar(null)).toBe('');
  });
  test('retorna string vacío para undefined', () => {
    expect(SIGCSeguridad.sanitizar(undefined)).toBe('');
  });
  test('sanitiza payload XSS completo', () => {
    const input  = '<script>alert("xss")</script>';
    const output = SIGCSeguridad.sanitizar(input);
    expect(output).not.toContain('<script>');
    expect(output).toContain('&lt;script&gt;');
  });
});

describe('contieneXSS', () => {
  test('detecta etiqueta script', () => {
    expect(SIGCSeguridad.contieneXSS('<script>alert(1)</script>')).toBe(true);
  });
  test('detecta javascript:', () => {
    expect(SIGCSeguridad.contieneXSS('javascript:void(0)')).toBe(true);
  });
  test('detecta onerror', () => {
    expect(SIGCSeguridad.contieneXSS('onerror=alert(1)')).toBe(true);
  });
  test('detecta onload', () => {
    expect(SIGCSeguridad.contieneXSS('onload=evil()')).toBe(true);
  });
  test('detecta eval(', () => {
    expect(SIGCSeguridad.contieneXSS('eval(code)')).toBe(true);
  });
  test('detecta carácter <', () => {
    expect(SIGCSeguridad.contieneXSS('<div>')).toBe(true);
  });
  test('no detecta texto limpio', () => {
    expect(SIGCSeguridad.contieneXSS('María García López')).toBe(false);
  });
  test('no detecta número limpio', () => {
    expect(SIGCSeguridad.contieneXSS('3001234567')).toBe(false);
  });
  test('retorna false para null', () => {
    expect(SIGCSeguridad.contieneXSS(null)).toBe(false);
  });
  test('retorna false para string vacío', () => {
    expect(SIGCSeguridad.contieneXSS('')).toBe(false);
  });
});

describe('procesarFormulario', () => {
  test('procesa formulario limpio sin detectar XSS', () => {
    const datos = { nombre: 'María', apellido: 'García', telefono: '3001234567' };
    const r = SIGCSeguridad.procesarFormulario(datos);
    expect(r.xssDetectado).toBe(false);
    expect(r.camposAfectados).toHaveLength(0);
  });
  test('detecta XSS en campo nombre', () => {
    const datos = { nombre: '<script>alert(1)</script>', apellido: 'García' };
    const r = SIGCSeguridad.procesarFormulario(datos);
    expect(r.xssDetectado).toBe(true);
    expect(r.camposAfectados).toContain('nombre');
  });
  test('sanitiza el campo afectado', () => {
    const datos = { nombre: '<script>' };
    const r = SIGCSeguridad.procesarFormulario(datos);
    expect(r.datos.nombre).not.toContain('<script>');
  });
  test('aplica trim a campos limpios', () => {
    const datos = { nombre: '  María  ' };
    const r = SIGCSeguridad.procesarFormulario(datos);
    expect(r.datos.nombre).toBe('María');
  });
  test('preserva campos no-string sin modificarlos', () => {
    const datos = { activo: true, edad: 30 };
    const r = SIGCSeguridad.procesarFormulario(datos);
    expect(r.datos.activo).toBe(true);
    expect(r.datos.edad).toBe(30);
  });
  test('detecta múltiples campos con XSS', () => {
    const datos = { nombre: '<script>', apellido: 'javascript:evil()' };
    const r = SIGCSeguridad.procesarFormulario(datos);
    expect(r.camposAfectados).toHaveLength(2);
  });
  test('retorna estructura completa con datos, xssDetectado y camposAfectados', () => {
    const r = SIGCSeguridad.procesarFormulario({ nombre: 'Test' });
    expect(r).toHaveProperty('datos');
    expect(r).toHaveProperty('xssDetectado');
    expect(r).toHaveProperty('camposAfectados');
  });
  test('procesa formulario vacío sin errores', () => {
    const r = SIGCSeguridad.procesarFormulario({});
    expect(r.xssDetectado).toBe(false);
    expect(r.camposAfectados).toHaveLength(0);
  });
});
