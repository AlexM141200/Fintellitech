import re
import requests
import long_responses as long
import subprocess

ALPHA_VANTAGE_API_KEY = 'RKH0BMX3MUBVLOY7'
ALPHA_VANTAGE_API_ENDPOINT = 'https://www.alphavantage.co/query'

companies = ['Apple', 'Microsoft', 'Amazon', 'Tesla']


def get_stock_data(symbol):
    params = {
        'function': 'TIME_SERIES_DAILY_ADJUSTED',
        'symbol': symbol,
        'apikey': ALPHA_VANTAGE_API_KEY,
    }
    response = requests.get(ALPHA_VANTAGE_API_ENDPOINT, params=params)
    data = response.json()

    if 'Time Series (Daily)' not in data:
        return None

    daily_data = data['Time Series (Daily)']
    daily_close = [float(daily_data[date]['4. close']) for date in daily_data]
    return {
        'symbol': symbol.upper(),
        'change': daily_close[0] - daily_close[-1],
        'percent_change': (daily_close[0] - daily_close[-1]) / daily_close[-1] * 100,
    }


def message_probability(user_message, recognised_words, single_response=False, required_words=[]):
    message_certainty = 0
    has_required_words = True

    # Counts how many words are present in each predefined message
    for word in user_message:
        if word in recognised_words:
            message_certainty += 1

    # Calculates the percent of recognised words in a user message
    percentage = float(message_certainty) / float(len(recognised_words))

    # Checks that the required words are in the string
    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break

    # Must either have the required words, or be a single response
    if has_required_words or single_response:
        return int(percentage * 100)
    else:
        return 0


def check_all_messages(message):
    highest_prob_list = {}

    # Simplifies response creation / adds it to the dict
    def response(bot_response, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob_list
        highest_prob_list[bot_response] = message_probability(
            message, list_of_words, single_response, required_words)

    # Responses -------------------------------------------------------------------------------------------------------
    response('Hello!', ['hello', 'hi', 'hey',
             'sup', 'heyo'], single_response=True)
    response('See you!', ['bye', 'goodbye'], single_response=True)
    # response('I\'m doing fine, and you?', ['how', 'are', 'you', 'doing'], required_words=['how'])
    response('You\'re welcome!', ['thank', 'thanks'], single_response=True)
    response('Thank you!', ['i', 'love', 'code', 'palace'],
             required_words=['code', 'palace'])
    response('The markets are doing positively recently!',
             ['how', 'markets', 'look' 'positive', 'in'], required_words=['markets', ])

    # Get stock data based on user input
    split_message = [word.lower() for word in message]
    if "how" in split_message and "has" in split_message and "been" in split_message:
        stock_index = split_message.index("stock") - 1 if "stock" in split_message else split_message.index(
            "stocks") - 1 if "stocks" in split_message else -1
        if stock_index != -1 and len(split_message) > stock_index:
            stock_data = get_stock_data(split_message[stock_index])
            print(stock_data)
            if stock_data is not None:
                response(
                    f"{stock_data['symbol']} has changed by {stock_data['change']} ({stock_data['percent_change']}%) today.",
                    ['how', 'has', 'been', 'doing'], required_words=[split_message[stock_index]])
            else:
                response(f"Sorry, I couldn't find any data for {split_message[stock_index]}.",
                         ['how', 'has', 'been', 'doing'], required_words=[split_message[stock_index]])

    split_message = [word.lower() for word in message]
    if "public" in split_message and "perception" in split_message:
        for company in companies:
            if company.lower() in split_message:
                # Run pushshiftperception.py with the company name as a command-line argument
                subprocess.run(['python', 'pushshiftperception.py', company])

    best_match = max(highest_prob_list, key=highest_prob_list.get)
    # print(highest_prob_list)
    # print(f'Best match = {best_match} | Score: {highest_prob_list[best_match]}')

    return long.unknown() if highest_prob_list[best_match] < 1 else best_match


# Used to get the response
def get_response(user_input):
    split_message = re.split(r'\s+|[,;?!.-]\s*', user_input.lower())
    response = check_all_messages(split_message)
    return response
