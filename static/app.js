// Store chat history
let chatHistory = [];
let isCoLearnerActive = false;

// DOM Elements
const chatForm = document.getElementById("chatForm");
const messageInput = document.getElementById("messageInput");
const chatContainer = document.getElementById("chatContainer");
const coLearnerToggle = document.getElementById("coLearnerToggle");

// Helper function to create message elements
function createMessageElement(message, sender = "user") {
  const messageDiv = document.createElement("div");
  messageDiv.className = `message ${sender}`;

  // Add speaker label for all message types
  const speakerDiv = document.createElement("div");
  speakerDiv.className = `speaker ${sender}`;

  if (sender === "user") {
    speakerDiv.textContent = "👤 You";
  } else if (sender === "tutor") {
    speakerDiv.textContent = "🧑‍🏫 Tutor";
  } else if (sender === "colearner") {
    speakerDiv.textContent = "👦 Co-learner";
  }

  messageDiv.appendChild(speakerDiv);

  // Add category for tutor messages
  if (sender === "tutor" && message.category) {
    const categoryDiv = document.createElement("div");
    categoryDiv.className = "category";
    categoryDiv.textContent = message.category
      .replace(/_/g, " ")
      .replace(/\b\w/g, (c) => c.toUpperCase());
    messageDiv.appendChild(categoryDiv);
  }

  const contentDiv = document.createElement("div");
  contentDiv.className = "content";
  contentDiv.textContent =
    sender === "user"
      ? message
      : message.content || message.response || message;
  messageDiv.appendChild(contentDiv);

  return messageDiv;
}

// Function to scroll to bottom of chat
function scrollToBottom() {
  // Use setTimeout to ensure DOM has updated
  setTimeout(() => {
    chatContainer.scrollTop = chatContainer.scrollHeight;
  }, 10);
}

// Function to add a message to the chat
function addMessage(message, sender = "user") {
  const messageElement = createMessageElement(message, sender);
  chatContainer.appendChild(messageElement);
  scrollToBottom();

  // Add to chat history only for user and tutor
  if (sender === "user" || sender === "tutor") {
    chatHistory.push({
      role: sender === "user" ? "user" : "assistant",
      content:
        sender === "user" ? message : message.response || message.content,
      ...(sender === "tutor" && message.category
        ? { category: message.category }
        : {}),
    });
  }
}

// Function to show typing indicator
function showTypingIndicator(sender = "tutor") {
  const typingDiv = document.createElement("div");
  typingDiv.className = "typing-indicator";
  typingDiv.id = `typing-${sender}`;

  // Add speaker label for both tutor and co-learner
  const speakerDiv = document.createElement("div");
  speakerDiv.className = `speaker ${sender}`;
  speakerDiv.textContent = sender === "tutor" ? "🧑‍🏫 Tutor" : "👦 Co-learner";
  speakerDiv.style.marginBottom = "0.5rem";
  typingDiv.appendChild(speakerDiv);

  const dotsContainer = document.createElement("div");
  dotsContainer.style.display = "flex";
  dotsContainer.style.gap = "4px";

  for (let i = 0; i < 3; i++) {
    const dot = document.createElement("div");
    dot.className = "typing-dot";
    dotsContainer.appendChild(dot);
  }

  typingDiv.appendChild(dotsContainer);
  chatContainer.appendChild(typingDiv);
  scrollToBottom();

  return typingDiv;
}

// Function to remove typing indicator
function removeTypingIndicator(sender = "tutor") {
  const indicator = document.getElementById(`typing-${sender}`);
  if (indicator) {
    indicator.remove();
  }
}

// Function to handle form submission
async function handleSubmit(e) {
  e.preventDefault();

  const message = messageInput.value.trim();
  if (!message) return;

  // Clear input
  messageInput.value = "";

  // Add user message to chat
  addMessage(message, "user");

  // Show typing indicators
  const tutorTyping = showTypingIndicator("tutor");
  let colearnerTyping = null;

  if (isCoLearnerActive) {
    colearnerTyping = showTypingIndicator("colearner");
  }

  try {
    // Send message to backend
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        messages: chatHistory,
        new_message: message,
        include_colearner: isCoLearnerActive,
      }),
    });

    if (!response.ok) {
      throw new Error("Network response was not ok");
    }

    const data = await response.json();

    // Remove typing indicators
    removeTypingIndicator("tutor");
    if (colearnerTyping) {
      removeTypingIndicator("colearner");
    }

    // Add tutor's response
    addMessage(data, "tutor");

    // Add co-learner's response if available
    if (data.colearner_response) {
      // Small delay to make it feel more natural
      setTimeout(() => {
        addMessage(data.colearner_response, "colearner");
      }, 800);
    }
  } catch (error) {
    console.error("Error:", error);
    removeTypingIndicator("tutor");
    if (colearnerTyping) {
      removeTypingIndicator("colearner");
    }

    addMessage(
      {
        response: "I'm sorry, I'm having trouble connecting. Please try again.",
        category: "error",
      },
      "tutor"
    );
  }
}

// Handle co-learner toggle
function handleCoLearnerToggle() {
  isCoLearnerActive = coLearnerToggle.checked;

  if (isCoLearnerActive) {
    // Add a message to indicate co-learner joined
    const joinMessage = document.createElement("div");
    joinMessage.style.textAlign = "center";
    joinMessage.style.padding = "1rem";
    joinMessage.style.color = "#666";
    joinMessage.style.fontStyle = "italic";
    joinMessage.innerHTML = "👦 A co-learner has joined the chat!";
    chatContainer.appendChild(joinMessage);
    scrollToBottom();
  } else {
    // Add a message to indicate co-learner left
    const leaveMessage = document.createElement("div");
    leaveMessage.style.textAlign = "center";
    leaveMessage.style.padding = "1rem";
    leaveMessage.style.color = "#666";
    leaveMessage.style.fontStyle = "italic";
    leaveMessage.innerHTML = "👦 Co-learner has left the chat.";
    chatContainer.appendChild(leaveMessage);
    scrollToBottom();
  }
}

// Event Listeners
chatForm.addEventListener("submit", handleSubmit);
coLearnerToggle.addEventListener("change", handleCoLearnerToggle);

// Handle enter key in chat
messageInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    chatForm.dispatchEvent(new Event("submit"));
  }
});

// Focus input on page load
messageInput.focus();

// Ensure proper scrolling when window is resized
window.addEventListener("resize", scrollToBottom);

// Initial scroll position
scrollToBottom();
