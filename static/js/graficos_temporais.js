let chartConversaoTemporal, chartAbertosTemporal, chartPerdidosTemporal;

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

// Função para atualizar os gráficos de variação temporal
function atualizarGraficosTemporais(inicio = '', fim = '') {
    fetch('/grafico_temporal/filtrar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            vendedores: vendedoresSelecionados, // Certifique-se de que essa variável esteja definida
            inicio: inicio,
            fim: fim
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Dados recebidos para gráficos temporais:", data);

        if (data.error) {
            alert(data.error);
        } else {
            const variacaoTemporal = data.variacao_temporal;
            const opcoesPadrao = {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Período'
                        }
                    }
                }
            };

            // Atualizar gráfico de Conversão Temporal
            const dadosConversao = {
                labels: variacaoTemporal.map(item => item.periodo),
                datasets: [{
                    label: 'Conversão',
                    data: variacaoTemporal.map(item => item.convertidos),
                    backgroundColor: 'rgba(75, 192, 192, 0.5)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }]
            };
            chartConversaoTemporal = atualizarGrafico(chartConversaoTemporal, document.getElementById('graficoConversaoTemporal').getContext('2d'), 'bar', dadosConversao, opcoesPadrao);

            // Atualizar gráfico de Leads Abertos Temporal
            const dadosAbertos = {
                labels: variacaoTemporal.map(item => item.periodo),
                datasets: [{
                    label: 'Abertos',
                    data: variacaoTemporal.map(item => item.abertos),
                    backgroundColor: 'rgba(255, 159, 64, 0.5)',
                    borderColor: 'rgba(255, 159, 64, 1)',
                    borderWidth: 1
                }]
            };
            chartAbertosTemporal = atualizarGrafico(chartAbertosTemporal, document.getElementById('graficoAbertosTemporal').getContext('2d'), 'bar', dadosAbertos, opcoesPadrao);

            // Atualizar gráfico de Leads Perdidos Temporal
            const dadosPerdidos = {
                labels: variacaoTemporal.map(item => item.periodo),
                datasets: [{
                    label: 'Perdidos',
                    data: variacaoTemporal.map(item => item.perdidos),
                    backgroundColor: 'rgba(255, 99, 132, 0.5)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 1
                }]
            };
            chartPerdidosTemporal = atualizarGrafico(chartPerdidosTemporal, document.getElementById('graficoPerdidosTemporal').getContext('2d'), 'bar', dadosPerdidos, opcoesPadrao);
        }
    })
    .catch(error => console.error('Erro ao atualizar os gráficos temporais:', error));
}
