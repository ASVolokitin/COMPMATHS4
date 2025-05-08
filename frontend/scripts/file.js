export function handleFileUpload(event) {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = function(e) {
        const content = e.target.result;
        const lines = content.trim().split('\n');
        const data = lines.map(line => line.replace(',', '.').split(/[ ;\t]+/).map(Number));

        const validData = data.filter(pair => pair.length === 2 && !isNaN(pair[0]) && !isNaN(pair[1]));
        if (validData.length === 0) {
            alert("Файл не содержит корректных чисел.");
            return;
        }

        fillTableWithData(validData);
    };

    reader.readAsText(file);
}

function fillTableWithData(data) {
    const tbody = document.getElementById('data-table').querySelector('tbody');
    tbody.innerHTML = '';

    document.getElementById('points-count').value = data.length;

    data.forEach(([x, y]) => {
        const row = document.createElement('tr');

        const cellX = document.createElement('td');
        const inputX = document.createElement('input');
        inputX.type = 'number';
        inputX.step = 'any';
        inputX.required = true;
        inputX.value = x;
        cellX.appendChild(inputX);

        const cellY = document.createElement('td');
        const inputY = document.createElement('input');
        inputY.type = 'number';
        inputY.step = 'any';
        inputY.required = true;
        inputY.value = y;
        cellY.appendChild(inputY);

        row.appendChild(cellX);
        row.appendChild(cellY);
        tbody.appendChild(row);
    });
}
