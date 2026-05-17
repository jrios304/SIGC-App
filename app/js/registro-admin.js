/**
 * SIGC — Controlador de Registro de Administrador
 * Cubre caso de prueba CP1-O
 */

SIGCStorage.init();

// CP1-O: Evaluación de fortaleza de contraseña en tiempo real
document.getElementById('a-pass').addEventListener('input', function () {
  const val  = this.value;
  const bar  = document.getElementById('pwd-bar');
  const hint = document.getElementById('pwd-hint');

  if (!val.length) {
    bar.style.width = '0';
    hint.textContent = 'La contraseña debe tener mínimo 8 caracteres, una mayúscula y un símbolo.';
    return;
  }

  const { score, label, color } = SIGCValidaciones.evaluarFortaleza(val);
  bar.style.width      = `${score * 25}%`;
  bar.style.background = color;
  hint.textContent     = `Fortaleza: ${label}`;
});

document.getElementById('form-admin').addEventListener('submit', e => {
  e.preventDefault();
  SIGCUI.ocultarAlertas(['alert-dup', 'alert-ok']);
  SIGCUI.limpiarErrores([
    ['a-name',  'err-name'],
    ['a-email', 'err-email'],
    ['a-pass',  'err-pass'],
    ['a-pass2', 'err-pass2'],
  ]);

  const datos = {
    nombre:          SIGCUI.getVal('a-name'),
    email:           SIGCUI.getVal('a-email'),
    password:        document.getElementById('a-pass').value,
    confirmPassword: document.getElementById('a-pass2').value,
  };

  // Validar formulario
  const { valido, errores } = SIGCValidaciones.validarRegistroAdmin(datos);
  if (!valido) {
    SIGCUI.aplicarErrores(errores, {
      nombre:          ['a-name',  'err-name'],
      email:           ['a-email', 'err-email'],
      password:        ['a-pass',  'err-pass'],
      confirmPassword: ['a-pass2', 'err-pass2'],
    });
    return;
  }

  // CP1-O: Verificar correo duplicado
  const registrado = SIGCStorage.registerAdmin({
    email: datos.email, password: datos.password, name: datos.nombre,
  });

  if (!registrado) {
    SIGCUI.marcarError('a-email', 'err-email');
    document.getElementById('msg-dup').textContent =
      `El correo ${datos.email} ya está registrado en el sistema.`;
    SIGCUI.mostrarAlerta('alert-dup');
    return;
  }

  SIGCUI.mostrarAlerta('alert-ok');
  document.getElementById('btn-reg').disabled = true;
  SIGCUI.redirigirDespues('index.html', 2000);
});
