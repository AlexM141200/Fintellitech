const chatWindow = document.getElementById('chat-window');
const output = document.getElementById('output');
const input = document.getElementById('input-message');
const submitButton = document.getElementById('submit-message');

submitButton.addEventListener('click', () => {
    // Get user input from the input field
    const message = input.value;

    // Send user input to the server
    fetch('/chat', {
        method: 'POST',
        body: JSON.stringify({ message }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then(response => response.json())
        .then(data => {
            // Display the response from the server
            output.innerHTML += `<p><strong>You:</strong> ${message}</p>`;
            console.log(message);
            output.innerHTML += `<p><strong>Bot:</strong> ${data.response}</p>`;
            chatWindow.scrollTop = chatWindow.scrollHeight;
        })
        .catch(error => console.error(error));

    // Clear the input field
    input.value = '';
});