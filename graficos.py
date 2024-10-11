from flask import Blueprint, jsonify, request
from dados import obter_todos_vendedores, obter_leads_por_periodo

grafico_bp = Blueprint('grafico', __name__)

# Função para calcular métricas de leads por vendedor
def calcular_metricas_por_vendedor(leads):
    total_leads = len(leads)
    abertos = sum(1 for lead in leads if lead['status'] == 'Aberto')
    convertidos = sum(1 for lead in leads if lead['status'] == 'Convertido')
    perdidos = sum(1 for lead in leads if lead['status'] == 'Perdido')
    return abertos, convertidos, perdidos

# Função para gerar dados para os gráficos com base nos vendedores e no período filtrado
def gerar_dados_graficos(vendedores_selecionados, inicio, fim):
    dados_graficos = {
        'total_leads': 0,
        'leads_abertos': 0,
        'leads_convertidos': 0,
        'leads_perdidos': 0
    }

    for vendedor_id in vendedores_selecionados:
        leads = obter_leads_por_periodo(vendedor_id, inicio, fim)
        abertos, convertidos, perdidos = calcular_metricas_por_vendedor(leads)

        # Atualizar as métricas dos gráficos
        dados_graficos['total_leads'] += len(leads)
        dados_graficos['leads_abertos'] += abertos
        dados_graficos['leads_convertidos'] += convertidos
        dados_graficos['leads_perdidos'] += perdidos

    return dados_graficos

# Rota para obter dados de leads filtrados por período e vendedor para exibir nos gráficos
@grafico_bp.route('/grafico/filtrar', methods=['POST'])
def filtrar_graficos():
    vendedores_selecionados = request.json.get('vendedores', [])
    inicio_str = request.json.get('inicio')
    fim_str = request.json.get('fim')
    
    # Filtra os leads de acordo com o período e os vendedores selecionados
    dados_graficos = gerar_dados_graficos(vendedores_selecionados, inicio_str, fim_str)
    
    return jsonify(dados_graficos)

# Rota para obter todos os vendedores para os gráficos de seleção
@grafico_bp.route('/grafico/vendedores', methods=['GET'])
def obter_vendedores_grafico():
    vendedores = obter_todos_vendedores()
    return jsonify(vendedores)
