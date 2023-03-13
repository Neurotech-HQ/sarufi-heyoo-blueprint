import os
import yaml
import logging
from sarufi import Sarufi
from heyoo import WhatsApp
from dotenv import load_dotenv
from flask import Flask, request, make_response

# Initialize Flask App
app = Flask(__name__)

# Load .env file
load_dotenv()
creds = yaml.safe_load(open("config.yaml"))
messenger = WhatsApp(
    creds["whatsapp"]["token"], phone_number_id=creds["whatsapp"]["phone_number_id"]
)
sarufi = Sarufi(creds["sarufi"]["username"], creds["sarufi"]["password"])
chatbot = sarufi.get_bot(creds["sarufi"]["bot_id"])

VERIFY_TOKEN = "30cca545-3838-48b2-80a7-9e43b1ae8ce4"

# Logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def execute_actions(actions: dict, mobile: str):
    if actions.get("actions"):
        actions = actions["actions"]
        for action in actions:
            if action.get("send_message"):
                message = action.get("send_message")
                if isinstance(message, list):
                    message = "\n".join(message)
                messenger.send_message(message=message, recipient_id=mobile)
            if action.get("send_reply_button"):
                reply_button = action.get("send_reply_button")
                messenger.send_reply_button(button=reply_button, recipient_id=mobile)
            if action.get("send_button"):
                messenger.send_button(
                    button=action.get("send_button"), recipient_id=mobile
                )


def respond(mobile: str, message: str, message_type: str = "text"):
    """
    Send message to user
    """
    response = sarufi.chat(
        bot_id=creds["sarufi"]["bot_id"],
        chat_id=mobile,
        message=message,
        message_type=message_type,
        channel="whatsapp",
    )
    execute_actions(actions=response, mobile=mobile)

@app.route("/", methods=["GET", "POST"])
def hook():
    if request.method == "GET":
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            logging.info("Verified webhook")
            response = make_response(request.args.get("hub.challenge"), 200)
            response.mimetype = "text/plain"
            return response
        logging.error("Webhook Verification failed")
        return "Invalid verification token"

    # Handle Webhook Subscriptions
    data = request.get_json()
    logging.info("Received webhook data: %s", data)
    changed_field = messenger.changed_field(data)
    if changed_field == "messages":
        new_message = messenger.get_mobile(data)
        if new_message:
            mobile = messenger.get_mobile(data)
            name = messenger.get_name(data)
            message_type = messenger.get_message_type(data)
            logging.info(
                f"New Message; sender:{mobile} name:{name} type:{message_type}"
            )
            if message_type == "text":
                message = messenger.get_message(data)
                name = messenger.get_name(data)
                logging.info("Message: %s", message)
                respond(
                    message=message,
                    message_type=message_type,
                    mobile=mobile,
                )

            elif message_type == "interactive":
                message_response = messenger.get_interactive_response(data)
                intractive_type = message_response.get("type")
                message_id = message_response[intractive_type]["id"]
                message_text = message_response[intractive_type]["title"]
                logging.info(f"Interactive Message; {message_id}: {message_text}")
                respond(
                    message=message_id,
                    message_type=message_type,
                    mobile=mobile,
                )

            elif message_type == "location":
                message_location = messenger.get_location(data)
                message_latitude = message_location["latitude"]
                message_longitude = message_location["longitude"]
                logging.info("Location: %s, %s", message_latitude, message_longitude)
                respond(
                    message=message,
                    message_type=message_type,
                    mobile=mobile,
                )

            elif message_type == "image":
                image = messenger.get_image(data)
                image_id, mime_type = image["id"], image["mime_type"]
                image_url = messenger.query_media_url(image_id)
                image_filename = messenger.download_media(image_url, mime_type)
                print(f"{mobile} sent image {image_filename}")
                logging.info(f"{mobile} sent image {image_filename}")
                respond(
                    message=message,
                    message_type=message_type,
                    mobile=mobile,
                )

            elif message_type == "video":
                video = messenger.get_video(data)
                video_id, mime_type = video["id"], video["mime_type"]
                video_url = messenger.query_media_url(video_id)
                video_filename = messenger.download_media(video_url, mime_type)
                print(f"{mobile} sent video {video_filename}")
                logging.info(f"{mobile} sent video {video_filename}")
                respond(
                    message=message,
                    message_type=message_type,
                    mobile=mobile,
                )

            elif message_type == "audio":
                audio = messenger.get_audio(data)
                audio_id, mime_type = audio["id"], audio["mime_type"]
                audio_url = messenger.query_media_url(audio_id)
                audio_filename = messenger.download_media(audio_url, mime_type)
                print(f"{mobile} sent audio {audio_filename}")
                logging.info(f"{mobile} sent audio {audio_filename}")
                respond(
                    message=message,
                    message_type=message_type,
                    mobile=mobile,
                )

            elif message_type == "file":
                file = messenger.get_file(data)
                file_id, mime_type = file["id"], file["mime_type"]
                file_url = messenger.query_media_url(file_id)
                file_filename = messenger.download_media(file_url, mime_type)
                print(f"{mobile} sent file {file_filename}")
                logging.info(f"{mobile} sent file {file_filename}")
            else:
                print(f"{mobile} sent {message_type} ")
                print(data)
        else:
            delivery = messenger.get_delivery(data)
            if delivery:
                print(f"Message : {delivery}")
            else:
                print("No new message")
    return "ok"


if __name__ == "__main__":
    app.run(port=5000, debug=True)
