from flask import Flask, render_template, request, redirect, url_for, jsonify
from settings import get_config
from dados import carregar_dados, salvar_dados, adicionar_vendedor, remover_vendedor, obter_vendedor
from graficos import calcular_metricas_por_vendedor, gerar_dados_graficos
from graficos import grafico_bp  # Importando o blueprint dos gráficos
from datetime import datetime

# Criação da aplicação Flask
app = Flask(__name__)

# Carregar configurações do arquivo settings.py
app.config.from_object(get_config())

# Registrar blueprint de gráficos
app.register_blueprint(grafico_bp)

# Rota inicial - Página principal
@app.route('/')
def index():
    dados = carregar_dados()
    leads_mensais = sum(len(v['leads']) for v in dados)
    leads_diarios = len([lead for v in dados for lead in v['leads'] if lead['data_lead'] == datetime.now().strftime('%Y-%m-%d')])

    return render_template('index.html', leads_mensais=leads_mensais, leads_diarios=leads_diarios, vendedores=dados)

# Rota para adicionar um vendedor
@app.route('/vendedores', methods=['GET', 'POST'])
def vendedores():
    dados = carregar_dados()
    if request.method == 'POST':
        nome_vendedor = request.form['nome_vendedor']
        adicionar_vendedor(dados, nome_vendedor)
        salvar_dados(dados)
        return redirect(url_for('vendedores'))

    return render_template('vendedores.html', vendedores=dados)

# Rota para remover um vendedor
@app.route('/vendedores/remover/<int:vendedor_id>', methods=['POST'])
def remover_vendedor_route(vendedor_id):
    dados = carregar_dados()
    remover_vendedor(dados, vendedor_id)
    salvar_dados(dados)
    return redirect(url_for('vendedores'))

# Rota para ver detalhes de um vendedor
@app.route('/vendedores/<int:vendedor_id>')
def detalhes_vendedor(vendedor_id):
    dados = carregar_dados()
    vendedor = obter_vendedor(dados, vendedor_id)
    if not vendedor:
        return redirect(url_for('vendedores'))

    inicio_str = request.args.get('inicio')
    fim_str = request.args.get('fim')
    inicio, fim = None, None

    if inicio_str and fim_str:
        inicio = datetime.strptime(inicio_str, '%Y-%m-%d')
        fim = datetime.strptime(fim_str, '%Y-%m-%d')

    # Filtrar leads para exibir
    leads_filtrados = [
        lead for lead in vendedor['leads']
        if (not inicio or datetime.strptime(lead['data_lead'], '%Y-%m-%d') >= inicio) and
           (not fim or datetime.strptime(lead['data_lead'], '%Y-%m-%d') <= fim)
    ]

    # Converter data_lead para datetime
    for lead in leads_filtrados:
        lead['data_lead'] = datetime.strptime(lead['data_lead'], '%Y-%m-%d')

    leads_filtrados.sort(key=lambda lead: lead['data_lead'], reverse=True)

    total_leads = len(leads_filtrados)
    aberto, convertido, perdido = calcular_metricas_por_vendedor(leads_filtrados)

    return render_template(
        'vendedor_detalhes.html',
        vendedor=vendedor,
        leads=leads_filtrados,
        total_leads=total_leads,
        quantidade_aberto=aberto,
        quantidade_convertido=convertido,
        quantidade_perdido=perdido,
        inicio_str=inicio_str,
        fim_str=fim_str
    )

