import { renderGraph } from './graphRenderer.js';   

export function createTabs(container, tabData) {

    console.log(tabData);
    const nav = document.createElement('div');
    nav.className = 'tab-nav';

    const contentArea = document.createElement('div');
    contentArea.className = 'tab-content';

    tabData.forEach((tab, index) => {
        const btn = document.createElement('button');
        btn.textContent = tab.title;
        const tabId = tab.title.toLowerCase().replace(/\s+/g, '-');

        btn.addEventListener('click', () => {
            const buttons = document.querySelectorAll('.tab-nav button');
            buttons.forEach(b => b.classList.remove('active'));

            btn.classList.add('active');

            const tabPanes = document.querySelectorAll('.tab-pane');
            tabPanes.forEach(pane => pane.classList.remove('active'));

            const activeTab = document.getElementById(tabId);
            if (activeTab) {
                activeTab.classList.add('active');
            }

            contentArea.style.opacity = 0;
            setTimeout(() => {
                contentArea.innerHTML = '';
                contentArea.appendChild(tab.content);
                contentArea.style.opacity = 1;
            }, 400);
        });

        if (tab.isBest) {
            btn.classList.add('best-tab');
        }

        console.log(tab);
        if (tab.isSuccessful == false) {
            btn.classList.add('failed-tab');
        }

        nav.appendChild(btn);

        if (index === 0) {
            contentArea.appendChild(tab.content); 
            btn.classList.add('active');
        }

        tab.content.id = tabId;
    });

    container.appendChild(nav);
    container.appendChild(contentArea);
}

export function createApproximationBlock(method, data) {
    const wrapper = document.createElement('div');

    const graphCanvas = document.createElement('canvas');
    graphCanvas.id = `graph-${method}`;
    wrapper.appendChild(graphCanvas);
    
    renderGraph(graphCanvas, data.x_for_graph, data.y_for_graph, data.x, data.y);

    const paramsTable = document.createElement('table');
    paramsTable.className = 'params-table'; // Для стилизации таблицы

    const tbody = document.createElement('tbody');
    
    for (const [key, value] of Object.entries(data)) {
        if (key !== 'x_for_graph' && key !== 'y_for_graph' && !key.endsWith("_dots")) {
            const row = document.createElement('tr');
            
            const cellKey = document.createElement('td');
            cellKey.className = 'param-key'; // Добавим классы для стилизации
            cellKey.textContent = key;
            row.appendChild(cellKey);

            const cellValue = document.createElement('td');
            cellValue.className = 'param-value'; // Классы для стилизации

            let formattedValue = value; // Меняем с const на let для возможности изменения

            if (Array.isArray(formattedValue)) {
                formattedValue = formattedValue.map(item => (typeof item === 'number') ? parseFloat(item.toFixed(10)) : item);
            } else if (typeof formattedValue === 'number') {
                formattedValue = parseFloat(formattedValue.toFixed(10));
            }

            if (formattedValue === "" || formattedValue === null || formattedValue === undefined || (Array.isArray(value) && value.length === 0)) {
                continue;
            }

            if (key.toLowerCase() === "errors" && !formattedValue) {
                continue;
            }
            

            if (Array.isArray(formattedValue)) {
                if (key.toLowerCase() === "errors") {
                    formattedValue = formattedValue.join('\n\n');
                    console.log(formattedValue);
                }
                else formattedValue = formattedValue.join(', ');
            }

            cellValue.textContent = formattedValue;
            row.appendChild(cellValue);

            tbody.appendChild(row);
        }
    }

    paramsTable.appendChild(tbody);
    wrapper.appendChild(paramsTable);
    
    return wrapper;
}




export function generateTable() {
    const count = parseInt(document.getElementById('points-count').value, 10);
    const tbody = document.getElementById('data-table').querySelector('tbody');
    tbody.innerHTML = "";

    const defaultX = Array.from({length: count}, (_, i) => i + 1);
    const defaultY = defaultX.map(xi => (2 * xi + 1 + Math.random() * 20 - 1).toFixed(2)); 

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