const API = import.meta.env?.VITE_API_URL || "http://localhost:5000";

async function load() {
    const res = await fetch(API + "/api/data");
    const data = await res.json();

    const list = document.getElementById("list");
    list.innerHTML = "";

    data.forEach(item => {
        const li = document.createElement("li");
        li.innerHTML = `${item[1]} <button onclick="del(${item[0]})">X</button>`;
        list.appendChild(li);
    });
}

async function add() {
    const name = document.getElementById("name").value;

    await fetch(API + "/api/data", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({name})
    });

    load();
}

async function del(id) {
    await fetch(API + "/api/data/" + id, {
        method: "DELETE"
    });

    load();
}

load();

