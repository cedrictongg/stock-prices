"""High level imports for this and that"""
from __future__ import print_function

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
    speech_output = 'Hi, welcome to Stock Checker.'
    reprompt_text = 'For help, please say: menu.'
    return builder(session_attributes, card_title, speech_output, reprompt_text, False)


def handle_session_end_request():
    card_title = 'Session Ended'
    speech_output = 'Thank you for using Stock Checker. Have a nice day!'
    return build_response({}, build_speechlet_response(card_title, speech_output, None, True))

# --------------- Intents ---------------


def handle_stock_lookup(intent, session):
    """Returns the stock information"""
    session_attributes = session.get('attributes', {})
    speech_output = ''
    reprompt_text = 'Is there anything else you would like to know? If not, say stop.'
    card_title = None
    should_end_session = False
    return builder(session_attributes, card_title, speech_output, reprompt_text, should_end_session)


# --------------- Helper Functions ---------------

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

    if intent_name == 'StockSearchIntent':
        return handle_stock_lookup(intent, session)
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
