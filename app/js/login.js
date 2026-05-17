/**
 * SIGC — Controlador de Login
 * Lógica de autenticación separada de la vista
 * Cubre caso de prueba CP2-O
 */

// Inicializar storage
SIGCStorage.init();

const BLOCK_DURATION_MS = 15000; // 15s para pruebas (producción: 15 * 60 * 1000)
const MAX_ATTEMPTS      = 3;

let cdInterval = null;

/** Actualiza la barra visual de intentos fallidos */
function actualizarBarraIntentos(fails) {
  for (let i = 1; i <= 3; i++) {
    document.getElementById(`d${i}`).classList.toggle('used', i <= fails);
  }
  document.getElementById('attempts-lbl').textContent = `Intentos fallidos: ${fails} de 3`;
  if (fails > 0) document.getElementById('attempts-bar').classList.add('show');
}

/** Inicia el countdown de desbloqueo */
function iniciarCountdown() {
  clearInterval(cdInterval);
  cdInterval = setInterval(() => {
    const rem = Math.max(0, SIGCStorage.getBlockEnd() - Date.now());
    if (rem <= 0) {
      clearInterval(cdInterval);
      SIGCStorage.clearBlock();
      SIGCUI.ocultarAlertas(['alert-cred', 'alert-block', 'alert-ok']);
      document.getElementById('attempts-bar').classList.remove('show');
      actualizarBarraIntentos(0);
      document.getElementById('btn-login').disabled = false;
      return;
    }
    const m = String(Math.floor(rem / 60000)).padStart(2, '0');
    const s = String(Math.floor((rem % 60000) / 1000)).padStart(2, '0');
    document.getElementById('countdown').textContent = `${m}:${s}`;
  }, 500);
}

/** Inicia el temporizador de sesión activa (30 minutos) */
function iniciarTemporizadorSesion() {
  let secs = 30 * 60;
  const badge   = document.getElementById('session-badge');
  const timerEl = document.getElementById('session-timer');
  badge.classList.add('show');
  const sInterval = setInterval(() => {
    secs--;
    const mm = String(Math.floor(secs / 60)).padStart(2, '0');
    const ss = String(secs % 60).padStart(2, '0');
    timerEl.textContent = `${mm}:${ss}`;
    if (secs <= 0) {
      clearInterval(sInterval);
      SIGCStorage.clearSession();
      location.reload();
    }
  }, 1000);
}

/** Maneja un intento de login fallido */
function manejarFalloLogin() {
  const fails = SIGCStorage.getFailedAttempts() + 1;
  SIGCStorage.setFailedAttempts(fails);
  document.getElementById('login-email').classList.add('err');
  document.getElementById('login-pass').classList.add('err');
  actualizarBarraIntentos(fails);

  if (fails >= MAX_ATTEMPTS) {
    SIGCStorage.setBlock(BLOCK_DURATION_MS);
    SIGCUI.ocultarAlertas(['alert-cred', 'alert-ok']);
    SIGCUI.mostrarAlerta('alert-block');
    document.getElementById('btn-login').disabled = true;
    iniciarCountdown();
  } else {
    const rem = MAX_ATTEMPTS - fails;
    document.getElementById('alert-cred-msg').textContent =
      `Credenciales inválidas. Te quedan ${rem} intento${rem !== 1 ? 's' : ''} antes del bloqueo.`;
    SIGCUI.mostrarAlerta('alert-cred');
  }
}

// ── Inicialización ─────────────────────────────────────────────────────────

// Verificar si hay bloqueo activo al cargar
if (SIGCStorage.isBlocked()) {
  SIGCUI.mostrarAlerta('alert-block');
  document.getElementById('attempts-bar').classList.add('show');
  document.getElementById('btn-login').disabled = true;
  actualizarBarraIntentos(SIGCStorage.getFailedAttempts());
  iniciarCountdown();
}

// ── Evento de submit ───────────────────────────────────────────────────────
document.getElementById('login-form').addEventListener('submit', e => {
  e.preventDefault();
  SIGCUI.ocultarAlertas(['alert-cred', 'alert-block', 'alert-ok']);
  document.getElementById('login-email').classList.remove('err');
  document.getElementById('login-pass').classList.remove('err');
  document.getElementById('err-email').classList.remove('show');
  document.getElementById('err-pass').classList.remove('show');

  if (SIGCStorage.isBlocked()) {
    SIGCUI.mostrarAlerta('alert-block');
    return;
  }

  const email = SIGCUI.getVal('login-email');
  const pass  = document.getElementById('login-pass').value;

  const { valido, errores } = SIGCValidaciones.validarLogin(email, pass);
  if (!valido) {
    SIGCUI.aplicarErrores(errores, {
      email:    ['login-email', 'err-email'],
      password: ['login-pass',  'err-pass'],
    });
    return;
  }

  const user = SIGCStorage.authenticateAdmin(email, pass);
  if (user) {
    SIGCStorage.setFailedAttempts(0);
    SIGCStorage.clearBlock();
    SIGCStorage.setSession(user);
    SIGCUI.mostrarAlerta('alert-ok');
    document.getElementById('btn-login').disabled = true;
    iniciarTemporizadorSesion();
    SIGCUI.redirigirDespues('dashboard.html');
  } else {
    manejarFalloLogin();
  }
});
