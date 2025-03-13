from services.google_sheets import get_due_dates
from services.whatsapp import send_whatsapp_message


def main():
    # reminders = get_due_dates()
    # for message in reminders:
    send_whatsapp_message(
        "Hola! soy un bot 🤖 creado por un ingeniero y comisionista de bolsa sin comision 💸"
    )


if __name__ == "__main__":
    main()
