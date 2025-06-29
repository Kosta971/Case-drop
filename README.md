# Case-drop
<!DOCTYPE html><html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>CaseBlitz</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    body { background: #0f172a; color: white; }
    .item { transition: transform 0.2s ease; }
    .item:hover { transform: scale(1.05); }
  </style>
</head>
<body class="p-4">
  <div class="text-center text-4xl font-bold mb-6">🎁 CaseBlitz</div>  <div class="text-center mb-4">
    💰 Balance: <span id="balance">1000</span>₽
    <button onclick="addFunds()" class="ml-4 px-3 py-1 bg-green-600 rounded hover:bg-green-700">Пополнить</button>
    <button onclick="loginUser()" class="ml-2 px-3 py-1 bg-slate-700 rounded hover:bg-slate-600">🔐 Войти</button>
  </div>  <div class="grid grid-cols-1 sm:grid-cols-4 gap-4">
    <div class="bg-slate-800 p-4 rounded-2xl shadow-xl text-center">
      <h2 class="text-xl font-semibold mb-2">Starter Case</h2>
      <p class="mb-2">Цена: 100₽</p>
      <button onclick="openCase(100, 'starter')" class="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded">Открыть</button>
    </div>
    <div class="bg-slate-800 p-4 rounded-2xl shadow-xl text-center">
      <h2 class="text-xl font-semibold mb-2">Epic Case</h2>
      <p class="mb-2">Цена: 300₽</p>
      <button onclick="openCase(300, 'epic')" class="px-4 py-2 bg-purple-600 hover:bg-purple-700 rounded">Открыть</button>
    </div>
    <div class="bg-slate-800 p-4 rounded-2xl shadow-xl text-center">
      <h2 class="text-xl font-semibold mb-2">Legendary Case</h2>
      <p class="mb-2">Цена: 600₽</p>
      <button onclick="openCase(600, 'legendary')" class="px-4 py-2 bg-yellow-500 hover:bg-yellow-600 rounded text-black">Открыть</button>
    </div>
    <div class="bg-slate-800 p-4 rounded-2xl shadow-xl text-center">
      <h2 class="text-xl font-semibold mb-2">Ultra Case</h2>
      <p class="mb-2">Цена: 1000₽</p>
      <button onclick="openCase(1000, 'ultra')" class="px-4 py-2 bg-red-500 hover:bg-red-600 rounded">Открыть</button>
    </div>
  </div>  <div class="mt-8 text-center">
    <h3 class="text-2xl mb-4">🧾 Твой дроп:</h3>
    <div id="dropResult" class="text-lg"></div>
  </div>  <div class="mt-10 text-center text-sm opacity-60">
    Сделано с ❤️ для проекта | Поддержать разработчика: <span class="font-bold">5168752028485707</span>
  </div>  <script>
    let balance = 1000;
    const balanceEl = document.getElementById('balance');
    const dropEl = document.getElementById('dropResult');

    const items = {
      starter: [
        { name: "Rusty Knife", price: 50 },
        { name: "Basic AK-47", price: 90 },
        { name: "Desert Camo", price: 150 },
        { name: "Speed Gloves", price: 200 }
      ],
      epic: [
        { name: "Neo Sniper", price: 300 },
        { name: "Fire Dragon AK", price: 350 },
        { name: "Storm Gloves", price: 500 },
        { name: "Shadow Dagger", price: 600 }
      ],
      legendary: [
        { name: "Golden AWP", price: 800 },
        { name: "Phoenix Gloves", price: 1000 },
        { name: "Electric Katana", price: 1200 },
        { name: "Dragon Lore", price: 1500 }
      ],
      ultra: [
        { name: "Galaxy Blade", price: 2000 },
        { name: "Quantum AWP", price: 2500 },
        { name: "Infernal Gloves", price: 3000 },
        { name: "Mythic Katana", price: 4000 }
      ]
    };

    function updateBalance() {
      balanceEl.innerText = balance;
    }

    function addFunds() {
      const amount = prompt("Введите сумму пополнения:", "500");
      if (amount) {
        balance += parseInt(amount);
        updateBalance();
      }
    }

    function openCase(price, type) {
      if (balance < price) {
        alert("Недостаточно средств!");
        return;
      }
      balance -= price;
      updateBalance();
      const pool = items[type];
      const won = pool[Math.floor(Math.random() * pool.length)];
      dropEl.innerHTML = `🎉 Тебе выпало: <strong>${won.name}</strong> за <strong>${won.price}₽</strong>`;
    }

    function loginUser() {
      const username = prompt("Введите имя пользователя:", "Player1");
      if (username) {
        alert(`Добро пожаловать, ${username}!`);
      }
    }
  </script></body>
</html>
