from django.contrib import admin

from .models import Usuario, Paises, EstadoFuerza, Frases, Municipios, PuntosInternacion, RescatePunto, ConteoRapidoPunto

admin.site.register(Usuario)
admin.site.register(Paises)
admin.site.register(EstadoFuerza)
admin.site.register(Frases)
admin.site.register(Municipios)
admin.site.register(PuntosInternacion)
admin.site.register(RescatePunto)
admin.site.register(ConteoRapidoPunto)
