from flask import Flask
from dotenv import load_dotenv
from routes import webhook, main_endpoint, verify
from services.whatsapp import send_message
from config.configuration import load_config

app = Flask(__name__)


def register_endpoints():
    app.route("/", methods=["GET", "POST"])(main_endpoint)
    app.route("/webhook", methods=["GET"])(verify)
    app.route("/webhook", methods=["POST"])(webhook)


def main():
    load_config(app)
    print(app.config)
    register_endpoints()
    app.run(debug=True, port=8000)


if __name__ == "__main__":
    main()
