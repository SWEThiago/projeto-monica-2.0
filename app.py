from flask import Flask, render_template, request, redirect, url_for, jsonify
from settings import get_config
from dados import carregar_dados, salvar_dados
from vendedores import adicionar_vendedor, remover_vendedor, obter_vendedor_por_id
from graficos import calcular_metricas_por_vendedor, gerar_dados_graficos
from datetime import datetime

# Criação da aplicação Flask
app = Flask(__name__)

# Carregar configurações do arquivo settings.py
app.config.from_object(get_config())

# Rota inicial - Página principal
@app.route('/')
def index():
    # Carregar dados dos vendedores e leads
    dados = carregar_dados()

    # Calcular leads mensais e diários para exibir na página principal
    leads_mensais = sum(len(v['leads']) for v in dados)  # Exemplo simples de cálculo
    leads_diarios = len([lead for v in dados for lead in v['leads'] if lead['data_lead'] == datetime.now().strftime('%Y-%m-%d')])  # Leads de hoje

    return render_template('index.html', leads_mensais=leads_mensais, leads_diarios=leads_diarios, vendedores=dados)

# Rota para adicionar um vendedor
@app.route('/vendedores', methods=['GET', 'POST'])
def vendedores():
    dados = carregar_dados()

    if request.method == 'POST':
        nome_vendedor = request.form['nome_vendedor']
        adicionar_vendedor(nome_vendedor)
        return redirect(url_for('vendedores'))

    return render_template('vendedores.html', vendedores=dados)

# Rota para remover um vendedor
@app.route('/vendedores/remover/<int:vendedor_id>', methods=['POST'])
def remover_vendedor(vendedor_id):
    remover_vendedor(vendedor_id)
    return redirect(url_for('vendedores'))

# Rota para ver detalhes de um vendedor
@app.route('/vendedores/<int:vendedor_id>')
def detalhes_vendedor(vendedor_id):
    vendedor = obter_vendedor_por_id(vendedor_id)

    if not vendedor:
        return redirect(url_for('vendedores'))

    # Filtrar leads por data, se fornecido
    inicio_str = request.args.get('inicio')
    fim_str = request.args.get('fim')
    inicio = None
    fim = None

    if inicio_str and fim_str:
        inicio = datetime.strptime(inicio_str, '%Y-%m-%d')
        fim = datetime.strptime(fim_str, '%Y-%m-%d')

    # Filtrar leads para exibir
    leads_filtrados = [lead for lead in vendedor['leads'] if (not inicio or datetime.strptime(lead['data_lead'], '%Y-%m-%d') >= inicio) and (not fim or datetime.strptime(lead['data_lead'], '%Y-%m-%d') <= fim)]

    # Ordenar leads por data decrescente
    leads_filtrados.sort(key=lambda lead: datetime.strptime(lead['data_lead'], '%Y-%m-%d'), reverse=True)

    # Calcular métricas
    total_leads = len(leads_filtrados)
    quantidade_aberto, quantidade_convertido, quantidade_perdido = calcular_metricas_por_vendedor(leads_filtrados)

    return render_template('vendedor_detalhes.html', vendedor=vendedor, leads=leads_filtrados, total_leads=total_leads,
                           quantidade_aberto=quantidade_aberto, quantidade_convertido=quantidade_convertido, quantidade_perdido=quantidade_perdido,
                           inicio_str=inicio_str, fim_str=fim_str)

# Rota para adicionar leads
@app.route('/leads', methods=['GET', 'POST'])
def leads():
    dados = carregar_dados()

    if request.method == 'POST':
        vendedor_id = int(request.form['vendedor_id'])
        novo_lead = {
            'id': len(dados[vendedor_id]['leads']) + 1,  # Gerar um ID simples
            'data_lead': datetime.now().strftime('%Y-%m-%d'),
            'nome': request.form['nome'],
            'contato': request.form['contato'],
            'veiculo': request.form['veiculo'],
            'modelo': request.form['modelo'],
            'status': 'Aberto',
            'faturado': 'Nao',
            'cliente_faturado': '',
            'nota_fiscal': ''
        }
        dados[vendedor_id]['leads'].append(novo_lead)
        salvar_dados(dados)
        return redirect(url_for('leads'))

    return render_template('leads.html', vendedores=dados)

# Rota para atualizar um lead
@app.route('/vendedores/<int:vendedor_id>/atualizar_lead', methods=['POST'])
def atualizar_lead(vendedor_id):
    dados = carregar_dados()
    vendedor = obter_vendedor_por_id(vendedor_id)

    if vendedor:
        try:
            lead_id = int(request.form.get('lead_id'))
            for lead in vendedor['leads']:
                if lead['id'] == lead_id:
                    lead['status'] = request.form.get(f'status_{lead_id}')
                    lead['faturado'] = request.form.get(f'faturado_{lead_id}')
                    lead['cliente_faturado'] = request.form.get(f'cliente_faturado_{lead_id}', '') if request.form.get(f'faturado_{lead_id}') == 'Sim' else ''
                    lead['nota_fiscal'] = request.form.get(f'nota_fiscal_{lead_id}', '')
                    salvar_dados(dados)
                    return redirect(url_for('detalhes_vendedor', vendedor_id=vendedor_id))
        except (KeyError, ValueError):
            return "Erro: Lead ID não encontrado ou inválido", 400

    return "Erro: Vendedor ou Lead não encontrado", 400

# Rota para remover um lead
@app.route('/vendedores/<int:vendedor_id>/remover_lead/<int:lead_id>', methods=['POST'])
def remover_lead(vendedor_id, lead_id):
    dados = carregar_dados()
    vendedor = obter_vendedor_por_id(vendedor_id)

    if vendedor:
        vendedor['leads'] = [lead for lead in vendedor['leads'] if lead['id'] != lead_id]
        salvar_dados(dados)
        return redirect(url_for('detalhes_vendedor', vendedor_id=vendedor_id))

    return "Erro: Vendedor ou Lead não encontrado", 400

# Rota para gerar gráficos com base nos filtros aplicados
@app.route('/filtrar_dados', methods=['POST'])
def filtrar_dados():
    dados = carregar_dados()
    vendedores_selecionados = request.json.get('vendedores', [])
    inicio_str = request.json.get('inicio')
    fim_str = request.json.get('fim')

    inicio = datetime.strptime(inicio_str, '%Y-%m-%d') if inicio_str else None
    fim = datetime.strptime(fim_str, '%Y-%m-%d') if fim_str else None

    # Filtrar leads de acordo com os vendedores selecionados e o período
    dados_filtrados = gerar_dados_graficos(dados, vendedores_selecionados, inicio, fim)

    return jsonify(dados_filtrados)

# Iniciar a aplicação
if __name__ == '__main__':
    app.run(debug=True)
