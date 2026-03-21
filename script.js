function goScripts() {
    window.location.href = "scripts.html";
}

function comingSoon() {
    showToast("⚙️ This feature is coming soon. Stay tuned!");
}

function showToast(msg) {
    const t = document.getElementById('toast');
    if (!t) return;
    t.textContent = msg;
    t.classList.add('show');
    setTimeout(() => t.classList.remove('show'), 3200);
}

function toggleBooster() {
    const isOn = document.getElementById("boosterToggle").checked;
    const status = document.getElementById("boosterStatus");
    const dashboard = document.querySelector(".dashboard");

    if (isOn) {
        status.textContent = "Optimizing — freeing RAM and closing background tasks...";
        dashboard.classList.add("optimizing");

        // Simulate optimization sequence
        setTimeout(() => {
            document.getElementById('ramStat').textContent = '6.8GB';
            document.getElementById('ramBar').style.width = '58%';
            document.getElementById('ramPct').textContent = '58%';
        }, 800);

        setTimeout(() => {
            document.getElementById('cpuStat').textContent = '8%';
            document.getElementById('cpuBar').style.width = '8%';
            document.getElementById('cpuPct').textContent = '8%';
        }, 1400);

        setTimeout(() => {
            document.getElementById('fpsStat').textContent = '240+';
            dashboard.classList.remove("optimizing");
            status.textContent = "✓ Boosted — System optimized for max gaming performance";
            showToast("🚀 Boost complete! Max performance unlocked.");
        }, 2200);
    } else {
        status.textContent = "Idle — Toggle to start system optimization";
        document.getElementById('fpsStat').textContent = '144';
        // Resume live simulation
        updateStats();
    }
}

// Live stats simulation (for index.html)
function updateStats() {
    const booster = document.getElementById("boosterToggle");
    if (booster && booster.checked) return; // Don't override boosted state

    const ramFree = (Math.random() * 4 + 2.5).toFixed(1);
    const ramPct = Math.round((16 - parseFloat(ramFree)) / 16 * 100);
    const cpu = Math.round(Math.random() * 35 + 12);
    const ping = Math.round(Math.random() * 18 + 10);

    const r = document.getElementById('ramStat');
    const rp = document.getElementById('ramPct');
    const rb = document.getElementById('ramBar');
    const cs = document.getElementById('cpuStat');
    const cp = document.getElementById('cpuPct');
    const cb = document.getElementById('cpuBar');
    const pv = document.getElementById('pingVal');

    if (r) r.textContent = ramFree + 'GB';
    if (rp) rp.textContent = ramPct + '%';
    if (rb) rb.style.width = ramPct + '%';
    if (cs) cs.textContent = cpu + '%';
    if (cp) cp.textContent = cpu + '%';
    if (cb) cb.style.width = cpu + '%';
    if (pv) pv.textContent = ping + 'ms';
}

// Initialize live stats
updateStats();
setInterval(updateStats, 3000);