$(function () {

    var $chatWindow = $('#chat-window');
    var $userInput = $('#user-input');
    var $sendButton = $('#send-button');
    var $stockButton = $('.stock-button');

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

    $('.perception-button').click(function () {
        var company_name = $(this).val().toLowerCase();
        var message = 'public perception ' + company_name;
        sendMessage(message);
    });

    $('.price-button').click(function () {
        var symbol = $(this).val().toLowerCase();
        var message = 'what is ' + symbol + ' price at the minute?';
        sendMessage(message);
    });

    $('.risk-button').click(function () {
        var risk = $(this).val().toLowerCase();
        var message = 'i have a ' + risk + ' risk tolerance';
        sendMessage(message);
    });


    $userInput.on('keypress', function (event) {
        if (event.which === 13) {
            var message = $userInput.val().trim();
            if (message !== '') {
                sendMessage(message);
            }
        }
    });

    function sendMessage(message) {
        console.log("message sent");
        $chatWindow.append('<p class="user-message">' + 'You: ' + message + '</p>');

        $.ajax({
            type: 'POST',
            url: '/chat',
            contentType: 'application/json',
            data: JSON.stringify({ message: message }),
            success: function (response) {
                $chatWindow.append('<p class="bot-message">' + 'Bot: ' + response.response + '</p>');
                $userInput.val('');
                $chatWindow.scrollTop($chatWindow[0].scrollHeight);
            },
        });
    }
});

