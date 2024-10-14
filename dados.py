import json
from datetime import datetime

# Caminho do arquivo de dados
DATA_FILE = 'dados.json'

# Função para carregar os dados do arquivo JSON
def carregar_dados():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Função para salvar os dados no arquivo JSON
def salvar_dados(dados):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

# Função para adicionar um novo vendedor com um ID único
def adicionar_vendedor(dados, nome_vendedor):
    novo_id = max([vendedor['id'] for vendedor in dados], default=0) + 1
    novo_vendedor = {
        "id": novo_id,
        "nome": nome_vendedor,
        "leads": []
    }
    dados.append(novo_vendedor)
    salvar_dados(dados)
    return novo_vendedor

# Função para remover um vendedor pelo ID
def remover_vendedor(dados, vendedor_id):
    dados = [vendedor for vendedor in dados if vendedor['id'] != vendedor_id]
    salvar_dados(dados)

# Função para obter um vendedor pelo ID
def obter_vendedor(dados, vendedor_id):
    for vendedor in dados:
        if vendedor['id'] == vendedor_id:
            return vendedor
    return None

# Função para adicionar um lead a um vendedor
def adicionar_lead(dados, vendedor_id, novo_lead):
    for vendedor in dados:
        if vendedor['id'] == vendedor_id:
            novo_lead_id = max([lead['id'] for lead in vendedor['leads']], default=0) + 1
            novo_lead['id'] = novo_lead_id
            vendedor['leads'].append(novo_lead)
            salvar_dados(dados)
            return novo_lead
    return None

# Função para remover um lead de um vendedor
def remover_lead(dados, vendedor_id, lead_id):
    for vendedor in dados:
        if vendedor['id'] == vendedor_id:
            vendedor['leads'] = [lead for lead in vendedor['leads'] if lead['id'] != lead_id]
            salvar_dados(dados)
            return True
    return False

# Função para obter todos os leads de um vendedor
def obter_leads(dados, vendedor_id):
    vendedor = obter_vendedor(dados, vendedor_id)
    if vendedor:
        return vendedor['leads']
    return []

# Função para filtrar leads por data e status
def filtrar_leads(dados, vendedor_id, inicio=None, fim=None, status=None):
    leads = obter_leads(dados, vendedor_id)
    resultado = []
    for lead in leads:
        data_lead = datetime.strptime(lead['data_lead'], '%Y-%m-%d')
        if (not inicio or data_lead >= inicio) and (not fim or data_lead <= fim):
            if not status or lead['status'].lower() == status.lower():
                resultado.append(lead)
    return resultado

# Função para calcular a quantidade de leads em diferentes status para relatórios
def calcular_leads_por_status(dados, vendedor_id):
    leads = obter_leads(dados, vendedor_id)
    total = len(leads)
    convertidos = sum(1 for lead in leads if lead['status'] == 'Convertido')
    abertos = sum(1 for lead in leads if lead['status'] == 'Aberto')
    perdidos = sum(1 for lead in leads if lead['status'] == 'Perdido')
    return {
        "total": total,
        "convertidos": convertidos,
        "abertos": abertos,
        "perdidos": perdidos
    }

# Função para obter todos os vendedores (para os gráficos)
def obter_todos_vendedores():
    dados = carregar_dados()
    return [{"id": vendedor['id'], "nome": vendedor['nome']} for vendedor in dados]

# Função para obter leads filtrados por período para os gráficos
def obter_leads_por_periodo(vendedores_selecionados, inicio_str, fim_str):
    dados = carregar_dados()
    inicio = datetime.strptime(inicio_str, '%Y-%m-%d') if inicio_str else None
    fim = datetime.strptime(fim_str, '%Y-%m-%d') if fim_str else None

    leads_filtrados = []
    for vendedor in dados:
        if vendedor['id'] in vendedores_selecionados:
            for lead in vendedor['leads']:
                data_lead = datetime.strptime(lead['data_lead'], '%Y-%m-%d')
                if (not inicio or data_lead >= inicio) and (not fim or data_lead <= fim):
                    leads_filtrados.append(lead)
    
    return leads_filtrados
