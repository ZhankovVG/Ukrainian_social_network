function sendMessage(message) {
    chatSocket.send(JSON.stringify({
        'command': 'new_message',
        'message': message,
        'from': username,
        'friend': friendName,
    }));
}

function handleMessage(event) {
    const data = JSON.parse(event.data);
    if (data['command'] === 'new_message') {
        const message = data['message'];
        displayMessage(message);
    }
}

document.querySelector('#send-button').addEventListener('click', function () {
    const messageInput = document.querySelector('#message-input');
    const message = messageInput.value;
    sendMessage(message);

    messageInput.value = '';
});

const chatSocket = new WebSocket('ws://localhost:8000/ws/chat/{{ room.friend.id }}/');

const friendName = '{{ room.friend.username }}';
const username = '{{ request.user.username }}';

chatSocket.onmessage = handleMessage;

function displayMessage(message) {
    const chatMessages = document.querySelector('#chat-messages');
    const listItem = document.createElement('li');
    if (message.author === username) {
        listItem.textContent = 'Вы: ' + message.content;
    } else {
        listItem.textContent = friendName + ': ' + message.content;
    }
    chatMessages.appendChild(listItem);
}