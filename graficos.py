from flask import Blueprint, jsonify, request
from dados import carregar_dados, obter_todos_vendedores, obter_leads_por_periodo, obter_vendedor
from datetime import datetime, timedelta

grafico_bp = Blueprint('grafico', __name__)

# Função para calcular métricas de leads por vendedor
def calcular_metricas_por_vendedor(leads):
    total_leads = len(leads)
    abertos = sum(1 for lead in leads if lead.get('status') == 'Aberto')
    convertidos = sum(1 for lead in leads if lead.get('status') == 'Convertido')
    perdidos = sum(1 for lead in leads if lead.get('status') == 'Perdido')
    return abertos, convertidos, perdidos

# Função para calcular o comparativo de vendas com leads convertidos ao longo do tempo
def calcular_comparativo_vendas(leads, inicio, fim):
    comparativo_vendas = []
    
    if not leads:
        return comparativo_vendas  # Retorna vazio se não houver leads

    delta = fim - inicio
    total_leads = len(leads)

    # Processar mensalmente para intervalo maior que 2 meses
    mes_inicio = inicio.replace(day=1)

    # Variável para capturar o primeiro mês como referência
    leads_primeiro_mes = 0

    while mes_inicio < fim:
        proximo_mes = (mes_inicio.replace(day=28) + timedelta(days=4)).replace(day=1)
        leads_mes = [lead for lead in leads if mes_inicio <= datetime.strptime(lead.get('data_lead'), '%Y-%m-%d') < proximo_mes]
        total_mes = len(leads_mes)
        convertidos_mes = sum(1 for lead in leads_mes if lead.get('status') == 'Convertido')

        # Definir o primeiro mês como referência
        if not leads_primeiro_mes and total_mes > 0:
            leads_primeiro_mes = convertidos_mes

        # Calcular a variação percentual com base no primeiro mês
        percentual_variacao = ((convertidos_mes - leads_primeiro_mes) / leads_primeiro_mes) * 100 if leads_primeiro_mes > 0 else 0

        comparativo_vendas.append({
            'periodo': mes_inicio.strftime('%Y-%m'),
            'leads_convertidos': convertidos_mes,
            'total_leads': total_mes,
            'percentual_conversao': percentual_variacao
        })
        mes_inicio = proximo_mes

    return comparativo_vendas

# Função para gerar dados para os gráficos com base nos vendedores e no período filtrado
def gerar_dados_graficos(vendedores_selecionados, inicio_str=None, fim_str=None):
    try:
        # Se não houver datas, pegar todos os leads
        if not inicio_str or not fim_str:
            inicio = None
            fim = None
        else:
            inicio = datetime.strptime(inicio_str, '%Y-%m-%d') if inicio_str else None
            fim = datetime.strptime(fim_str, '%Y-%m-%d') if fim_str else None
        
        # Inicializar os dados dos gráficos
        dados_graficos = {
            'total_leads': 0,
            'leads_abertos': 0,
            'leads_convertidos': 0,
            'leads_perdidos': 0,
            'variacao_temporal': [],
            'ranking_vendedores': [],
            'leads_por_veiculo': {},
            'comparativo_vendas': [],
            'total_leads_vendedores': [],
            'percentual_conversao_vendedores': [],
            'percentual_abertos_vendedores': [],
            'percentual_perdidos_vendedores': [],
            'vendedores': []
        }

        dados = carregar_dados()

        all_leads = []

        for vendedor_id in vendedores_selecionados:
            vendedor = obter_vendedor(dados, vendedor_id)
            if not vendedor:
                continue

            nome_vendedor = vendedor['nome'] if vendedor else 'Desconhecido'
            dados_graficos['vendedores'].append(nome_vendedor)

            leads = obter_leads_por_periodo([vendedor_id], inicio_str, fim_str)
            if leads is None:
                leads = []

            all_leads.extend(leads)

            abertos, convertidos, perdidos = calcular_metricas_por_vendedor(leads)

            total_leads = len(leads)
            dados_graficos['total_leads_vendedores'].append(total_leads)
            percentual_conversao = (convertidos / total_leads) * 100 if total_leads > 0 else 0
            percentual_abertos = (abertos / total_leads) * 100 if total_leads > 0 else 0
            percentual_perdidos = (perdidos / total_leads) * 100 if total_leads > 0 else 0

            dados_graficos['percentual_conversao_vendedores'].append(percentual_conversao)
            dados_graficos['percentual_abertos_vendedores'].append(percentual_abertos)
            dados_graficos['percentual_perdidos_vendedores'].append(percentual_perdidos)

            # Leads por veículo
            for lead in leads:
                veiculo = lead.get('veiculo', 'Desconhecido')
                if veiculo in dados_graficos['leads_por_veiculo']:
                    dados_graficos['leads_por_veiculo'][veiculo] += 1
                else:
                    dados_graficos['leads_por_veiculo'][veiculo] = 1

            # Adicionar dados para o gráfico de ranking
            dados_graficos['ranking_vendedores'].append({
                'vendedor': nome_vendedor,
                'convertidos': convertidos
            })

        # Calcular comparativo de vendas para todos os leads agregados
        if inicio and fim:
            comparativo_vendas = calcular_comparativo_vendas(all_leads, inicio, fim)
            dados_graficos['comparativo_vendas'].extend(comparativo_vendas)

        return dados_graficos

    except Exception as e:
        print(f"Erro ao gerar os dados dos gráficos: {str(e)}")
        return None

# Rota para obter dados de leads filtrados por período e vendedor para exibir nos gráficos
@grafico_bp.route('/grafico/filtrar', methods=['POST'])
def filtrar_graficos():
    try:
        vendedores_selecionados = request.json.get('vendedores', [])
        inicio_str = request.json.get('inicio')
        fim_str = request.json.get('fim')

        if not vendedores_selecionados:
            return jsonify({"error": "Nenhum vendedor selecionado"}), 400

        dados_graficos = gerar_dados_graficos(vendedores_selecionados, inicio_str, fim_str)

        if dados_graficos is None:
            return jsonify({"error": "Erro ao gerar os dados dos gráficos"}), 500

        return jsonify(dados_graficos)

    except Exception as e:
        return jsonify({"error": "Erro interno no servidor"}), 500

# Rota para obter todos os vendedores para os gráficos de seleção
@grafico_bp.route('/grafico/vendedores', methods=['GET'])
def obter_vendedores_grafico():
    try:
        vendedores = obter_todos_vendedores()
        return jsonify(vendedores)
    except Exception as e:
        return jsonify({"error": "Erro ao obter vendedores"}), 500
