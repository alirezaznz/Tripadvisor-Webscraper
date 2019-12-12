from selenium import webdriver
import time
from bs4 import BeautifulSoup as soup
import re
import csv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

constants = {
        'hotel_rate': 'hotels-hotel-review-about-with-photos-Reviews__overallRating--vElGA',
        'hotel_rate_string': 'hotels-hotel-review-about-with-photos-Reviews__ratingLabel--24XY2',
        'hotel_class': 'hotels-hr-about-layout-TextItem__textitem--2JToc',
        'hotel_aspects': 'hotels-hotel-review-about-with-photos-Reviews__subratingRow--2u0CJ',
        'username': 'ui_header_link social-member-event-MemberEventOnObjectBlock__member--35-jC',
        'user_rate': 'location-review-review-list-parts-RatingLine__bubbles--GcJvM',
        'review_title': 'location-review-review-list-parts-ReviewTitle__reviewTitle--2GO9Z',
        'review_text': 'location-review-review-list-parts-ExpandableReview__reviewText--gOmRC',
        'date_of_stay': 'location-review-review-list-parts-EventDate__event_date--1epHa',
        'review_helpfulness_vote': 'social-member-MemberHeaderStats__bold--3z3qh',
        'trip_type': 'location-review-review-list-parts-TripType__trip_type--3w17i',
        'review_aspects': 'location-review-review-list-parts-AdditionalRatings__rating--1_G5W location-review-review-list-parts-AdditionalRatings__large--IOg2u',
        'reviews_next_button': '//*[@id="component_11"]/div/div[3]/div[8]/div/a',
        'reviews': 'hotels-community-tab-common-Card__card--ihfZB hotels-community-tab-common-Card__section--4r93H',
        'hotel_name': 'HEADING',
        'hotel_about': 'ABOUT_TAB',
        'read_more_button': '//span[@class= "location-review-review-list-parts-ExpandableReview__cta--2mR2g"]',
        'hotels_button': '//span[@class="ui_icon hotels brand-quick-links-QuickLinkTileItem__icon--2iguo"]',
        'city_search_input': '//input[@class="Smftgery"]',
        'hotels_in_city': '//a[@class="property_title prominent "]',
        'close_pop_up': '//div[@class="ui_close_x"]'
}
constants['review-class'] = 'review-container'


def getPageSoup(driver):
    page_source = driver.page_source
    page_soup = soup(page_source, 'html.parser')
    return page_soup


def processHotelAspects(aspects):
    for aspect in aspects:
        aspect_name = aspect.div.text.strip()
        aspect_rate = int(aspect.span["class"][1].split("_")[1])/10
        for hotel_aspect in hotel_aspects:
            if hotel_aspect["aspect"] == aspect_name:
                hotel_aspect["rating"] = aspect_rate
    data_row.extend([hotel_aspects[0]["rating"], hotel_aspects[1]["rating"], hotel_aspects[2]["rating"]])

        
def processHotelAbouts(hotel_about):
    hotel_rate = hotel_about.find("span",{"class": constants['hotel_rate']}).text.strip()
    hotel_rate_string = hotel_about.find("div", {"class": constants['hotel_rate_string']}).text.strip()
    try:
        hotel_class = int(hotel_about.find("div", {"class": constants['hotel_class']}).span["class"][1].split("_")[1])/10
    except Exception:
        hotel_class = ''
    data_row.extend([hotel_class, hotel_rate, hotel_rate_string])
    try:
        aspects = hotel_about.findAll("div", {"class": constants['hotel_aspects']})
        processHotelAspects(aspects)
    except Exception:
        processHotelAspects([])
        pass

    
def processReviews(review):
    trip_type = 'not mentioned'
    for review_aspect in review_hotel_aspects:
        review_aspect["rating"] = -1
    user = review.find("a",{"class": constants['username']}).text.strip()
    user_rate =int (review.find("div", {"class": constants['user_rate']}).span["class"][1].split("_")[1])/10
    review_title = review.find("div", {"class": constants['review_title']}).a.span.text.strip()
    review_text = review.find("q", {"class": constants['review_text']}).span.text
    try:
        date_of_stay = review.find("span", {"class": constants['date_of_stay']}).text.split(":")[1].strip()
    except Exception:
        date_of_stay = ' '
    try:
        review_helpfulness_vote = review.find("span",{"class": constants['review_helpfulness_vote']}).text.strip()
    except Exception:
        review_helpfulness_vote = 0
    try:
        trip_type = review.find("span", {"class": constants['trip_type']}).text.split(":")[1].strip()
    except Exception:
        pass
    data_row.extend([user, review_title, review_text, date_of_stay, user_rate, review_helpfulness_vote, trip_type])
    try:
        aspects = review.findAll("div", {"class": constants['review_aspects']})
        for aspect in aspects:
            aspect_name = aspect.text.strip()
            aspect_rating = int(aspect.span.span["class"][1].split("_")[1])/10
            for review_aspect in review_hotel_aspects:
                if review_aspect["aspect"] == aspect_name:
                    review_aspect["rating"] = aspect_rating
    except Exception as e:
        print(e)
        pass 
    data_row.extend([review_hotel_aspects[0]["rating"], review_hotel_aspects[1]["rating"], review_hotel_aspects[2]["rating"], review_hotel_aspects[3]["rating"], review_hotel_aspects[4]["rating"], review_hotel_aspects[5]["rating"]])


