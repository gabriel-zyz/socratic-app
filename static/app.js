// Store chat history
let chatHistory = [];

// DOM Elements
const chatForm = document.getElementById("chatForm");
const messageInput = document.getElementById("messageInput");
const chatContainer = document.getElementById("chatContainer");

// Helper function to create message elements
function createMessageElement(message, isUser = false) {
  const messageDiv = document.createElement("div");
  messageDiv.className = `message ${isUser ? "user" : "tutor"}`;

  if (!isUser && message.category) {
    const categoryDiv = document.createElement("div");
    categoryDiv.className = "category";
    categoryDiv.textContent = message.category
      .replace(/_/g, " ")
      .replace(/\b\w/g, (c) => c.toUpperCase());
    messageDiv.appendChild(categoryDiv);
  }

  const contentDiv = document.createElement("div");
  contentDiv.className = "content";
  contentDiv.textContent = isUser
    ? message
    : message.content || message.response;
  messageDiv.appendChild(contentDiv);

  return messageDiv;
}

// Function to scroll to bottom of chat
function scrollToBottom() {
  // Use requestAnimationFrame to ensure DOM has updated
  requestAnimationFrame(() => {
    chatContainer.scrollTop = chatContainer.scrollHeight;
  });
}

// Function to add a message to the chat
function addMessage(message, isUser = false) {
  const messageElement = createMessageElement(message, isUser);
  chatContainer.appendChild(messageElement);
  scrollToBottom();

  // Add to chat history
  chatHistory.push({
    role: isUser ? "user" : "assistant",
    content: isUser ? message : message.response,
    ...(isUser ? {} : { category: message.category }),
  });
}

// Function to handle form submission
async function handleSubmit(e) {
  e.preventDefault();

  const message = messageInput.value.trim();
  if (!message) return;

  // Clear input
  messageInput.value = "";

  // Add user message to chat
  addMessage(message, true);

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
      }),
    });

    if (!response.ok) {
      throw new Error("Network response was not ok");
    }

    const data = await response.json();

    // Add tutor's response to chat
    addMessage(data);
  } catch (error) {
    console.error("Error:", error);
    addMessage({
      response: "I'm sorry, I'm having trouble connecting. Please try again.",
      category: "error",
    });
  }
}

// Event Listeners
chatForm.addEventListener("submit", handleSubmit);

// Handle enter key
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
