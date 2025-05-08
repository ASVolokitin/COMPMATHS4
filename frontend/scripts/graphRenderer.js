export function renderGraph(canvas, x, y, originalX, originalY) {
    new Chart(canvas, {
        type: 'line',
        data: {
            labels: x,
            datasets: [
                {
                    label: 'Approximation',
                    data: y,
                    borderColor: 'blue',
                    tension: 0.3,
                    pointRadius: 0,
                },
                {
                    label: 'Input points',
                    data: originalY.map((val, index) => ({ x: originalX[index], y: val })),
                    borderColor: 'transparent',
                    backgroundColor: 'red',
                    pointRadius: 5,
                    pointStyle: 'circle',
                    fill: false,
                }
            ]
        },
        options: {
            responsive: true,
            plugins: { legend: { display: true } },
            scales: {
                x: {
                    type: 'linear',
                    title: { display: true, text: 'X' },
                    min: Math.ceil(x[0]),
                    max: Math.floor(x[x.length - 1])
                },
                y: {
                    title: { display: true, text: 'Y' },
                    ticks: {
                        beginAtZero: false,
                    },
                },
            },
        },
    });
}
