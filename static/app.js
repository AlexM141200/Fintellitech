$(function () {
    // Get references to HTML elements
    var $chatWindow = $('#chat-window');
    var $userInput = $('#user-input');
    var $sendButton = $('#send-button');
    var $stockButton = $('.stock-button');

    // Send user message to server when send button is clicked
    $sendButton.on('click', function () {
        var message = $userInput.val().trim();
        if (message !== '') {
            sendMessage(message);
        }
    });


    $('.stock-button').click(function () {
        var stock_symbol = $(this).val().toLowerCase();
        var message = 'how has ' + stock_symbol + ' stock been doing?';
        sendMessage(message);
    });

    // ...




    // Send user message to server when enter key is pressed
    $userInput.on('keypress', function (event) {
        if (event.which === 13) {
            var message = $userInput.val().trim();
            if (message !== '') {
                sendMessage(message);
            }
        }
    });

    // Send user message to server and display response in chat window
    function sendMessage(message) {
        // Add user message to chat window
        console.log("message sent");
        $chatWindow.append('<p class="user-message">' + 'You: ' + message + '</p>');

        // Send message to server
        $.ajax({
            type: 'POST',
            url: '/chat',
            contentType: 'application/json',
            data: JSON.stringify({ message: message }),
            success: function (response) {
                // Add bot response to chat window
                $chatWindow.append('<p class="bot-message">' + 'Bot: ' + response.response + '</p>');

                // Clear user input field
                $userInput.val('');

                // Scroll chat window to bottom
                $chatWindow.scrollTop($chatWindow[0].scrollHeight);
            },
        });
    }
});

