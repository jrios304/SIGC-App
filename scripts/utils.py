"""
SIGC — Utilidades compartidas para scripts de prueba
Módulo base que reduce duplicación y complejidad ciclomática
en los scripts de prueba automatizados con Selenium.
"""

import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Configuración global
BASE_URL         = "http://127.0.0.1:5500/app"
VALID_EMAIL      = "admin@medical.com"
VALID_PASSWORD   = "Sistemas2026*"
INVALID_EMAIL    = "admin@mediconnect.com"
INVALID_PASSWORD = "clave123"
WAIT_TIMEOUT     = 10

MEDICO_DEFAULT = {
    "nombre": "Javier", "apellido": "Sanjuanelo",
    "correo": "javier@sigc.com", "especialidad": "Urología",
    "tarjeta": "TP-8877", "horario": ""
}

PACIENTE_DEFAULT = {
    "nombre": "María", "apellido": "García",
    "tipoId": "Cédula de ciudadanía", "id": "123456",
    "fecha": "1990-05-15", "telefono": "3001234567",
    "eps": "Sanitas", "direccion": "Calle 45 #12-30"
}

ADMIN_DEFAULT = {
    "email": "admin@medical.com",
    "password": "Sistemas2026*",
    "name": "Super Admin"
}


def crear_driver(headless=False):
    """
    Crea y configura una instancia de ChromeDriver.

    Args:
        headless (bool): Si True, ejecuta Chrome sin interfaz gráfica (CI/CD).

    Returns:
        webdriver.Chrome: Instancia configurada del driver.
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--incognito")
    if headless:
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )


def crear_wait(driver, timeout=WAIT_TIMEOUT):
    """
    Crea un WebDriverWait con timeout configurable.

    Args:
        driver (webdriver.Chrome): Instancia del driver.
        timeout (int): Segundos de espera máxima.

    Returns:
        WebDriverWait: Instancia configurada.
    """
    return WebDriverWait(driver, timeout)


def inyectar_sesion(driver, nombre="Admin Test"):
    """
    Inyecta sesión de administrador en localStorage.

    Args:
        driver (webdriver.Chrome): Instancia del driver.
        nombre (str): Nombre del usuario de sesión.
    """
    driver.execute_script(
        f"localStorage.setItem('sigc_session', JSON.stringify({{name: '{nombre}'}}));"
    )


def inyectar_admins(driver, admins=None):
    """
    Inyecta lista de administradores en localStorage.

    Args:
        driver (webdriver.Chrome): Instancia del driver.
        admins (list): Lista de admins. Usa ADMIN_DEFAULT si es None.
    """
    data = admins if admins is not None else [ADMIN_DEFAULT]
    driver.execute_script(
        f"localStorage.setItem('sigc_admins', JSON.stringify({json.dumps(data)}));"
    )


def inyectar_medicos(driver, medicos=None):
    """
    Inyecta lista de médicos en localStorage.

    Args:
        driver (webdriver.Chrome): Instancia del driver.
        medicos (list): Lista de médicos. Usa [] si es None.
    """
    data = medicos if medicos is not None else []
    driver.execute_script(
        f"localStorage.setItem('sigc_medicos', JSON.stringify({json.dumps(data)}));"
    )


def inyectar_pacientes(driver, pacientes=None):
    """
    Inyecta lista de pacientes en localStorage.

    Args:
        driver (webdriver.Chrome): Instancia del driver.
        pacientes (list): Lista de pacientes. Usa [] si es None.
    """
    data = pacientes if pacientes is not None else []
    driver.execute_script(
        f"localStorage.setItem('sigc_pacientes', JSON.stringify({json.dumps(data)}));"
    )


def limpiar_storage(driver):
    """
    Limpia completamente el localStorage.

    Args:
        driver (webdriver.Chrome): Instancia del driver.
    """
    driver.execute_script("localStorage.clear();")


def refrescar_y_esperar(driver, wait, selector, delay=0.3):
    """
    Refresca la página y espera a que un elemento esté disponible.

    Args:
        driver (webdriver.Chrome): Instancia del driver.
        wait (WebDriverWait): Instancia de espera.
        selector (str): CSS selector del elemento a esperar.
        delay (float): Pausa antes de refrescar en segundos.
    """
    time.sleep(delay)
    driver.refresh()
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
