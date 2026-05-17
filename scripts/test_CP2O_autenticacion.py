"""
SIGC v2 — Script de Prueba Automatizada
Caso: CP2-O | Módulo: Autenticación
Escenarios: login exitoso, credenciales inválidas, bloqueo tras 3 intentos, barra de intentos
Refactorizado: usa utils.py — sin duplicación de configuración de driver
"""

import time
import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from utils import (
    BASE_URL, VALID_EMAIL, VALID_PASSWORD,
    INVALID_EMAIL, INVALID_PASSWORD,
    crear_driver, crear_wait,
    limpiar_storage, inyectar_admins, ADMIN_DEFAULT
)


class CP2O_Autenticacion(unittest.TestCase):
    """CP2-O: Autenticación — login, credenciales inválidas y bloqueo."""

    def setUp(self):
        """Inicializa driver y navega al login."""
        self.driver = crear_driver()
        self.wait   = crear_wait(self.driver)
        self.driver.get(f"{BASE_URL}/index.html")
        limpiar_storage(self.driver)
        inyectar_admins(self.driver, [ADMIN_DEFAULT])
        self.driver.refresh()
        self.wait.until(
            EC.presence_of_element_located((By.ID, "login-form"))
        )

    def tearDown(self):
        """Cierra el navegador después de cada prueba."""
        time.sleep(0.8)
        self.driver.quit()

    def _ingresar_credenciales(self, email, password):
        """
        Ingresa credenciales y hace submit del formulario de login.

        Args:
            email (str): Correo electrónico a ingresar.
            password (str): Contraseña a ingresar.
        """
        campo_email = self.driver.find_element(By.ID, "login-email")
        campo_pass  = self.driver.find_element(By.ID, "login-pass")
        campo_email.clear()
        campo_pass.clear()
        campo_email.send_keys(email)
        campo_pass.send_keys(password)
        self.driver.find_element(By.ID, "btn-login").click()

    def test_01_login_exitoso(self):
        """CP2-O.1: Login con credenciales válidas redirige al dashboard."""
        print("\n[CP2-O.1] Login exitoso...")
        self._ingresar_credenciales(VALID_EMAIL, VALID_PASSWORD)
        alert = self.wait.until(
            EC.visibility_of_element_located((By.ID, "alert-ok"))
        )
        self.assertTrue(alert.is_displayed())
        self.wait.until(EC.url_contains("dashboard.html"))
        print("  ✅ PASÓ")

    def test_02_credenciales_invalidas(self):
        """CP2-O.2: Credenciales incorrectas muestran alerta de error."""
        print("\n[CP2-O.2] Credenciales inválidas...")
        self._ingresar_credenciales(INVALID_EMAIL, INVALID_PASSWORD)
        alert = self.wait.until(
            EC.visibility_of_element_located((By.ID, "alert-cred"))
        )
        self.assertTrue(alert.is_displayed())
        campo = self.driver.find_element(By.ID, "login-email")
        self.assertIn("err", campo.get_attribute("class"))
        print("  ✅ PASÓ")

    def test_03_bloqueo_tras_3_intentos(self):
        """CP2-O.3: Tres intentos fallidos activan el bloqueo de cuenta."""
        print("\n[CP2-O.3] Bloqueo tras 3 intentos...")
        for _ in range(3):
            self._ingresar_credenciales(INVALID_EMAIL, INVALID_PASSWORD)
            time.sleep(0.5)
        alert = self.wait.until(
            EC.visibility_of_element_located((By.ID, "alert-block"))
        )
        self.assertTrue(alert.is_displayed())
        btn = self.driver.find_element(By.ID, "btn-login")
        self.assertFalse(btn.is_enabled())
        print("  ✅ PASÓ")

    def test_04_barra_intentos(self):
        """CP2-O.4: Un intento fallido muestra la barra de intentos."""
        print("\n[CP2-O.4] Barra de intentos visible...")
        self._ingresar_credenciales(INVALID_EMAIL, INVALID_PASSWORD)
        time.sleep(0.5)
        barra = self.driver.find_element(By.ID, "attempts-bar")
        self.assertIn("show", barra.get_attribute("class"))
        print("  ✅ PASÓ")


if __name__ == "__main__":
    unittest.main(verbosity=2)
