import os
import logging
import uvicorn
from sarufi import Sarufi
from heyoo import WhatsApp
from dotenv import load_dotenv
from fastapi import FastAPI,Response, Request

# Initialize FastAPI App
from mangum import Mangum


app = FastAPI()
handler = Mangum(app)

# Load .env file
load_dotenv(".env")

messenger = WhatsApp(
    os.getenv("WHATSAPP_TOKEN"), phone_number_id=os.getenv("PHONE_NUMBER_ID")
)
sarufi = Sarufi(api_key=os.getenv('SARUFI_API_KEY'))
chatbot = sarufi.get_bot(os.getenv("SARUFI_BOT_ID"))

VERIFY_TOKEN = "30cca545-3838-48b2-80a7-9e43b1ae8ce4"

# Logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# FUNCTIONS
def respond(mobile: str, message: str, message_type: str = "text")->None:
    """
    Send message to user
    """
    try:
        response = sarufi.chat(
            bot_id=os.getenv("SARUFI_BOT_ID"),
            chat_id=mobile,
            message=message,
            message_type=message_type,
            channel="whatsapp",
        )
        execute_actions(actions=response, mobile=mobile)
    except Exception as error:
       logging.error("Error in respond function: %s", error)


def execute_actions(actions: dict, mobile: str)->None:
    if actions.get("actions"):
        actions = reversed(actions.get("actions"))
        for action in actions:
            
            if action.get("send_message"):
                message = action.get("send_message")
                if isinstance(message, list):
                    message = "\n".join(message)
                messenger.send_message(message=message, recipient_id=mobile)

            elif action.get("send_reply_button"):
                reply_button = action.get("send_reply_button")
                messenger.send_reply_button(button=reply_button, recipient_id=mobile)
            
            elif action.get("send_button"):
                button=action.get("send_button")
                messenger.send_button(button=button, recipient_id=mobile)
            
            elif action.get("send_images"):
              images=action.get("send_images")
              send_medias(images,mobile,"images")
              
            elif action.get("send_videos"):
              videos=action.get("send_videos")
              send_medias(videos,mobile,"videos")

            elif action.get("send_audios"):
              audios=action.get("send_audios")
              send_medias(audios,mobile,"audios")

            elif action.get("send_documents"):
              documents=action.get("send_documents")
              send_medias(documents,mobile,"documents")


            elif action.get("send_stickers"):
              stickers=action.get("send_stickers")
              send_medias(stickers,mobile,"stickers")
    
    logging.info("No response")


# send media
def send_medias(medias:dict,mobile:str ,type:str)->None:
  for media in medias:
    link=media.get("link")
    caption=media.get("caption")
    if type=="images":
       messenger.send_image(image=link,recipient_id=mobile,caption=caption )
    elif type =="videos":
      messenger.send_video(video=link,recipient_id=mobile,caption=caption)
    elif type == "audios":
      messenger.send_document(document=link,recipient_id=mobile,caption=caption)
    elif type=="stickers":
      messenger.send_sticker(sticker=link,recipient_id=mobile)
    elif type=="documents":
      messenger.send_document(document=link,recipient_id=mobile,caption=caption)
    else:
        logging.error("Unrecognized type")

# WEBHOOK ROUTE
@app.get("/")
async def wehbook_verification(request: Request):
    if request.query_params.get("hub.verify_token") == VERIFY_TOKEN:
        content=request.query_params.get("hub.challenge")
        logging.info("Verified webhook")
        return Response(content=content, media_type="text/plain", status_code=200)
    
    logging.error("Webhook Verification failed")
    return "Invalid verification token"

@app.post("/")
async def webhook_handler(request: Request):

    # Handle Webhook Subscriptions
    data = await request.json()
    # logging.info("Received webhook data: %s", data)
    changed_field = messenger.changed_field(data)

    if changed_field == "messages":
        new_message = messenger.is_message(data)
        if new_message:
            mobile = messenger.get_mobile(data)
            name = messenger.get_name(data)
            message_type = messenger.get_message_type(data)
            logging.info(
                f"New Message; sender:{mobile} name:{name} type:{message_type}"
            )
            # Mark message as read
            message_id = messenger.get_message_id(data)
            messenger.mark_as_read(message_id)

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

            elif message_type == "image":
                image = messenger.get_image(data)
                image_id, mime_type = image["id"], image["mime_type"]
                image_url = messenger.query_media_url(image_id)
                image_filename = messenger.download_media(image_url, mime_type)
                logging.info(f"{mobile} sent image {image_filename}")

            elif message_type == "video":
                video = messenger.get_video(data)
                video_id, mime_type = video["id"], video["mime_type"]
                video_url = messenger.query_media_url(video_id)
                video_filename = messenger.download_media(video_url, mime_type)
                logging.info(f"{mobile} sent video {video_filename}")


            elif message_type == "audio":
                audio = messenger.get_audio(data)
                audio_id, mime_type = audio["id"], audio["mime_type"]
                audio_url = messenger.query_media_url(audio_id)
                audio_filename = messenger.download_media(audio_url, mime_type)
                logging.info(f"{mobile} sent audio {audio_filename}")

            elif message_type == "file":
                file = messenger.get_file(data)
                file_id, mime_type = file["id"], file["mime_type"]
                file_url = messenger.query_media_url(file_id)
                file_filename = messenger.download_media(file_url, mime_type)
                logging.info(f"{mobile} sent file {file_filename}")
            else:
                print(f"{mobile} sent {message_type}\n{data}")
        else:
            delivery = messenger.get_delivery(data)
            if delivery:
                logging.info(f"Message : {delivery}")
            else:
                logging.info("No new message")
    return "OK",200


if __name__ == "__main__":
    uvicorn.run("main:app",port=5000,reload=True)