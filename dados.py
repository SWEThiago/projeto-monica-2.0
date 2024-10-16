import json
from datetime import datetime

# Caminho do arquivo de dados
DATA_FILE = 'dados.json'

# Função para carregar os dados do arquivo JSON
def carregar_dados():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            dados = json.load(f)
            print(f"Dados carregados com sucesso: {dados}")  # Log para verificar os dados carregados
            return dados
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Erro ao carregar dados: {str(e)}")  # Log para capturar erros
        return []

# Função para salvar os dados no arquivo JSON
def salvar_dados(dados):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)
        print(f"Dados salvos: {dados}")  # Log para verificar a gravação dos dados

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
    print(f"Novo vendedor adicionado: {novo_vendedor}")  # Log para verificar a adição de vendedor
    return novo_vendedor

# Função para remover um vendedor pelo ID
def remover_vendedor(dados, vendedor_id):
    vendedor_existente = obter_vendedor(dados, vendedor_id)
    if vendedor_existente:
        dados[:] = [vendedor for vendedor in dados if vendedor['id'] != vendedor_id]  # Atualizando a lista diretamente
        salvar_dados(dados)  # Salva os dados após a remoção
        print(f"Vendedor removido: {vendedor_existente}")  # Log para verificar a remoção de vendedor
    else:
        raise ValueError(f"Vendedor com ID {vendedor_id} não encontrado")

# Função para obter um vendedor pelo ID (convertendo ID para inteiro)
def obter_vendedor(dados, vendedor_id):
    vendedor_id = int(vendedor_id)  # Certificar que o ID seja um inteiro
    for vendedor in dados:
        if vendedor['id'] == vendedor_id:
            print(f"Vendedor encontrado: {vendedor}")  # Log para verificar a obtenção de vendedor
            return vendedor
    print(f"Vendedor com ID {vendedor_id} não encontrado")  # Log para vendedor não encontrado
    return None

# Função para adicionar um lead a um vendedor
def adicionar_lead(dados, vendedor_id, novo_lead):
    vendedor = obter_vendedor(dados, vendedor_id)
    if vendedor:
        novo_lead_id = max([lead['id'] for lead in vendedor['leads']], default=0) + 1
        novo_lead['id'] = novo_lead_id
        vendedor['leads'].append(novo_lead)
        salvar_dados(dados)
        print(f"Novo lead adicionado ao vendedor {vendedor_id}: {novo_lead}")  # Log para verificar a adição de lead
        return novo_lead
    raise ValueError(f"Vendedor com ID {vendedor_id} não encontrado")

# Função para remover um lead de um vendedor
def remover_lead(dados, vendedor_id, lead_id):
    vendedor = obter_vendedor(dados, vendedor_id)
    if vendedor:
        leads_existentes = [lead for lead in vendedor['leads'] if lead['id'] == lead_id]
        if not leads_existentes:
            raise ValueError(f"Lead com ID {lead_id} não encontrado")
        vendedor['leads'] = [lead for lead in vendedor['leads'] if lead['id'] != lead_id]
        salvar_dados(dados)
        print(f"Lead removido do vendedor {vendedor_id}: Lead ID {lead_id}")  # Log para verificar a remoção de lead
        return True
    raise ValueError(f"Vendedor com ID {vendedor_id} não encontrado")

# Função para obter todos os leads de um vendedor
def obter_leads(dados, vendedor_id):
    vendedor = obter_vendedor(dados, vendedor_id)
    if vendedor:
        print(f"Leads obtidos para o vendedor {vendedor_id}: {vendedor['leads']}")  # Log para verificar leads
        return vendedor['leads']
    raise ValueError(f"Vendedor com ID {vendedor_id} não encontrado")

# Função para filtrar leads por data e status
def filtrar_leads(dados, vendedor_id, inicio=None, fim=None, status=None):
    leads = obter_leads(dados, vendedor_id)
    resultado = []
    for lead in leads:
        data_lead = datetime.strptime(lead['data_lead'], '%Y-%m-%d')
        if (not inicio or data_lead >= inicio) and (not fim or data_lead <= fim):
            if not status or lead['status'].lower() == status.lower():
                resultado.append(lead)
    print(f"Leads filtrados para o vendedor {vendedor_id} com período {inicio} - {fim}: {resultado}")  # Log para filtro de leads
    return resultado

# Função para calcular a quantidade de leads em diferentes status para relatórios
def calcular_leads_por_status(dados, vendedor_id):
    leads = obter_leads(dados, vendedor_id)
    total = len(leads)
    convertidos = sum(1 for lead in leads if lead['status'] == 'Convertido')
    abertos = sum(1 for lead in leads if lead['status'] == 'Aberto')
    perdidos = sum(1 for lead in leads if lead['status'] == 'Perdido')
    resultado = {
        "total": total,
        "convertidos": convertidos,
        "abertos": abertos,
        "perdidos": perdidos
    }
    print(f"Status dos leads para o vendedor {vendedor_id}: {resultado}")  # Log para verificar os status dos leads
    return resultado

# Função para obter todos os vendedores (para os gráficos)
def obter_todos_vendedores():
    dados = carregar_dados()
    vendedores = [{"id": vendedor['id'], "nome": vendedor['nome']} for vendedor in dados]
    print(f"Todos os vendedores obtidos: {vendedores}")  # Log para verificar todos os vendedores
    return vendedores



# Função para obter leads filtrados por período para os gráficos
def obter_leads_por_periodo(vendedores_selecionados, inicio_str, fim_str):
    dados = carregar_dados()
    inicio = datetime.strptime(inicio_str, '%Y-%m-%d') if inicio_str else None
    fim = datetime.strptime(fim_str, '%Y-%m-%d') if fim_str else None

    leads_filtrados = []
    for vendedor in dados:
        if vendedor['id'] in map(int, vendedores_selecionados):  # Converte os IDs para int para comparar corretamente
            for lead in vendedor['leads']:
                data_lead = datetime.strptime(lead['data_lead'], '%Y-%m-%d')
                if (not inicio or data_lead >= inicio) and (not fim or data_lead <= fim):
                    leads_filtrados.append(lead)

    print(f"Leads filtrados para vendedores {vendedores_selecionados}: {leads_filtrados}")  # Log para verificar leads filtrados
    
    return leads_filtrados
