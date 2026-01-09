// =================== CONFIG ===================
const API_BASE = "http://127.0.0.1:8000";
const token = localStorage.getItem("access_token"); // Ensure you store token on login

if (!token) {
  alert("Please login first!");
  window.location.href = "login.html"; // redirect to login
}

// =================== LOGOUT ===================
function logout() {
  localStorage.removeItem("access_token");
  window.location.href = "login.html";
}

// =================== FETCH PREDICTIONS ===================
async function fetchHistory() {
  const res = await fetch(`${API_BASE}/admin/predictions/history`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) {
    alert("Failed to fetch prediction history");
    return [];
  }
  return await res.json();
}

async function fetchStats() {
  const res = await fetch(`${API_BASE}/admin/predictions/stats`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.ok ? await res.json() : { fake: 0, real: 0 };
}

async function fetchDaily() {
  const res = await fetch(`${API_BASE}/admin/predictions/daily`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.ok ? await res.json() : { labels: [], counts: [] };
}

async function fetchConfidence() {
  const res = await fetch(`${API_BASE}/admin/predictions/confidence`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.ok ? await res.json() : { confidence: [], counts: [] };
}

// =================== POPULATE TABLE ===================
async function populateTable() {
  const data = await fetchHistory();
  const tbody = document.getElementById("historyTable");
  tbody.innerHTML = "";

  data.forEach((item) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${item.id}</td>
      <td>${item.username}</td>
      <td>${item.prediction}</td>
      <td>${item.confidence}</td>
      <td>${item.created_at}</td>
    `;
    tbody.appendChild(tr);
  });
}

// =================== RENDER CHARTS ===================
async function renderCharts() {
  // Fake vs Real
  const stats = await fetchStats();
  new Chart(document.getElementById("statsChart"), {
    type: "pie",
    data: {
      labels: ["Fake", "Real"],
      datasets: [{
        data: [stats.fake, stats.real],
        backgroundColor: ["#e74c3c", "#27ae60"]
      }]
    }
  });

  // Daily Predictions
  const daily = await fetchDaily();
  new Chart(document.getElementById("dailyChart"), {
    type: "bar",
    data: {
      labels: daily.labels,
      datasets: [{
        label: "Predictions per day",
        data: daily.counts,
        backgroundColor: "#3498db"
      }]
    },
    options: {
      responsive: true,
      scales: { y: { beginAtZero: true } }
    }
  });

  // Confidence Distribution
  const conf = await fetchConfidence();
  new Chart(document.getElementById("confidenceChart"), {
    type: "line",
    data: {
      labels: conf.confidence,
      datasets: [{
        label: "Confidence count",
        data: conf.counts,
        backgroundColor: "rgba(52,152,219,0.2)",
        borderColor: "#2980b9",
        borderWidth: 2,
        fill: true
      }]
    },
    options: { responsive: true }
  });
}

// =================== EXPORT CSV ===================
async function exportCSV() {
  const res = await fetch(`${API_BASE}/admin/predictions/export`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) {
    alert("Failed to export CSV");
    return;
  }
  const blob = await res.blob();
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "predictions.csv";
  a.click();
  window.URL.revokeObjectURL(url);
}

// =================== INITIALIZE DASHBOARD ===================
async function init() {
  await populateTable();
  await renderCharts();
}

// Load dashboard
window.onload = init;
