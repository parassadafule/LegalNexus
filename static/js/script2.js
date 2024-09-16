const chatbotToggler = document.querySelector(".chatbot-toggler");
const closeBtn = document.querySelector(".close-btn");
const chatbox = document.querySelector(".chatbox");
const chatInput = document.querySelector(".chat-input textarea");
const sendChatBtn = document.querySelector(".chat-input span");
let userMessage = null; // Variable to store user's message
const inputInitHeight = chatInput.scrollHeight;


const createChatLi = (message, className) => {
  // Create a chat <li> element with passed message and className
  const chatLi = document.createElement("li");
  chatLi.classList.add("chat", `${className}`);

  // Get the current time and date
  const now = new Date();
  const timeString = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  const dateString = now.toLocaleDateString();

  let chatContent = className === "outgoing" ? `<p></p> <span class="timestamp">${timeString}, ${dateString}</span>` : `<i class="fa-solid fa-volume-high icon"></i> <p></p><br><span class="timestamp">${timeString}, ${dateString}</span>`;
  chatLi.classList.add("icon");
  chatLi.innerHTML = chatContent;
  chatLi.querySelector("p").textContent = message;

  return chatLi; // return chat <li> element
}

const Ques_suggest = document.getElementsByClassName("Ques_suggest");

// Loop through each element in the collection
for (let i = 0; i < Ques_suggest.length; i++) {
  Ques_suggest[i].addEventListener("click", async () => {
    // alert("Hey, you clicked");
    chatInput.innerHTML = Ques_suggest[i].innerHTML;
    handleChat();
  });
}


const handleChat = () => {
  userMessage = chatInput.value.trim(); // Get user entered message and remove extra whitespace
  if (!userMessage) return;

  document.querySelector(".suggestion").style.display = "block"
  document.querySelector(".welcome").style.display = "none"
  document.querySelector(".suggest").style.display = "none"

  // Clear the input textarea and set its height to default
  chatInput.value = "";
  chatInput.style.height = `${inputInitHeight}px`;

  // Append the user's message to the chatbox
  chatbox.appendChild(createChatLi(userMessage, "outgoing"));
  chatbox.scrollTo(0, chatbox.scrollHeight);

  fetch('/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ query: userMessage }) // Send userMessage to backend
  })
    .then(response => response.json())
    .then(data => {
      finalResult = JSON.stringify(data.result).replace(/"/g, '');
      const incomingChatLi = createChatLi(finalResult, "incoming");
      chatbox.appendChild(incomingChatLi);
      chatbox.scrollTo(0, chatbox.scrollHeight);  // Scroll to bottom of chat
    })
    .catch(error => {
      console.error('Error:', error);
      const errorChatLi = createChatLi(data2, "incoming");
      chatbox.appendChild(errorChatLi);
      chatbox.scrollTo(0, chatbox.scrollHeight);
    });
}


chatInput.addEventListener("input", () => {
  // Adjust the height of the input textarea based on its content
  chatInput.style.height = `${inputInitHeight}px`;
  chatInput.style.height = `${chatInput.scrollHeight}px`;
});

chatInput.addEventListener("keydown", (e) => {
  // If Enter key is pressed without Shift key and the window 
  // width is greater than 800px, handle the chat
  if (e.key === "Enter" && !e.shiftKey && window.innerWidth > 800) {
    e.preventDefault();
    handleChat();
  }
});

sendChatBtn.addEventListener("click", handleChat);
closeBtn.addEventListener("click", () => document.body.classList.remove("show-chatbot"));
chatbotToggler.addEventListener("click", () => document.body.classList.toggle("show-chatbot"));

chatbox.addEventListener("click", (event) => {
  if (event.target && event.target.classList.contains("icon")) {
    const message = event.target.nextElementSibling.textContent;
    const utterance = new SpeechSynthesisUtterance(message);
    speechSynthesis.speak(utterance);
  }
});