import json
import requests
from .models import Product

def consultar_ollama_productos(pregunta_usuario, producto_id=None):
    """
    Extrae la información completa del producto seleccionado de forma estructurada
    para garantizar que el LLM responda exclusivamente sobre sus características.
    """
    try:
        if producto_id:
            productos = Product.objects.select_related('category').filter(pk=producto_id, available=True)
        else:
            productos = Product.objects.select_related('category').filter(available=True)[:1]

        if not productos.exists():
            return "Lo siento, no se encontró el producto o servicio especificado en la base de datos."

        contexto_productos = "=== FICHA TÉCNICA OFICIAL DEL PRODUCTO (SmartQuail) ===\n"
        for p in productos:
            categoria = p.category.name if p.category else "Sin categoría"
            
            contexto_productos += f"- Nombre del Producto / Servicio: {p.name}\n"
            contexto_productos += f"- Categoría: {categoria}\n"
            
            if getattr(p, 'cloud_type', None):
                contexto_productos += f"- Tipo de Nube: {p.cloud_type}\n"
            if getattr(p, 'os', None):
                contexto_productos += f"- Sistema Operativo (OS): {p.os}\n"
            
            cpu = getattr(p, 'vCPU', getattr(p, 'cpu', None))
            if cpu is not None:
                contexto_productos += f"- Procesamiento CPU: {cpu} vCPUs\n"
                
            if getattr(p, 'memoria', None) is not None:
                contexto_productos += f"- Memoria RAM: {p.memoria} GB\n"
                
            if getattr(p, 'almacenamiento', None) is not None:
                contexto_productos += f"- Almacenamiento SSD/NVMe: {p.almacenamiento} GB\n"
                
            if getattr(p, 'price_amount', None) is not None:
                contexto_productos += f"- Inversión / Precio: ${p.price_amount} USD\n"
            elif getattr(p, 'price', None) is not None:
                contexto_productos += f"- Inversión / Precio: {p.price}\n"
                
            software = p.get_software_display() if hasattr(p, 'get_software_display') else getattr(p, 'software', None)
            if software:
                contexto_productos += f"- Arquitectura Software: {software}\n"
                
            if getattr(p, 'latencia_aproximada', None):
                contexto_productos += f"- Latencia estimada: {p.latencia_aproximada}\n"
                
            concurrencia = p.get_usuarios_simultaneos_display() if hasattr(p, 'get_usuarios_simultaneos_display') else getattr(p, 'usuarios_simultaneos', None)
            if concurrencia:
                contexto_productos += f"- Capacidad concurrente: {concurrencia} usuarios\n"
                
            if getattr(p, 'automatizacion', None):
                contexto_productos += f"- Automatización integrada: {p.automatizacion}\n"
            if getattr(p, 'inteligencia_artificial', None):
                contexto_productos += f"- Inteligencia Artificial / Agéntico: {p.inteligencia_artificial}\n"
                
            if p.description:
                contexto_productos += f"- Descripción detallada y módulos: {p.description}\n"

        system_prompt = (
            "Eres un asistente de IA corporativo y estrictamente técnico desarrollado por SmartQuail, Inc. "
            "Tu única función es informar al usuario sobre las características, especificaciones técnicas, módulos, "
            "costos y capacidades del producto listado en la 'FICHA TÉCNICA OFICIAL'.\n\n"
            "REGLAS ABSOLUTAS E INQUEBRANTABLES:\n"
            "1. Responde ÚNICAMENTE basándote en los datos de la ficha técnica provistos arriba.\n"
            "2. Está estrictamente prohibido responder sobre temas generales, programación, chistes, opinión personal, "
            "saludos fuera del contexto comercial, o cualquier característica que no esté explícitamente escrita en los datos.\n"
            "3. Si el usuario pregunta algo que no figure en los datos o se sale de las características del producto, "
            "responde exactamente y sin agregar nada más con la siguiente frase:\n"
            "'Para consultas técnicas avanzadas o cuestiones fuera de esta ficha técnica, por favor comuníquese con nuestro equipo de atención al cliente.'\n"
            "4. No inventes precios, capacidades de RAM, CPU ni tecnologías que no aparezcan en el contexto.\n"
            "5. Mantén un tono profesional, ejecutivo, directo y orientado a soluciones cloud."
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
                "temperature": 0.0,  # Cero creatividad para evitar alucinaciones y forzar apego al contexto
                "num_ctx": 2048
            }
        }

        response = requests.post(url, data=json.dumps(payload), headers={"Content-Type": "application/json"}, timeout=90)
        
        if response.status_code == 200:
            resultado = response.json()
            return resultado.get("message", {}).get("content", "Por seguridad no pudo procesar la respuesta.")
        else:
            return f"Error al conectar con el servidor de Ollama (Código {response.status_code})."
            
    except requests.exceptions.RequestException as e:
        return f"Error de conexión con Ollama en el clúster: Detalle: {e}"
    except Exception as e:
        return f"Error interno en el servicio de IA: {str(e)}"