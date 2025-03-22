import requests
import json
import logging
from flask import current_app
from utils import MessageType


def log_http_response(response) -> None:
    logging.info(f"Status: {response.status_code}")
    logging.info(f"Content-type: {response.headers.get('content-type')}")
    logging.info(f"Body: {response.text}")


def is_status_update(body: dict) -> bool:
    return (
        body.get("entry", [{}])[0]
        .get("changes", [{}])[0]
        .get("value", {})
        .get("statuses")
    )


def is_interactive(body: dict) -> bool:
    return (
        body.get("entry", [{}])[0]
        .get("changes", [{}])[0]
        .get("value", {})
        .get("messages", [{}])
        .get("type")
    ) == "interactive"


def is_list_reply(interactive: dict) -> bool:
    return interactive.get("type", "") == "list_reply"


def is_text(body: dict) -> bool:
    return (
        body.get("entry", [{}])[0]
        .get("changes", [{}])[0]
        .get("value", {})
        .get("messages", [{}])
        .get("type")
    ) == "text"


def is_valid_whatsapp_message(body):
    """
    Check if the incoming webhook event has a valid WhatsApp message structure.
    """
    return (
        body.get("object")
        and body.get("entry")
        and body["entry"][0].get("changes")
        and body["entry"][0]["changes"][0].get("value")
        and body["entry"][0]["changes"][0]["value"].get("messages")
        and body["entry"][0]["changes"][0]["value"]["messages"][0]
    )


def process_whatsapp_message(body):
    wa_id = body["entry"][0]["changes"][0]["value"]["contacts"][0]["wa_id"]
    name = body["entry"][0]["changes"][0]["value"]["contacts"][0]["profile"]["name"]
    message = body["entry"][0]["changes"][0]["value"]["messages"][0]
    message_body = message["text"]["body"]

    response = generate_response(wa_id, message_body)


def handle_text_message(body):
    message = body["entry"][0]["changes"][0]["value"]["messages"][0]
    message_body: str = message["text"]["body"]

    if message_body.lower():
        wa_id = body["entry"][0]["changes"][0]["value"]["contacts"][0]["wa_id"]
        send_message(build_hello_menu(wa_id))


def handle_interactive_message(message):
    sender = message["from"]
    interactive_type = message["interactive"]["type"]

    if interactive_type == "list_reply":
        selected_option = message["interactive"]["list_reply"]["id"]
        print(f"✅ {sender} seleccionó la opción: {selected_option}")

    elif interactive_type == "button_reply":
        button_id = message["interactive"]["button_reply"]["id"]
        print(f"🔘 {sender} presionó el botón: {button_id}")


def handle_message(body: dict):
    message = body["entry"][0]["changes"][0]["value"]["messages"][0]
    message_type = message["type"]

    if is_status_update(body):
        handle_status_update(body)
    elif message_type == "interactive":
        handle_interactive_message(message)
    elif message_type == "text":
        handle_text_message(message)
    else:
        return

    # add more options as responses come


def build_hello_menu(recipient_wa_id):
    return json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient_wa_id,
            "type": "interactive",
            "interactive": {
                "type": "list",
                "header": {"type": "text", "text": "Elige una opción"},
                "body": {"text": "Elije una opción para iniciar"},
                "footer": {"text": ""},
                "action": {
                    "sections": [
                        {
                            "title": "Opciones",
                            "rows": [
                                {
                                    "id": "portfolio_resume",
                                    "title": "🗠 Resumen Portafolio",
                                    "description": "Un resumen del portafolio en este momento",
                                },
                                {
                                    "id": "comision",
                                    "title": "Gastar una 🍕 al autor",
                                    "description": "GRANDE",
                                },
                            ],
                        }
                    ],
                    "button": "Menu",
                },
            },
        }
    )


def build_text_message(recipient_wa_id, text):
    return json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient_wa_id,
            "type": "text",
            "text": {"preview_url": "false", "body": text},
        }
    )


def send_message(data):
    url = f"https://graph.facebook.com/v22.0/{current_app.config["PHONE_NUMBER_ID"]}/messages"
    headers = {
        "Authorization": f"Bearer {current_app.config["ACCESS_TOKEN"]}",
        "Content-Type": "application/json",
    }
    response = requests.post(url, data=data, headers=headers)
    print("----- Response -----")
    # log_http_response(response.json())
    return response.json()
