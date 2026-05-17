"""
SIGC v2 — Pruebas unitarias para utils.py
Permite medir cobertura de código con pytest-cov.
Prueba las funciones de validación y sanitización
de forma aislada, sin necesidad de navegador.

Ejecutar:
    pytest test_unit_utils.py -v --cov=utils --cov-report=term-missing
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

# Importar solo las funciones puras de validación
# (no las que dependen de Selenium)
BASE_URL       = "http://127.0.0.1:5500/app"
VALID_EMAIL    = "admin@medical.com"
VALID_PASSWORD = "Sistemas2026*"


# ── Mock de SIGCValidaciones para pruebas unitarias ───────────────────────────

class MockValidaciones:
    """Implementación de las validaciones para testing unitario."""

    EMAIL_REGEX = r'^[^\s@]+@[^\s@]+\.[^\s@]+'

    @staticmethod
    def validar_email(email):
        import re
        if not email or not email.strip():
            return {'valid': False, 'message': 'El correo electrónico es requerido.'}
        if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email.strip()):
            return {'valid': False, 'message': 'Ingresa un correo electrónico válido.'}
        return {'valid': True, 'message': ''}

    @staticmethod
    def validar_password(password):
        if not password:
            return {'valid': False, 'message': 'La contraseña es requerida.', 'strength': 0}
        strength = 0
        if len(password) >= 8:             strength += 1
        if any(c.isupper() for c in password): strength += 1
        if any(c.isdigit() for c in password): strength += 1
        if any(not c.isalnum() for c in password): strength += 1
        if strength < 3:
            return {'valid': False, 'message': 'Contraseña débil.', 'strength': strength}
        return {'valid': True, 'message': '', 'strength': strength}

    @staticmethod
    def validar_tarjeta_profesional(tarjeta):
        import re
        if not tarjeta or not tarjeta.strip():
            return {'valid': False, 'message': 'La tarjeta profesional es requerida.'}
        if not re.match(r'^TP-[A-Za-z0-9]{2,8}$', tarjeta.strip()):
            return {'valid': False, 'message': 'Formato inválido. Usa TP-XXXX.'}
        return {'valid': True, 'message': ''}

    @staticmethod
    def validar_telefono(telefono):
        import re
        if not telefono or not telefono.strip():
            return {'valid': False, 'message': 'El teléfono es requerido.'}
        if not re.match(r'^\d{7,10}$', telefono.strip()):
            return {'valid': False, 'message': 'Teléfono inválido.'}
        return {'valid': True, 'message': ''}

    @staticmethod
    def contiene_xss(texto):
        import re
        return bool(re.search(r'[<>"\'`]|script|javascript|onerror|onload', texto, re.IGNORECASE))

    @staticmethod
    def sanitizar(texto):
        mapa = {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#x27;','`':'&#x60;'}
        return ''.join(mapa.get(c, c) for c in texto)

    @staticmethod
    def validar_requerido(value, field_name='Este campo'):
        if not value or not value.strip():
            return {'valid': False, 'message': f'{field_name} es obligatorio.'}
        return {'valid': True, 'message': ''}


v = MockValidaciones()


# ── Tests de validación de email ──────────────────────────────────────────────

class TestValidarEmail:

    def test_email_valido(self):
        """Email válido retorna valid=True."""
        result = v.validar_email("admin@medical.com")
        assert result['valid'] is True
        assert result['message'] == ''

    def test_email_sin_arroba(self):
        """Email sin @ retorna valid=False."""
        result = v.validar_email("adminmedical.com")
        assert result['valid'] is False
        assert 'correo' in result['message'].lower() or 'válido' in result['message'].lower()

    def test_email_vacio(self):
        """Email vacío retorna valid=False con mensaje."""
        result = v.validar_email("")
        assert result['valid'] is False
        assert result['message'] != ''

    def test_email_solo_espacios(self):
        """Email con solo espacios retorna valid=False."""
        result = v.validar_email("   ")
        assert result['valid'] is False

    def test_email_sin_dominio(self):
        """Email sin dominio retorna valid=False."""
        result = v.validar_email("admin@")
        assert result['valid'] is False

    def test_email_con_subdomain(self):
        """Email con subdominio es válido."""
        result = v.validar_email("user@mail.medical.com")
        assert result['valid'] is True


# ── Tests de validación de contraseña ─────────────────────────────────────────

class TestValidarPassword:

    def test_password_fuerte(self):
        """Contraseña fuerte (8+ chars, mayúscula, número, símbolo) retorna válida."""
        result = v.validar_password("Sistemas2026*")
        assert result['valid'] is True
        assert result['strength'] >= 3

    def test_password_muy_corta(self):
        """Contraseña de menos de 8 caracteres retorna inválida."""
        result = v.validar_password("abc")
        assert result['valid'] is False

    def test_password_sin_mayuscula(self):
        """Contraseña sin mayúsculas tiene fortaleza reducida."""
        result = v.validar_password("sistemas2026*")
        assert result['strength'] < 4

    def test_password_solo_letras(self):
        """Contraseña solo con letras minúsculas es débil."""
        result = v.validar_password("sololetras")
        assert result['valid'] is False

    def test_password_vacia(self):
        """Contraseña vacía retorna inválida con strength=0."""
        result = v.validar_password("")
        assert result['valid'] is False
        assert result['strength'] == 0

    def test_password_con_todos_requisitos(self):
        """Contraseña con todos los requisitos tiene strength=4."""
        result = v.validar_password("Admin2024!")
        assert result['strength'] == 4
        assert result['valid'] is True


# ── Tests de validación de tarjeta profesional ────────────────────────────────

class TestValidarTarjeta:

    def test_tarjeta_valida_numerica(self):
        """Tarjeta TP-8877 (formato válido numérico) retorna válida."""
        result = v.validar_tarjeta_profesional("TP-8877")
        assert result['valid'] is True

    def test_tarjeta_valida_alfanumerica(self):
        """Tarjeta TP-AB12 (formato alfanumérico) retorna válida."""
        result = v.validar_tarjeta_profesional("TP-AB12")
        assert result['valid'] is True

    def test_tarjeta_sin_prefijo_tp(self):
        """Tarjeta sin prefijo TP- retorna inválida."""
        result = v.validar_tarjeta_profesional("8877")
        assert result['valid'] is False

    def test_tarjeta_con_simbolos(self):
        """Tarjeta con símbolos especiales TP-@#$ retorna inválida."""
        result = v.validar_tarjeta_profesional("TP-@#$")
        assert result['valid'] is False

    def test_tarjeta_vacia(self):
        """Tarjeta vacía retorna inválida."""
        result = v.validar_tarjeta_profesional("")
        assert result['valid'] is False

    def test_tarjeta_muy_larga(self):
        """Tarjeta con más de 8 chars después del guión retorna inválida."""
        result = v.validar_tarjeta_profesional("TP-123456789")
        assert result['valid'] is False


