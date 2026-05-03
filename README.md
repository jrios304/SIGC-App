# SIGC — Sistema Integral de Gestión Clínica

Aplicación web de práctica para pruebas automatizadas con Selenium. Simula los módulos principales de un sistema de gestión clínica.

---

## Páginas disponibles

| Archivo | Descripción | Casos de prueba |
|---|---|---|
| `index.html` | Login del sistema | CP2-O |
| `registro-admin.html` | Registro de administrador | CP1-O |
| `dashboard.html` | Panel principal (requiere login) | — |
| `registro-medico.html` | Registro de médicos | CP3-O, CP4-O |
| `registro-paciente.html` | Registro de pacientes | CP4-O, CP5-O |

## Credenciales de prueba

```
Email:    admin@medical.com
Password: Sistemas2026*
```

---

## Correr en local

### Requisitos
- [VS Code](https://code.visualstudio.com/)
- Extensión **Live Server** (instalar desde el marketplace de VS Code)

### Pasos

```bash
# 1. Clona el repositorio
git clone https://github.com/tu-usuario/sigc-app.git

# 2. Abre la carpeta en VS Code
cd sigc-app
code .

# 3. Click derecho sobre index.html → "Open with Live Server"
#    La app corre en: http://127.0.0.1:5500/index.html
```

---

## Notas

- Los datos se guardan en `localStorage` del navegador — no hay base de datos real.
- El bloqueo por intentos fallidos dura **15 segundos** en modo de prueba (en producción serían 15 minutos).
- Para resetear todos los datos: abrir la consola del navegador (`F12`) y ejecutar `localStorage.clear()`.
