<samp>

# sarufi-heyoo-blueprint
Starter code to integrating sarufi with heyoo

A blueprint for deploying sarufi chabot on WhatsApp Cloud API. 

## Requirements

Make sure you have [sarufi package](https://github.com/Neurotech-HQ/sarufi-python-sdk) installed on your machine before launching your whatsapp bot, you can easily install by the following command;

```bash
git clone https://github.com/Neurotech-HQ/sarufi-python-sdk
cd sarufi-python-sdk
sarufi-python-sdk $ python setup.py install
```

## YAML CONFIGURATION

Configure yaml to resemble your project details and whatsapp cloud API keys

```YAML
sarufi:
  username: sarufi_username
  password: sarufi_password
  bot_id: sarufi_bot_id

whatsapp:
  token: whatsapp_token
  phone_number_id: whatsapp_phone_number_id
```

## LAUNCH

Once you have configured your YAML file, now you are ready to launch your whatsapp bot.

```bash
python3 app.py
```

## Issues

If you will face any issue, please raise one so as we can fix it as soon as possible

## Contribution

If there is something you would like to contribute, from typos to code to documentation, feel free to do so, `JUST FORK IT`.

## Credits

All the credits to

1. [kalebu](https://github.com/Kalebu/)
2. All other contributors

</samp>
