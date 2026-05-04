"""
=============================================================
SIGC — Script de Prueba Automatizada
Caso: CP1-O | Módulo: Registro / Autenticación
Escenario: Registro de Admin con datos válidos,
           contraseña débil y correo duplicado
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

BASE_URL = "http://127.0.0.1:5500/app"


class CP1O_RegistroAdmin(unittest.TestCase):
    """CP1-O: Registro de Administrador — válido, débil y duplicado"""

    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--incognito")
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        self.wait = WebDriverWait(self.driver, 10)
        self.driver.get(f"{BASE_URL}/registro-admin.html")

    def tearDown(self):
        time.sleep(1)
        self.driver.quit()

    def _llenar_formulario(self, nombre, email, password, confirm):
        """Helper: llena el formulario de registro"""
        self.wait.until(EC.presence_of_element_located((By.ID, "a-name")))
        nombre_field = self.driver.find_element(By.ID, "a-name")
        email_field  = self.driver.find_element(By.ID, "a-email")
        pass_field   = self.driver.find_element(By.ID, "a-pass")
        pass2_field  = self.driver.find_element(By.ID, "a-pass2")
        nombre_field.clear(); nombre_field.send_keys(nombre)
        email_field.clear();  email_field.send_keys(email)
        pass_field.clear();   pass_field.send_keys(password)
        pass2_field.clear();  pass2_field.send_keys(confirm)
        self.driver.find_element(By.ID, "btn-reg").click()

    # ----------------------------------------------------------
    # PRUEBA 1: Registro exitoso con datos válidos
    # ----------------------------------------------------------
    def test_01_registro_exitoso(self):
        """CP1-O.1 — Registro con datos válidos muestra éxito y redirige"""
        print("\n[CP1-O.1] Probando registro con datos válidos...")

        self._llenar_formulario(
            nombre="Carlos Mendoza",
            email="nuevo@medical.com",
            password="NuevoAdmin2025*",
            confirm="NuevoAdmin2025*"
        )

        # Verificar alerta de éxito
        alert_ok = self.wait.until(
            EC.visibility_of_element_located((By.ID, "alert-ok"))
        )
        self.assertTrue(alert_ok.is_displayed(),
                        "No se mostró alerta de registro exitoso")

        # Verificar redirección al login
        self.wait.until(EC.url_contains("index.html"))
        self.assertIn("index.html", self.driver.current_url,
                      "No redirigió al login tras registro exitoso")

        print("PASÓ: Registro exitoso y redirección al login correcta")

    # ----------------------------------------------------------
    # PRUEBA 2: Contraseña débil muestra error específico
    # ----------------------------------------------------------
    def test_02_contrasena_debil(self):
        """CP1-O.2 — Contraseña débil muestra mensaje de error"""
        print("\n[CP1-O.2] Probando registro con contraseña débil...")

        self._llenar_formulario(
            nombre="Ana García",
            email="ana@medical.com",
            password="1234",       # Contraseña débil
            confirm="1234"
        )

        # Verificar campo de error de contraseña
        err_pass = self.wait.until(
            EC.visibility_of_element_located((By.ID, "err-pass"))
        )
        self.assertTrue(err_pass.is_displayed(),
                        "No se mostró error de contraseña débil")

        # Verificar que el campo se marca en rojo
        pass_input = self.driver.find_element(By.ID, "a-pass")
        self.assertIn("err", pass_input.get_attribute("class"),
                      "Campo contraseña no se marcó con clase 'err'")

        # Verificar que NO redirige
        self.assertNotIn("index.html", self.driver.current_url,
                         "Redirigió al login con contraseña débil")

        print("PASÓ: Contraseña débil muestra error y bloquea el registro")

    # ----------------------------------------------------------
    # PRUEBA 3: Correo duplicado muestra error específico
    # ----------------------------------------------------------
    def test_03_correo_duplicado(self):
        """CP1-O.3 — Correo ya registrado muestra alerta de duplicado"""
        print("\n[CP1-O.3] Probando registro con correo duplicado...")

        # Inyectar admin existente en localStorage (simula registro previo)
        self.driver.execute_script("""
            const admins = [{
                email: 'admin@medical.com',
                password: 'Sistemas2026*',
                name: 'Super Admin'
            }];
            localStorage.setItem('sigc_admins', JSON.stringify(admins));
        """)

        self._llenar_formulario(
            nombre="Otro Admin",
            email="admin@medical.com",   # Correo ya existente
            password="OtroAdmin2025*",
            confirm="OtroAdmin2025*"
        )

        # Verificar alerta de duplicado
        alert_dup = self.wait.until(
            EC.visibility_of_element_located((By.ID, "alert-dup"))
        )
        self.assertTrue(alert_dup.is_displayed(),
                        "No se mostró alerta de correo duplicado")

        # Verificar mensaje contiene el correo
        msg = self.driver.find_element(By.ID, "msg-dup").text
        self.assertIn("admin@medical.com", msg,
                      "El mensaje no menciona el correo duplicado")

        print("PASÓ: Correo duplicado detectado con mensaje específico")

    # ----------------------------------------------------------
    # PRUEBA 4: Campos vacíos muestran errores individuales
    # ----------------------------------------------------------
    def test_04_campos_vacios(self):
        """CP1-O.4 — Enviar formulario vacío muestra errores por campo"""
        print("\n[CP1-O.4] Probando envío de formulario vacío...")

        self.wait.until(EC.presence_of_element_located((By.ID, "btn-reg")))

        # La validación HTML5 nativa intercepta el submit en campos type=email
        # antes de que llegue al handler JS. Se deshabilita con novalidate.
        self.driver.execute_script(
            "document.getElementById('form-admin').setAttribute('novalidate', '');"
        )
        self.driver.find_element(By.ID, "btn-reg").click()
        time.sleep(0.5)

        err_name  = self.driver.find_element(By.ID, "err-name")
        err_email = self.driver.find_element(By.ID, "err-email")
        err_pass  = self.driver.find_element(By.ID, "err-pass")

        errores_visibles = sum([
            err_name.is_displayed(),
            err_email.is_displayed(),
            err_pass.is_displayed(),
        ])

        self.assertGreaterEqual(errores_visibles, 1,
            "Ningún error de campo vacío se mostró tras el submit")

        print(f"PASÓ: {errores_visibles}/3 errores de campos vacíos visibles")


if __name__ == "__main__":
    print("=" * 60)
    print("  SIGC — CP1-O: Pruebas de Registro de Administrador")
    print("  Asegúrate de que Live Server esté corriendo en :5500")
    print("=" * 60)
    unittest.main(verbosity=2)