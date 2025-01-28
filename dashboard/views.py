from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Sum
import urllib.parse
from .models import Medicao  # Importar o modelo Medicao
from datetime import datetime

def listar_medicoes(request):
    # Obter parâmetros de filtro do GET
    agente = request.GET.get('agente', '').strip()
    ponto_grupo = request.GET.get('ponto_grupo', '').strip()
    data = request.GET.get('data', '').strip()

    # Decodificar `ponto_grupo` para lidar com caracteres especiais
    ponto_grupo = urllib.parse.unquote(ponto_grupo)

    # Validar data
    try:
        if data:
            datetime.strptime(data, '%Y-%m-%d')  # Garantir que o formato é YYYY-MM-DD
    except ValueError:
        data = ''  # Ignorar filtro de data inválido

    # Query inicial
    medicoes_list = Medicao.objects.all()

    # Aplicar filtros
    if agente:
        medicoes_list = medicoes_list.filter(agente=agente)
    if ponto_grupo:
        medicoes_list = medicoes_list.filter(ponto_grupo=ponto_grupo)
    if data:
        medicoes_list = medicoes_list.filter(data=data)

    print(f"Agente: {agente}, Ponto Grupo: {ponto_grupo}, Data: {data}")
    print(f"Registros encontrados: {medicoes_list.count()}")

    # Dados do gráfico
    horas = [
        hora.strftime('%H:%M') if hora else "Desconhecido"  # Formatar para 'HH:MM'
        for hora in medicoes_list.values_list('hora', flat=True).distinct()
    ]
    ativa_c_data = [
        medicoes_list.filter(hora=hora).aggregate(Sum('ativa_c'))['ativa_c__sum'] or 0
        for hora in medicoes_list.values_list('hora', flat=True).distinct()
    ]

    # Garantir que `horas` e `ativa_c_data` sejam listas válidas
    horas = horas or []
    ativa_c_data = ativa_c_data or []
    
    # Paginação
    paginator = Paginator(medicoes_list, 100)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'dashboard/medicoes_dashboard.html', {
        'page_obj': page_obj,
        'agentes': Medicao.objects.values_list('agente', flat=True).distinct(),
        'pontos_grupo': Medicao.objects.values_list('ponto_grupo', flat=True).distinct(),
        'horas': horas or [],
        'ativa_c_data': ativa_c_data or [],
        'request': request,
    })
def home(request):
    return render(request, 'dashboard/home.html')