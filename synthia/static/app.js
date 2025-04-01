function showPage(id) {
    document.querySelectorAll('.page').forEach(page => {
      page.classList.remove('active');
    });
    document.getElementById(id).classList.add('active');
  }
  
  // Default to main
  showPage('main');
  
  // --- 🧠 Synthia Chat UI + Logic ---
  document.addEventListener("DOMContentLoaded", () => {
    const mainPage = document.getElementById("main");
  
    const form = document.createElement("form");
    form.innerHTML = `
      <h2>Chat with Synthia</h2>
      <input id="prompt" placeholder="Say something..." style="width:80%;padding:0.5em;margin-top:1em;" />
      <button type="submit" style="padding:0.5em 1em;margin-left:0.5em;">Send</button>
      <div id="response" style="margin-top:1em;background:#333;padding:1em;border-radius:6px;"></div>
    `;
  
    mainPage.appendChild(form);
  
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
  
      const input = document.getElementById("prompt");
      const responseBox = document.getElementById("response");
      const prompt = input.value.trim();
  
      if (!prompt) return;
  
      responseBox.innerHTML = "Thinking... 🤔";
      input.disabled = true;
  
      const formData = new FormData();
      formData.append("prompt", prompt);
  
      try {
        const res = await fetch("/api/chat", {
          method: "POST",
          body: formData,
        });
        const data = await res.json();
        responseBox.innerHTML = data.reply
          ? `<strong>Synthia:</strong> ${data.reply}`
          : `<span style="color:red;">❌ ${data.error || "No response."}</span>`;
      } catch (err) {
        responseBox.innerHTML = `<span style="color:red;">🚫 Failed to contact backend</span>`;
      }
  
      input.disabled = false;
      input.value = "";
      input.focus();
    });
  });
  