import json
import urllib.error
import urllib.request
from django.conf import settings
from .models import AIAgent


class AgentExecutionError(Exception):
    pass


# Registro explícito de funciones Python permitidas (o puente hacia tu cliente MCP)
TOOL_REGISTRY = {
    # "buscar_huecos_agenda": buscar_huecos_agenda_fn,
}


def _llamar_ollama_chat(model: str, messages: list[dict], tools: list[dict] | None = None, temperature: float = 0.2) -> dict:
    base_url = getattr(settings, "OLLAMA_BASE_URL", "http://127.0.0.1:11434").rstrip("/")
    timeout = int(getattr(settings, "OLLAMA_TIMEOUT", 90))

    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
        "options": {"temperature": temperature},
    }
    if tools:
        payload["tools"] = tools

    req = urllib.request.Request(
        f"{base_url}/api/chat",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise AgentExecutionError(f"Fallo al conectar con Ollama local: {exc}") from exc


def ejecutar_agente(agent_slug: str, mensaje_usuario: str, historial: list[dict] | None = None, tools_schema: list[dict] | None = None) -> str:
    agente = (
        AIAgent.objects.select_related("soul")
        .prefetch_related("skills")
        .get(slug=agent_slug, activo=True)
    )

    skills_activas = list(agente.skills.filter(activa=True))
    herramientas_autorizadas = {
        tool_name
        for skill in skills_activas
        for tool_name in (skill.herramientas_permitidas or [])
    }

    system_prompt = agente.compilar_system_prompt(skills_filtradas=skills_activas)
    messages = [{"role": "system", "content": system_prompt}]
    if historial:
        messages.extend(historial)
    messages.append({"role": "user", "content": mensaje_usuario})

    # Bucle acotado (máx. 4 pasos) para evitar ciclos infinitos con modelos locales pequeños
    for _ in range(4):
        respuesta_raw = _llamar_ollama_chat(
            model=agente.modelo_ollama,
            messages=messages,
            tools=tools_schema if herramientas_autorizadas else None,
            temperature=agente.temperatura,
        )
        msg = respuesta_raw.get("message", {})
        tool_calls = msg.get("tool_calls") or []

        if not tool_calls:
            return msg.get("content", "").strip()

        messages.append(msg)
        for call in tool_calls:
            fn_info = call.get("function", {})
            nombre_tool = fn_info.get("name", "")
            argumentos = fn_info.get("arguments") or {}

            if nombre_tool not in herramientas_autorizadas or nombre_tool not in TOOL_REGISTRY:
                resultado = {"error": f"Herramienta '{nombre_tool}' no autorizada para este agente."}
            else:
                resultado = TOOL_REGISTRY[nombre_tool](**argumentos)

            messages.append({
                "role": "tool",
                "content": json.dumps(resultado, ensure_ascii=False),
            })

    raise AgentExecutionError("El agente alcanzó el límite máximo de iteraciones sin respuesta final.")