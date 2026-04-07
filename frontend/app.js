const API_URL = "http://localhost:8000";

const ticketsEl = document.getElementById("tickets");
const historyEl = document.getElementById("history");
const productListEl = document.getElementById("productList");
const productSearchEl = document.getElementById("productSearch");

async function fetchJSON(path, options = {}) {
  const response = await fetch(`${API_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!response.ok) throw new Error(`Error ${response.status}`);
  return response.json();
}

function renderTicket(ticket) {
  return `
    <article class="ticket ${ticket.priority}">
      <div><strong>${ticket.customer_name}</strong> · ${new Date(ticket.created_at).toLocaleTimeString()}</div>
      <div>${ticket.message}</div>
      <div>Producto: <strong>${ticket.product_name ?? "Sin detectar"}</strong></div>
      <div>Estado: <span class="tag">${ticket.status}</span> · Prioridad: <span class="tag">${ticket.priority}</span></div>
      <div class="quick-actions">
        <button onclick="updateStatus(${ticket.id}, 'responded')">Respondido</button>
        <button onclick="updateStatus(${ticket.id}, 'reserved')">Reservado</button>
        <button onclick="updateStatus(${ticket.id}, 'sold')">Vendido</button>
      </div>
    </article>
  `;
}

function renderHistory(tickets) {
  historyEl.innerHTML = tickets
    .slice(0, 30)
    .map((t) => `<div>• ${t.customer_name}: ${t.message} (${t.status})</div>`)
    .join("");
}

async function refreshTickets() {
  const tickets = await fetchJSON("/tickets");
  ticketsEl.innerHTML = tickets.map(renderTicket).join("");
  renderHistory(tickets);
}

async function refreshProducts(query = "") {
  const products = await fetchJSON(`/products?search=${encodeURIComponent(query)}`);
  productListEl.innerHTML = products
    .map((p) => `<li>${p.name} · SKU ${p.sku} · $${p.price_ars} · Stock ${p.stock}</li>`)
    .join("");
}

async function createManualComment(event) {
  event.preventDefault();
  const customerName = document.getElementById("customerName").value;
  const message = document.getElementById("message").value;

  await fetchJSON("/comments", {
    method: "POST",
    body: JSON.stringify({ customer_name: customerName, message }),
  });

  event.target.reset();
  await refreshTickets();
}

async function simulateComment() {
  await fetchJSON("/simulate", { method: "POST" });
  await refreshTickets();
}

window.updateStatus = async (ticketId, status) => {
  await fetchJSON(`/tickets/${ticketId}/status`, {
    method: "PATCH",
    body: JSON.stringify({ status }),
  });
  await refreshTickets();
};

function connectWS() {
  const socket = new WebSocket("ws://localhost:8000/ws/live");
  socket.onopen = () => socket.send("frontend_connected");
  socket.onmessage = () => refreshTickets();
  socket.onclose = () => setTimeout(connectWS, 1500);
}

productSearchEl.addEventListener("input", (event) => refreshProducts(event.target.value));
document.getElementById("manualForm").addEventListener("submit", createManualComment);
document.getElementById("simulateBtn").addEventListener("click", simulateComment);

(async function init() {
  await refreshProducts();
  await refreshTickets();
  connectWS();
})();
