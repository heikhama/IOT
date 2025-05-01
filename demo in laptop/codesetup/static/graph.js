const ctx = document.getElementById('graph').getContext('2d');
const chart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [
            {
                label: 'CPU Temp (°C)',
                data: [],
                borderColor: 'red',
                fill: false
            },
            {
                label: 'Power (W)',
                data: [],
                borderColor: 'blue',
                fill: false
            }
        ]
    },
    options: {
        animation: false,
        scales: {
            x: { title: { display: true, text: "Time" }},
            y: { title: { display: true, text: "Reading" }}
        }
    }
});

function updateData() {
    fetch('/data')
    .then(res => res.json())
    .then(data => {
        document.getElementById('temp').value = data.temperature;
        document.getElementById('power').value = data.power;

        const now = new Date().toLocaleTimeString();

        chart.data.labels.push(now);
        chart.data.datasets[0].data.push(data.temperature);
        chart.data.datasets[1].data.push(data.power);

        if (chart.data.labels.length > 20) {
            chart.data.labels.shift();
            chart.data.datasets[0].data.shift();
            chart.data.datasets[1].data.shift();
        }

        chart.update();
    });
}

setInterval(updateData, 1000);
