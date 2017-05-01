from bs4 import BeautifulSoup
import json
import os
import sys
import requests
import time
from tabulate import tabulate
import urllib.parse
import yagmail

# Set directory and point to config file
os.chdir(sys.path[0])
CONFIG_FILE = 'config.json'

# Load (JSON) config file and read from it
with open(CONFIG_FILE) as json_data_file:
    config_data = json.load(json_data_file)

sender_email = config_data.get('sender_email')
sender_pwd = config_data.get('sender_pwd')
recipient_email = config_data.get('recipient_email')

# Link to Showroom cinema's listings page /  Rotten Tomatoes search
showroom_URL = 'http://www.showroomworkstation.org.uk/guide/'
RT_URL_pt1 = 'https://www.rottentomatoes.com/m/'
RT_URL_pt2 = '/?search='
full_RT_URLs = []

print('Getting cinema listings - please wait...')

# Scrape HTML from Showroom site
r = requests.get(showroom_URL)
data = r.text
soup = BeautifulSoup(data, "html.parser")

# Find all elements that exist in film class
film_frames = soup.find_all('li', class_='p clearfix film')

# Initialize list of films
films_list = []
RT_ratings_list = []

# Parse film info and extract film titles
for film in film_frames:
    film_title = film.a.get_text()

    if film_title not in films_list:
        films_list.append(film_title)

# Remove certification info from film titles
certs_etc_to_remove = [' (U)', ' (PG)', ' (12)', ' (12A)', ' (15)', ' (18)', ' with Q&A;', ' + Q&A;']

for cert in certs_etc_to_remove:
    films_list = [film.replace(cert, '') for film in films_list]

# Define characters to remove when forming search string <- USE THIS
chars_to_remove = ['\'', ':', '-']

for film in films_list:
    film = film.strip()
    film_search_pt1 = film.replace('\'', '')
    film_search_pt1 = film_search_pt1.replace(' :', '')
    film_search_pt1 = film_search_pt1.replace(' -', '')
    film_search_pt1 = film_search_pt1.replace(' ', '_')
    film_search_pt2 = film.replace(film, urllib.parse.quote(film, safe=''))
    RT_URL_full = RT_URL_pt1 + film_search_pt1 + RT_URL_pt2 + film_search_pt2
    full_RT_URLs.append(RT_URL_full)

for RT_URL in full_RT_URLs:
    # Scrape HTML from Rotten Tomatoes
    r = requests.get(RT_URL)
    data = r.text
    soup = BeautifulSoup(data, "html.parser")
    review_frame = soup.find('span', class_='meter-value')

    if review_frame:
        RT_score = review_frame.get_text()

    else:
        RT_score = 'Not available'
    RT_ratings_list.append(RT_score)

films_with_ratings = []

for i in range(len(films_list)):
    film_and_rating = (films_list[i], RT_ratings_list[i])
    films_with_ratings.append(film_and_rating)

msg_heading = '<p>Cinema listings for week beginning ' + time.strftime("%d/%m/%Y") + ':<br>'
table_headers = ['Title', 'RT Score']
msg_html_table = tabulate(films_with_ratings, table_headers, tablefmt='html')

# Send cinema listings via email
from_addr = 'shoppinglistmailer@gmail.com'

email_subject = 'Cinema listings - ' + time.strftime("%d/%m/%Y")

yag = yagmail.SMTP(sender_email, sender_pwd)
html_msg = msg_heading + msg_html_table
yag.send(recipient_email, email_subject, html_msg)

print('Cinema listings sent!')
