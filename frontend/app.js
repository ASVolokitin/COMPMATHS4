function generateTable() {
    const count = parseInt(document.getElementById('points-count').value, 10);
    const tbody = document.getElementById('data-table').querySelector('tbody');
    tbody.innerHTML = "";

    const defaultX = Array.from({length: count}, (_, i) => i + 1);
    const defaultY = defaultX.map(xi => (2 * xi + 1 + Math.random() * 2 - 1).toFixed(2)); 

    for (let i = 0; i < count; i++) {
        const row = document.createElement('tr');

        const cellX = document.createElement('td');
        const inputX = document.createElement('input');
        inputX.type = 'number';
        inputX.step = 'any';
        inputX.required = true;
        inputX.value = defaultX[i];
        cellX.appendChild(inputX);

        const cellY = document.createElement('td');
        const inputY = document.createElement('input');
        inputY.type = 'number';
        inputY.step = 'any';
        inputY.required = true;
        inputY.value = defaultY[i];
        cellY.appendChild(inputY);

        row.appendChild(cellX);
        row.appendChild(cellY);
        tbody.appendChild(row);
    }
}


window.onload = generateTable;

async function sendData() {
    const tbody = document.getElementById('data-table').querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    const x = [];
    const y = [];

    for (const row of rows) {
        const inputs = row.querySelectorAll('input');
        const xi = parseFloat(inputs[0].value);
        const yi = parseFloat(inputs[1].value);

        if (isNaN(xi) || isNaN(yi)) {
            alert('Пожалуйста, заполните все поля корректными числами.');
            return;
        }

        x.push(xi);
        y.push(yi);
    }

    const response = await fetch('http://localhost:8000/approximate', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ x, y })
    });

    const result = await response.json();
    console.log(result);

    displayResults(result);
    drawChart(x, y, result.approximations);
}

