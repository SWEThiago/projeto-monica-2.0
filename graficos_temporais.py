from flask import Blueprint, jsonify, request
from dados import carregar_dados, obter_leads_por_periodo
from datetime import datetime, timedelta

# Criar o blueprint para os gráficos temporais
grafico_temporal_bp = Blueprint('grafico_temporal', __name__)

# Função para calcular os dados de variação temporal de leads
def calcular_variacao_temporal(leads, inicio, fim):
    variacao_temporal = []
    
    if not leads:
        return variacao_temporal

    mes_inicio = inicio.replace(day=1)

    while mes_inicio < fim:
        proximo_mes = (mes_inicio.replace(day=28) + timedelta(days=4)).replace(day=1)
        leads_mes = [lead for lead in leads if mes_inicio <= datetime.strptime(lead.get('data_lead'), '%Y-%m-%d') < proximo_mes]
        total_mes = len(leads_mes)
        convertidos_mes = sum(1 for lead in leads_mes if lead.get('status') == 'Convertido')
        abertos_mes = sum(1 for lead in leads_mes if lead.get('status') == 'Aberto')
        perdidos_mes = sum(1 for lead in leads_mes if lead.get('status') == 'Perdido')

        variacao_temporal.append({
            'periodo': mes_inicio.strftime('%Y-%m'),
            'convertidos': convertidos_mes,
            'abertos': abertos_mes,
            'perdidos': perdidos_mes,
            'total_leads': total_mes
        })
        mes_inicio = proximo_mes

    return variacao_temporal

# Rota para obter os dados de variação temporal
@grafico_temporal_bp.route('/grafico_temporal/filtrar', methods=['POST'])
def filtrar_graficos_temporais():
    try:
        vendedores_selecionados = request.json.get('vendedores', [])
        inicio_str = request.json.get('inicio')
        fim_str = request.json.get('fim')

        if not vendedores_selecionados:
            return jsonify({"error": "Nenhum vendedor selecionado"}), 400

        inicio = datetime.strptime(inicio_str, '%Y-%m-%d') if inicio_str else None
        fim = datetime.strptime(fim_str, '%Y-%m-%d') if fim_str else None

        dados = carregar_dados()
        all_leads = []

        for vendedor_id in vendedores_selecionados:
            leads = obter_leads_por_periodo([vendedor_id], inicio_str, fim_str)
            if leads:
                all_leads.extend(leads)

        variacao_temporal = calcular_variacao_temporal(all_leads, inicio, fim)

        return jsonify({
            'variacao_temporal': variacao_temporal
        })

    except Exception as e:
        return jsonify({"error": f"Erro ao gerar os gráficos temporais: {str(e)}"}), 500
