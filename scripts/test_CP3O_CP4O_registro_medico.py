"""
SIGC v2 — Script de Prueba Automatizada
Casos: CP3-O, CP4-O | Módulo: Gestión de Médicos
Escenarios: registro válido, especialidad vacía, tarjeta inválida,
            tarjeta duplicada, correo duplicado
Refactorizado: usa utils.py — CC reducida de 3 a 2
"""

import time
import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from utils import (
    BASE_URL, MEDICO_DEFAULT,
    crear_driver, crear_wait,
    limpiar_storage, inyectar_sesion,
    inyectar_medicos, refrescar_y_esperar
)


class CP3O_CP4O_RegistroMedico(unittest.TestCase):
    """CP3-O y CP4-O: Registro de Médico — validaciones y duplicidad."""

    def setUp(self):
        """Inicializa driver, inyecta sesión y navega al formulario."""
        self.driver = crear_driver()
        self.wait   = crear_wait(self.driver)
        self.driver.get(f"{BASE_URL}/registro-medico.html")
        limpiar_storage(self.driver)
        inyectar_sesion(self.driver)
        inyectar_medicos(self.driver, [])
        refrescar_y_esperar(self.driver, self.wait, "#form-medico")

    def tearDown(self):
        """Cierra el navegador después de cada prueba."""
        time.sleep(0.8)
        self.driver.quit()

    def _llenar_medico(self, nombre, apellido, correo, especialidad, tarjeta):
        """
        Rellena el formulario de registro de médico.

        Args:
            nombre (str): Nombres del médico.
            apellido (str): Apellidos del médico.
            correo (str): Correo electrónico.
            especialidad (str): Especialidad médica.
            tarjeta (str): Número de tarjeta profesional (formato TP-XXXX).
        """
        self.driver.find_element(By.ID, "med-nombre").clear()
        self.driver.find_element(By.ID, "med-apellido").clear()
        self.driver.find_element(By.ID, "med-correo").clear()
        self.driver.find_element(By.ID, "med-tarjeta").clear()
        self.driver.find_element(By.ID, "med-nombre").send_keys(nombre)
        self.driver.find_element(By.ID, "med-apellido").send_keys(apellido)
        self.driver.find_element(By.ID, "med-correo").send_keys(correo)
        if especialidad:
            from selenium.webdriver.support.ui import Select
            Select(self.driver.find_element(By.ID, "med-especialidad")).select_by_visible_text(especialidad)
        self.driver.find_element(By.ID, "med-tarjeta").send_keys(tarjeta)
        self.driver.find_element(By.ID, "btn-registrar-medico").click()

    def test_01_registro_medico_exitoso(self):
        """CP3-O.1: Registro con datos válidos muestra alerta de éxito."""
        print("\n[CP3-O.1] Registro médico exitoso...")
        self._llenar_medico(
            MEDICO_DEFAULT["nombre"], MEDICO_DEFAULT["apellido"],
            MEDICO_DEFAULT["correo"], MEDICO_DEFAULT["especialidad"],
            MEDICO_DEFAULT["tarjeta"]
        )
        alert = self.wait.until(
            EC.visibility_of_element_located((By.ID, "alert-ok"))
        )
        self.assertTrue(alert.is_displayed())
        print("  ✅ PASÓ")

    def test_02_especialidad_vacia(self):
        """CP3-O.2: Especialidad no seleccionada muestra error de campo."""
        print("\n[CP3-O.2] Especialidad vacía...")
        self._llenar_medico(
            MEDICO_DEFAULT["nombre"], MEDICO_DEFAULT["apellido"],
            MEDICO_DEFAULT["correo"], "",
            MEDICO_DEFAULT["tarjeta"]
        )
        err = self.driver.find_element(By.ID, "err-especialidad")
        self.assertIn("show", err.get_attribute("class"))
        print("  ✅ PASÓ")

    def test_03_formato_tarjeta_invalido(self):
        """CP3-O.3: Tarjeta con formato incorrecto muestra error."""
        print("\n[CP3-O.3] Formato de tarjeta inválido...")
        self._llenar_medico(
            MEDICO_DEFAULT["nombre"], MEDICO_DEFAULT["apellido"],
            MEDICO_DEFAULT["correo"], MEDICO_DEFAULT["especialidad"],
            "8877"  # sin prefijo TP-
        )
        err = self.driver.find_element(By.ID, "err-tarjeta")
        self.assertIn("show", err.get_attribute("class"))
        print("  ✅ PASÓ")

    def test_04_tarjeta_duplicada(self):
        """CP4-O.1: Tarjeta ya registrada muestra alerta de duplicado."""
        print("\n[CP4-O.1] Tarjeta duplicada...")
        inyectar_medicos(self.driver, [MEDICO_DEFAULT])
        refrescar_y_esperar(self.driver, self.wait, "#form-medico")
        self._llenar_medico(
            "Otro", "Medico", "otro@sigc.com",
            MEDICO_DEFAULT["especialidad"], MEDICO_DEFAULT["tarjeta"]
        )
        alert = self.wait.until(
            EC.visibility_of_element_located((By.ID, "alert-dup-tarjeta"))
        )
        self.assertTrue(alert.is_displayed())
        print("  ✅ PASÓ")

    def test_05_correo_medico_duplicado(self):
        """CP4-O.2: Correo ya registrado muestra alerta de duplicado."""
        print("\n[CP4-O.2] Correo médico duplicado...")
        inyectar_medicos(self.driver, [MEDICO_DEFAULT])
        refrescar_y_esperar(self.driver, self.wait, "#form-medico")
        self._llenar_medico(
            "Otro", "Medico", MEDICO_DEFAULT["correo"],
            MEDICO_DEFAULT["especialidad"], "TP-9999"
        )
        alert = self.wait.until(
            EC.visibility_of_element_located((By.ID, "alert-dup-correo"))
        )
        self.assertTrue(alert.is_displayed())
        print("  ✅ PASÓ")


if __name__ == "__main__":
    unittest.main(verbosity=2)
