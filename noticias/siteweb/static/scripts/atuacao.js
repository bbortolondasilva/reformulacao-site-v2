new Chart(segmentos, {
    type: 'pie',
    data: {
        labels: ['Autopeças', 'Comércio', 'Oficinas', 'Outros'],
        datasets: [{
            data: [40, 25, 20, 15]
        }]
    }
});

new Chart(estados, {
    type: 'bar',
    data: {
        labels: ['RS', 'SC', 'PR'],
        datasets: [{
            label: 'Clientes',
            data: [180, 40, 20]
        }]
    },
    options: {
        responsive: true
    }
});

new Chart(crescimento, {
    type: 'line',
    data: {
        labels: [
            '2018',
            '2019',
            '2020',
            '2021',
            '2022',
            '2023',
            '2024',
            '2025',
            '2026'
        ],
        datasets: [{
            label: 'Clientes',
            data: [30, 45, 70, 95, 130, 160, 190, 220, 240],
            fill: false
        }]
    }
});