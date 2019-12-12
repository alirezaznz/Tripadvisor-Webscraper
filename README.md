# Tripadvisor-Webscraper
Python based script for scraping hotel reviews in www.tripadvisor.com

######################
This code is for who wants to scrap reviews from hotels in a specific city which is given as an input.
Number of reviews is given as input as well.


###############
Tripadvisor changes elements of webpage in a period of time so scrapers that are copied does not work any more , So there is a dictionary in the python file which you can change anytime tripadvisor changes it's elements ( you can find class of html elements with inspect element option in web browsers).


###########
Output of this script will be a csv file which has 20 features (columns):
"Hotel Name", "Hotel Class", "Hotel Rating", "Hotel Quality", 3 of hotel aspects, "User Name", "Review Title", "Review Text",
"Date of Stay", "User Rating", "Review Likes", "Trip Type", 6 of hotel aspects that users would mention in their review
