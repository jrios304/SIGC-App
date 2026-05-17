/**
 * SIGC — Controlador de Registro de Paciente
 * Cubre casos de prueba CP4-O y CP5-O
 * Refactorizado: CC reducida de 4 a 2 mediante separación de responsabilidades
 */

SIGCStorage.init();
const user = SIGCStorage.getSession() || { name: 'Admin' };
SIGCUI.actualizarSidebar(user);
SIGCUI.configurarLogout('btn-logout');

/** Renderiza la lista de pacientes registrados */
function renderLista() {
  const pacientes = SIGCStorage.getPacientes();
  SIGCUI.renderizarLista(
    'lista-pacientes', pacientes,
    p => `<div class="list-item">
            <div class="li-name">🧑‍🤝‍🧑 ${p.nombre} ${p.apellido}</div>
            <div class="li-sub">ID: ${p.id} — ${p.eps}</div>
          </div>`,
    'No hay pacientes registrados aún.'
  );
}

/**
 * Recolecta los datos del formulario de paciente
 * Separado de la validación para reducir CC
 * @returns {Object} Datos del formulario
 */
function recolectarDatos() {
  return {
    nombre:    SIGCUI.getVal('pac-nombre'),
    apellido:  SIGCUI.getVal('pac-apellido'),
    tipoId:    SIGCUI.getVal('pac-tipo-id'),
    id:        SIGCUI.getVal('pac-id'),
    fecha:     SIGCUI.getVal('pac-fecha'),
    telefono:  SIGCUI.getVal('pac-telefono'),
    email:     SIGCUI.getVal('pac-email'),
    eps:       SIGCUI.getVal('pac-eps'),
    direccion: SIGCUI.getVal('pac-direccion'),
  };
}

/** Mapa de campos a IDs de inputs y errores */
const CAMPO_MAPA = {
  nombre:    ['pac-nombre',    'err-nombre'],
  apellido:  ['pac-apellido', 'err-apellido'],
  tipoId:    ['pac-tipo-id',  'err-tipo-id'],
  id:        ['pac-id',       'err-id'],
  fecha:     ['pac-fecha',    'err-fecha'],
  telefono:  ['pac-telefono', 'err-telefono'],
  email:     ['pac-email',    'err-email'],
  eps:       ['pac-eps',      'err-eps'],
  direccion: ['pac-direccion','err-direccion'],
};

renderLista();

document.getElementById('form-paciente').addEventListener('submit', e => {
  e.preventDefault();
  SIGCUI.ocultarAlertas(['alert-dup-id', 'alert-xss', 'alert-ok']);
  SIGCUI.limpiarErrores(Object.values(CAMPO_MAPA));
  document.getElementById('xss-nombre').classList.remove('show');

  // Recolectar y procesar seguridad (CP5-O: XSS)
  const raw = recolectarDatos();
  const { datos, xssDetectado } = SIGCSeguridad.procesarFormulario(raw);

  if (xssDetectado) {
    document.getElementById('xss-nombre').classList.add('show');
  }

  // Validar formulario
  const { valido, errores } = SIGCValidaciones.validarRegistroPaciente(datos);
  if (!valido) {
    SIGCUI.aplicarErrores(errores, CAMPO_MAPA);
    return;
  }

  if (xssDetectado) {
    SIGCUI.mostrarAlerta('alert-xss');
  }

  // CP4-O: Verificar duplicidad de ID
  const resultado = SIGCStorage.registerPaciente(datos);
  if (!resultado.success) {
    SIGCUI.marcarError('pac-id', 'err-id');
    document.getElementById('msg-dup-id').textContent =
      `El número de identificación ${datos.id} ya se encuentra registrado en el sistema.`;
    SIGCUI.mostrarAlerta('alert-dup-id');
    return;
  }

  SIGCUI.mostrarAlerta('alert-ok');
  document.getElementById('form-paciente').reset();
  renderLista();
  setTimeout(() => SIGCUI.ocultarAlerta('alert-ok'), 3000);
});
