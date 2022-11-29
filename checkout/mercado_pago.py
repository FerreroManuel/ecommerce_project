import mercadopago
from django.conf import settings

from core.settings.base import MY_SECRET_KEYS

# Estados de pago => {'cod_mercadpago': 'Leyenda'}
PAYMENT_STATUS = {
    'approved': 'Aprobado',
    'cc_rejected_insufficient_amount': 'Saldo insuficiente',
    'cc_rejected_other_reason': 'Error general',
    'pending_contingency': 'Pendiente de pago',
    'cc_rejected_call_for_authorize': 'Necesita autorización',
    'cc_rejected_bad_filled_security_code': 'Código de seguridad erroneo',
    'cc_rejected_bad_filled_date': 'Tarjeta vencida o fecha de vencimiento erronea',
    'cc_rejected_bad_filled_other': 'Error en el formulario',
}

mp_secret_key = str(MY_SECRET_KEYS["MERCADOPAGO"])

# SDK mercadopago
sdk = mercadopago.SDK(mp_secret_key)
