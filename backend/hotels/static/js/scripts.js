// Dark/Light Mode Toggler
document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('theme-toggle');
    const userPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

    // Check user preference and set theme
    if (userPrefersDark) {
        document.documentElement.classList.add('dark');
        themeToggle.textContent = 'L';
    } else {
        document.documentElement.classList.add('light');
        themeToggle.textContent = 'D';
    }

    themeToggle.onclick = () => {
        document.documentElement.classList.toggle('dark');
        document.documentElement.classList.toggle('light');
        themeToggle.textContent = document.documentElement.classList.contains('dark') ? '☀️' : '🌙';
    };
});

// Mehmonlar sonini ± bilan boshqarish animatsiyasi
function adjust(field, diff) {
    const input = document.getElementById('id_' + field);
    let val = parseInt(input.value);
    val += diff;
    if (field === 'adults') val = Math.max(1, val);
    else val = Math.max(0, val);
    input.value = val;

    input.classList.add('pulse');
    setTimeout(() => input.classList.remove('pulse'), 200);
}

// Mehmonlar inputiga "pulse" animatsiyasi
document.querySelectorAll('input[type="number"]').forEach(input => {
    input.addEventListener('input', () => {
        input.classList.add('pulse');
        setTimeout(() => input.classList.remove('pulse'), 200);
    });
});
