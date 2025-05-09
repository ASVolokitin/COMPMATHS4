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
