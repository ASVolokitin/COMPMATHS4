import { renderGraph } from './graphRenderer.js';  
import { saveJsonToFile } from './file.js'

export function createTabs(container, tabData) {

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

    const canvasContainer = document.createElement('div');
    canvasContainer.style.height="500px";
    const graphCanvas = document.createElement('canvas');
    graphCanvas.id = `graph-${method}`;
    canvasContainer.appendChild(graphCanvas)
    wrapper.appendChild(canvasContainer);
    
    renderGraph(graphCanvas, data.x_for_graph, data.y_for_graph, data.x, data.y);

    const paramsTable = document.createElement('table');
    paramsTable.className = 'params-table';

    const tbody = document.createElement('tbody');
    
    for (const [key, value] of Object.entries(data)) {
        if (key !== 'x_for_graph' && key !== 'y_for_graph' && key !=='phi_dots') {
            const row = document.createElement('tr');
            
            let cellKey = document.createElement('td');
            cellKey.className = 'param-key'; 
            cellKey.textContent = key.replace(/_/g, " ");
            if (key === "mse") cellKey.textContent = cellKey.textContent.toUpperCase();
            row.appendChild(cellKey);

            const cellValue = document.createElement('td');
            cellValue.className = 'param-value';

            let formattedValue = value; 
            if (key ==="x" || key === "y" || key === "coefficients") {
                if (Array.isArray(formattedValue)) {
                    formattedValue = formattedValue.map(item => (typeof Decimal(item).toNumber() === 'number') ? parseFloat(Decimal(item).toNumber().toFixed(10)) : item);
                } else if (typeof formattedValue === 'number') {
                    formattedValue = parseFloat(formattedValue.toFixed(10));
                }
            }

            if (key === "e_dots") {
                formattedValue = formattedValue.map(item => (typeof Decimal(item).toNumber() === 'number') ? parseFloat(Decimal(item).toNumber().toFixed(20)) : item);
            }

            if (formattedValue === "" || formattedValue === null || formattedValue === undefined || (Array.isArray(value) && value.length === 0)) {
                continue;
            }

            if (key.toLowerCase() === "errors" && !formattedValue) {
                continue;
            }

            if (typeof value === "boolean") {
                formattedValue =  value ? "✅" : "❌";
            }

            if (Array.isArray(formattedValue)) {
                if (key.toLowerCase() === "errors") {
                    formattedValue = formattedValue.join('\n\n');
                }
                else if (key.toLowerCase() === "e_dots") {
                    formattedValue = "• " + formattedValue.join('\n• ');
                }
                else formattedValue = formattedValue.join(', ');
            }

            if (key.toLowerCase() == "coefficient_of_determination") {
                cellValue.innerHTML = `
                    <div class="result-value-container">
                        <a class='result-value'>${formattedValue}</a>
                        <a class='underline-value'>${interpretDetermination(formattedValue)}</a>
                    </div>
                    `;
                    cellValue.style.display = 'contents';
                    cellValue.style.gap = '5px';
            }
            else cellValue.textContent = formattedValue;
            console.log(cellValue);
            row.appendChild(cellValue);

            tbody.appendChild(row);
        }
    }

    

    paramsTable.appendChild(tbody);
    wrapper.appendChild(paramsTable);

    const saveBtn = document.createElement('button');
    saveBtn.id = 'save-results';
    saveBtn.style.marginTop='20px';
    saveBtn.class ='button';
    saveBtn.className = 'button';
    saveBtn.textContent = 'Save result';
    saveBtn.addEventListener('click', () => saveJsonToFile(method, data));

    wrapper.appendChild(saveBtn);
    
    return wrapper;
}

function interpretDetermination(val) {
    const num = new Decimal(val).toNumber();
    if (isNaN(num)) return '';
    if (num == 1) return "Amazing result!";
    if (num >= 0.95) return 'High precision approximation';
    if (num >= 0.75) return 'Satisfactory approximation';
    if (num >= 0.5) return 'Weak approximation';
    if (num == -1) return "It is impossible to approximate these points with this function";
    return 'Model requires modification, approximation accuracy is inadequate';
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