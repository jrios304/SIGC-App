"""
=============================================================
SIGC — Script de Prueba Automatizada
Caso: CP3-O | Módulo: Gestión de Talento Humano
      CP4-O | Módulo: Gestión Pacientes / BD
Escenario: Registro de médico con datos válidos,
           campo vacío, formato inválido y duplicidad
           de tarjeta profesional y correo
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


class CP3O_CP4O_RegistroMedico(unittest.TestCase):
    """CP3-O y CP4-O: Registro de Médico — validaciones y duplicidad"""

    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--incognito")
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        self.wait = WebDriverWait(self.driver, 10)
        self.driver.get(f"{BASE_URL}/registro-medico.html")
        # Inyectar sesión para evitar redirección
        self.driver.execute_script("""
            localStorage.setItem('sigc_session', JSON.stringify({name: 'Admin Test'}));
            localStorage.setItem('sigc_medicos', JSON.stringify([]));
        """)
        self.driver.refresh()
        self.wait.until(EC.presence_of_element_located((By.ID, "form-medico")))

    def tearDown(self):
        time.sleep(1)
        self.driver.quit()

    def _llenar_medico(self, nombre, apellido, correo, especialidad, tarjeta, horario=""):
        """Helper: llena el formulario de médico"""
        self.driver.find_element(By.ID, "med-nombre").clear()
        self.driver.find_element(By.ID, "med-nombre").send_keys(nombre)
        self.driver.find_element(By.ID, "med-apellido").clear()
        self.driver.find_element(By.ID, "med-apellido").send_keys(apellido)
        self.driver.find_element(By.ID, "med-correo").clear()
        self.driver.find_element(By.ID, "med-correo").send_keys(correo)
        if especialidad:
            Select(self.driver.find_element(By.ID, "med-especialidad")).select_by_visible_text(especialidad)
        self.driver.find_element(By.ID, "med-tarjeta").clear()
        self.driver.find_element(By.ID, "med-tarjeta").send_keys(tarjeta)
        if horario:
            self.driver.find_element(By.ID, "med-horario").send_keys(horario)
        self.driver.find_element(By.ID, "btn-registrar-medico").click()

    # ----------------------------------------------------------
    # PRUEBA 1: Registro exitoso con datos completos válidos
    # ----------------------------------------------------------
    def test_01_registro_medico_exitoso(self):
        """CP3-O.1 — Registro de médico con datos válidos"""
        print("\n[CP3-O.1] Probando registro de médico con datos válidos...")

        self._llenar_medico(
            nombre="Javier",
            apellido="Sanjuanelo",
            correo="javier@sigc.com",
            especialidad="Urología",
            tarjeta="TP-8877",
            horario="Lunes a Viernes 8:00am - 4:00pm"
        )

        alert_ok = self.wait.until(
            EC.visibility_of_element_located((By.ID, "alert-ok"))
        )
        self.assertTrue(alert_ok.is_displayed(),
                        "No se mostró confirmación de registro exitoso")

        # Verificar que aparece en la lista
        lista = self.driver.find_element(By.ID, "lista-medicos")
        self.assertIn("Javier", lista.text,
                      "El médico registrado no aparece en la lista")

        print("PASÓ: Médico registrado y visible en la lista")

    # ----------------------------------------------------------
    # PRUEBA 2: Especialidad vacía muestra error
    # ----------------------------------------------------------
    def test_02_especialidad_vacia(self):
        """CP3-O.2 — Especialidad no seleccionada muestra error"""
        print("\n[CP3-O.2] Probando registro sin especialidad...")

        self._llenar_medico(
            nombre="María",
            apellido="López",
            correo="maria@sigc.com",
            especialidad="",    # Sin especialidad
            tarjeta="TP-1234"
        )

        err_esp = self.wait.until(
            EC.visibility_of_element_located((By.ID, "err-especialidad"))
        )
        self.assertTrue(err_esp.is_displayed(),
                        "No se mostró error de especialidad requerida")

        print("PASÓ: Sin especialidad muestra error 'Especialidad requerida'")

    # ----------------------------------------------------------
    # PRUEBA 3: Formato de tarjeta inválido
    # ----------------------------------------------------------
    def test_03_formato_tarjeta_invalido(self):
        """CP3-O.3 — Tarjeta profesional con formato inválido"""
        print("\n[CP3-O.3] Probando tarjeta con formato inválido...")

        self._llenar_medico(
            nombre="Pedro",
            apellido="Ramírez",
            correo="pedro@sigc.com",
            especialidad="Cardiología",
            tarjeta="TP-@#$"    # Formato inválido
        )

        err_tarjeta = self.wait.until(
            EC.visibility_of_element_located((By.ID, "err-tarjeta"))
        )
        self.assertTrue(err_tarjeta.is_displayed(),
                        "No se mostró error de formato de tarjeta inválido")

        tarjeta_input = self.driver.find_element(By.ID, "med-tarjeta")
        self.assertIn("err", tarjeta_input.get_attribute("class"),
                      "Campo tarjeta no se marcó en rojo")

        print("PASÓ: Formato inválido de tarjeta detectado con error")

    # ----------------------------------------------------------
    # PRUEBA 4: CP4-O — Duplicidad de tarjeta profesional
    # ----------------------------------------------------------
    def test_04_tarjeta_duplicada(self):
        """CP4-O.1 — Tarjeta profesional duplicada muestra alerta"""
        print("\n[CP4-O.1] Probando duplicidad de tarjeta profesional...")

        # Inyectar médico existente con TP-8877
        self.driver.execute_script("""
            localStorage.setItem('sigc_medicos', JSON.stringify([{
                nombre: 'Javier', apellido: 'Sanjuanelo',
                correo: 'javier@sigc.com', especialidad: 'Urología',
                tarjeta: 'TP-8877', horario: ''
            }]));
        """)
        self.driver.refresh()
        self.wait.until(EC.presence_of_element_located((By.ID, "form-medico")))

        self._llenar_medico(
            nombre="Luis",
            apellido="Pérez",
            correo="luis@sigc.com",
            especialidad="Pediatría",
            tarjeta="TP-8877"   # Tarjeta duplicada
        )

        alert_dup = self.wait.until(
            EC.visibility_of_element_located((By.ID, "alert-dup-tarjeta"))
        )
        self.assertTrue(alert_dup.is_displayed(),
                        "No se mostró alerta de tarjeta duplicada")

        msg = self.driver.find_element(By.ID, "msg-dup-tarjeta").text
        self.assertIn("TP-8877", msg,
                      "El mensaje no menciona la tarjeta duplicada")

        print("PASÓ: Duplicidad de tarjeta detectada con mensaje específico")

    # ----------------------------------------------------------
    # PRUEBA 5: CP4-O — Duplicidad de correo médico
    # ----------------------------------------------------------
    def test_05_correo_medico_duplicado(self):
        """CP4-O.2 — Correo médico duplicado muestra alerta"""
        print("\n[CP4-O.2] Probando duplicidad de correo de médico...")

        self.driver.execute_script("""
            localStorage.setItem('sigc_medicos', JSON.stringify([{
                nombre: 'Javier', apellido: 'Sanjuanelo',
                correo: 'javier@sigc.com', especialidad: 'Urología',
                tarjeta: 'TP-8877', horario: ''
            }]));
        """)
        self.driver.refresh()
        self.wait.until(EC.presence_of_element_located((By.ID, "form-medico")))

        self._llenar_medico(
            nombre="Carlos",
            apellido="Gómez",
            correo="javier@sigc.com",   # Correo duplicado
            especialidad="Neurología",
            tarjeta="TP-9999"
        )

        alert_dup_correo = self.wait.until(
            EC.visibility_of_element_located((By.ID, "alert-dup-correo"))
        )
        self.assertTrue(alert_dup_correo.is_displayed(),
                        "No se mostró alerta de correo duplicado")

        print("PASÓ: Duplicidad de correo médico detectada correctamente")


if __name__ == "__main__":
    print("=" * 60)
    print("  SIGC — CP3-O / CP4-O: Pruebas de Registro de Médico")
    print("  Asegúrate de que Live Server esté corriendo en :5500")
    print("=" * 60)
    unittest.main(verbosity=2)
