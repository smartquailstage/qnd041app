from django.contrib import admin
from citas_regulares import models
from unfold.admin import ModelAdmin
from django.utils.html import format_html
from django.urls import reverse, path
from django.utils.safestring import mark_safe
from django.shortcuts import render
from datetime import datetime
import calendar

# Vista personalizada en el admin con Unfold + Calendario
@admin.register(models.Event)
class EventAdmin(ModelAdmin):
    model = models.Event
    change_list_template = "admin/events_calendar.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('calendar/', self.admin_site.admin_view(self.calendar_view), name='events_calendar'),
        ]
        return custom_urls + urls

    def calendar_view(self, request):
        current_month = datetime.now().month
        current_year = datetime.now().year
        events = self.model.objects.filter(
            start_time__month=current_month,
            start_time__year=current_year
        )

        event_data = [
            {
                "title": event.title,
                "start": event.start_time.strftime('%Y-%m-%dT%H:%M:%S'),
                "end": event.end_time.strftime('%Y-%m-%dT%H:%M:%S'),
                "description": event.description,
            }
            for event in events
        ]

        context = {
            'title': 'Calendario de Eventos',
            'calendar': mark_safe(self.generate_calendar(current_month, current_year)),
            'events': event_data,
        }
        return render(request, 'admin/events_calendar.html', context)

    def generate_calendar(self, month, year):
        cal = calendar.Calendar(firstweekday=6)
        month_days = cal.monthdayscalendar(year, month)
        html = '<table class="calendar"><thead><tr>'
        for day_name in ['Dom', 'Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb']:
            html += f'<th>{day_name}</th>'
        html += '</tr></thead><tbody>'
        for week in month_days:
            html += '<tr>'
            for day in week:
                if day == 0:
                    html += '<td class="empty"></td>'
                else:
                    html += f'<td>{day}</td>'
            html += '</tr>'
        html += '</tbody></table>'
        return html

    def ver_en_calendario(self, obj):
        url = reverse("admin:events_calendar")
        return format_html('<a href="{}?fecha={}">📅 Ver</a>', url, obj.created_at.date().isoformat())
    ver_en_calendario.short_description = "Calendario"

    def colored_is_active(self, obj):
        return format_html(
            '<span style="color: green;">Activo</span>' if obj.is_active else '<span style="color: gray;">Inactivo</span>'
        )
    colored_is_active.short_description = "Activo"

    def colored_is_deleted(self, obj):
        return format_html(
            '<span style="color: red;">Eliminado</span>' if obj.is_deleted else '<span style="color: gray;">Disponible</span>'
        )
    colored_is_deleted.short_description = "Eliminado"

    list_display = (
        "id",
        "title",
        "user",
        "colored_is_active",
        "colored_is_deleted",
        "created_at",
        "updated_at",
        "ver_en_calendario",
    )

    list_filter = ["is_active", "is_deleted", "created_at"]
    search_fields = ["title"]
    readonly_fields = ("created_at", "updated_at")

    # Configuración Unfold
    compressed_fields = True
    warn_unsaved_form = True
    list_filter_submit = False
    list_fullwidth = False
    list_filter_sheet = True
    list_horizontal_scrollbar_top = False
    list_disable_select_all = False


@admin.register(models.EventMember)
class EventMemberAdmin(ModelAdmin):
    model = models.EventMember
    list_display = ["id", "event", "user", "created_at", "updated_at"]
    list_filter = ["event"]
