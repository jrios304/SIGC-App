"""
SIGC v2 — Script de Prueba Automatizada
Casos: CP4-O, CP5-O | Módulo: Gestión de Pacientes
Escenarios: registro válido, ID duplicado, campos obligatorios,
            nombre vacío, sanitización XSS
Refactorizado: usa utils.py — CC reducida de 4 a 2 con CAMPO_MAPA
"""

import time
import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoAlertPresentException
from utils import (
    BASE_URL, PACIENTE_DEFAULT,
    crear_driver, crear_wait,
    limpiar_storage, inyectar_sesion,
    inyectar_pacientes, refrescar_y_esperar
)

# Mapa de campos del formulario de paciente: campo → ID del elemento
CAMPO_MAPA = {
    "nombre":    "pac-nombre",
    "apellido":  "pac-apellido",
    "tipoId":    "pac-tipo-id",
    "id":        "pac-id",
    "fecha":     "pac-fecha",
    "telefono":  "pac-telefono",
    "email":     "pac-email",
    "eps":       "pac-eps",
    "direccion": "pac-direccion",
}


class CP4O_CP5O_RegistroPaciente(unittest.TestCase):
    """CP4-O y CP5-O: Registro de Paciente — duplicidad, campos y XSS."""

    def setUp(self):
        """Inicializa driver, inyecta sesión y navega al formulario."""
        self.driver = crear_driver()
        self.wait   = crear_wait(self.driver)
        self.driver.get(f"{BASE_URL}/registro-paciente.html")
        limpiar_storage(self.driver)
        inyectar_sesion(self.driver)
        inyectar_pacientes(self.driver, [])
        refrescar_y_esperar(self.driver, self.wait, "#form-paciente")

    def tearDown(self):
        """Cierra el navegador después de cada prueba."""
        time.sleep(0.8)
        self.driver.quit()

    def _llenar_paciente(self, datos):
        """
        Rellena el formulario de paciente con un diccionario de datos.
        Usa CAMPO_MAPA para reducir CC — reemplaza 9 parámetros individuales.

        Args:
            datos (dict): Diccionario con los valores del formulario.
                          Claves: nombre, apellido, tipoId, id, fecha,
                          telefono, email, eps, direccion.
        """
        selects = {"tipoId", "eps"}
        for campo, elem_id in CAMPO_MAPA.items():
            valor = datos.get(campo, "")
            elemento = self.driver.find_element(By.ID, elem_id)
            if campo in selects:
                if valor:
                    Select(elemento).select_by_visible_text(valor)
            else:
                elemento.clear()
                if valor:
                    elemento.send_keys(valor)
        self.driver.find_element(By.ID, "btn-registrar-paciente").click()

    def test_01_registro_paciente_exitoso(self):
        """CP4-O.1: Registro con datos válidos muestra alerta de éxito."""
        print("\n[CP4-O.1] Registro de paciente exitoso...")
        self._llenar_paciente(PACIENTE_DEFAULT)
        alert = self.wait.until(
            EC.visibility_of_element_located((By.ID, "alert-ok"))
        )
        self.assertTrue(alert.is_displayed())
        print("  ✅ PASÓ")

    def test_02_id_paciente_duplicado(self):
        """CP4-O.2: ID ya registrado muestra alerta de duplicado."""
        print("\n[CP4-O.2] ID de paciente duplicado...")
        inyectar_pacientes(self.driver, [PACIENTE_DEFAULT])
        refrescar_y_esperar(self.driver, self.wait, "#form-paciente")
        datos_dup = {**PACIENTE_DEFAULT, "nombre": "Otro"}
        self._llenar_paciente(datos_dup)
        alert = self.wait.until(
            EC.visibility_of_element_located((By.ID, "alert-dup-id"))
        )
        self.assertTrue(alert.is_displayed())
        print("  ✅ PASÓ")

    def test_03_campos_obligatorios_vacios(self):
        """CP4-O.3: Formulario vacío muestra errores en campos requeridos."""
        print("\n[CP4-O.3] Campos obligatorios vacíos...")
        self.driver.find_element(By.ID, "btn-registrar-paciente").click()
        campos_requeridos = ["err-nombre", "err-id", "err-fecha",
                             "err-telefono", "err-eps", "err-direccion"]
        errores_visibles = sum(
            1 for campo_id in campos_requeridos
            if "show" in self.driver.find_element(
                By.ID, campo_id).get_attribute("class")
        )
        self.assertGreaterEqual(errores_visibles, 4)
        print(f"  ✅ PASÓ — {errores_visibles} errores visibles")

    def test_04_nombre_paciente_vacio(self):
        """CP5-O.1: Nombre vacío con resto de campos válidos muestra error."""
        print("\n[CP4-O.4] Nombre de paciente vacío...")
        datos_sin_nombre = {**PACIENTE_DEFAULT, "nombre": ""}
        self._llenar_paciente(datos_sin_nombre)
        err = self.driver.find_element(By.ID, "err-nombre")
        self.assertIn("show", err.get_attribute("class"))
        print("  ✅ PASÓ")

    def test_05_xss_sanitizacion(self):
        """CP5-O.2: Payload XSS en nombre es sanitizado y notificado."""
        print("\n[CP5-O.2] Sanitización XSS...")
        datos_xss = {
            **PACIENTE_DEFAULT,
            "nombre": "<script>alert('xss')</script>",
            "id": "XSS999"
        }
        self._llenar_paciente(datos_xss)
        try:
            alert_js = self.driver.switch_to.alert
            alert_js.dismiss()
            self.fail("XSS ejecutado — el script no fue sanitizado")
        except NoAlertPresentException:
            pass  # correcto — no hay alerta JavaScript
        alerta_warn = self.wait.until(
            EC.visibility_of_element_located((By.ID, "alert-xss"))
        )
        self.assertTrue(alerta_warn.is_displayed())
        print("  ✅ PASÓ — XSS detectado y sanitizado correctamente")


if __name__ == "__main__":
    unittest.main(verbosity=2)
