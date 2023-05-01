from flask import Flask, jsonify, request, render_template
import re
import requests
import long_responses as long
import subprocess
import publicperception as psp

ALPHA_VANTAGE_API_KEY = 'RKH0BMX3MUBVLOY7'
ALPHA_VANTAGE_API_ENDPOINT = 'https://www.alphavantage.co/query'

companies = ['Apple', 'Amazon', 'Tesla', 'IBM', 'Sony', 'Microsoft', 'Google', 'Facebook', 'Netflix', 'Disney', 'Intel', 'AMD', 'Nvidia', 'PayPal', 'Visa', 'Mastercard', 'Starbucks', 'McDonalds', 'Walmart', 'Target', 'Costco',
             'Nike', 'Coca-Cola', 'Pepsi', 'AT&T', 'Verizon', 'T-Mobile', 'Sprint', 'Comcast', 'Twitch', 'TikTok', 'Snapchat', 'Twitter', 'Uber', 'Lyft', 'Airbnb', 'Spotify', 'Dropbox', 'Ebay', 'Etsy', 'Reddit', 'Tinder', 'Zoom']


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


def get_stock_price(symbol):
    params = {
        'function': 'GLOBAL_QUOTE',
        'symbol': symbol,
        'apikey': ALPHA_VANTAGE_API_KEY,
    }
    response = requests.get(ALPHA_VANTAGE_API_ENDPOINT, params=params)
    data = response.json()

    if 'Global Quote' not in data:
        return None

    stock_data = data['Global Quote']
    price = float(stock_data['05. price'])
    return {
        'symbol': symbol.upper(),
        'price': price,
    }


def message_probability(user_message, recognised_words, single_response=False, required_words=[]):
    message_certainty = 0
    has_required_words = True

    for word in user_message:
        if word in recognised_words:
            message_certainty += 1

    percentage = float(message_certainty) / float(len(recognised_words))

    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break
    if has_required_words or single_response:
        return int(percentage * 100)
    else:
        return 0


def check_all_messages(message):
    print(message)
    highest_prob_list = {}

    def response(bot_response, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob_list
        list_of_words = [word.lower() for word in list_of_words]
        highest_prob_list[bot_response] = message_probability(
            message, list_of_words, single_response, required_words)

    # Responses -------------------------------------------------------------------------------------------------------
    response('Hello!', ['hello', 'hi', 'hey',
             'sup', 'heyo'], single_response=True)
    response('See you!', ['bye', 'goodbye'], single_response=True)
    response('I\'m doing fine, and you?', [
             'how', 'are', 'you', 'doing'], required_words=['how'])
    response('You\'re welcome!', ['thank', 'thanks'], single_response=True)
    response('Thank you!', ['i', 'love', 'code', 'palace'],
             required_words=['code', 'palace'])
    response('The markets are doing positively recently!', [
             'how', 'markets', 'look', 'positive', 'in'], required_words=['markets'])
    response('If you have a high risk tolerance, it may be better to look at investing in options with high growth potential, such as cryptocurrencies!', [
             'i', 'have', 'a', 'high', 'risk', 'tolerance'], required_words=['high', 'risk', 'tolerance'])
    response('If you have a low risk tolerance, it may be better to look at stable investments, such as bonds or mutual funds!', [
             'i', 'have', 'a', 'high', 'risk', 'tolerance'], required_words=['low', 'risk', 'tolerance'])

    # Get stock data based on user input
    split_message = [word.lower() for word in message]

    if "public" in split_message and "perception" in split_message:
        for company in companies:
            if company.lower() in split_message:
                sentiment = psp.get_public_perception(company)
                print(company)
                response(f"{sentiment}.", [
                    'what', 'is', 'public', 'perception', 'of'], required_words=[company.lower()])

    if "how" in split_message and "has" in split_message and "been" in split_message:
        stock_index = split_message.index("stock") - 1 if "stock" in split_message else split_message.index(
            "stocks") - 1 if "stocks" in split_message else -1
        if stock_index != -1 and len(split_message) > stock_index:

            stock_data = get_stock_data(split_message[stock_index])
            if stock_data is not None:
                response(f"{stock_data['symbol']} has changed by {stock_data['change']} ({stock_data['percent_change']}%) today.", [
                         'how', 'has', 'been', 'doing'], required_words=[split_message[stock_index]])
            else:
                response(f"Sorry, I couldn't find any data for {stock_data}.", [
                         'how', 'has', 'been', 'doing'], required_words=[split_message[stock_index]])

    if "what" in split_message and "is" in split_message and "price" in split_message:
        stock_index = split_message.index(
            "price") - 1 if "price" in split_message else -1
        if stock_index != -1 and len(split_message) > stock_index:

            stock_data = get_stock_price(split_message[stock_index])
            if stock_data is not None:
                response(f"{stock_data['symbol']} is currently {stock_data['price']} today.", [
                         'what', 'is', 'price'], required_words=[split_message[stock_index]])
            else:
                response(f"Sorry, I couldn't find any data for {stock_data}.", [
                         'what', 'is', 'price'], required_words=[split_message[stock_index]])

    best_match = max(highest_prob_list, key=highest_prob_list.get)

    # print(highest_prob_list)
    # print(f'Best match = {best_match} | Score: {highest_prob_list[best_match]}')

    return long.unknown() if highest_prob_list[best_match] < 1 else best_match
