from graphviz import Digraph

dot = Digraph(comment='Diagrama ER - MEDDES con Automatización', format='png')
dot.attr(rankdir='LR', size='10')

entidades = {
    "User": "User\n(Django Auth)",
    "Profile": "Profile\n(Paciente)",
    "Perfil_Terapeuta": "Perfil_Terapeuta",
    "Prospecion_Administrativa": "Prospeción\nAdministrativa",
    "Pagos": "Pagos",
    "Tareas": "Tareas\nTerapéuticas",
    "Mensaje": "Mensajes\nInternos",
    "Cita": "Citas\nMédicas",
    "Dashboard": "Dashboard\nInformativo",
    "WebInterface": "🌐 Interfaz Web\n(Gestión de usuarios, citas, mensajes, tareas)",
    "EmailService": "📧 Servicio de Email\n(Notificaciones Automáticas)",
    "WhatsAppAPI": "📱 WhatsApp API\n(Mensajería Automatizada)",
}

for key, label in entidades.items():
    dot.node(key, label, shape='box', style='filled', color='lightblue')

relaciones = [
    ("User", "Profile"),
    ("User", "Perfil_Terapeuta"),
    ("User", "Prospecion_Administrativa"),
    ("User", "Pagos"),
    ("User", "Tareas"),
    ("User", "Mensaje"),
    ("Profile", "Tareas"),
    ("Profile", "Pagos"),
    ("Profile", "Cita"),
    ("Perfil_Terapeuta", "Profile"),
    ("Perfil_Terapeuta", "Tareas"),
    ("Mensaje", "User"),
    ("Cita", "User"),
    ("Dashboard", "WebInterface"),
    ("WebInterface", "User"),
    ("WebInterface", "Mensaje"),
    ("WebInterface", "Cita"),
    ("WebInterface", "Tareas"),
    ("WebInterface", "Pagos"),
    ("WebInterface", "Profile"),
    ("EmailService", "Mensaje"),
    ("EmailService", "Cita"),
    ("WhatsAppAPI", "Cita"),
    ("WhatsAppAPI", "Mensaje"),
]

for origen, destino in relaciones:
    dot.edge(origen, destino)

dot.render('diagrama_erp_meddes_completo', cleanup=False)
