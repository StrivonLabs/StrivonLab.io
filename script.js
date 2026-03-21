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
    const isOn = document.getElementById("boosterToggle").checked;
    const status = document.getElementById("boosterStatus");
    const dashboard = document.querySelector(".dashboard");

    if (isOn) {
        status.textContent = "Optimizing — High Priority Set";
        dashboard.style.borderColor = "var(--accent)";

        setTimeout(() => {
            document.getElementById('ramStat').textContent = '4.2GB';
            document.getElementById('ramBar').style.width = '26%';
            document.getElementById('ramPct').textContent = '26%';
        }, 800);

        setTimeout(() => {
            document.getElementById('cpuStat').textContent = '5%';
            document.getElementById('cpuBar').style.width = '5%';
            document.getElementById('fpsStat').textContent = '360+';
            status.textContent = "✓ Optimized for Max Performance";
            showToast("🚀 Strivon Booster: System targets optimized.");
        }, 1500);
    } else {
        status.textContent = "Idle";
        statusStats();
    }
}

function statusStats() {
    const r = document.getElementById('ramStat');
    if (!r) return;
    r.textContent = (Math.random() * 8 + 4).toFixed(1) + 'GB';
    document.getElementById('cpuStat').textContent = Math.round(Math.random() * 20 + 5) + '%';
    document.getElementById('pingVal').textContent = Math.round(Math.random() * 15 + 8) + 'ms';
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