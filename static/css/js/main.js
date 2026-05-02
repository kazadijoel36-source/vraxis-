document.addEventListener('DOMContentLoaded', () => {
    const textarea = document.querySelector('textarea');
    const charCountDisplay = document.querySelector('.char-count');

    if (textarea) {
        textarea.addEventListener('input', (e) => {
            const count = e.target.value.length;
            // Update the char count in the header if you have one
            if (charCountDisplay) {
                charCountDisplay.textContent = `${count} chars`;
            }
        });
    }

    // Logic for expiry buttons
    const expiryButtons = document.querySelectorAll('.expiry-btn');
    expiryButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            expiryButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
        });
    });
});
document.addEventListener('DOMContentLoaded', () => {
    const textarea = document.querySelector('textarea');
    const charCountDisplay = document.querySelector('.char-count');
    const expiryButtons = document.querySelectorAll('.expiry-btn');
    const hiddenExpiryInput = document.createElement('input');
    
    // Setup hidden input to track expiry choice
    hiddenExpiryInput.type = 'hidden';
    hiddenExpiryInput.name = 'expiry';
    hiddenExpiryInput.value = '24h';
    document.querySelector('form').appendChild(hiddenExpiryInput);

    if (textarea && charCountDisplay) {
        textarea.addEventListener('input', (e) => {
            charCountDisplay.textContent = `${e.target.value.length} chars`;
        });
    }

    expiryButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            expiryButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            // Update hidden input based on text (1h, 24h, 7d)
            hiddenExpiryInput.value = btn.textContent.includes('1h') ? '1h' : 
                                     btn.textContent.includes('7d') ? '7d' : '24h';
        });
    });
});