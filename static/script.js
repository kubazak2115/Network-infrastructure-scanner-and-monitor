const REFRESH_INTERVAL = 30000;
let lastUpdated = null;

function barColor(pct) {
  if (pct >= 90) return 'danger';
  if (pct >= 70) return 'warn';
  return '';
}

function formatTimestamp(ts) {
  return new Date(ts).toLocaleString('en-GB', { dateStyle: 'short', timeStyle: 'short' });
}

function renderHosts(data) {
  const container = document.getElementById('hosts-container');
  const hosts = Object.values(data);

  if (!hosts.length) {
    container.innerHTML = '<div class="empty">No hosts found.</div>';
    return;
  }

  const badge = document.getElementById('hosts-badge');
  badge.textContent = hosts.length + ' host' + (hosts.length !== 1 ? 's' : '') + ' online';

  container.innerHTML = hosts.map(h => {
    const cpu      = h.cpu_used_pct ?? 0;
    const ram      = h.ram?.used_pct ?? 0;
    const ramUsed  = h.ram?.used_mb ?? 0;
    const ramTotal = h.ram?.total_mb ?? 0;

    const ifaces = Object.entries(h.interfaces || {}).map(([name, info]) => {
      const ip  = info.ip_address  ? `<strong>${info.ip_address}</strong>` : '';
      const mac = info.mac_address ? info.mac_address : '';
      return `<div>${name}${ip ? ' — ' + ip : ''}${mac ? ' | ' + mac : ''}</div>`;
    }).join('');

    return `
    <div class="card">
      <div class="host-header">
        <div>
          <div class="hostname">${h.hostname || h.host}</div>
          <div class="ip">${h.host}</div>
        </div>
        <span class="status-up">UP</span>
      </div>
      <div class="metric-row">
        <span class="label">CPU</span>
        <span class="val">${cpu.toFixed(1)}%</span>
      </div>
      <div class="bar-wrap">
        <div class="bar cpu ${barColor(cpu)}" style="width:${Math.min(cpu, 100)}%"></div>
      </div>
      <div class="metric-row">
        <span class="label">RAM</span>
        <span class="val">${ramUsed} / ${ramTotal} MB (${ram.toFixed(1)}%)</span>
      </div>
      <div class="bar-wrap">
        <div class="bar ram ${barColor(ram)}" style="width:${Math.min(ram, 100)}%"></div>
      </div>
      <div class="iface">${ifaces || '—'}</div>
      <div class="ts">${h.timestamp ? formatTimestamp(h.timestamp) : ''}</div>
    </div>`;
  }).join('');
}

async function fetchMetrics() {
  try {
    const res  = await fetch('/metrics');
    const data = await res.json();
    renderHosts(data);
    lastUpdated = new Date();
    document.getElementById('refresh-info').textContent = 'updated just now';
  } catch {
    document.getElementById('refresh-info').textContent = 'connection error';
  }
}

async function runScan() {
  const btn       = document.getElementById('scan-btn');
  const container = document.getElementById('scan-results');
  btn.disabled    = true;
  btn.textContent = 'Scanning...';
  container.innerHTML = '<div class="empty">Scanning network...</div>';

  try {
    const res   = await fetch('/scan');
    const data  = await res.json();
    const hosts = data.hosts || [];

    if (!hosts.length) {
      container.innerHTML = '<div class="empty">No hosts found.</div>';
      return;
    }

    container.innerHTML = `
      <table>
        <thead><tr><th>IP</th><th>Status</th><th>Open ports</th></tr></thead>
        <tbody>
          ${hosts.map(h => `
          <tr>
            <td>${h.ip}</td>
            <td><span class="pill ${h.alive ? 'up' : 'down'}">${h.alive ? 'UP' : 'DOWN'}</span></td>
            <td>${(h.open_ports || []).map(p => `<span class="pill port">${p}</span>`).join('') || '—'}</td>
          </tr>`).join('')}
        </tbody>
      </table>
      <div class="ts" style="margin-top:10px">Scanned: ${data.scanned}</div>`;
  } catch {
    container.innerHTML = '<div class="empty">Scan failed.</div>';
  } finally {
    btn.disabled    = false;
    btn.textContent = 'Run scan';
  }
}

setInterval(() => {
  if (!lastUpdated) return;
  const secs = Math.round((new Date() - lastUpdated) / 1000);
  document.getElementById('refresh-info').textContent =
    secs < 60 ? `updated ${secs}s ago` : `updated ${Math.round(secs / 60)}m ago`;
}, 5000);

fetchMetrics();
setInterval(fetchMetrics, REFRESH_INTERVAL);