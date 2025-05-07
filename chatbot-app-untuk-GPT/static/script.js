
document.getElementById("chat-form").addEventListener("submit", async function (e) {
  e.preventDefault();

  const input = document.getElementById("user-input");
  const chatBox = document.getElementById("chat-box");
  const userMessage = input.value.trim();

  if (!userMessage) return;

  chatBox.innerHTML += `<div class="message"><span class="user">Anda:</span> ${userMessage}</div>`;
  input.value = "";

  const response = await fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: userMessage }),
  });

  const data = await response.json();
  chatBox.innerHTML += `<div class="message"><span class="bot">Gemini:</span> ${data.response}</div>`;
  chatBox.scrollTop = chatBox.scrollHeight;
});
