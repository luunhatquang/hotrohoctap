// ChatGPT-style Chat AI - Basic Structure for API Integration
const chatMessages = document.getElementById('chatMessages');
const chatInput = document.getElementById('chatInput');
const sendButton = document.getElementById('sendButton');
const emptyState = document.getElementById('emptyState');
const messagesContainer = document.getElementById('messagesContainer');

let conversationId = null; // Track current conversation

// Auto-resize textarea
chatInput.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = Math.min(this.scrollHeight, 200) + 'px';
});

// Handle input changes
function handleInput() {
    const hasText = chatInput.value.trim().length > 0;
    sendButton.disabled = !hasText;
    sendButton.classList.toggle('active', hasText);
}

// Handle Enter key
function handleKeyPress(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

// Clear chat
function clearChat() {
    if (confirm('Bạn có chắc muốn xóa toàn bộ cuộc trò chuyện này?')) {
        messagesContainer.innerHTML = '';
        emptyState.style.display = 'flex';
        chatInput.value = '';
        chatInput.style.height = 'auto';
        conversationId = null; // Reset conversation
        handleInput();
    }
}

// Send message - Real API Integration
async function sendMessage() {
    const message = chatInput.value.trim();
    
    if (!message) return;

    // Hide empty state
    if (emptyState) {
        emptyState.style.display = 'none';
    }

    // Add user message
    addMessage(message, 'user');
    
    // Clear input
    chatInput.value = '';
    chatInput.style.height = 'auto';
    handleInput();
    
    // Disable send button
    sendButton.disabled = true;
    
    // Show AI typing indicator
    showTypingIndicator();
    
    // Call real API
    try {
        const aiResponse = await callAIAPI(message);
        hideTypingIndicator();
        addMessage(aiResponse, 'ai');
    } catch (error) {
        hideTypingIndicator();
        addMessage('Xin lỗi, đã có lỗi xảy ra khi kết nối với AI. Vui lòng thử lại.', 'ai');
        console.error('AI API Error:', error);
    } finally {
        sendButton.disabled = false;
        chatInput.focus();
    }
}

// Add message to chat
function addMessage(text, sender) {
    const messageRow = document.createElement('div');
    messageRow.className = `message-row ${sender}-message`;
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    
    if (sender === 'user') {
        avatar.innerHTML = '<i class="fas fa-user"></i>';
    } else {
        avatar.innerHTML = '<i class="fas fa-robot"></i>';
    }
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    
    const author = document.createElement('div');
    author.className = 'message-author';
    author.textContent = sender === 'user' ? 'Bạn' : 'AI Trợ Lý';
    
    const messageText = document.createElement('div');
    messageText.className = 'message-text';
    messageText.innerHTML = formatMessage(text);
    
    messageContent.appendChild(author);
    messageContent.appendChild(messageText);
    
    if (sender === 'ai') {
        const actions = document.createElement('div');
        actions.className = 'message-actions';
        actions.innerHTML = `
            <button class="message-action-btn" onclick="copyMessage(this)">
                <i class="fas fa-copy"></i> Sao chép
            </button>
        `;
        messageContent.appendChild(actions);
    }
    
    messageRow.appendChild(avatar);
    messageRow.appendChild(messageContent);
    
    messagesContainer.appendChild(messageRow);
    scrollToBottom();
}

// Show typing indicator
function showTypingIndicator() {
    const typingRow = document.createElement('div');
    typingRow.className = 'message-row ai-message';
    typingRow.id = 'typingIndicator';
    
    typingRow.innerHTML = `
        <div class="message-avatar">
            <i class="fas fa-robot"></i>
        </div>
        <div class="message-content">
            <div class="message-author">AI Trợ Lý</div>
            <div class="typing-indicator active">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        </div>
    `;
    
    messagesContainer.appendChild(typingRow);
    scrollToBottom();
}

// Hide typing indicator
function hideTypingIndicator() {
    const typing = document.getElementById('typingIndicator');
    if (typing) {
        typing.remove();
    }
}

// Format message text
function formatMessage(text) {
    // Convert line breaks to <br>
    text = text.replace(/\n/g, '<br>');
    
    // Bold text **text**
    text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    // Italic text *text*
    text = text.replace(/\*(.*?)\*/g, '<em>$1</em>');
    
    // Bullet points
    text = text.replace(/^• (.+)$/gm, '<li>$1</li>');
    if (text.includes('<li>')) {
        text = text.replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>');
    }
    
    return text;
}

// Copy message
function copyMessage(button) {
    const messageText = button.closest('.message-content').querySelector('.message-text').innerText;
    navigator.clipboard.writeText(messageText).then(() => {
        const originalHTML = button.innerHTML;
        button.innerHTML = '<i class="fas fa-check"></i> Đã sao chép';
        setTimeout(() => {
            button.innerHTML = originalHTML;
        }, 2000);
    });
}

// Scroll to bottom
function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Initial focus
chatInput.focus();

// Call AI API
async function callAIAPI(message) {
    try {
        const response = await fetch('/chat-ai/api/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ 
                message: message,
                conversation_id: conversationId
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.success) {
            // Update conversation ID for next messages
            conversationId = data.conversation_id;
            return data.response;
        } else {
            throw new Error(data.error || 'Unknown error');
        }
    } catch (error) {
        console.error('Error calling AI API:', error);
        throw error;
    }
}

// Get CSRF Token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
