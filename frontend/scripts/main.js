import {sendData} from './http.js'
import { createApproximationBlock, generateTable, createTabs } from './uiBuilder.js';

document.getElementById('sendButton').addEventListener('click', async () => {
    const response = await sendData();

    const container = document.getElementById('resultContainer');
    container.innerHTML = ''; 
    const tabData = [];

    for (const [method, data] of Object.entries(response)) {
        const block = createApproximationBlock(method, data);
        tabData.push({ title: method, content: block, isBest: data.best_approximation });
    }

    createTabs(container, tabData);
});

document.getElementById('points-count').addEventListener('change', async () => {
    generateTable();
});

window.onload = generateTable;