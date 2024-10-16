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
            'variacao_temporal': [],
            'ranking_vendedores': [],
            'leads_por_veiculo': {},
            'comparativo_vendas': []
        }

        dados = carregar_dados()  # Carregar dados uma vez para evitar carregar repetidamente

        for vendedor_id in vendedores_selecionados:
            vendedor = obter_vendedor(dados, vendedor_id)  # Pegar o nome do vendedor
            if not vendedor:
                print(f"Vendedor com ID {vendedor_id} não encontrado")  # Log de depuração
                continue  # Se o vendedor não for encontrado, pula

            nome_vendedor = vendedor['nome'] if vendedor else 'Desconhecido'

            leads = obter_leads_por_periodo([vendedor_id], inicio_str, fim_str)
            if leads is None:
                leads = []  # Prevenir erros caso não haja leads

            # Log para verificar os leads retornados para cada vendedor
            print(f"Leads para o vendedor {nome_vendedor} (ID {vendedor_id}): {leads}")

            # Filtrar leads com status não nulo
            leads_validos = [lead for lead in leads if lead.get('status')]

            abertos, convertidos, perdidos = calcular_metricas_por_vendedor(leads_validos)

            # Atualizar as métricas dos gráficos
            dados_graficos['total_leads'] += len(leads_validos)
            dados_graficos['leads_abertos'] += abertos
            dados_graficos['leads_convertidos'] += convertidos
            dados_graficos['leads_perdidos'] += perdidos

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
                dados_graficos['variacao_temporal'].append({
                    'vendedor': nome_vendedor,
                    'data': lead['data_lead'],
                    'status': lead['status']
                })

            # Adicionar dados para o comparativo de vendas entre vendedores
            dados_graficos['comparativo_vendas'].append({
                'vendedor': nome_vendedor,
                'convertidos': convertidos
            })

        # Log para verificar os dados finais gerados para os gráficos
        print(f"Dados gerados para gráficos: {dados_graficos}")
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

        # Logs para verificar os dados recebidos
        print("Vendedores selecionados:", vendedores_selecionados)
        print("Período de início:", inicio_str)
        print("Período de fim:", fim_str)

        if not vendedores_selecionados:
            return jsonify({"error": "Nenhum vendedor selecionado"}), 400

        dados_graficos = gerar_dados_graficos(vendedores_selecionados, inicio_str, fim_str)

        if dados_graficos is None:
            return jsonify({"error": "Erro ao gerar os dados dos gráficos"}), 500

        # Log para verificar os dados gerados para os gráficos
        print("Dados gerados para os gráficos:", dados_graficos)

        return jsonify(dados_graficos)

    except Exception as e:
        print(f"Erro no endpoint '/grafico/filtrar': {str(e)}")
        return jsonify({"error": "Erro interno no servidor"}), 500

# Rota para obter todos os vendedores para os gráficos de seleção
@grafico_bp.route('/grafico/vendedores', methods=['GET'])
def obter_vendedores_grafico():
    try:
        vendedores = obter_todos_vendedores()
        return jsonify(vendedores)
    except Exception as e:
        print(f"Erro ao obter vendedores: {str(e)}")
        return jsonify({"error": "Erro ao obter vendedores"}), 500
