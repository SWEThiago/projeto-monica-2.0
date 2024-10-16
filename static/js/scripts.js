// ==================== SCRIPTS PARA index.html ====================

let vendedoresSelecionados = [];
let chartConversao, chartAberto, chartPerdido, chartVariacao, chartRanking, chartVeiculo, chartComparativo; // Variáveis para armazenar instâncias dos gráficos

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
    fetch('/grafico/filtrar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            vendedores: vendedoresSelecionados,
            inicio: inicio,
            fim: fim
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Dados recebidos do backend:", data);  // Adicionando log para depurar os dados recebidos

        if (data.error) {
            alert(data.error);
        } else {
            atualizarGraficoConversao(data);
            atualizarGraficoAberto(data);
            atualizarGraficoPerdido(data);
            atualizarGraficoVariacao(data);
            atualizarGraficoRanking(data);
            atualizarGraficoVeiculo(data);
            atualizarGraficoComparativo(data);
        }
    })
    .catch(error => console.error('Erro ao atualizar os gráficos:', error));
}


// Funções para atualizar gráficos individuais

function atualizarGraficoConversao(data) {
    const ctxConversao = document.getElementById('graficoConversao').getContext('2d');
    
    // Destruir o gráfico anterior se existir
    if (chartConversao) {
        chartConversao.destroy();
    }

    chartConversao = new Chart(ctxConversao, {
        type: 'bar',
        data: {
            labels: ['Abertos', 'Convertidos', 'Perdidos'],
            datasets: [{
                label: 'Leads',
                data: [
                    data.leads_abertos ?? 0, 
                    data.leads_convertidos ?? 0, 
                    data.leads_perdidos ?? 0
                ],
                backgroundColor: ['#FFCE56', '#4CAF50', '#F7464A'],
                borderColor: ['#FFCE56', '#4CAF50', '#F7464A'],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Status dos Leads'
                    }
                },
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Quantidade de Leads'
                    }
                }
            }
        }
    });
}

function atualizarGraficoAberto(data) {
    const ctxAberto = document.getElementById('graficoAberto').getContext('2d');

    // Destruir o gráfico anterior se existir
    if (chartAberto) {
        chartAberto.destroy();
    }

    // Criar um novo gráfico
    chartAberto = new Chart(ctxAberto, {
        type: 'bar',
        data: {
            labels: ['Leads em Aberto'],
            datasets: [{
                label: 'Abertos',
                data: [data.leads_abertos ?? 0],
                backgroundColor: '#FFCE56',
                borderColor: '#FFCE56',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function atualizarGraficoPerdido(data) {
    const ctxPerdido = document.getElementById('graficoPerdido').getContext('2d');

    // Destruir o gráfico anterior se existir
    if (chartPerdido) {
        chartPerdido.destroy();
    }

    // Criar um novo gráfico
    chartPerdido = new Chart(ctxPerdido, {
        type: 'bar',
        data: {
            labels: ['Leads Perdidos'],
            datasets: [{
                label: 'Perdidos',
                data: [data.leads_perdidos ?? 0],
                backgroundColor: '#F7464A',
                borderColor: '#F7464A',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function atualizarGraficoVariacao(data) {
    const ctxVariacao = document.getElementById('graficoVariacao').getContext('2d');

    // Destruir o gráfico anterior se existir
    if (chartVariacao) {
        chartVariacao.destroy();
    }

    // Criar um novo gráfico
    chartVariacao = new Chart(ctxVariacao, {
        type: 'line',
        data: {
            labels: data.variacao_temporal.map(item => item.data || 'N/A'),
            datasets: [{
                label: 'Status Temporal',
                data: data.variacao_temporal.map(item => item.status === 'Convertido' ? 1 : (item.status === 'Aberto' ? 0.5 : 0)),
                backgroundColor: '#4CAF50',
                borderColor: '#4CAF50',
                fill: false,
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function atualizarGraficoRanking(data) {
    const ctxRanking = document.getElementById('graficoRanking').getContext('2d');

    // Destruir o gráfico anterior se existir
    if (chartRanking) {
        chartRanking.destroy();
    }

    // Criar um novo gráfico
    chartRanking = new Chart(ctxRanking, {
        type: 'bar',
        data: {
            labels: data.ranking_vendedores.map(item => item.vendedor || 'Desconhecido'),
            datasets: [{
                label: 'Leads Convertidos',
                data: data.ranking_vendedores.map(item => item.convertidos ?? 0),
                backgroundColor: '#4CAF50',
                borderColor: '#4CAF50',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function atualizarGraficoVeiculo(data) {
    const ctxVeiculo = document.getElementById('graficoVeiculo').getContext('2d');

    // Destruir o gráfico anterior se existir
    if (chartVeiculo) {
        chartVeiculo.destroy();
    }

    // Criar um novo gráfico
    chartVeiculo = new Chart(ctxVeiculo, {
        type: 'pie',
        data: {
            labels: Object.keys(data.leads_por_veiculo),
            datasets: [{
                label: 'Leads por Veículo',
                data: Object.values(data.leads_por_veiculo),
                backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4CAF50', '#F7464A'],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true
        }
    });
}

function atualizarGraficoComparativo(data) {
    const ctxComparativo = document.getElementById('graficoComparativo').getContext('2d');

    // Destruir o gráfico anterior se existir
    if (chartComparativo) {
        chartComparativo.destroy();
    }

    // Criar um novo gráfico
    chartComparativo = new Chart(ctxComparativo, {
        type: 'line',
        data: {
            labels: data.comparativo_vendas.map(item => item.vendedor || 'Desconhecido'),
            datasets: [{
                label: 'Leads Convertidos',
                data: data.comparativo_vendas.map(item => item.convertidos ?? 0),
                backgroundColor: '#4CAF50',
                borderColor: '#4CAF50',
                fill: false,
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}
