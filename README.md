# ShowroomScraper v1.0
## Gathers listings from the Showroom cinema in Sheffield, UK, and mails a table of films showing and corresponding Rotten Tomatoes scores

* Looks up listings from the Showroom Cinema (an independent cinema based in Sheffield, UK : https://www.showroomworkstation.org.uk/), and mails the user a table showing what's on, and how each film has been reviewed according to Rotten Tomatoes (https://www.rottentomatoes.com/)
* When using ShowroomScraper for the first time, run SETUP.py, which will ask for an email account to be used for sending cinema listings, and an email account for receiving the listings. These details are saved in 'config.json'.
* Next, launch 'RUN.py', which will search for listings, grab the corresponding RT ratings, and mail an HTML-formatted table to the address specified during setup.
* Note that not all films will have aggregate review scores on Rotten Tomatoes. In these cases, the rating is given as 'Not available'.

## DEPENDENCIES
Python 3
beautifulsoup 4
yagmail 0.5.140
