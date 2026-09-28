const list = document.getElementById("task-list");
const form = document.getElementById("task-form");
const stats = document.getElementById("task-stats");
let tasks = [
  { id: 1, title: "Ship FastAPI CRUD", done: true },
  { id: 2, title: "Document Swagger paths", done: false },
  { id: 3, title: "Prove honest 404s", done: false },
];
let nextId = 4;
function render() {
  list.innerHTML = tasks.map(t => `<li><span>${t.done ? "✓ " : ""}${t.title}</span><button type="button" data-id="${t.id}">${t.done ? "open" : "done"}</button></li>`).join("");
  const done = tasks.filter(t => t.done).length;
  stats.textContent = `GET /stats → { total: ${tasks.length}, done: ${done}, open: ${tasks.length - done} }`;
  list.querySelectorAll("button").forEach(btn => btn.addEventListener("click", () => {
    const t = tasks.find(x => x.id === Number(btn.dataset.id));
    if (t) { t.done = !t.done; render(); }
  }));
}
form.addEventListener("submit", (e) => {
  e.preventDefault();
  const input = document.getElementById("task-title");
  const title = input.value.trim();
  if (!title) return;
  tasks.push({ id: nextId++, title, done: false });
  input.value = "";
  render();
});
render();