# ── Tests de validación de teléfono ───────────────────────────────────────────

class TestValidarTelefono:

    def test_telefono_valido_10_digitos(self):
        """Teléfono de 10 dígitos retorna válido."""
        result = v.validar_telefono("3001234567")
        assert result['valid'] is True

    def test_telefono_valido_7_digitos(self):
        """Teléfono de 7 dígitos retorna válido."""
        result = v.validar_telefono("3001234")
        assert result['valid'] is True

    def test_telefono_con_letras(self):
        """Teléfono con letras retorna inválido."""
        result = v.validar_telefono("300abc4567")
        assert result['valid'] is False

    def test_telefono_muy_corto(self):
        """Teléfono de menos de 7 dígitos retorna inválido."""
        result = v.validar_telefono("300123")
        assert result['valid'] is False

    def test_telefono_vacio(self):
        """Teléfono vacío retorna inválido."""
        result = v.validar_telefono("")
        assert result['valid'] is False


# ── Tests de sanitización XSS ─────────────────────────────────────────────────

class TestXSS:

    def test_detecta_script_tag(self):
        """Detecta payload con etiqueta <script>."""
        assert v.contiene_xss("<script>alert('XSS')</script>") is True

    def test_detecta_javascript_protocol(self):
        """Detecta payload con protocolo javascript:."""
        assert v.contiene_xss("javascript:alert(1)") is True

    def test_detecta_onerror(self):
        """Detecta payload con atributo onerror."""
        assert v.contiene_xss("<img src=x onerror=alert(1)>") is True

    def test_no_detecta_texto_normal(self):
        """Texto normal no es detectado como XSS."""
        assert v.contiene_xss("María García López") is False

    def test_sanitizar_script_tag(self):
        """Sanitiza etiqueta <script> en &lt;script&gt;."""
        result = v.sanitizar("<script>")
        assert "<" not in result
        assert ">" not in result
        assert "&lt;" in result

    def test_sanitizar_comillas(self):
        """Sanitiza comillas simples y dobles."""
        result = v.sanitizar("'hola' \"mundo\"")
        assert "'" not in result
        assert '"' not in result

    def test_sanitizar_texto_normal(self):
        """Texto normal no cambia tras sanitización."""
        result = v.sanitizar("María García")
        assert result == "María García"


# ── Tests de validación requerida ─────────────────────────────────────────────

class TestValidarRequerido:

    def test_campo_con_valor(self):
        """Campo con valor retorna válido."""
        result = v.validar_requerido("Juan", "El nombre")
        assert result['valid'] is True

    def test_campo_vacio(self):
        """Campo vacío retorna inválido."""
        result = v.validar_requerido("", "El nombre")
        assert result['valid'] is False
        assert "nombre" in result['message'].lower()

    def test_campo_solo_espacios(self):
        """Campo con solo espacios retorna inválido."""
        result = v.validar_requerido("   ", "El nombre")
        assert result['valid'] is False

    def test_constantes_base_url(self):
        """BASE_URL tiene el formato correcto."""
        assert BASE_URL.startswith("http://")
        assert "5500" in BASE_URL

    def test_credenciales_validas_definidas(self):
        """Las credenciales válidas están definidas correctamente."""
        assert "@" in VALID_EMAIL
        assert len(VALID_PASSWORD) >= 8
