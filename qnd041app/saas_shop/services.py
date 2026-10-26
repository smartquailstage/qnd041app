import json
import requests
from .models import Product

def consultar_ollama_productos(pregunta_usuario, producto_id=None):
    """
    Extrae la información únicamente del producto seleccionado (o un subconjunto seguro)
    e inyecta un prompt estricto para que Ollama responda sin desbordar el contexto ni generar timeouts.
    """
    # 1. Filtrar estrictamente por el producto seleccionado si viene en la petición,
    # o limitar a un grupo seguro para evitar saturar el prompt si no hay ID.
    if producto_id:
        productos = Product.objects.select_related('category').filter(pk=producto_id, available=True)
    else:
        # Fallback seguro: tomar solo los primeros o dejar vacío si se requiere selección explícita
        productos = Product.objects.select_related('category').filter(available=True)[:5]

    if not productos.exists():
        return "Lo siento, no se encontró el producto o servicio especificado en la base de datos."

    contexto_productos = "INFORMACIÓN DEL PRODUCTO / SERVICIO TECNOLÓGICO (SmartQuail):\n"
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

    # 2. Definir el System Prompt estricto
    system_prompt = (
        "Eres un asistente de IA corporativo y estricto para SmartQuail, Inc. "
        "Tu única fuente de verdad es la 'INFORMACIÓN DEL PRODUCTO' provista a continuación. "
        "REGLAS ESTRICTAS:\n"
        "1. Responde ÚNICAMENTE basándote en la información del producto listado abajo.\n"
        "2. Si la respuesta no se encuentra explícitamente en los datos provistos, debes responder exactamente: "
        "'Lo siento, no dispongo de información sobre esa característica específica en este producto.'\n"
        "3. No inventes precios, especificaciones técnicas ni características que no estén escritas en el contexto.\n"
        "4. Mantén un tono profesional, técnico y orientado a negocios y tecnología cloud."
    )

    # 3. Construir el payload hacia el servicio interno en Kubernetes
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
                "num_ctx": 2048  # 👈 Limita estrictamente la ventana de contexto a 2048 tokens
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
        print(f"DEBUG EXCEPTION OLLAMA: {e}")
        return f"Error de conexión con Ollama en el clúster: Detalle: {e}"