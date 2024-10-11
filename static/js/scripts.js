// ==================== SCRIPTS PARA index.html ====================

let vendedoresSelecionados = [];

// Capturar checkboxes de vendedores e gráficos
document.querySelectorAll('input[name="vendedores"]').forEach(function(checkbox) {
    checkbox.addEventListener('change', function() {
        const vendedorId = this.value;
        if (this.checked) {
            vendedoresSelecionados.push(vendedorId);
        } else {
            vendedoresSelecionados = vendedoresSelecionados.filter(id => id !== vendedorId);
        }
        atualizarGraficos();
    });
});

// Função de filtro por tempo
function filtrarPorTempo() {
    const inicio = document.getElementById('inicio').value;
    const fim = document.getElementById('fim').value;
    atualizarGraficos(inicio, fim);
}

function atualizarGraficos(inicio = '', fim = '') {
    const leadsFiltrados = getLeadsFiltrados(vendedoresSelecionados, inicio, fim);
    atualizarGraficoConversao(leadsFiltrados);
    atualizarGraficoAberto(leadsFiltrados);
    atualizarGraficoPerdido(leadsFiltrados);
    atualizarGraficoVariacao(leadsFiltrados);
    atualizarGraficoRanking(leadsFiltrados);
    atualizarGraficoVeiculo(leadsFiltrados);
    atualizarGraficoComparativo(leadsFiltrados);
}

function getLeadsFiltrados(vendedoresSelecionados, inicio, fim) {
    // Função simulada para pegar leads filtrados dos vendedores
    return [];
}

function atualizarGraficoConversao(leads) {
    const ctxConversao = document.getElementById('graficoConversao').getContext('2d');
    // Código para atualizar gráfico de taxa de conversão
}

function atualizarGraficoAberto(leads) {
    const ctxAberto = document.getElementById('graficoAberto').getContext('2d');
    // Código para atualizar gráfico de leads em aberto
}

function atualizarGraficoPerdido(leads) {
    const ctxPerdido = document.getElementById('graficoPerdido').getContext('2d');
    // Código para atualizar gráfico de leads perdidos
}

function atualizarGraficoVariacao(leads) {
    const ctxVariacao = document.getElementById('graficoVariacao').getContext('2d');
    // Código para atualizar gráfico de variação de performance
}

function atualizarGraficoRanking(leads) {
    const ctxRanking = document.getElementById('graficoRanking').getContext('2d');
    // Código para atualizar gráfico de ranking dos vendedores
}

function atualizarGraficoVeiculo(leads) {
    const ctxVeiculo = document.getElementById('graficoVeiculo').getContext('2d');
    // Código para atualizar gráfico de leads por tipo de veículo
}

function atualizarGraficoComparativo(leads) {
    const ctxComparativo = document.getElementById('graficoComparativo').getContext('2d');
    // Código para atualizar gráfico comparativo de vendas
}


// ==================== SCRIPTS PARA vendedor_detalhes.html ====================

function atualizarLead(leadId, vendedorId) {
    // Função para atualizar os detalhes de um lead em vendedor_detalhes.html
    // Exemplo de lógica:
    const status = document.getElementById(`status_${leadId}`).value;
    const faturado = document.getElementById(`faturado_${leadId}`).value;
    const notaFiscal = document.getElementById(`nota_fiscal_${leadId}`).value;

    // Fazer a chamada ao backend para atualizar o lead
    fetch(`/vendedores/${vendedorId}/atualizar_lead`, {
        method: 'POST',
        body: JSON.stringify({ leadId, status, faturado, notaFiscal }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(response => response.json()).then(data => {
        if (data.success) {
            alert('Lead atualizado com sucesso!');
        } else {
            alert('Erro ao atualizar o lead.');
        }
    });
}


// ==================== SCRIPTS PARA leads.html ====================

function validarFormularioLead() {
    const nome = document.getElementById('nome').value;
    const contato = document.getElementById('contato').value;
    const veiculo = document.getElementById('veiculo').value;

    if (nome === '' || contato === '' || veiculo === '') {
        alert('Por favor, preencha todos os campos obrigatórios.');
        return false;
    }

    // Submeter o formulário caso esteja válido
    return true;
}


// ==================== SCRIPTS PARA historico-leads.html ====================

function carregarHistoricoLeads() {
    // Lógica para carregar o histórico de leads e renderizar os gráficos
    const inicio = document.getElementById('inicio').value;
    const fim = document.getElementById('fim').value;

    fetch('/historico_leads', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(response => response.json()).then(data => {
        // Atualizar o gráfico com os dados retornados
        atualizarGraficoHistorico(data.leads_por_mes_ano);
    });
}

function atualizarGraficoHistorico(leadsPorMesAno) {
    const ctxHistorico = document.getElementById('graficoHistorico').getContext('2d');
    // Código para atualizar gráfico de histórico de leads por mês/ano
}
