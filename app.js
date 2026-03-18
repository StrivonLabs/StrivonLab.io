let allData = [];

fetch("data.json")
    .then(res => res.json())
    .then(data => {
        allData = data;
        display(data);
    });

function display(data) {
    const container = document.getElementById("content");
    container.innerHTML = "";

    data.forEach(item => {
        const card = document.createElement("div");
        card.className = "card";

        card.innerHTML = `
      <div class="card-header">
        <i class="fas ${item.icon}"></i>
        <h3>${item.title}</h3>
      </div>
      <p>${item.description}</p>
      <small>${item.category}</small>
    `;

        container.appendChild(card);
    });
}

function filter(category) {
    if (category === "all") {
        display(allData);
    } else {
        display(allData.filter(item => item.category === category));
    }
}