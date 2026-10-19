import requests

def enviar_factura_al_microservicio(xml_generado):
    url = "http://facturacion-service:8080/factura/emitir/"
    headers = {'Content-Type': 'application/xml'}

    try:
        response = requests.post(url, data=xml_generado, headers=headers)
        response.raise_for_status()
        return response.json()  # o response.text si es XML
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