# Rota para adicionar leads
@app.route('/leads', methods=['GET', 'POST'])
def leads():
    dados = carregar_dados()
    if request.method == 'POST':
        vendedor_id = int(request.form['vendedor_id'])
        vendedor = obter_vendedor(dados, vendedor_id)
        if not vendedor:
            return "Erro: Vendedor não encontrado", 400
        
        novo_lead = {
            'id': len(vendedor['leads']) + 1,
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
        vendedor['leads'].append(novo_lead)
        salvar_dados(dados)
        return redirect(url_for('leads'))

    return render_template('leads.html', vendedores=dados)

# Rota para atualizar um lead
@app.route('/vendedores/<int:vendedor_id>/atualizar_lead', methods=['POST'])
def atualizar_lead(vendedor_id):
    dados = carregar_dados()
    vendedor = obter_vendedor(dados, vendedor_id)

    if vendedor:
        try:
            lead_id = int(request.form.get('lead_id'))
            for lead in vendedor['leads']:
                if lead['id'] == lead_id:
                    lead['status'] = request.form.get('status')
                    lead['faturado'] = request.form.get('faturado')
                    lead['cliente_faturado'] = request.form.get('cliente_faturado', '')
                    lead['nota_fiscal'] = request.form.get('nota_fiscal', '')
                    salvar_dados(dados)
                    return redirect(url_for('detalhes_vendedor', vendedor_id=vendedor_id))
        except (KeyError, ValueError):
            return "Erro: Lead ID não encontrado ou inválido", 400

    return "Erro: Vendedor ou Lead não encontrado", 400

# Rota para remover um lead
@app.route('/vendedores/<int:vendedor_id>/remover_lead/<int:lead_id>', methods=['POST'])
def remover_lead(vendedor_id, lead_id):
    dados = carregar_dados()
    vendedor = obter_vendedor(dados, vendedor_id)

    if vendedor:
        vendedor['leads'] = [lead for lead in vendedor['leads'] if lead['id'] != lead_id]
        salvar_dados(dados)
        return redirect(url_for('detalhes_vendedor', vendedor_id=vendedor_id))

    return "Erro: Vendedor ou Lead não encontrado", 400

# Rota para gerar o gráfico temporal do desempenho do vendedor
@app.route('/vendedores/<int:vendedor_id>/desempenho_temporal', methods=['POST'])
def desempenho_temporal(vendedor_id):
    dados = carregar_dados()
    vendedor = obter_vendedor(dados, vendedor_id)

    if not vendedor:
        return jsonify({"error": "Vendedor não encontrado"}), 404

    inicio_str = request.json.get('inicio')
    fim_str = request.json.get('fim')

    # Converte strings de data para objetos datetime
    inicio = datetime.strptime(inicio_str, '%Y-%m') if inicio_str else None
    fim = datetime.strptime(fim_str, '%Y-%m') if fim_str else None

    # Inicializa os dados do gráfico para cada mês
    desempenho_por_mes = {}

    for lead in vendedor['leads']:
        data_lead = datetime.strptime(lead['data_lead'], '%Y-%m-%d')
        
        if (not inicio or data_lead >= inicio) and (not fim or data_lead <= fim):
            mes = data_lead.strftime('%Y-%m')
            if mes not in desempenho_por_mes:
                desempenho_por_mes[mes] = {'abertos': 0, 'convertidos': 0, 'perdidos': 0}
            
            if lead['status'] == 'Aberto':
                desempenho_por_mes[mes]['abertos'] += 1
            elif lead['status'] == 'Convertido':
                desempenho_por_mes[mes]['convertidos'] += 1
            elif lead['status'] == 'Perdido':
                desempenho_por_mes[mes]['perdidos'] += 1

    # Formata os dados para o gráfico
    meses = sorted(desempenho_por_mes.keys())
    dados_grafico = {
        'meses': meses,
        'abertos': [desempenho_por_mes[mes]['abertos'] for mes in meses],
        'convertidos': [desempenho_por_mes[mes]['convertidos'] for mes in meses],
        'perdidos': [desempenho_por_mes[mes]['perdidos'] for mes in meses],
    }

    return jsonify(dados_grafico)

# Rota para gerar gráficos filtrados
@app.route('/filtrar_dados', methods=['POST'])
def filtrar_dados():
    dados = carregar_dados()
    vendedores_selecionados = request.json.get('vendedores', [])
    inicio_str = request.json.get('inicio')
    fim_str = request.json.get('fim')

    inicio = datetime.strptime(inicio_str, '%Y-%m-%d') if inicio_str else None
    fim = datetime.strptime(fim_str, '%Y-%m-%d') if fim_str else None

    dados_filtrados = gerar_dados_graficos(vendedores_selecionados, inicio, fim)

    return jsonify(dados_filtrados)

# Rota para o histórico de leads
@app.route('/historico_leads', methods=['GET'])
def historico_leads():
    return render_template('historico-leads.html')

# Iniciar a aplicação
if __name__ == '__main__':
    app.run(debug=True)
