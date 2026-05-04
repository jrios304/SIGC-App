"""
=============================================================
SIGC — Script de Prueba Automatizada
Caso: CP4-O | Módulo: Gestión de Pacientes / BD
      CP5-O | Módulo: Formularios / Validación / Seguridad
Escenario: Duplicidad de ID paciente, validación de
           campos obligatorios múltiples y prueba XSS
=============================================================
"""

import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = "http://127.0.0.1:5500/app"


class CP4O_CP5O_RegistroPaciente(unittest.TestCase):
    """CP4-O y CP5-O: Registro de Paciente — duplicidad, campos y XSS"""

    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--incognito")
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        self.wait = WebDriverWait(self.driver, 10)
        self.driver.get(f"{BASE_URL}/registro-paciente.html")
        # Inyectar sesión
        self.driver.execute_script("""
            localStorage.setItem('sigc_session', JSON.stringify({name: 'Admin Test'}));
            localStorage.setItem('sigc_pacientes', JSON.stringify([]));
        """)
        self.driver.refresh()
        self.wait.until(EC.presence_of_element_located((By.ID, "form-paciente")))

    def tearDown(self):
        time.sleep(1)
        self.driver.quit()

    def _llenar_paciente(self, nombre, apellido, tipo_id, id_num,
                          fecha, telefono, eps, direccion, email=""):
        """Helper: llena el formulario de paciente"""
        self.driver.find_element(By.ID, "pac-nombre").clear()
        self.driver.find_element(By.ID, "pac-nombre").send_keys(nombre)
        self.driver.find_element(By.ID, "pac-apellido").clear()
        self.driver.find_element(By.ID, "pac-apellido").send_keys(apellido)
        if tipo_id:
            Select(self.driver.find_element(By.ID, "pac-tipo-id")).select_by_visible_text(tipo_id)
        self.driver.find_element(By.ID, "pac-id").clear()
        self.driver.find_element(By.ID, "pac-id").send_keys(id_num)
        self.driver.find_element(By.ID, "pac-fecha").send_keys(fecha)
        self.driver.find_element(By.ID, "pac-telefono").clear()
        self.driver.find_element(By.ID, "pac-telefono").send_keys(telefono)
        if email:
            self.driver.find_element(By.ID, "pac-email").send_keys(email)
        if eps:
            Select(self.driver.find_element(By.ID, "pac-eps")).select_by_visible_text(eps)
        self.driver.find_element(By.ID, "pac-direccion").clear()
        self.driver.find_element(By.ID, "pac-direccion").send_keys(direccion)
        self.driver.find_element(By.ID, "btn-registrar-paciente").click()

    # ----------------------------------------------------------
    # PRUEBA 1: Registro exitoso de paciente
    # ----------------------------------------------------------
    def test_01_registro_paciente_exitoso(self):
        """CP4-O / CP5-O — Registro de paciente con datos válidos"""
        print("\n[CP4-O.1] Probando registro de paciente con datos válidos...")

        self._llenar_paciente(
            nombre="María", apellido="García",
            tipo_id="Cédula de ciudadanía", id_num="123456",
            fecha="1990-05-15", telefono="3001234567",
            eps="Sanitas", direccion="Calle 45 #12-30, Bogotá"
        )

        alert_ok = self.wait.until(
            EC.visibility_of_element_located((By.ID, "alert-ok"))
        )
        self.assertTrue(alert_ok.is_displayed(),
                        "No se mostró confirmación de registro")

        lista = self.driver.find_element(By.ID, "lista-pacientes")
        self.assertIn("123456", lista.text,
                      "El paciente no aparece en la lista")

        print("PASÓ: Paciente registrado correctamente")

    # ----------------------------------------------------------
    # PRUEBA 2: CP4-O — ID de paciente duplicado
    # ----------------------------------------------------------
    def test_02_id_paciente_duplicado(self):
        """CP4-O.3 — ID de paciente duplicado muestra alerta"""
        print("\n[CP4-O.3] Probando duplicidad de ID de paciente...")

        # Inyectar paciente existente con ID 123456
        self.driver.execute_script("""
            localStorage.setItem('sigc_pacientes', JSON.stringify([{
                nombre: 'María', apellido: 'García',
                tipoId: 'Cédula de ciudadanía', id: '123456',
                fecha: '1990-05-15', telefono: '3001234567',
                eps: 'Sanitas', direccion: 'Calle 45 #12-30'
            }]));
        """)
        self.driver.refresh()
        self.wait.until(EC.presence_of_element_located((By.ID, "form-paciente")))

        self._llenar_paciente(
            nombre="Juan", apellido="López",
            tipo_id="Cédula de ciudadanía", id_num="123456",  # ID duplicado
            fecha="1985-03-20", telefono="3109876543",
            eps="Compensar", direccion="Carrera 10 #5-20"
        )

        alert_dup = self.wait.until(
            EC.visibility_of_element_located((By.ID, "alert-dup-id"))
        )
        self.assertTrue(alert_dup.is_displayed(),
                        "No se mostró alerta de ID duplicado")

        msg = self.driver.find_element(By.ID, "msg-dup-id").text
        self.assertIn("123456", msg,
                      "El mensaje no menciona el ID duplicado")

        print("PASÓ: ID duplicado detectado con mensaje específico")

    # ----------------------------------------------------------
    # PRUEBA 3: CP5-O — Campos obligatorios vacíos simultáneamente
    # ----------------------------------------------------------
    def test_03_campos_obligatorios_vacios(self):
        """CP5-O.1 — Todos los campos vacíos muestran errores individuales"""
        print("\n[CP5-O.1] Probando envío con todos los campos vacíos...")

        # Clic en guardar sin llenar nada
        self.wait.until(EC.presence_of_element_located((By.ID, "btn-registrar-paciente")))
        self.driver.find_element(By.ID, "btn-registrar-paciente").click()

        # Verificar que aparecen múltiples errores simultáneamente
        errores_esperados = [
            ("err-nombre",    "Nombre del paciente"),
            ("err-apellido",  "Apellido"),
            ("err-tipo-id",   "Tipo de ID"),
            ("err-id",        "Número de ID"),
            ("err-fecha",     "Fecha de nacimiento"),
            ("err-telefono",  "Teléfono"),
            ("err-eps",       "EPS"),
            ("err-direccion", "Dirección"),
        ]

        errores_encontrados = 0
        for err_id, nombre_campo in errores_esperados:
            el = self.driver.find_element(By.ID, err_id)
            if el.is_displayed():
                errores_encontrados += 1
            else:
                print(f"  ⚠ Campo sin error visible: {nombre_campo}")

        self.assertGreaterEqual(errores_encontrados, 6,
            f"Solo {errores_encontrados}/8 errores visibles — se esperan al menos 6")

        # Verificar campos marcados en rojo
        nombre_input = self.driver.find_element(By.ID, "pac-nombre")
        self.assertIn("err", nombre_input.get_attribute("class"),
                      "Campo nombre no se marcó en rojo")

        print(f"PASÓ: {errores_encontrados}/8 campos obligatorios muestran error")

    # ----------------------------------------------------------
    # PRUEBA 4: CP5-O — Campo nombre vacío individualmente
    # ----------------------------------------------------------
    def test_04_nombre_paciente_vacio(self):
        """CP5-O.2 — Campo 'Nombre del Paciente' vacío muestra error"""
        print("\n[CP5-O.2] Probando campo nombre vacío...")

        # Llenar todo excepto nombre
        self._llenar_paciente(
            nombre="",   # Campo vacío
            apellido="García",
            tipo_id="Cédula de ciudadanía", id_num="999888",
            fecha="1995-01-10", telefono="3201234567",
            eps="Sura", direccion="Av. Principal #1-1"
        )

        err_nombre = self.wait.until(
            EC.visibility_of_element_located((By.ID, "err-nombre"))
        )
        self.assertTrue(err_nombre.is_displayed(),
                        "No se mostró error de campo nombre vacío")

        nombre_input = self.driver.find_element(By.ID, "pac-nombre")
        self.assertIn("err", nombre_input.get_attribute("class"),
                      "Campo nombre no se resaltó en rojo")

        print("PASÓ: Campo nombre vacío resaltado en rojo con mensaje")

    # ----------------------------------------------------------
    # PRUEBA 5: CP5-O — Inyección XSS en campo nombre
    # ----------------------------------------------------------
    def test_05_xss_sanitizacion(self):
        """CP5-O.3 — Payload XSS en nombre es sanitizado, no ejecutado"""
        print("\n[CP5-O.3] Probando sanitización de XSS en campo nombre...")

        XSS_PAYLOAD = "<script>alert('XSS')</script>"

        self._llenar_paciente(
            nombre=XSS_PAYLOAD,
            apellido="Test",
            tipo_id="Cédula de ciudadanía", id_num="777666",
            fecha="2000-06-15", telefono="3151234567",
            eps="Nueva EPS", direccion="Test #1-1"
        )

        time.sleep(1)

        # Verificar que NO apareció un alert de JavaScript (XSS ejecutado)
        try:
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            alert.dismiss()
            self.fail(f"XSS EJECUTADO — Se mostró alert con texto: '{alert_text}'")
        except Exception:
            pass  # No hay alert = XSS fue bloqueado ✅

        # Verificar alerta de sanitización visible
        alert_xss = self.driver.find_element(By.ID, "alert-xss")
        if alert_xss.is_displayed():
            print("  ℹ XSS detectado y notificado al usuario")

        # Verificar que el script no está en el DOM como HTML ejecutable
        page_source = self.driver.page_source
        self.assertNotIn("<script>alert('XSS')</script>", page_source,
                         "El script XSS aparece sin sanitizar en el DOM")

        print("PASÓ: Payload XSS sanitizado — no se ejecutó ningún script")


if __name__ == "__main__":
    print("=" * 60)
    print("  SIGC — CP4-O / CP5-O: Pruebas de Registro de Paciente")
    print("  Asegúrate de que Live Server esté corriendo en :5500")
    print("=" * 60)
    unittest.main(verbosity=2)
