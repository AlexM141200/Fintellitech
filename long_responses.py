import random

R_EATING = "I don't like eating anything because I'm a bot obviously!"
R_ADVICE = "If I were you, I would go to the internet and type exactly what you wrote there!"
R_STOCK_X = "Stock X hasn't been looking good lately, I would maybe avoid it for a bit"
R_STOCK_Y = "Stock Y has been performing well! Remember that it may not last forever, though!"
R_STOCK_ADVICE = "Remember, when investing, it is all about minimizing risk. Slow and steady wins the race!"
R_FINTELLITECH = "Fintellitech is a great company, with cutting-edge artificial intelligence technology!"


def unknown():
    response = ["Could you please re-phrase that? ",
                "...",
                "Sounds about right.",
                "What does that mean?"][
        random.randrange(4)]
    return response
