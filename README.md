# Whatsapp web parser
Web scrapping tool for whatsapp web using selenium and beautiful soup.
This script will parse whatsapp chats and parse the text chats for the last two days and export them as JSON. It will also save the images in base64 format with the respective chats.

## USAGE
Open firefox and login into whatsapp web using your phone so that your login profile will be saved. It will be in the path /home/<username>/.mozilla/firefox/<hashkey>.default
Copy and paste this path in the settings.txt file
After that you can start the script using
``` python scraper.py```


## Prerequisities
Install the requirements using
``` sudo pip install -r requirements.txt```

Inspiration and base template credits:
[JMGama](https://github.com/JMGama/WhatsApp-Scraping)