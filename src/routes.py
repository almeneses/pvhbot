import logging
import json
from flask import request
from services.whatsapp import (
    handle_message,
    is_valid_whatsapp_message,
)


def main_endpoint():
    return "HELLO WORLD!!"


def webhook():
    body: dict = request.get_json()
    print("\n --------- Llega mensaje en webhook --------")
    print(body)
    print("\n --------------------------------")
    # if not is_valid_whatsapp_message(body):
    #    return {"status": "error", "message": "Not a valid WhatsApp API message"}, 400

    handle_message(body)
    return {"status": "ok"}, 200


# Required webhook verifictaion for WhatsApp
def verify():
    print("----- verify called ----")
    # Parse params from the webhook verification request
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    # Check if a token and mode were sent
    if mode and token:
        # Check the mode and token sent are correct
        if mode == "subscribe" and token == "12345":
            # Respond with 200 OK and challenge token from the request
            logging.info("WEBHOOK_VERIFIED")
            return challenge, 200
        else:
            # Responds with '403 Forbidden' if verify tokens do not match
            logging.info("VERIFICATION_FAILED")
            return jsonify({"status": "error", "message": "Verification failed"}), 403
    else:
        # Responds with '400 Bad Request' if verify tokens do not match
        logging.info("MISSING_PARAMETER")
        return jsonify({"status": "error", "message": "Missing parameters"}), 400
