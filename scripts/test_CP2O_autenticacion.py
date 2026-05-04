"""
=============================================================
SIGC — Script de Prueba Automatizada
Caso: CP2-O | Módulo: Autenticación / Seguridad
Escenario: Credenciales inválidas, bloqueo tras 3 intentos
           y expiración de sesión
=============================================================
"""

import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# ── Configuración ─────────────────────────────────────────
BASE_URL = "http://127.0.0.1:5500/app"
VALID_EMAIL    = "admin@medical.com"
VALID_PASSWORD = "Sistemas2026*"
INVALID_EMAIL  = "admin@mediconnect.com"
INVALID_PASS   = "clave123"


class CP2O_Autenticacion(unittest.TestCase):
    """CP2-O: Autenticación con credenciales inválidas y bloqueo"""

    def setUp(self):
        """Configurar el driver de Chrome antes de cada prueba"""
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        # Limpiar localStorage entre pruebas para evitar bloqueos residuales
        options.add_argument("--incognito")
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        self.wait = WebDriverWait(self.driver, 10)
        self.driver.get(f"{BASE_URL}/index.html")

    def tearDown(self):
        """Cerrar el navegador después de cada prueba"""
        time.sleep(1)
        self.driver.quit()

    # ----------------------------------------------------------
    # PRUEBA 1: Login exitoso con credenciales válidas
    # ----------------------------------------------------------
    def test_01_login_exitoso(self):
        """CP2-O.1 — Login exitoso redirige al Dashboard"""
        print("\n[CP2-O.1] Probando login con credenciales válidas...")

        # Ingresar credenciales válidas
        self.wait.until(EC.presence_of_element_located((By.ID, "login-email")))
        self.driver.find_element(By.ID, "login-email").send_keys(VALID_EMAIL)
        self.driver.find_element(By.ID, "login-pass").send_keys(VALID_PASSWORD)
        self.driver.find_element(By.ID, "btn-login").click()

        # Verificar alerta de éxito
        alert_ok = self.wait.until(
            EC.visibility_of_element_located((By.ID, "alert-ok"))
        )
        self.assertTrue(alert_ok.is_displayed(), "No se mostró alerta de éxito")

        # Esperar redirección al dashboard
        self.wait.until(EC.url_contains("dashboard.html"))
        self.assertIn("dashboard.html", self.driver.current_url,
                      "No redirigió al Dashboard tras login exitoso")

        print("PASÓ: Login exitoso y redirección al Dashboard correcta")

    # ----------------------------------------------------------
    # PRUEBA 2: Credenciales inválidas — mensaje de error
    # ----------------------------------------------------------
    def test_02_credenciales_invalidas(self):
        """CP2-O.2 — Credenciales inválidas muestran mensaje de error"""
        print("\n[CP2-O.2] Probando login con credenciales incorrectas...")

        self.wait.until(EC.presence_of_element_located((By.ID, "login-email")))
        self.driver.find_element(By.ID, "login-email").send_keys(INVALID_EMAIL)
        self.driver.find_element(By.ID, "login-pass").send_keys(INVALID_PASS)
        self.driver.find_element(By.ID, "btn-login").click()

        # Verificar mensaje de error
        alert_cred = self.wait.until(
            EC.visibility_of_element_located((By.ID, "alert-cred"))
        )
        self.assertTrue(alert_cred.is_displayed(),
                        "No se mostró alerta de credenciales inválidas")

        # Verificar que los campos se marcan en rojo
        email_input = self.driver.find_element(By.ID, "login-email")
        self.assertIn("err", email_input.get_attribute("class"),
                      "Campo email no se marcó con clase 'err'")

        # Verificar que NO redirige
        self.assertNotIn("dashboard.html", self.driver.current_url,
                         "Redirigió al Dashboard con credenciales inválidas")

        print("PASÓ: Credenciales inválidas muestran error y no redirigen")

    # ----------------------------------------------------------
    # PRUEBA 3: Bloqueo tras 3 intentos fallidos
    # ----------------------------------------------------------
    def test_03_bloqueo_tras_3_intentos(self):
        """CP2-O.3 — Cuenta bloqueada tras 3 intentos fallidos consecutivos"""
        print("\n[CP2-O.3] Probando bloqueo tras 3 intentos fallidos...")

        self.wait.until(EC.presence_of_element_located((By.ID, "login-email")))

        # Realizar 3 intentos fallidos
        for intento in range(1, 4):
            print(f"  Intento fallido #{intento}...")
            # Limpiar campos antes de cada intento
            email_field = self.driver.find_element(By.ID, "login-email")
            pass_field  = self.driver.find_element(By.ID, "login-pass")
            email_field.clear()
            pass_field.clear()
            email_field.send_keys(INVALID_EMAIL)
            pass_field.send_keys(INVALID_PASS)
            self.driver.find_element(By.ID, "btn-login").click()
            time.sleep(0.5)

        # Verificar alerta de bloqueo visible
        alert_block = self.wait.until(
            EC.visibility_of_element_located((By.ID, "alert-block"))
        )
        self.assertTrue(alert_block.is_displayed(),
                        "No se mostró alerta de bloqueo tras 3 intentos")

        # Verificar botón de login deshabilitado
        btn_login = self.driver.find_element(By.ID, "btn-login")
        self.assertFalse(btn_login.is_enabled(),
                         "Botón de login sigue habilitado tras bloqueo")

        # Verificar que el countdown está visible
        countdown = self.driver.find_element(By.ID, "countdown")
        self.assertTrue(countdown.is_displayed(),
                        "No se muestra el contador de bloqueo")

        print("PASÓ: Cuenta bloqueada tras 3 intentos — botón deshabilitado")

    # ----------------------------------------------------------
    # PRUEBA 4: Intentos fallidos muestran barra de progreso
    # ----------------------------------------------------------
    def test_04_barra_intentos(self):
        """CP2-O.4 — Barra de intentos se actualiza correctamente"""
        print("\n[CP2-O.4] Verificando barra de intentos fallidos...")

        self.wait.until(EC.presence_of_element_located((By.ID, "login-email")))

        # Primer intento fallido
        self.driver.find_element(By.ID, "login-email").send_keys(INVALID_EMAIL)
        self.driver.find_element(By.ID, "login-pass").send_keys(INVALID_PASS)
        self.driver.find_element(By.ID, "btn-login").click()
        time.sleep(0.5)

        # Verificar que la barra de intentos aparece
        attempts_bar = self.driver.find_element(By.ID, "attempts-bar")
        self.assertIn("show", attempts_bar.get_attribute("class"),
                      "Barra de intentos no aparece tras primer fallo")

        # Verificar texto del label
        label = self.driver.find_element(By.ID, "attempts-lbl")
        self.assertIn("1", label.text,
                      "Label de intentos no muestra '1'")

        print("PASÓ: Barra de intentos se muestra y actualiza correctamente")


if __name__ == "__main__":
    print("=" * 60)
    print("  SIGC — CP2-O: Pruebas de Autenticación")
    print("  Asegúrate de que Live Server esté corriendo en :5500")
    print("=" * 60)
    unittest.main(verbosity=2)