def processHotel(page_soup):
    data_row.clear()
    global reviews_count
    hotel_name = page_soup.find("h1", {"id": constants['hotel_name']}).text.strip()
    hotel_about_tab = page_soup.find("div", {"id": constants['hotel_about']})
    data_row.append(hotel_name)
    
    processHotelAbouts(hotel_about_tab)
    
    try:
        reviews_next_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, constants['reviews_next_button'])))
        #read_more_button = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, '//span[@class= "hotels-review-list-parts-ExpandableReview__cta--3U9OU"]')))
    except TimeoutException:
        reviews_next_button = ''
        
    while reviews_next_button != None:
        while True:
            try:
                read_more_button = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, constants['read_more_button'])))
            except TimeoutException:
                break
            read_more_button.click()
#            time.sleep(3)
            
        page_soup = getPageSoup(driver)
        reviews = page_soup.findAll("div", {"class": constants['reviews']})
        for review in reviews:
            processReviews(review)
            writer.writerow(data_row)
            reviews_count+=1
            if reviews_count >= reviews_num:
                break
            del data_row[7:]
        if reviews_count >= reviews_num:
            break
#        time.sleep(3)
        try:
            reviews_next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, constants['reviews_next_button'])))
            reviews_next_button.click()
            reviews_next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, constants['reviews_next_button'])))
        except TimeoutException:
            break

#def main():
    
review_hotel_aspects =[{"aspect":"Value", "rating": -1}, {"aspect":"Location", "rating": -1} , {"aspect":"Cleanliness", "rating": -1}, {"aspect":"Service", "rating": -1}, {"aspect":"Rooms", "rating": -1}, {"aspect":"Sleep Quality", "rating": -1}]
hotel_aspects =[ {"aspect":"Location", "rating": -1}, {"aspect":"Cleanliness", "rating": -1}, {"aspect":"Service", "rating": -1}]
header_row = ["Hotel Name", "Hotel Class", "Hotel Rating", "Hotel Quality", hotel_aspects[0]["aspect"], hotel_aspects[1]["aspect"], hotel_aspects[2]["aspect"], "User Name", "Review Title", "Review Text",
                  "Date of Stay", "User Rating", "Review Likes", "Trip Type", review_hotel_aspects[0]["aspect"],
                  review_hotel_aspects[1]["aspect"],review_hotel_aspects[2]["aspect"],review_hotel_aspects[3]["aspect"],
                  review_hotel_aspects[4]["aspect"], review_hotel_aspects[5]["aspect"]] 
data_row = []
reviews_count = 0
hotels_clicked = 0
URL = "https://www.tripadvisor.com/"
f = open('hotel_reviews2.csv', 'a')
writer = csv.writer(f)
writer.writerow(header_row)
processed_hotels = []
driver = webdriver.Firefox(executable_path = '/Users/alireza/Downloads/geckodriver')
driver.get(URL)
driver.maximize_window()


action_key_down_command = ActionChains(driver).key_down(Keys.COMMAND)
action_key_up_command = ActionChains(driver).key_up(Keys.COMMAND)

city = input("Enter city: ")
reviews_num = int(input("Enter number of reviews: "))
hotels_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, constants['hotels_button'] )))

hotels_button.click()
#time.sleep(3)


input_city = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, constants['city_search_input'])))
input_city.send_keys(city)
input_city.send_keys(Keys.ENTER)
try:
    WebDriverWait(driver, 3).until(EC.alert_is_present(),
                                   'Timed out waiting for PA creation ' +
                                   'confirmation popup to appear.')

    alert = browser.switch_to.alert
    alert.accept()
    print("alert accepted")
except TimeoutException:
    print("no alert")
    
#ActionChains(driver).send_keys(Keys.ESCAPE).perform()
input_city.send_keys(Keys.ENTER)
hotels = WebDriverWait(driver,15).until(EC.presence_of_all_elements_located((By.XPATH, constants['hotels_in_city'])))
ActionChains(driver).send_keys(Keys.ESCAPE).perform()
# get the Session id of the Parent
parentGUID = driver.current_window_handle;
hotels_in_page = len(hotels)
while hotels_clicked <= hotels_in_page:
    for hotel in hotels:
        if hotel.text not in processed_hotels:
            print(hotel.text)
            action_key_down_command.perform()
            hotel.click()
            hotels_clicked += 1
            processed_hotels.append(hotel.text)
            action_key_up_command.perform()
            break
            # get the All the session id of the browsers
        else: 
            continue
    allGUID = driver.window_handles
        # iterate the values in the set
    for guid in allGUID:
    	# one enter into if blobk if the GUID is not equal to parent window's GUID
    	if(guid != parentGUID):
            # switch to the guid
            driver.switch_to.window(guid)
#            time.sleep(2)
            try:
                WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, '//div[@id="ABOUT_TAB"]')))
                #process the Hotel
                processHotel(getPageSoup(driver))
                # close the browser
            except TimeoutException:
                pass
            driver.close()
            # switch back to the parent window
            driver.switch_to.window(parentGUID)
#            time.sleep(3)
            print(reviews_count)
            try: 
                close_pop_up = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, constants['close_pop_up'])))
                close_pop_up.click()
                time.sleep(3)
            except TimeoutException:
                pass
    hotels = WebDriverWait(driver,15).until(EC.presence_of_all_elements_located((By.XPATH, constants['hotels_in_city'])))
print("Scrap Completed")

driver.close();
f.close()
