import mercadopago
from django.conf import settings

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

# SDK mercadopago
sdk = mercadopago.SDK("TEST-5622471274489517-111321-e57eecea6c970f0cad625288764233de-27937419")
