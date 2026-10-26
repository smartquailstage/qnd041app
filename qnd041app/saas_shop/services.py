import requests
import json
from .models import Product

def consultar_ollama_productos(pregunta_usuario):
    """
    Extrae la información de la base de datos de productos y la inyecta 
    en un prompt estricto para que Ollama responda exclusivamente con base en esos datos.
    """
    # 1. Extraer todos los productos y sus características clave de la base de datos
    productos = Product.objects.select_related('category').filter(available=True)
    
    contexto_productos = "BASE DE DATOS DE PRODUCTOS Y SERVICIOS TECNOLÓGICOS (SmartQuail):\n"
    for p in productos:
        categoria = p.category.name if p.category else "Sin categoría"
        tamano = p.category.get_tamano_empresa_display() if p.category else "N/A"
        
        contexto_productos += (
            f"- Producto: {p.name} | Categoría: {categoria} ({tamano}) | "
            f"Tipo de Nube: {p.cloud_type} | OS: {p.os} | CPU: {p.vCPU if hasattr(p, 'vCPU') else p.cpu} vCPUs | "
            f"Memoria: {p.memoria} GB | Almacenamiento: {p.almacenamiento} GB | "
            f"Precio: ${p.price_amount or 0} USD | "
            f"Software: {p.get_software_display() if hasattr(p, 'get_software_display') else p.software} | "
            f"Latencia: {p.latencia_aproximada} | Concurrencia: {p.get_usuarios_simultaneos_display() if hasattr(p, 'get_usuarios_simultaneos_display') else p.usuarios_simultaneos} | "
            f"Automatización: {p.automatizacion} | IA: {p.inteligencia_artificial} | "
            f"Descripción: {p.description}\n"
        )

    # 2. Definir el System Prompt estricto (Restricción dura)
    system_prompt = (
        "Eres un asistente de IA corporativo y estricto para SmartQuail, Inc. "
        "Tu única fuente de verdad es la 'BASE DE DATOS DE PRODUCTOS Y SERVICIOS TECNOLÓGicos' provista a continuación. "
        "REGLAS ESTRICTAS:\n"
        "1. Responde ÚNICAMENTE basándote en la información de los productos listados abajo.\n"
        "2. Si la respuesta no se encuentra explícitamente en los datos provistos, debes responder exactamente: "
        "'Lo siento, no dispongo de información sobre ese producto o característica en nuestra base de datos actual.'\n"
        "3. No inventes precios, especificaciones técnicas, nombres de software ni características que no estén escritas en el contexto.\n"
        "4. Mantén un tono profesional, técnico y orientado a negocios y tecnología cloud."
    )

    # 3. Construir el payload para la API de Ollama (usando un modelo local como llama3, mistral o qwen)
    url = "http://localhost:11434/api/chat"
    
    payload = {
        "model": "llama3",  # O el modelo que tengas descargado en tu Ollama local (ej: mistral, phi3)
        "messages": [
            {"role": "system", "content": f"{system_prompt}\n\n{contexto_productos}"},
            {"role": "user", "content": pregunta_usuario}
        ],
        "stream": False,
        "options": {
            "temperature": 0.1  # Temperatura baja para evitar alucinaciones y obligarlo a ceñirse a los datos
        }
    }

    try:
        response = requests.post(url, data=json.dumps(payload), headers={"Content-Type": "application/json"}, timeout=30)
        if response.status_code == 200:
            resultado = response.json()
            return resultado.get("message", {}).get("content", "No se pudo procesar la respuesta.")
        else:
            return f"Error al conectar con el servidor de Ollama (Código {response.status_code})."
    except requests.exceptions.RequestException as e:
        return f"Error de conexión con Ollama: Asegúrate de que el servicio esté corriendo localmente. Detalle: {e}"