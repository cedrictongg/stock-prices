"""High level imports for this and that"""
from __future__ import print_function
from datetime import datetime, date
import calendar

from pytz import timezone

from api import alpha_vantage as av
from api import ticker_symbol as ts

# --------------- Helpers that build all of the responses ----------------------


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

# --------------- Functions that control the skill's behavior ------------------


def get_welcome_response():
    session_attributes = {}
    card_title = 'Welcome'
    speech_output = 'Hi, welcome to Stock Buddy. If you need help, just ask.'
    reprompt_text = 'For help, please say: help.'
    return builder(session_attributes, card_title, speech_output, reprompt_text, False)


def handle_session_end_request():
    card_title = 'Session Ended'
    speech_output = 'Thank you for using Stock Buddy. Have a good one!'
    return builder({}, card_title, speech_output, None, True)

# --------------- Intents ---------------


def handle_stock_portfolio(intent, session):
    """Returns the stock symbol and add it into list"""
    # TODO: later for more features
    return None


def handle_portfolio_contents(intent, session):
    """Returns the contents of your portfolio"""
    # TODO: later for more features
    return None


def handle_stock_info(intent, session):
    """Returns the stock information"""
    session_attributes = session.get('attributes', {})
    speech_output = ''
    reprompt_text = 'Is there anything else you would like to know? If not, say stop.'
    card_title = 'Stock Information'
    print('stock info intent')
    if weekend_checker() is False and time_checker() is True and 'value' in intent['slots']['company']:
        print('not weekend and after opening')
        company = intent['slots']['company']['value']
        ticker_symbol = ts.get_symbol(ts.filter_tags(company))
        latest_data = av.daily_intraday_stock(ticker_symbol)
        speech_output = av.open_format_intraday(latest_data)
    elif weekend_checker() is False and time_checker() is False and 'value' in intent['slots']['company']:
        print('not weekend and before opening')
        company = intent['slots']['company']['value']
        speech_output = f'The stock market is currently closed.\
    However, I can provide the latest information on {company}.'
        ticker_symbol = ts.get_symbol(ts.filter_tags(company))
        latest_data = av.daily_single_stock(ticker_symbol)
        if return_latest(ticker_symbol):
            speech_output = ' '.join([speech_output, av.closed_format_singles(latest_data, return_latest(ticker_symbol))])
        else:
            speech_output = 'I could not find any stock information about that company.'
    elif weekend_checker() is True and 'value' in intent['slots']['company']:
        print('is weekend')
        company = intent['slots']['company']['value']
        speech_output = f'Stocks are not being traded on the weekends. \
However, I can provide the latest information on {company}.'
        ticker_symbol = ts.get_symbol(ts.filter_tags(company))
        latest_data = av.daily_single_stock(ticker_symbol)
        if return_latest(ticker_symbol):
            speech_output = ' '.join([speech_output, av.closed_format_singles(latest_data, return_latest(ticker_symbol))])
        else:
            speech_output = 'I could not find any stock information about that company.'
    return builder(session_attributes, card_title, speech_output, reprompt_text, True)


def handle_help(intent, session):
    """Returns the options available within the skill"""
    print('help intent')
    session_attributes = session.get('attributes', {})
    reprompt_text = 'Is there anything else you would like to know? If not, say stop.'
    card_title = 'Help Menu'
    should_end_session = False
    speech_output = 'You can do the following:'
    speech_output = ' '.join([speech_output, '\nLook up a publicly traded company stock info.'])
    speech_output = ' '.join([speech_output, 'For example, stocks for Amazon.'])
    return builder(session_attributes, card_title, speech_output, reprompt_text, should_end_session)


def handle_fallback(intent, session):
    """Handles all the bad requests to the Skill"""
    session_attributes = session.get('attributes', {})
    speech_output = 'Sorry, Stock Buddy cannot help with that. For what I can do, please say, help.'
    return builder(session_attributes, 'Request Error', speech_output, speech_output, False)

# --------------- Helper Functions ---------------

def weekend_checker():
    """
    Checks to see if the current day is a weekend or not
    """
    check = calendar.day_name[datetime.now(timezone('US/Eastern')).weekday()]
    return bool(check in ['Saturday', 'Sunday'])


def time_checker():
    """Checks to see if the stock market is open."""
    _ = datetime.now(timezone('US/Eastern'))
    curr_time = '{}'.format(_.strftime('%H%M'))
    return bool(int(curr_time) > 930 and int(curr_time) < 1600)


def return_latest(symbol):
    """Returns the first date in the stocks data"""
    data = av.daily_single_stock(symbol)
    if 'Time Series (Daily)' in data:
        return list(data['Time Series (Daily)'].keys())[0]
    return None


def builder(session, card, out, reprompt, end):
    """helper function to return response"""
    return build_response(session,
                          build_speechlet_response(card, out, reprompt, end))

# --------------- Events ---------------


def on_session_started(session_started_request, session):
    """ Called when the session starts """
    print('on_session_started requestId = {}, sessionId = {}'.format(session_started_request['requestId'], session['sessionId']))


def on_session_ended(session_ended_request, session):
    """
    Called when the user ends their session
    It is not called when skill returns should_end_session = true
    """
    print('on_session_ended requestId = {}, sessionId = {}'.format(session_ended_request['requestId'], session['sessionId']))


def on_launch(launch_request, session):
    """
    Called when the user launches the skill without
    specifying what they want
    """
    print('on_launch requestId = {}, sessionId = {}'.format(launch_request['requestId'], session['sessionId']))
    return get_welcome_response()


def on_intent(intent_request, session):
    """Called when the user specifies an intent for this skill"""
    print('on_intent requestId = {}, sessionId = {}'.format(intent_request['requestId'], session['sessionId']))
    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    if intent_name == 'StockInfo':
        return handle_stock_info(intent, session)
    elif intent_name == 'StockPortfolio':
        return handle_stock_portfolio(intent, session)
    elif intent_name == 'AMAZON.HelpIntent':
        return handle_help(intent, session)
    elif intent_name == 'AMAZON.FallbackIntent':
        return handle_fallback(intent, session)
    elif intent_name == 'AMAZON.CancelIntent' or intent_name == 'AMAZON.StopIntent':
        return handle_session_end_request()
    else:
        raise ValueError('Invalid Intent')

# --------------- Main handler ------------------


def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print('event.session.application.applicationId=' + event['session']['application']['applicationId'])

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']}, event['session'])

    if event['request']['type'] == 'LaunchRequest':
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == 'IntentRequest':
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == 'SessionEndedRequest':
        return on_session_ended(event['request'], event['session'])
