/**
 * SIGC — Controlador del Dashboard
 * Panel principal de administración
 */

SIGCStorage.init();
const user = SIGCStorage.getSession() || { name: 'Admin' };
SIGCUI.actualizarSidebar(user);
SIGCUI.configurarLogout('btn-logout');

document.getElementById('welcome-msg').textContent = `Bienvenido, ${user?.name || 'Administrador'}`;

// Estadísticas
const medicos   = SIGCStorage.getMedicos();
const pacientes = SIGCStorage.getPacientes();
const admins    = SIGCStorage.getAdmins();
document.getElementById('stat-med').textContent = medicos.length;
document.getElementById('stat-pac').textContent = pacientes.length;
document.getElementById('stat-adm').textContent = admins.length;

// Tabla de médicos recientes
if (medicos.length > 0) {
  document.getElementById('tbody-med').innerHTML = medicos.slice(-5).reverse().map(m =>
    `<tr>
      <td>${m.nombre} ${m.apellido}</td>
      <td>${m.especialidad}</td>
      <td>${m.tarjeta}</td>
      <td><span class="badge">Activo</span></td>
    </tr>`
  ).join('');
}
