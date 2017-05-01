import json
import re

CONFIG_FILE = 'config.json'

# Prompt user for email account details to use
while True:
    recipient_email = input('Enter an email address to receive cinema listings: \n')
    if not re.match("[^@]+@[^@]+\.[^@]+", recipient_email):  # rough check for email format
        print('Invalid address! Please enter a valid email address')
    else:
        break

while True:
    sender_email = input('Enter the email address that will be used to send the listings (MUST be a Gmail account): \n')
    if not re.match("[^@]+@[^@]+\.[^@]+", sender_email):  # rough check for email format
        print('Invalid address! Please enter a valid email address')
    else:
        break

sender_pwd = input('Enter the password associated with this email account: \n')

# Build dictionary with email account details
config = {'recipient_email': recipient_email,
          'sender_email': sender_email,
          'sender_pwd': sender_pwd
          }

# Write dictionary to JSON config file
with open(CONFIG_FILE, 'w') as outfile:
    json.dump(config, outfile)

print('User config info saved!')
