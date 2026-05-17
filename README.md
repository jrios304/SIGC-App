# SIGC — Sistema Integral de Gestión Clínica test pipeline

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
# 1. Descarga y descomprime el archivo SIGC-Actividad3.zip

# 2. Abre la carpeta RAÍZ del proyecto en VS Code
code .

# 3. Click derecho sobre app/index.html → "Open with Live Server"
#    La app corre en: http://127.0.0.1:5500/app/index.html
```

---

## Ejecutar las pruebas automatizadas

### Requisitos previos
- [Python 3.x](https://www.python.org/downloads/) — marcar la opción **"Add Python to PATH"** durante la instalación
- Google Chrome instalado

### Instalación de dependencias

```bash
# Desde la carpeta raíz del proyecto
cd scripts
pip install -r requirements.txt
```

Esto instala:
- `selenium` — framework de automatización de navegador
- `webdriver-manager` — descarga ChromeDriver automáticamente, sin configuración manual

### Ejecutar toda la suite

```bash
# Asegúrate de que Live Server esté corriendo antes de ejecutar
cd scripts
python run_all_tests.py
```

Resultado esperado:
```
Total ejecutados : 18
✅ Exitosos       : 18
❌ Fallidos       : 0
⚠  Con errores   : 0

🎉 TODAS LAS PRUEBAS PASARON EXITOSAMENTE
```

### Ejecutar un caso de prueba específico

```bash
python test_CP2O_autenticacion.py          # Autenticación y bloqueo
python test_CP1O_registro_admin.py         # Registro de administrador
python test_CP3O_CP4O_registro_medico.py   # Registro de médico y duplicidad
python test_CP4O_CP5O_registro_paciente.py # Registro de paciente, campos y XSS
```

### Casos de prueba cubiertos

| Script | Caso | Pruebas |
|---|---|---|
| `test_CP2O_autenticacion.py` | CP2-O | Login exitoso, credenciales inválidas, bloqueo tras 3 intentos, barra de intentos |
| `test_CP1O_registro_admin.py` | CP1-O | Registro válido, contraseña débil, correo duplicado, campos vacíos |
| `test_CP3O_CP4O_registro_medico.py` | CP3-O, CP4-O | Registro válido, especialidad vacía, tarjeta inválida, tarjeta duplicada, correo duplicado |
| `test_CP4O_CP5O_registro_paciente.py` | CP4-O, CP5-O | Registro válido, ID duplicado, campos vacíos múltiples, nombre vacío, XSS sanitizado |

---

## Notas

- Los datos se guardan en `localStorage` del navegador — no hay base de datos real.
- El bloqueo por intentos fallidos dura **15 segundos** en modo de prueba (en producción serían 15 minutos).
- Para resetear todos los datos: abrir la consola del navegador (`F12`) y ejecutar `localStorage.clear()`.
- Los mensajes de error USB o `DEPRECATED_ENDPOINT` en consola al correr los tests son logs internos de Chrome y no afectan los resultados.