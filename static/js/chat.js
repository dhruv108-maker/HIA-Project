document.addEventListener("DOMContentLoaded", () => {
  const chatForm = document.getElementById("chat-form");
  const userInput = document.getElementById("user-input");
  const chatBox = document.getElementById("chat-box");
  const toggleSidebar = document.getElementById("toggle-sidebar");

  toggleSidebar.onclick = () => {
    document.querySelector('.sidebar').classList.toggle('collapsed');
  };

  chatForm.onsubmit = async (e) => {
    e.preventDefault();
    const message = userInput.value.trim();
    if (!message) return;

    const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    chatBox.innerHTML += `
      <div class="message user">
        <div class="bubble">${message}<span class="time">${time}</span></div>
        <div class="avatar"><i class="fas fa-user"></i></div>
      </div>
    `;
    chatBox.scrollTop = chatBox.scrollHeight;
    userInput.value = "";

    const response = await fetch("/send_message", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message })
    });
    const data = await response.json();
    const botTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    chatBox.innerHTML += `
      <div class="message bot">
        <div class="avatar bot"><i class="fas fa-robot"></i></div>
        <div class="bubble">${data.reply}<span class="time">${botTime}</span></div>
      </div>
    `;
    chatBox.scrollTop = chatBox.scrollHeight;
  };
});


const toggleSidebar = document.getElementById("toggle-sidebar");
const sidebar = document.querySelector('.sidebar');

toggleSidebar.onclick = () => {
  sidebar.classList.toggle('collapsed');
};

const overlay = document.getElementById("overlay");

toggleSidebar.onclick = () => {
  sidebar.classList.toggle('collapsed');
  overlay.style.display = sidebar.classList.contains('collapsed') ? 'none' : 'block';
};

overlay.onclick = () => {
  sidebar.classList.add('collapsed');
  overlay.style.display = 'none';
};


