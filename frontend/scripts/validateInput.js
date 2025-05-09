export function validateInputs() {
    const inputs = document.querySelectorAll('#data-table input');
    let valid = true;

    inputs.forEach(input => {
        input.classList.remove('input-error');
        const existingMessage = input.parentElement.querySelector('.error-message');
        if (existingMessage) existingMessage.remove();

        const value = input.value.replace(',', '.');
        const number = parseFloat(value);

        if (isNaN(number)) {
            valid = false;
            input.classList.add('input-error');

            const msg = document.createElement('div');
            msg.className = 'error-message';
            msg.textContent = 'Enter a number';
            input.parentElement.appendChild(msg);
        }
    });

    return valid;
}

// export function showModal(message) {
//     let alertBox = document.getElementById('customAlertBox');
    
//     if (!alertBox) {
//         alertBox = document.createElement('div');
//         alertBox.id = 'customAlertBox';
//         alertBox.style.cssText = `
//             position: fixed;
//             top: 50%;
//             left: 50%;
//             transform: translate(-50%, -50%);
//             padding: 20px;
//             background: white;
//             border: 1px solid #ccc;
//             box-shadow: 0 4px 8px rgba(0,0,0,0.1);
//             z-index: 1000;
//             border-radius: 5px;
//             text-align: center;
//         `;
        
//         const messageEl = document.createElement('div');
//         messageEl.id = 'customAlertMessage';
//         messageEl.style.marginBottom = '15px';
        
//         const okButton = document.createElement('button');
//         okButton.textContent = 'OK';
//         okButton.style.cssText = `
//             padding: 5px 15px;
//             background: #007bff;
//             color: white;
//             border: none;
//             border-radius: 3px;
//             cursor: pointer;
//         `;
//         okButton.onclick = function() {
//             document.body.removeChild(alertBox);
//         };
        
//         alertBox.appendChild(messageEl);
//         alertBox.appendChild(okButton);
//         document.body.appendChild(alertBox);
//     }
    
//     document.getElementById('customAlertMessage').textContent = message;
// }


export function showModal(message) {
    let alertBox = document.getElementById('customAlertBox');
    let overlay = document.getElementById('modalOverlay');
    
    if (alertBox) document.body.removeChild(alertBox);
    if (overlay) document.body.removeChild(overlay);
    
    alertBox = document.createElement('div');
    alertBox.id = 'customAlertBox';
    alertBox.style.cssText = `
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%) scale(0.9);
        padding: 25px;
        background: #ffffff;
        border: none;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
        z-index: 1000;
        border-radius: 12px;
        text-align: center;
        max-width: 80%;
        width: 300px;
        opacity: 0;
        transition: all 0.3s ease-out;
        font-family: 'Segoe UI', Roboto, sans-serif;
    `;
    
    const messageEl = document.createElement('div');
    messageEl.id = 'customAlertMessage';
    messageEl.style.cssText = `
        margin-bottom: 20px;
        font-size: 16px;
        color: #333;
        line-height: 1.5;
    `;
    
    const okButton = document.createElement('button');
    okButton.textContent = 'OK';
    okButton.style.cssText = `
        padding: 8px 20px;
        background: #4a6bff;
        color: white;
        border: none;
        border-radius: 6px;
        cursor: pointer;
        font-size: 14px;
        font-weight: 500;
        transition: all 0.2s ease;
    `;
    
    okButton.onmouseover = function() {
        this.style.background = '#3a56e0';
        this.style.transform = 'translateY(-1px)';
    };
    
    okButton.onmouseout = function() {
        this.style.background = '#4a6bff';
        this.style.transform = 'translateY(0)';
    };
    
    const closeModal = () => {
        alertBox.style.opacity = '0';
        alertBox.style.transform = 'translate(-50%, -50%) scale(0.9)';
        if (overlay) overlay.style.opacity = '0';
        
        setTimeout(() => {
            if (alertBox.parentNode) document.body.removeChild(alertBox);
            if (overlay && overlay.parentNode) document.body.removeChild(overlay);
        }, 300);
    };
    
    okButton.onclick = closeModal;
    
    alertBox.appendChild(messageEl);
    alertBox.appendChild(okButton);
    document.body.appendChild(alertBox);
    
    messageEl.textContent = message;
    
    setTimeout(() => {
        alertBox.style.opacity = '1';
        alertBox.style.transform = 'translate(-50%, -50%) scale(1)';
    }, 10);
    
    overlay = document.createElement('div');
    overlay.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.5);
        z-index: 999;
        opacity: 0;
        transition: opacity 0.3s ease;
    `;
    overlay.id = 'modalOverlay';
    
    overlay.onclick = closeModal;
    
    document.body.appendChild(overlay);
    setTimeout(() => {
        overlay.style.opacity = '1';
    }, 10);
}