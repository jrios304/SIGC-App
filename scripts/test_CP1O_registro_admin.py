"""
SIGC v2 — Script de Prueba Automatizada
Caso: CP1-O | Módulo: Registro de Administrador
Escenarios: registro válido, contraseña débil, correo duplicado, campos vacíos
Refactorizado: usa utils.py — sin duplicación de configuración de driver
"""

import time
import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from utils import (
    BASE_URL, crear_driver, crear_wait,
    limpiar_storage, inyectar_admins, ADMIN_DEFAULT
)


class CP1O_RegistroAdmin(unittest.TestCase):
    """CP1-O: Registro de Administrador — válido, débil y duplicado."""

    def setUp(self):
        """Inicializa driver y navega al formulario de registro."""
        self.driver = crear_driver()
        self.wait   = crear_wait(self.driver)
        self.driver.get(f"{BASE_URL}/registro-admin.html")
        limpiar_storage(self.driver)
        inyectar_admins(self.driver, [ADMIN_DEFAULT])
        self.driver.refresh()
        self.wait.until(
            EC.presence_of_element_located((By.ID, "form-admin"))
        )

    def tearDown(self):
        """Cierra el navegador después de cada prueba."""
        time.sleep(0.8)
        self.driver.quit()

    def _llenar_y_enviar(self, nombre, email, password, confirm):
        """
        Rellena y envía el formulario de registro de administrador.

        Args:
            nombre (str): Nombre completo del administrador.
            email (str): Correo electrónico.
            password (str): Contraseña.
            confirm (str): Confirmación de contraseña.
        """
        self.driver.find_element(By.ID, "a-name").clear()
        self.driver.find_element(By.ID, "a-email").clear()
        self.driver.find_element(By.ID, "a-pass").clear()
        self.driver.find_element(By.ID, "a-pass2").clear()
        self.driver.find_element(By.ID, "a-name").send_keys(nombre)
        self.driver.find_element(By.ID, "a-email").send_keys(email)
        self.driver.find_element(By.ID, "a-pass").send_keys(password)
        self.driver.find_element(By.ID, "a-pass2").send_keys(confirm)
        self.driver.find_element(By.ID, "btn-reg").click()

    def test_01_registro_exitoso(self):
        """CP1-O.1: Registro con datos válidos muestra alerta de éxito."""
        print("\n[CP1-O.1] Registro exitoso...")
        self._llenar_y_enviar(
            "William Chavez", "william@sigc.com",
            "Admin@2026!", "Admin@2026!"
        )
        alert = self.wait.until(
            EC.visibility_of_element_located((By.ID, "alert-ok"))
        )
        self.assertTrue(alert.is_displayed())
        print("  ✅ PASÓ")

    def test_02_contrasena_debil(self):
        """CP1-O.2: Contraseña sin símbolo ni mayúscula muestra error."""
        print("\n[CP1-O.2] Contraseña débil...")
        self._llenar_y_enviar(
            "Test Admin", "test@sigc.com",
            "clave123", "clave123"
        )
        err = self.driver.find_element(By.ID, "err-pass")
        self.assertIn("show", err.get_attribute("class"))
        print("  ✅ PASÓ")

    def test_03_correo_duplicado(self):
        """CP1-O.3: Correo ya registrado muestra alerta de duplicado."""
        print("\n[CP1-O.3] Correo duplicado...")
        self._llenar_y_enviar(
            "Duplicado", ADMIN_DEFAULT["email"],
            "Admin@2026!", "Admin@2026!"
        )
        alert = self.wait.until(
            EC.visibility_of_element_located((By.ID, "alert-dup"))
        )
        self.assertTrue(alert.is_displayed())
        print("  ✅ PASÓ")

    def test_04_campos_vacios(self):
        """CP1-O.4: Formulario vacío muestra errores en campos requeridos."""
        print("\n[CP1-O.4] Campos vacíos...")
        self.driver.find_element(By.ID, "btn-reg").click()
        err_nombre = self.driver.find_element(By.ID, "err-name")
        err_email  = self.driver.find_element(By.ID, "err-email")
        self.assertIn("show", err_nombre.get_attribute("class"))
        self.assertIn("show", err_email.get_attribute("class"))
        print("  ✅ PASÓ")


if __name__ == "__main__":
    unittest.main(verbosity=2)
