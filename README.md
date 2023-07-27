# UK Real Estate Bot

This is a telegram bot for searching properties for rent in the UK.
The user enters a UK city and receives in response a list of residential properties from a pool of houses and apartments
that the agency has available.

## Building a repository and running it locally
Run in the console:
```
git clone https://gitlab.skillbox.ru/nikolai_solovev/python_basic_diploma
pip install -r requirments.txt
```

### Setup
Create an .env file and add the following settings to it:
```
BOT_TOKEN = "The API key you received from BotFather"

SITE_API = "API key, which you will receive after registration on the site: https://rapidapi.com/apidojo/api/zoopla"

HOST_API="zoopla.p.rapidapi.com"
```


### Start-up
Run the **main**.py file.