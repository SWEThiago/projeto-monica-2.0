from flask import Blueprint, jsonify, request
from dados import carregar_dados, obter_todos_vendedores, obter_leads_por_periodo, obter_vendedor
from datetime import datetime

grafico_bp = Blueprint('grafico', __name__)

# Função para calcular métricas de leads por vendedor
def calcular_metricas_por_vendedor(leads):
    total_leads = len(leads)
    abertos = sum(1 for lead in leads if lead.get('status') == 'Aberto')
    convertidos = sum(1 for lead in leads if lead.get('status') == 'Convertido')
    perdidos = sum(1 for lead in leads if lead.get('status') == 'Perdido')
    return abertos, convertidos, perdidos

# Função para gerar dados para os gráficos com base nos vendedores e no período filtrado
def gerar_dados_graficos(vendedores_selecionados, inicio_str, fim_str):
    try:
        # Converter as strings de data para objetos datetime (se existirem)
        inicio = datetime.strptime(inicio_str, '%Y-%m-%d') if inicio_str else None
        fim = datetime.strptime(fim_str, '%Y-%m-%d') if fim_str else None
        
        # Inicializar os dados dos gráficos
        dados_graficos = {
            'total_leads': 0,
            'leads_abertos': 0,
            'leads_convertidos': 0,
            'leads_perdidos': 0,
            'variacao_temporal': [],  # Adicionar campo para variação temporal
            'ranking_vendedores': [],
            'leads_por_veiculo': {},
            'comparativo_vendas': [],
            'total_leads_vendedores': [],  # Para gráfico de taxa de conversão
            'percentual_conversao_vendedores': [],  # Para gráfico de taxa de conversão
            'percentual_abertos_vendedores': [],  # Para gráfico de leads abertos
            'percentual_perdidos_vendedores': [],  # Para gráfico de leads perdidos
            'vendedores': [],  # Nome dos vendedores
        }

        dados = carregar_dados()  # Carregar dados uma vez para evitar carregar repetidamente

        for vendedor_id in vendedores_selecionados:
            vendedor = obter_vendedor(dados, vendedor_id)  # Pegar o nome do vendedor
            if not vendedor:
                continue  # Se o vendedor não for encontrado, pula

            nome_vendedor = vendedor['nome'] if vendedor else 'Desconhecido'
            dados_graficos['vendedores'].append(nome_vendedor)

            leads = obter_leads_por_periodo([vendedor_id], inicio_str, fim_str)
            if leads is None:
                leads = []  # Prevenir erros caso não haja leads

            # Filtrar leads com status não nulo
            leads_validos = [lead for lead in leads if lead.get('status')]

            abertos, convertidos, perdidos = calcular_metricas_por_vendedor(leads_validos)

            # Atualizar as métricas dos gráficos
            dados_graficos['total_leads'] += len(leads_validos)
            dados_graficos['leads_abertos'] += abertos
            dados_graficos['leads_convertidos'] += convertidos
            dados_graficos['leads_perdidos'] += perdidos

            # Adicionar para taxa de conversão
            total_leads = len(leads_validos)
            dados_graficos['total_leads_vendedores'].append(total_leads)
            percentual_conversao = (convertidos / total_leads) * 100 if total_leads > 0 else 0
            percentual_abertos = (abertos / total_leads) * 100 if total_leads > 0 else 0
            percentual_perdidos = (perdidos / total_leads) * 100 if total_leads > 0 else 0

            # Preencher os percentuais
            dados_graficos['percentual_conversao_vendedores'].append(percentual_conversao)
            dados_graficos['percentual_abertos_vendedores'].append(percentual_abertos)
            dados_graficos['percentual_perdidos_vendedores'].append(percentual_perdidos)

            # Leads por veículo
            for lead in leads_validos:
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

            # Adicionar dados para variação temporal
            for lead in leads_validos:
                abertos, convertidos, perdidos = calcular_metricas_por_vendedor([lead])
                total_leads = 1  # Um único lead
                percentual_conversao = (convertidos / total_leads) * 100 if total_leads > 0 else 0
                percentual_abertos = (abertos / total_leads) * 100 if total_leads > 0 else 0
                percentual_perdidos = (perdidos / total_leads) * 100 if total_leads > 0 else 0

                dados_graficos['variacao_temporal'].append({
                    'vendedor': nome_vendedor,
                    'data': lead['data_lead'],
                    'conversao': percentual_conversao,
                    'abertos': percentual_abertos,
                    'perdidos': percentual_perdidos
                })

            # Adicionar dados para o comparativo de vendas entre vendedores
            dados_graficos['comparativo_vendas'].append({
                'vendedor': nome_vendedor,
                'convertidos': convertidos
            })

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
