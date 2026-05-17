"""
SIGC v2 — Runner de pruebas automatizadas
Ejecuta la suite completa de scripts Selenium E2E y muestra resumen.
"""

import unittest
import time

from test_CP1O_registro_admin      import CP1O_RegistroAdmin
from test_CP2O_autenticacion       import CP2O_Autenticacion
from test_CP3O_CP4O_registro_medico import CP3O_CP4O_RegistroMedico
from test_CP4O_CP5O_registro_paciente import CP4O_CP5O_RegistroPaciente


def run_suite():
    """Construye y ejecuta la suite completa de pruebas."""
    loader  = unittest.TestLoader()
    suite   = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(CP2O_Autenticacion))
    suite.addTests(loader.loadTestsFromTestCase(CP1O_RegistroAdmin))
    suite.addTests(loader.loadTestsFromTestCase(CP3O_CP4O_RegistroMedico))
    suite.addTests(loader.loadTestsFromTestCase(CP4O_CP5O_RegistroPaciente))

    runner = unittest.TextTestRunner(verbosity=2)
    inicio = time.time()
    result = runner.run(suite)
    duracion = time.time() - inicio

    total   = result.testsRun
    fallidos = len(result.failures)
    errores  = len(result.errors)
    exitosos = total - fallidos - errores

    print("\n" + "=" * 50)
    print(f"  Total ejecutados : {total}")
    print(f"  ✅ Exitosos       : {exitosos}")
    print(f"  ❌ Fallidos       : {fallidos}")
    print(f"  ⚠  Con errores   : {errores}")
    print(f"  ⏱  Tiempo total   : {duracion:.3f} segundos")
    print("=" * 50)

    if exitosos == total:
        print("\n🎉 TODAS LAS PRUEBAS PASARON EXITOSAMENTE\n")
    else:
        print(f"\n⚠️  {fallidos + errores} PRUEBA(S) FALLARON\n")


if __name__ == "__main__":
    run_suite()
