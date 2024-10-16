from flask import Blueprint, render_template, request, redirect, url_for
from dados import (
    carregar_dados, adicionar_vendedor, remover_vendedor, obter_vendedor, 
    adicionar_lead, remover_lead, obter_leads, calcular_leads_por_status, salvar_dados
)

vendedores_bp = Blueprint('vendedores', __name__)

# Rota para exibir a lista de vendedores
@vendedores_bp.route('/vendedores')
def listar_vendedores():
    dados = carregar_dados()
    return render_template('vendedores.html', vendedores=dados)

# Rota para adicionar um novo vendedor
@vendedores_bp.route('/vendedores/adicionar', methods=['POST'])
def adicionar_vendedor_route():
    dados = carregar_dados()  # Carregar os dados do arquivo
    nome_vendedor = request.form['nome_vendedor']
    adicionar_vendedor(dados, nome_vendedor)  # Função já existente em dados.py
    salvar_dados(dados)  # Salvar os dados após a adição
    return redirect(url_for('vendedores.listar_vendedores'))

# Rota para remover um vendedor
@vendedores_bp.route('/vendedores/remover/<int:vendedor_id>', methods=['POST'])
def remover_vendedor_route(vendedor_id):
    dados = carregar_dados()  # Carregar os dados do arquivo
    remover_vendedor(dados, vendedor_id)  # Função já existente em dados.py
    salvar_dados(dados)  # Salvar os dados após a remoção
    return redirect(url_for('vendedores.listar_vendedores'))

# Rota para exibir detalhes de um vendedor e seus leads
@vendedores_bp.route('/vendedores/<int:vendedor_id>')
def detalhes_vendedor(vendedor_id):
    dados = carregar_dados()  # Carregar os dados do arquivo
    vendedor = obter_vendedor(dados, vendedor_id)  # Função já existente em dados.py
    if not vendedor:
        return redirect(url_for('vendedores.listar_vendedores'))

    leads = obter_leads(dados, vendedor_id)  # Função já existente em dados.py
    stats = calcular_leads_por_status(dados, vendedor_id)  # Função já existente em dados.py
    return render_template('vendedor_detalhes.html', vendedor=vendedor, leads=leads, stats=stats)

# Rota para adicionar um lead a um vendedor
@vendedores_bp.route('/vendedores/<int:vendedor_id>/adicionar_lead', methods=['POST'])
def adicionar_lead_route(vendedor_id):
    dados = carregar_dados()  # Carregar os dados do arquivo
    novo_lead = {
        "data_lead": request.form['data_lead'],
        "nome": request.form['nome'],
        "contato": request.form['contato'],
        "veiculo": request.form['veiculo'],
        "modelo": request.form['modelo'],
        "status": request.form['status'],
        "faturado": request.form['faturado'],
        "cliente_faturado": request.form['cliente_faturado'],
        "nota_fiscal": request.form['nota_fiscal']
    }
    adicionar_lead(dados, vendedor_id, novo_lead)  # Função já existente em dados.py
    salvar_dados(dados)  # Salvar os dados após a adição do lead
    return redirect(url_for('vendedores.detalhes_vendedor', vendedor_id=vendedor_id))

# Rota para remover um lead de um vendedor
@vendedores_bp.route('/vendedores/<int:vendedor_id>/remover_lead/<int:lead_id>', methods=['POST'])
def remover_lead_route(vendedor_id, lead_id):
    dados = carregar_dados()  # Carregar os dados do arquivo
    remover_lead(dados, vendedor_id, lead_id)  # Função já existente em dados.py
    salvar_dados(dados)  # Salvar os dados após a remoção do lead
    return redirect(url_for('vendedores.detalhes_vendedor', vendedor_id=vendedor_id))
