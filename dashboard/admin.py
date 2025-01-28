from django.contrib import admin
from .models import Medicao

@admin.register(Medicao)
class MedicaoAdmin(admin.ModelAdmin):
    list_display = ('agente', 'ponto_grupo', 'data', 'hora', 'ativa_c')
    list_filter = ('qualidade', 'origem')
    search_fields = ('agente', 'ponto_grupo')
