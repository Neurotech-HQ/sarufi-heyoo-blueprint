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

- Creae a project folder and virtual environment

  Lets Make a project folder named `whatsapp-bot`. Navigate into it to create virtual environment `whatsapp-bot-env` Activate the environment. Run the command to make the magic 🔥 happen.

  - For unix based systems __[Linux and Mac]__

    - Install virtual environment

      This step is optional as you may have python virtual environment already installed. If not, you can install it by running the command below.

      ```bash
      sudo apt install python3-venv
      ```
    - Create project folder and virtual environment

      ```bash
      mkdir whatsapp-bot
      cd whatsapp-bot
      python3 -m venv whatsapp-bot-env
      source  whatsapp-bot-env/bin/activate
      ```
  
  - For windows

    - Install virtual environment

      This step is optional as you may have python virtual environment already installed. If not, you can install it by running the command below.

      ```bash
      pip install virtualenv
      ```
    - Create project folder and virtual environment

      ```bash
      mkdir whatsapp-bot
      cd whatsapp-bot
      python -m venv whatsapp-bot-env
      whatsapp-bot-env\Scripts\activate.bat

- Create a file named `.env`
  
  In your working folder, create `.env` file to hold environment variables using your text editor.

  With the file created, add the following credentials. With whatsapp cloud api, instructions are at the top where as for sarufi, please read on how to [get sarufi credentials](#getting-sarufi-credentials).

  ```bash
   SARUFI_API_KEY  = Your API KEY
   SARUFI_BOT_ID   = Your Bot Id
   WHATSAPP_TOKEN  = Your Whatsapp token
   PHONE_NUMBER_ID = whatsapp phone number id
   VERIFY_TOKEN    = Your verify token
  ```

  **Note**: The verification token is a random string. You can just create a random string and use it as your verification token. It will be used to verify your webhook.

- Once you have environment variables set, you are ready to fire 🚀 your `main.py` in activated virtual envirnoment.

  1. Fire up your python script
  
  ```bash
  python3 main.py
  ```
  
  2. Start ngrok

  ```bash
  ngrok http 8000
  ```

  **`Note:`** keep the port number the same as used in `main.py`

- Finish up.
  
  After running the command, you will have to copy the url ngrok provides. The url looks like `https://xxxxxxxxxxx.ngrok.io`

  With the provided url, follow simple steps at [Setting whatsapp webhook](#setting-whatsapp-webhook)

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
  |`PHONE_NUMBER_ID` | Whatsapp cloud phone ID|
  |`WHATSAPP_TOKEN` | Your whatsapp token|
  |`SARUFI_API_KEY` | Your sarufi API KEY|
  |`SARUFI_BOT_ID` | Your sarufi bot id|
  |`VERIFY_TOKEN` | Your verify token|

- Start the App

  After creating the secret keys, click `Run` button. A small webview window will open up with a url that looks like `https://{your repl name}.{your replit username}.repl.co`.

  With the url, follow simple steps at [Setting whatsapp webhook](#setting-whatsapp-webhook)

- Final touches

  Go into your repl, copy the `VERIFY_TOKEN` --> paste into verify token in your whatsapp cloud --> **verify and save**.

  We are reaching at a good point with the set-up. Lets [subscribe to message topic](#webhook-field-subscription).
  When done ,you are good to go... fire 🚀 up your bot in whatsapp by sending text.

## Getting Sarufi Credentials

To authorize our chabot, we are are going to use authorization keys from sarufi. Log in into your [sarufi account](https://sarufi.io). Go to your Profile on account to get Authorization keys

![Sarufi authorazation keys](./img/sarufi_authorization.png)

For **Bot ID**, Navigate to settings >> General(in your bot)>> copy `bot ID`

## Setting whatsapp webhook

Navigate to your whatsapp cloud account --> `configuration` -->(Webhook) edit --> then paste the url into callback url.

For Verify token, open `main.py` copy the `VERIFY_TOKEN` --> paste into verify token in your whatsapp cloud --> **verify and save**.

![Web hook setup](./img/webhook_setup.png)

## Webhook field subscription

After veryfing and saving whatsapp webook, navigate to webhook fields --> click `manage` to subscribe to `message` topic.

![Webhook fields subscription](./img/webhook_subscription.png)

## Sample Bot test

Navigate to your whatsapp cloud account >> **API setup** >> scroll down to a field written `To`. Click manage phone number to add you phone number. Follow instructions till you finish

Click **send message** to start testing your bot. You will receive a message from your test number which your will use in testing your bot.

![Send Test Message to Your Number](/img/whatsapp-send-test-message.png)

You can test WhatsApp by sending a message to your bot. With a bot deployed in Whatsapp, here is a sample of a pizza bot.

![Bot deployed in whatsapp](./img/sample.gif)

## Issues

If you will face any issue, please raise one so as we can fix it as soon as possible

## Contribution

If there is something you would like to contribute, from typos to code to documentation, feel free to do so, `JUST FORK IT`

## Credits

All the credits to

1. [kalebu](https://github.com/Kalebu/)
2. [Jovine](https://github.com/jovyinny/)
3. All other contributors
