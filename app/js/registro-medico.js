/**
 * SIGC — Controlador de Registro de Médico
 * Cubre casos de prueba CP3-O y CP4-O
 */

SIGCStorage.init();
const user = SIGCStorage.getSession() || { name: 'Admin' };
SIGCUI.actualizarSidebar(user);
SIGCUI.configurarLogout('btn-logout');

/** Renderiza la lista de médicos registrados */
function renderLista() {
  const medicos = SIGCStorage.getMedicos();
  SIGCUI.renderizarLista(
    'lista-medicos', medicos,
    m => `<div class="list-item">
            <div class="li-name">👨‍⚕️ ${m.nombre} ${m.apellido}</div>
            <div class="li-sub">${m.especialidad} — ${m.tarjeta}</div>
          </div>`,
    'No hay médicos registrados aún.'
  );
}

renderLista();

document.getElementById('form-medico').addEventListener('submit', e => {
  e.preventDefault();
  SIGCUI.ocultarAlertas(['alert-dup-tarjeta', 'alert-dup-correo', 'alert-ok']);
  SIGCUI.limpiarErrores([
    ['med-nombre', 'err-nombre'], ['med-apellido', 'err-apellido'],
    ['med-correo', 'err-correo'], ['med-especialidad', 'err-especialidad'],
    ['med-tarjeta', 'err-tarjeta'],
  ]);

  const datos = {
    nombre:      SIGCUI.getVal('med-nombre'),
    apellido:    SIGCUI.getVal('med-apellido'),
    correo:      SIGCUI.getVal('med-correo'),
    especialidad: SIGCUI.getVal('med-especialidad'),
    tarjeta:     SIGCUI.getVal('med-tarjeta'),
    horario:     SIGCUI.getVal('med-horario'),
  };

  // Validar formulario
  const { valido, errores } = SIGCValidaciones.validarRegistroMedico(datos);
  if (!valido) {
    SIGCUI.aplicarErrores(errores, {
      nombre:      ['med-nombre',      'err-nombre'],
      apellido:    ['med-apellido',    'err-apellido'],
      correo:      ['med-correo',      'err-correo'],
      especialidad: ['med-especialidad', 'err-especialidad'],
      tarjeta:     ['med-tarjeta',     'err-tarjeta'],
    });
    return;
  }

  // CP4-O: Verificar duplicidad en storage
  const resultado = SIGCStorage.registerMedico(datos);

  if (!resultado.success) {
    if (resultado.error === 'tarjeta') {
      SIGCUI.marcarError('med-tarjeta', 'err-tarjeta');
      document.getElementById('msg-dup-tarjeta').textContent =
        `La tarjeta profesional ${datos.tarjeta} ya está registrada.`;
      SIGCUI.mostrarAlerta('alert-dup-tarjeta');
    } else {
      SIGCUI.marcarError('med-correo', 'err-correo');
      SIGCUI.mostrarAlerta('alert-dup-correo');
    }
    return;
  }

  SIGCUI.mostrarAlerta('alert-ok');
  document.getElementById('form-medico').reset();
  renderLista();
  setTimeout(() => SIGCUI.ocultarAlerta('alert-ok'), 3000);
});
