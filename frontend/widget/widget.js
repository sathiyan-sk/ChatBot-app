(function() {
  // Prevent duplicate load
  if (window.OceanRAGWidgetLoaded) return;
  window.OceanRAGWidgetLoaded = true;

  // Retrieve embed configurations
  const config = window.OceanRAGWidgetConfig || {
    apiKey: "",
    appId: "default-app",
    backendUrl: window.location.origin
  };

  const API_URL = config.backendUrl || window.location.origin;

  // Load css stylesheet dynamically
  const link = document.createElement("link");
  link.rel = "stylesheet";
  link.href = API_URL + "/widget/widget.css";
  document.head.appendChild(link);

  let widgetTheme = "#00D4FF";
  let greetingMessage = "Hello! Ask me any questions about our policies.";

  // Setup widget container
  const container = document.createElement("div");
  container.id = "oceanrag-widget-root";
  document.body.appendChild(container);

  // Inject HTML Elements
  container.innerHTML = `
    <!-- Floating Circular Launcher -->
    <button id="oceanrag-launcher" class="oceanrag-launcher" title="Chat with Assistant" data-testid="widget-launcher-btn">
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="oceanrag-icon"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
    </button>

    <!-- Chat Box Window panel -->
    <div id="oceanrag-chatbox" class="oceanrag-chatbox oceanrag-hidden" data-testid="widget-chatbox">
      <div id="oceanrag-header" class="oceanrag-header">
        <div class="oceanrag-header-brand">
          <span class="oceanrag-pulse-dot"></span>
          <span id="oceanrag-title" class="oceanrag-title">OceanRAG Client Widget</span>
        </div>
        <button id="oceanrag-close-btn" class="oceanrag-close-btn" title="Minimize Chat">&times;</button>
      </div>

      <div id="oceanrag-messages" class="oceanrag-messages"></div>

      <form id="oceanrag-input-form" class="oceanrag-input-form">
        <input type="text" id="oceanrag-text-input" placeholder="Type query details..." required data-testid="widget-chat-input" />
        <button type="submit" id="oceanrag-send-btn" class="oceanrag-send-btn" data-testid="widget-chat-submit">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg>
        </button>
      </form>
    </div>
  `;

  // Grab nodes
  const launcher = document.getElementById("oceanrag-launcher");
  const chatbox = document.getElementById("oceanrag-chatbox");
  const closeBtn = document.getElementById("oceanrag-close-btn");
  const textInput = document.getElementById("oceanrag-text-input");
  const form = document.getElementById("oceanrag-input-form");
  const messagesBox = document.getElementById("oceanrag-messages");
  const header = document.getElementById("oceanrag-header");

  // Fetch widget customized styles from backend contract
  async function loadWidgetSettings() {
    try {
      const response = await fetch(`${API_URL}/api/widget?app_id=${config.appId}`);
      if (response.ok) {
        const data = await response.json();
        widgetTheme = data.theme_color || "#00D4FF";
        greetingMessage = data.greeting_message || "Hello! Ask me any questions.";
        
        // Apply styling variables dynamically
        launcher.style.backgroundColor = widgetTheme;
        header.style.backgroundColor = widgetTheme;
        
        if (data.launcher_position === "bottom-left") {
          launcher.style.right = "auto";
          launcher.style.left = "24px";
          chatbox.style.right = "auto";
          chatbox.style.left = "24px";
        }
      }
    } catch (e) {
      console.warn("Could not sync custom widget settings.", e);
    }
    
    // Welcome Greeting Prompt
    addMessage(greetingMessage, "bot");
  }

  loadWidgetSettings();

  // Launcher Events
  launcher.addEventListener("click", () => {
    chatbox.classList.toggle("oceanrag-hidden");
    if (!chatbox.classList.contains("oceanrag-hidden")) {
      textInput.focus();
    }
  });

  closeBtn.addEventListener("click", () => {
    chatbox.classList.add("oceanrag-hidden");
  });

  // Render text bubble
  function addMessage(text, sender, sources = []) {
    const bubble = document.createElement("div");
    bubble.className = `oceanrag-msg-row oceanrag-msg-${sender}`;
    
    // Simulate formatting
    let formattedText = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    formattedText = formattedText.split('\n').join('<br/>');

    bubble.innerHTML = `
      <div class="oceanrag-bubble">
        ${formattedText}
      </div>
    `;

    // Render source segments
    if (sources && sources.length > 0) {
      const sourcesDiv = document.createElement("div");
      sourcesDiv.className = "oceanrag-sources-list";
      sourcesDiv.innerHTML = `<span class="sources-title">Verified citations:</span>`;
      sources.forEach(src => {
        const item = document.createElement("div");
        item.className = "source-item";
        item.innerHTML = `
          <div class="source-item-meta">File: ${src.source_file || "Context"} • Score ${(src.score * 100).toFixed(0)}%</div>
          <div class="source-item-text">"${src.text}"</div>
        `;
        sourcesDiv.appendChild(item);
      });
      bubble.appendChild(sourcesDiv);
    }

    messagesBox.appendChild(bubble);
    messagesBox.scrollTop = messagesBox.scrollHeight;
  }

  // Handle queries
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const query = textInput.value.trim();
    if (!query) return;

    addMessage(query, "user");
    textInput.value = "";

    // Show searching bubble
    const thinkingRow = document.createElement("div");
    thinkingRow.className = "oceanrag-msg-row oceanrag-msg-bot oceanrag-thinking-row";
    thinkingRow.innerHTML = `
      <div class="oceanrag-bubble typing">
        <span class="dot"></span>
        <span class="dot"></span>
        <span class="dot"></span>
      </div>
    `;
    messagesBox.appendChild(thinkingRow);
    messagesBox.scrollTop = messagesBox.scrollHeight;

    try {
      const response = await fetch(`${API_URL}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          question: query,
          app_id: config.appId,
          top_k: 4
        })
      });

      // Remove thinking
      thinkingRow.remove();

      if (response.ok) {
        const data = await response.json();
        addMessage(data.answer, "bot", data.sources);
      } else {
        addMessage("⚠️ Failed to parse API contract mapping.", "bot");
      }
    } catch (err) {
      thinkingRow.remove();
      addMessage("⚠️ Connection error with FastAPI RAG server.", "bot");
    }
  });

})();
