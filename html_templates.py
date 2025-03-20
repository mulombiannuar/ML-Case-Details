css = '''
<style>
/* General chat container styling */
.chat-container {
    max-width: 800px;
    margin: auto;
    padding: 1rem;
    background-color: #f9f9f9;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* Chat message styling */
.chat-message {
    padding: 1rem;
    border-radius: 10px;
    margin-bottom: 1rem;
    display: flex;
    align-items: flex-start;
    max-width: 80%;
}

/* User message styling */
.chat-message.user {
    background-color: #0078d4;
    color: white;
    margin-left: auto; /* Align user messages to the right */
}

/* Bot message styling */
.chat-message.bot {
    background-color: #e1e1e1;
    color: #333;
    margin-right: auto; /* Align bot messages to the left */
}

/* Avatar styling */
.chat-message .avatar {
    width: 40px;
    height: 40px;
    margin-right: 1rem;
}

.chat-message .avatar img {
    width: 100%;
    height: 100%;
    border-radius: 50%;
    object-fit: cover;
}

/* Message text styling */
.chat-message .message {
    padding: 0.5rem 1rem;
    border-radius: 5px;
    font-size: 1rem;
    line-height: 1.4;
}

/* Timestamp styling (optional) */
.chat-message .timestamp {
    font-size: 0.75rem;
    color: #666;
    margin-top: 0.5rem;
    text-align: right;
}

/* Input area styling */
.chat-input {
    display: flex;
    gap: 0.5rem;
    margin-top: 1rem;
}

.chat-input input {
    flex: 1;
    padding: 0.75rem;
    border: 1px solid #ddd;
    border-radius: 5px;
    font-size: 1rem;
}

.chat-input button {
    padding: 0.75rem 1.5rem;
    background-color: #0078d4;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 1rem;
}

.chat-input button:hover {
    background-color: #005bb5;
}
</style>
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://i.ibb.co/cN0nmSj/Screenshot-2023-05-28-at-02-37-21.png">
    </div>
    <div class="message">{{MSG}}</div>
    <!-- Optional: Add a timestamp -->
    <div class="timestamp">Bot • Just now</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://i.ibb.co/rdZC7LZ/Photo-logo-1.png">
    </div>
    <div class="message">{{MSG}}</div>
    <!-- Optional: Add a timestamp -->
    <div class="timestamp">You • Just now</div>
</div>
'''