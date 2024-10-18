// ==================== SCRIPTS PARA index.html ====================

let vendedoresSelecionados = [];
let chartConversao, chartAberto, chartPerdido, chartConversaoTemporal, chartAbertosTemporal, chartPerdidosTemporal, chartRanking, chartVeiculo, chartComparativo;

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
        console.log("Dados recebidos do backend:", data);

        if (data.error) {
            alert(data.error);
        } else {
            atualizarGraficoConversao(data);
            atualizarGraficoAberto(data);
            atualizarGraficoPerdido(data);
            atualizarGraficoConversaoTemporal(data);  // Atualiza o gráfico de Conversão Temporal
            atualizarGraficoAbertosTemporal(data);  // Atualiza o gráfico de Abertos Temporal
            atualizarGraficoPerdidosTemporal(data);  // Atualiza o gráfico de Perdidos Temporal
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
    
    if (chartConversao) {
        chartConversao.destroy();
    }

    chartConversao = new Chart(ctxConversao, {
        type: 'bar',
        data: {
            labels: data.vendedores,
            datasets: [{
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
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    type: 'linear',
                    position: 'left',
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Total de Leads'
                    }
                },
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
        }
    });
}

function atualizarGraficoAberto(data) {
    const ctxAberto = document.getElementById('graficoAberto').getContext('2d');

    if (chartAberto) {
        chartAberto.destroy();
    }

    chartAberto = new Chart(ctxAberto, {
        type: 'bar',
        data: {
            labels: data.vendedores,
            datasets: [{
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
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    type: 'linear',
                    position: 'left',
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Total de Leads'
                    }
                },
                y1: {
                    type: 'linear',
                    position: 'right',
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Percentual de Leads Abertos (%)'
                    },
                    grid: {
                        drawOnChartArea: false
                    }
                }
            }
        }
    });
}

function atualizarGraficoPerdido(data) {
    const ctxPerdido = document.getElementById('graficoPerdido').getContext('2d');

    if (chartPerdido) {
        chartPerdido.destroy();
    }

    chartPerdido = new Chart(ctxPerdido, {
        type: 'bar',
        data: {
            labels: data.vendedores,
            datasets: [{
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
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    type: 'linear',
                    position: 'left',
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Total de Leads'
                    }
                },
                y1: {
                    type: 'linear',
                    position: 'right',
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Percentual de Leads Perdidos (%)'
                    },
                    grid: {
                        drawOnChartArea: false
                    }
                }
            }
        }
    });
}

// Funções para gráficos de variação temporal

function atualizarGraficoConversaoTemporal(data) {
    const ctxConversaoTemporal = document.getElementById('graficoConversaoTemporal').getContext('2d');

    if (chartConversaoTemporal) {
        chartConversaoTemporal.destroy();
    }

    chartConversaoTemporal = new Chart(ctxConversaoTemporal, {
        type: 'bar',
        data: {
            labels: data.variacao_temporal.map(item => item.data || 'N/A'),
            datasets: data.vendedores.map((vendedor, index) => ({
                label: `Conversão - ${vendedor}`,
                data: data.variacao_temporal.filter(item => item.vendedor === vendedor).map(item => item.conversao || 0),
                backgroundColor: `rgba(0, ${index * 50}, 255, 0.5)`,
                borderColor: `rgba(0, ${index * 50}, 255, 1)`,
                borderWidth: 1
            }))
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Percentual (%)'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Tempo'
                    }
                }
            }
        }
    });
}

function atualizarGraficoAbertosTemporal(data) {
    const ctxAbertosTemporal = document.getElementById('graficoAbertosTemporal').getContext('2d');

    if (chartAbertosTemporal) {
        chartAbertosTemporal.destroy();
    }

    chartAbertosTemporal = new Chart(ctxAbertosTemporal, {
        type: 'bar',
        data: {
            labels: data.variacao_temporal.map(item => item.data || 'N/A'),
            datasets: data.vendedores.map((vendedor, index) => ({
                label: `Abertos - ${vendedor}`,
                data: data.variacao_temporal.filter(item => item.vendedor === vendedor).map(item => item.abertos || 0),
                backgroundColor: `rgba(255, ${index * 50}, 0, 0.5)`,
                borderColor: `rgba(255, ${index * 50}, 0, 1)`,
                borderWidth: 1
            }))
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Percentual (%)'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Tempo'
                    }
                }
            }
        }
    });
}

function atualizarGraficoPerdidosTemporal(data) {
    const ctxPerdidosTemporal = document.getElementById('graficoPerdidosTemporal').getContext('2d');

    if (chartPerdidosTemporal) {
        chartPerdidosTemporal.destroy();
    }

    chartPerdidosTemporal = new Chart(ctxPerdidosTemporal, {
        type: 'bar',
        data: {
            labels: data.variacao_temporal.map(item => item.data || 'N/A'),
            datasets: data.vendedores.map((vendedor, index) => ({
                label: `Perdidos - ${vendedor}`,
                data: data.variacao_temporal.filter(item => item.vendedor === vendedor).map(item => item.perdidos || 0),
                backgroundColor: `rgba(0, ${index * 50}, 255, 0.5)`,
                borderColor: `rgba(0, ${index * 50}, 255, 1)`,
                borderWidth: 1
            }))
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Percentual (%)'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Tempo'
                    }
                }
            }
        }
    });
}

function atualizarGraficoRanking(data) {
    const ctxRanking = document.getElementById('graficoRanking').getContext('2d');

    if (chartRanking) {
        chartRanking.destroy();
    }

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

    if (chartVeiculo) {
        chartVeiculo.destroy();
    }

    chartVeiculo = new Chart(ctxVeiculo, {
        type: 'bar',
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

    if (chartComparativo) {
        chartComparativo.destroy();
    }

    // Totalizar leads convertidos por período (diário, quinzenal ou mensal)
    const labels = data.comparativo_vendas.map(item => item.periodo);
    const totalLeadsConvertidos = data.comparativo_vendas.reduce((acc, item) => acc + item.leads_convertidos, 0);
    
    chartComparativo = new Chart(ctxComparativo, {
        type: 'bar',
        data: {
            labels: labels,  // Período (dias, quinzenas, meses)
            datasets: [{
                label: 'Leads Convertidos',
                data: data.comparativo_vendas.map(item => item.leads_convertidos),
                backgroundColor: '#4CAF50',
                borderColor: '#4CAF50',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Leads Convertidos'
                    }
                }
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(tooltipItem) {
                            const totalLeads = data.comparativo_vendas[tooltipItem.dataIndex].total_leads;
                            const leadsConvertidos = data.comparativo_vendas[tooltipItem.dataIndex].leads_convertidos;
                            const percentual = data.comparativo_vendas[tooltipItem.dataIndex].percentual_conversao.toFixed(2);
                            return `Leads Convertidos: ${leadsConvertidos}/${totalLeads} (${percentual}%)`;
                        }
                    }
                }
            }
        }
    });
}



