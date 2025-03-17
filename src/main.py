from flask import Flask
from dotenv import load_dotenv
from routes import handle_wa_message, main_endpoint, verify
from services.whatsapp import send_whatsapp_message

app = Flask(__name__)


def register_endpoints():
    app.route("/", methods=["GET", "POST"])(main_endpoint)
    app.route("/webhook", methods=["GET"])(verify)
    app.route("/webhook", methods=["POST"])(handle_wa_message)


def main():
    load_dotenv("../.env")
    register_endpoints()


if __name__ == "__main__":
    main()
    app.run(debug=True, port=8000)
    # send_whatsapp_message(
    #     "Hola! soy un bot 🤖 en proceso de creación por un ingeniero y corredor de bolsa sin comision 💰. Gastele una 🍕"
    # )
