from django.contrib import admin

from .models import Usuario, Paises, EstadoFuerza, Frases, Municipios, PuntosInternacion, RescatePunto, ConteoRapidoPunto, MsgUpdate

class RescateAdmin(admin.ModelAdmin):
    list_display = ['idRescate', 'oficinaRepre', 'puntoEstra']
    list_editable = ['puntoEstra']
    list_filter = ['oficinaRepre', 'puntoEstra']
    search_fields = ['oficinaRepre', 'puntoEstra']

class EstadoAdmin(admin.ModelAdmin):
    list_display = ['idEdoFuerza', 'oficinaR', 'nomPuntoRevision', 'tipoP']
    list_filter = ['oficinaR', 'tipoP']
    search_fields = ['oficinaR', 'nomPuntoRevision']

class InternacionAdmin(admin.ModelAdmin):
    list_display = ['idPuntoInter', 'estadoPunto', 'nombrePunto', 'tipoPunto']
    list_filter = ['estadoPunto', 'tipoPunto']
    search_fields = ['nombrePunto']

admin.site.register(Usuario)
admin.site.register(Paises)
admin.site.register(EstadoFuerza)
admin.site.register(Frases)
admin.site.register(Municipios)
admin.site.register(PuntosInternacion)
admin.site.register(RescatePunto)
admin.site.register(ConteoRapidoPunto)
admin.site.register(MsgUpdate)
