"""
=============================================================
SIGC — Runner principal de pruebas automatizadas
Ejecuta todos los casos de prueba en secuencia y
genera un reporte en consola con los resultados.
=============================================================
Uso:
    python run_all_tests.py
=============================================================
"""

import unittest
import sys
import time
from datetime import datetime

# Importar todos los módulos de prueba
from test_CP1O_registro_admin    import CP1O_RegistroAdmin
from test_CP2O_autenticacion     import CP2O_Autenticacion
from test_CP3O_CP4O_registro_medico  import CP3O_CP4O_RegistroMedico
from test_CP4O_CP5O_registro_paciente import CP4O_CP5O_RegistroPaciente


def run_suite():
    print("\n" + "=" * 65)
    print("   SIGC — SUITE COMPLETA DE PRUEBAS AUTOMATIZADAS")
    print(f"   Ejecución: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 65)
    print("   ⚠  Asegúrate de que Live Server esté corriendo en")
    print("      http://127.0.0.1:5500 antes de continuar.")
    print("=" * 65 + "\n")
    time.sleep(2)

    # Construir suite con todos los casos
    loader = unittest.TestLoader()
    suite  = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(CP2O_Autenticacion))
    suite.addTests(loader.loadTestsFromTestCase(CP1O_RegistroAdmin))
    suite.addTests(loader.loadTestsFromTestCase(CP3O_CP4O_RegistroMedico))
    suite.addTests(loader.loadTestsFromTestCase(CP4O_CP5O_RegistroPaciente))

    # Ejecutar con reporte detallado
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(suite)

    # Resumen final
    total   = result.testsRun
    fallos  = len(result.failures)
    errores = len(result.errors)
    exitos  = total - fallos - errores

    print("\n" + "=" * 65)
    print("   RESUMEN FINAL")
    print("=" * 65)
    print(f"   Total ejecutados : {total}")
    print(f"   Exitosos       : {exitos}")
    print(f"   Fallidos       : {fallos}")
    print(f"   Con errores   : {errores}")
    print("=" * 65)

    if result.wasSuccessful():
        print("\n   TODAS LAS PRUEBAS PASARON EXITOSAMENTE\n")
    else:
        print("\n   ⚠  ALGUNAS PRUEBAS FALLARON — Revisar detalle arriba\n")

    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_suite())
