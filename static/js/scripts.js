// ==================== SCRIPTS PARA index.html ====================

let vendedoresSelecionados = [];
let chartConversao, chartAberto, chartPerdido, chartRanking, chartVeiculo, chartComparativo;

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

// Função genérica para atualizar qualquer gráfico
function atualizarGrafico(graficoExistente, ctx, tipo, dados, opcoes) {
    if (graficoExistente) {
        graficoExistente.destroy();
    }
    return new Chart(ctx, {
        type: tipo,
        data: dados,
        options: opcoes
    });
}

// Função para atualizar gráficos individuais a partir de dados genéricos
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
        console.log("Dados recebidos do backend:", data);

        if (data.error) {
            alert(data.error);
        } else {
            const opcoesPadrao = {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            };

            // Atualizar gráfico de conversão
            const dadosConversao = {
                labels: data.vendedores,
                datasets: [
                    {
                        label: 'Total de Leads',
                        data: data.total_leads_vendedores,
                        backgroundColor: '#4CAF50',
                        borderColor: '#4CAF50',
                        borderWidth: 1,
                        yAxisID: 'y'
                    },
                    {
                        label: 'Percentual de Conversão (%)',
                        data: data.percentual_conversao_vendedores,
                        backgroundColor: '#FFCE56',
                        borderColor: '#FFCE56',
                        borderWidth: 1,
                        yAxisID: 'y1'
                    }
                ]
            };
            chartConversao = atualizarGrafico(chartConversao, document.getElementById('graficoConversao').getContext('2d'), 'bar', dadosConversao, {
                ...opcoesPadrao,
                scales: {
                    ...opcoesPadrao.scales,
                    y1: {
                        type: 'linear',
                        position: 'right',
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Percentual de Conversão (%)'
                        },
                        grid: {
                            drawOnChartArea: false
                        }
                    }
                }
            });

            // Atualizar gráfico de leads abertos
            const dadosAbertos = {
                labels: data.vendedores,
                datasets: [
                    {
                        label: 'Total de Leads',
                        data: data.total_leads_vendedores,
                        backgroundColor: '#4CAF50',
                        borderColor: '#4CAF50',
                        borderWidth: 1,
                        barThickness: 30,
                        maxBarThickness: 50,
                        yAxisID: 'y'
                    },
                    {
                        label: 'Percentual de Leads Abertos (%)',
                        data: data.percentual_abertos_vendedores,
                        backgroundColor: '#FFCE56',
                        borderColor: '#FFCE56',
                        borderWidth: 1,
                        barThickness: 30,
                        maxBarThickness: 50,
                        yAxisID: 'y1'
                    }
                ]
            };
            chartAberto = atualizarGrafico(chartAberto, document.getElementById('graficoAberto').getContext('2d'), 'bar', dadosAbertos, opcoesPadrao);

            // Atualizar gráfico de leads perdidos
            const dadosPerdidos = {
                labels: data.vendedores,
                datasets: [
                    {
                        label: 'Total de Leads',
                        data: data.total_leads_vendedores,
                        backgroundColor: '#4CAF50',
                        borderColor: '#4CAF50',
                        borderWidth: 1,
                        barThickness: 30,
                        maxBarThickness: 50,
                        yAxisID: 'y'
                    },
                    {
                        label: 'Percentual de Leads Perdidos (%)',
                        data: data.percentual_perdidos_vendedores,
                        backgroundColor: '#F7464A',
                        borderColor: '#F7464A',
                        borderWidth: 1,
                        barThickness: 30,
                        maxBarThickness: 50,
                        yAxisID: 'y1'
                    }
                ]
            };
            chartPerdido = atualizarGrafico(chartPerdido, document.getElementById('graficoPerdido').getContext('2d'), 'bar', dadosPerdidos, opcoesPadrao);

            // Atualizar gráfico de ranking
            const dadosRanking = {
                labels: data.ranking_vendedores.map(item => item.vendedor || 'Desconhecido'),
                datasets: [
                    {
                        label: 'Leads Convertidos',
                        data: data.ranking_vendedores.map(item => item.convertidos ?? 0),
                        backgroundColor: '#4CAF50',
                        borderColor: '#4CAF50',
                        borderWidth: 1
                    }
                ]
            };
            chartRanking = atualizarGrafico(chartRanking, document.getElementById('graficoRanking').getContext('2d'), 'bar', dadosRanking, opcoesPadrao);

            // Atualizar gráfico por veículo
            const dadosVeiculo = {
                labels: Object.keys(data.leads_por_veiculo),
                datasets: [{
                    label: 'Leads por Veículo',
                    data: Object.values(data.leads_por_veiculo),
                    backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4CAF50', '#F7464A'],
                    borderWidth: 1
                }]
            };
            chartVeiculo = atualizarGrafico(chartVeiculo, document.getElementById('graficoVeiculo').getContext('2d'), 'bar', dadosVeiculo, opcoesPadrao);

            // Atualizar gráfico comparativo de vendas
            const dadosComparativo = {
                labels: data.comparativo_vendas.map(item => item.periodo),
                datasets: [{
                    label: 'Leads Convertidos',
                    data: data.comparativo_vendas.map(item => item.leads_convertidos),
                    backgroundColor: '#4CAF50',
                    borderColor: '#4CAF50',
                    borderWidth: 1
                }]
            };
            chartComparativo = atualizarGrafico(chartComparativo, document.getElementById('graficoComparativo').getContext('2d'), 'bar', dadosComparativo, {
                ...opcoesPadrao,
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function(tooltipItem) {
                                const leads = data.comparativo_vendas[tooltipItem.dataIndex].leads_convertidos;
                                const percentual = data.comparativo_vendas[tooltipItem.dataIndex].percentual_conversao.toFixed(2);
                                return `Leads Convertidos: ${leads} (${percentual}%)`;
                            }
                        }
                    }
                }
            });
        }
    })
    .catch(error => console.error('Erro ao atualizar os gráficos:', error));
}
