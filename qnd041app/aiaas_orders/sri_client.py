from zeep import Client
from zeep.transports import Transport
from django.conf import settings
import base64
import time


RECEPCION_WSDL = 'https://celcer.sri.gob.ec/comprobantes-electronicos-ws/RecepcionComprobantesOffline?wsdl'
AUTORIZACION_WSDL = 'https://celcer.sri.gob.ec/comprobantes-electronicos-ws/AutorizacionComprobantesOffline?wsdl'


def enviar_comprobante(xml_str):
    """
    Envía el comprobante al SRI (web service de recepción).
    """
    client = Client(RECEPCION_WSDL, transport=Transport(timeout=10))
    xml_base64 = base64.b64encode(xml_str.encode()).decode()
    
    result = client.service.validarComprobante(xml_base64)
    estado = result.comprobantes[0].estado if result.comprobantes else result.estado

    return {
        'estado': estado,
        'mensaje': result
    }


def autorizar_comprobante(clave_acceso):
    """
    Consulta el estado de autorización del comprobante.
    """
    client = Client(AUTORIZACION_WSDL, transport=Transport(timeout=10))

    # Esperar un momento para que el SRI procese la recepción
    time.sleep(2)

    result = client.service.autorizacionComprobante(clave_acceso)

    if hasattr(result, 'autorizaciones') and result.autorizaciones:
        autorizacion = result.autorizaciones.autorizacion[0]
        return {
            'estado': autorizacion.estado,
            'numero_autorizacion': autorizacion.numeroAutorizacion,
            'fecha_autorizacion': autorizacion.fechaAutorizacion,
            'comprobante': autorizacion.comprobante
        }

    return {
        'estado': 'NO AUTORIZADO',
        'mensaje': 'Comprobante no autorizado o clave no encontrada'
    }
