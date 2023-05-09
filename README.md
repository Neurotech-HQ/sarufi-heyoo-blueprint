# sarufi heyoo blueprint

Starter code to integrate sarufi with [heyoo](https://github.com/Neurotech-HQ/heyoo).
This is a blueprint for deploying sarufi chabot on WhatsApp using WhatsApp Cloud API. In this blueprint, we shall set up a webhook to receive whatsapp messages. There are several ways you can set up a webhook. We shall be working on how to use [ngrok](#using-ngrok) and [Replit](#using-replit) in the deployment.

## Whatsapp cloud account

To get started using this blueprint for your [sarufi bot](https://sarufi.io), you will need `TOKEN` and `TEST WHATSAPP NUMBER` obtained from [Facebook Developer Portal](https://developers.facebook.com/).

Here are steps to follow for you to get started:

- [Go to your apps](https://developers.facebook.com/apps).
- [create an app](https://developers.facebook.com/apps/create/).
- Select Business >> Business.
- It will prompt you to enter basic app informations.
- It will ask you to add products to your app. Add Whatsapp.
- Right there you will see a your TOKEN and TEST WHATSAPP NUMBER and its phone_number_id.
- Lastly verify the number you will be using for testing on the To field.

## Deploying the bot

### USING NGROK

Make sure you have [ngrok](https://ngrok.com/) installed in your working machine.

#### Quick setup

Have [sarufi package](https://github.com/Neurotech-HQ/sarufi-python-sdk) installed on your machine before launching your whatsapp bot.

- Make Project folder
  Lets Make a project folder named `whatsapp-bot`. Navigate into it to create virtual evironment `whatsapp-bot-env`. Activate the environment and install sarufi.

  Run the command to make the magic happen

  ```bash
  mkdir whatsapp-bot
  cd whatsapp-bot
  python -m venv whatsapp-bot-env
  source  whatsapp-bot-env/bin/activate
  ```

- Clone blueprint and install packages

  ```bash
  git clone https://github.com/Neurotech-HQ/sarufi-heyoo-blueprint.git
  cd telegram-chatbot-blueprint
  pip3 install -r requirements.txt
  ```

- Create a file named '.env`.
  
  In your working folder, create `.env` file to hold environment variables using your text editor.

  With the file created, add the following credentials. With whatsapp cloud api, instructions are at the top where as for sarufi, please read on how to [get sarufi credentials](#getting-sarufi-credentials).

  ```bash
   sarufi_api_key = Your API KEY
   sarufi_bot_id   = Your Bot Id
   whatsapp_token  = Your Whatsapp token
   phone_number_id = whatsapp phone number id
  ```

- Once you have environment variables set, you are ready to fire 🚀 your `main.py` in activated virtual envirnoment.

  1. Fire up your python script
  
  ```bash
  python3 main.py
  ```
  
  2. Start ngrok

  ```bash
  ./ngrok http 5000
  ```

  **`Note:`** keep the port number the same as used in `main.py`.

- Finish up.
  
  After running the command, you will have to copy the url ngrok provides. The url looks like `https://xxxxxxxxxxx.ngrok.io`.

  With the provided url, follow simple steps at [Setting whatsapp webhook](#setting-whatsapp-webhook).

  Open `main.py`, copy the `VERIFY_TOKEN`--> paste into verify token in your whatsapp cloud --> **verify and save**.

  We are heading a the best part of this journey. Just take time to [subscribe to message topic](#webhook-field-subscription).
  When done ,you are good to go... fire up your bot in whatsapp by sending text.

  🏁 When done with saving the token and url, go on to text your bot. Check out the sample [below](#sample-bot-test).

### USING REPLIT

- Log into your [Replit](https://replit.com/) account.

  Fork the repo [Whatsapp bot using sarufi API and heyoo](https://replit.com/@neurotechafrica/sarufi-heyoo-blueprint) into your account.

  Navigate to `Tools`--> `Secrets` to create environment variables. We have discussed on how to get whatsapp cloud api at the introduction part where as for sarufi view instructions here [get sarufi credentials](#getting-sarufi-credentials).

  Create
  |Secrete key | Description|
  |:--- |:--- |
  |`phone_number_id` | Whatsapp cloud phone ID|
  |`whatsapp_token` | Your whatsapp token|
  |`sarufi_api_key` | Your sarufi API KEY|
  |`sarufi_bot_id` | Your sarufi bot id|

- Run the script

  After creating the secret keys, run your `main.py`. A small webview window will open up with a url that looks like `https://{your repl name}.{your replit username}.repl.co`.

  With the url, follow simple steps at [Setting whatsapp webhook](#setting-whatsapp-webhook).

- Final touches

  Go into your repl, copy the `VERIFY_TOKEN` --> paste into verify token in your whatsapp cloud --> **verify and save**.

  We are reaching at a good point with the set-up. Lets [subscribe to message topic](#webhook-field-subscription).
  When done ,you are good to go... fire 🚀 up your bot in whatsapp by sending text.

## Getting Sarufi Credentials

To authorize our chabot, we are are going to use authorization keys from sarufi. Log in into your [sarufi account](https://sarufi.io). Go to your Profile on account to get Authorization keys

![Sarufi authorazation keys](./img/sarufi_authorization.png)

## Setting whatsapp webhook

Navigate to your whatsapp cloud account --> `configuration` --> edit --> then paste the url into callback url.

![Web hook setup](./img/webhook_setup.png)

## Webhook field subscription

After veryfing and saving whatsapp webook, navigate to webhook fields --> click `manage` to subscribe to `message` topic.

![Webhook fields subscription](./img/webhook_subscription.png)

## Sample Bot test

With a bot deployed in Whatsapp, here is a sample of a pizza bot.
![Bot deployed in whatsapp](./img/sample.gif)

## Issues

If you will face any issue, please raise one so as we can fix it as soon as possible

## Contribution

If there is something you would like to contribute, from typos to code to documentation, feel free to do so, `JUST FORK IT`.

## Credits

All the credits to

1. [kalebu](https://github.com/Kalebu/)
2. [Jovine](https://github.com/jovyinny/)
3. All other contributors
