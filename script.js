// THEME SYSTEM
const colors = [
    '#a855f7', '#ec4899', '#ef4444', '#f59e0b', '#10b981', '#06b6d4', '#3b82f6', '#6366f1', 
    '#8b5cf6', '#d946ef', '#f43f5e', '#fb923c', '#22c55e', '#14b8a6', '#0ea5e9', '#4f46e5',
    '#c084fc', '#f472b6', '#fb7185', '#fbbf24', '#4ade80', '#22d3ee', '#60a5fa', '#818cf8',
    '#a78bfa', '#e879f9', '#fda4af', '#fcd34d', '#86efac', '#67e8f9', '#93c5fd', '#a5b4fc',
    '#c4b5fd', '#f5d0fe', '#fff1f2', '#fef3c7', '#dcfce7', '#ecfeff'
];

function initTheme() {
    const savedColor = localStorage.getItem('strivon-accent') || '#a855f7';
    const savedMode = localStorage.getItem('strivon-mode') || 'dark';
    
    setAccent(savedColor);
    setMode(savedMode);
    
    // Generate color grid
    const grid = document.getElementById('colorGrid');
    if (grid) {
        colors.forEach(c => {
            const dot = document.createElement('div');
            dot.className = 'color-dot' + (c === savedColor ? ' active' : '');
            dot.style.backgroundColor = c;
            dot.onclick = () => setAccent(c, dot);
            grid.appendChild(dot);
        });
    }

    // Event listeners
    const pickerToggle = document.getElementById('pickerToggle');
    const themePicker = document.getElementById('themePicker');
    const closePicker = document.getElementById('closePicker');
    const themeToggle = document.getElementById('themeToggle');

    if (pickerToggle) {
        pickerToggle.onclick = () => themePicker.classList.toggle('open');
    }
    if (closePicker) {
        closePicker.onclick = () => themePicker.classList.remove('open');
    }
    if (themeToggle) {
        themeToggle.onclick = () => {
            const newMode = document.body.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
            setMode(newMode);
        };
    }
}

function setAccent(color, el) {
    document.documentElement.style.setProperty('--accent', color);
    const rgb = hexToRgb(color);
    document.documentElement.style.setProperty('--accent-rgb', `${rgb.r}, ${rgb.g}, ${rgb.b}`);
    localStorage.setItem('strivon-accent', color);
    
    if (el) {
        document.querySelectorAll('.color-dot').forEach(d => d.classList.remove('active'));
        el.classList.add('active');
    }
}

function setMode(mode) {
    document.body.setAttribute('data-theme', mode);
    localStorage.setItem('strivon-mode', mode);
}

function hexToRgb(hex) {
    var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16)
    } : null;
}

// BOOSTER & STATS
function toggleBooster() {
    const boosterToggle = document.getElementById("boosterToggle");
    if (!boosterToggle) return;
    
    const isOn = boosterToggle.checked;
    const dashboard = document.querySelector(".dashboard");

    if (isOn) {
        if (dashboard) dashboard.style.borderColor = "var(--accent)";

        setTimeout(() => {
            const ramStat = document.getElementById('ramStat');
            const ramBar = document.getElementById('ramBar');
            if (ramStat) ramStat.textContent = '2.1GB';
            if (ramBar) ramBar.style.width = '12%';
        }, 800);

        setTimeout(() => {
            const cpuStat = document.getElementById('cpuStat');
            const cpuBar = document.getElementById('cpuBar');
            const fpsStat = document.getElementById('fpsStat');
            
            if (cpuStat) cpuStat.textContent = '2%';
            if (cpuBar) cpuBar.style.width = '2%';
            if (fpsStat) fpsStat.textContent = '+88%';
            showToast("🚀 Strivon Booster: Kernel-level optimizations active.");
        }, 1500);
    } else {
        statusStats();
        if (dashboard) dashboard.style.borderColor = "var(--border)";
    }
}

function statusStats() {
    const r = document.getElementById('ramStat');
    const c = document.getElementById('cpuStat');
    const rb = document.getElementById('ramBar');
    const cb = document.getElementById('cpuBar');

    if (r) r.textContent = (Math.random() * 4 + 8).toFixed(1) + 'GB';
    if (c) c.textContent = Math.round(Math.random() * 15 + 10) + '%';
    
    // Smoothly update bars if they exist
    if (rb) rb.style.width = Math.round(Math.random() * 20 + 60) + '%';
    if (cb) cb.style.width = Math.round(Math.random() * 10 + 70) + '%';
}

function showToast(msg) {
    const t = document.getElementById('toast');
    if (!t) return;
    t.textContent = msg;
    t.classList.add('show');
    setTimeout(() => t.classList.remove('show'), 3200);
}

function goScripts() { window.location.href = "scripts.html"; }

// Initialize
initTheme();
if (document.getElementById('ramStat')) {
    setInterval(statusStats, 3000);
}