import os
import sys
import json
from datetime import datetime
from ImageCheck import *
import requests
from flask import Flask, request
import re

app = Flask(__name__)


@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():

    # endpoint for processing incoming messaging events

    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event["message"].get("attachments"):

                    sender_id = messaging_event["sender"]["id"]
                    attachment_link = messaging_event["message"]["attachments"][0]["payload"]["url"]
                    send_message(sender_id, "We are looking for recipes with your ingredients.......")
                    tuple_output = output_prediction(attachment_link)
                    send_message(sender_id, "Image recognized as: " + tuple_output[0])                  
                    send_message(sender_id, tuple_output[1])

                elif messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    message_text = messaging_event["message"]["text"]  # the message's text
                    if re.search("help", message_text, re.IGNORECASE):
                        send_message(sender_id, "Hi! You can either 1) message me food ingredients separated by commas " + 
                        "or 2) send me a picture of an ingredient and I will search for an appropriate recipe.")
                    elif re.search("credit", message_text, re.IGNORECASE):
                        send_message(sender_id, "This bot was developed by Soho, Moho, Shinho, and Madiho. " + 
                        "Please send us an email to cspost2017@gmail.com for any inquires!")
                    else:
                        send_message(sender_id, "We are looking for recipes with your ingredients.......")
                        send_message(sender_id, get_recipe(message_text.split(", "),[])[0])

                        # send_message(sender_id, "message_text " + message_text)

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200


def send_message(recipient_id, message_text):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def log(msg, *args, **kwargs):  # simple wrapper for logging to stdout on heroku
    try:
        if type(msg) is dict:
            msg = json.dumps(msg)
        else:
            msg = unicode(msg).format(*args, **kwargs)
        print u"{}: {}".format(datetime.now(), msg)
    except UnicodeEncodeError:
        pass  # squash logging errors in case of non-ascii text
    sys.stdout.flush()




if __name__ == '__main__':
    app.run(debug=True)
