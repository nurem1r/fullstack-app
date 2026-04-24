const API_URL = window.location.origin.includes("localhost")
  ? "http://localhost:5000"
  : import.meta?.env?.VITE_API_URL || "";

async function loadData() {
    const res = await fetch(`${API_URL}/api/data`);
    const data = await res.json();

    const list = document.getElementById("list");
    list.innerHTML = "";

    data.forEach(item => {
        const li = document.createElement("li");
        li.textContent = item.name;

        const btn = document.createElement("button");
        btn.textContent = "Delete";
        btn.onclick = () => deleteStudent(item.id);

        li.appendChild(btn);
        list.appendChild(li);
    });
}

async function addStudent() {
    const name = document.getElementById("nameInput").value;

    await fetch(`${API_URL}/api/data`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ name })
    });

    loadData();
}

async function deleteStudent(id) {
    await fetch(`${API_URL}/api/data/${id}`, {
        method: "DELETE"
    });

    loadData();
}

loadData();
