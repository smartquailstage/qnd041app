import json
import requests
from .models import Product

def consultar_ollama_productos(pregunta_usuario, producto_id=None):
    """
    Extrae la información del producto seleccionado de forma limpia,
    omitiendo campos vacíos/None para que el modelo no genere respuestas nulas.
    """
    try:
        if producto_id:
            productos = Product.objects.select_related('category').filter(pk=producto_id, available=True)
        else:
            productos = Product.objects.select_related('category').filter(available=True)[:5]

        if not productos.exists():
            return "Lo siento, no se encontró el producto o servicio especificado en la base de datos."

        contexto_productos = "INFORMACIÓN DEL PRODUCTO / SERVICIO TECNOLÓGICO (SmartQuail):\n"
        for p in productos:
            categoria = p.category.name if p.category else "Sin categoría"
            
            # Agregamos únicamente los campos que tienen valor real
            detalles = [f"- Producto: {p.name}", f"Categoría: {categoria}"]
            
            if getattr(p, 'cloud_type', None):
                detalles.append(f"Tipo de Nube: {p.cloud_type}")
            if getattr(p, 'os', None):
                detalles.append(f"OS: {p.os}")
            
            cpu = getattr(p, 'vCPU', getattr(p, 'cpu', None))
            if cpu is not None:
                detalles.append(f"CPU: {cpu} vCPUs")
                
            if getattr(p, 'memoria', None) is not None:
                detalles.append(f"Memoria: {p.memoria} GB")
                
            if getattr(p, 'almacenamiento', None) is not None:
                detalles.append(f"Almacenamiento: {p.almacenamiento} GB")
                
            if getattr(p, 'price_amount', None) is not None:
                detalles.append(f"Precio: ${p.price_amount} USD")
                
            software = p.get_software_display() if hasattr(p, 'get_software_display') else getattr(p, 'software', None)
            if software:
                detalles.append(f"Software: {software}")
                
            if getattr(p, 'latencia_aproximada', None):
                detalles.append(f"Latencia: {p.latencia_aproximada}")
                
            concurrencia = p.get_usuarios_simultaneos_display() if hasattr(p, 'get_usuarios_simultaneos_display') else getattr(p, 'usuarios_simultaneos', None)
            if concurrencia:
                detalles.append(f"Concurrencia: {concurrencia}")
                
            if getattr(p, 'automatizacion', None):
                detalles.append(f"Automatización: {p.automatizacion}")
            if getattr(p, 'inteligencia_artificial', None):
                detalles.append(f"IA: {p.inteligencia_artificial}")
                
            if p.description:
                detalles.append(f"Descripción: {p.description}")

            contexto_productos += " | ".join(detalles) + "\n"

        system_prompt = (
            "Eres un asistente de IA corporativo y estricto para SmartQuail, Inc. "
            "Tu única fuente de verdad es la 'INFORMACIÓN DEL PRODUCTO' provista a continuación. "
            "REGLAS ESTRICTAS:\n"
            "1. Responde ÚNICAMENTE basándote en la información del producto listado abajo.\n"
            "2. Si la pregunta solicita una característica o especificación técnica que no está explícitamente en los datos, responde exactamente: "
            "'Este producto o servicio no especifica esa característica en su ficha técnica.'\n"
            "3. No inventes precios ni características que no estén escritas en el contexto.\n"
            "4. Mantén un tono profesional, técnico y orientado a negocios y tecnología cloud."
        )

        url = "http://ollama100-service.ai-models.svc.cluster.local:11434/api/chat"
        
        payload = {
            "model": "qwen2.5:0.5b",
            "messages": [
                {"role": "system", "content": f"{system_prompt}\n\n{contexto_productos}"},
                {"role": "user", "content": pregunta_usuario}
            ],
            "stream": False,
            "options": {
                "temperature": 0.1,
                "num_ctx": 2048
            }
        }

        response = requests.post(url, data=json.dumps(payload), headers={"Content-Type": "application/json"}, timeout=90)
        
        if response.status_code == 200:
            resultado = response.json()
            return resultado.get("message", {}).get("content", "No se pudo procesar la respuesta.")
        else:
            return f"Error al conectar con el servidor de Ollama (Código {response.status_code})."
            
    except requests.exceptions.RequestException as e:
        return f"Error de conexión con Ollama en el clúster: Detalle: {e}"
    except Exception as e:
        return f"Error interno en el servicio de IA: {str(e)}"