#se registran las opciones del menu admin
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from.models import PlantillaCarnet, ElementoPlantilla

# Opción 1: Simple
"""
admin.site.register(PlantillaCarnet)
admin.site.register(ElementoPlantilla)

# Opción 2: Con más opciones, recomendado
@admin.register(PlantillaCarnet)
class PlantillaCarnetAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'empresa', 'orientacion']
    list_filter = ['orientacion', 'empresa']
    search_fields = ['nombre', 'empresa']

@admin.register(ElementoPlantilla)
class ElementoPlantillaAdmin(admin.ModelAdmin):
    list_display = ['id', 'plantilla', 'tipo', 'texto_fijo', 'x', 'y']
    list_filter = ['plantilla', 'tipo']

"""

class ElementoPlantillaInline(admin.TabularInline):
    model = ElementoPlantilla
    extra = 0
    fields = ['tipo', 'texto_fijo', 'x', 'y', 'width', 'height', 'font_size','color']

@admin.register(PlantillaCarnet)
class PlantillaCarnetAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'empresa', 'orientacion', 'descargar_pdf']

    inlines = [ElementoPlantillaInline]

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['editor_url'] = f"/plantilla/{object_id}/editar/"
        return super().change_view(request, object_id, form_url, extra_context=extra_context)
    
    def descargar_pdf(self, obj):
        url = reverse('generar_pdf', args=[obj.id])
        return format_html('<a class="button" href="{}" target="_blank">PDF</a>', url)
    descargar_pdf.short_description = "Vista Previa"

@admin.register(ElementoPlantilla)
class ElementoPlantillaAdmin(admin.ModelAdmin):
    list_display = ['id', 'plantilla', 'tipo', 'texto_fijo', 'x', 'y']
