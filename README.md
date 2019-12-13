# Tripadvisor-Webscraper

Python based script for scraping hotel reviews in www.tripadvisor.com

## Getting Started

This code is for  scraping reviews from hotels in a specific city which is given as an input.
Number of reviews is given as input as well.

Tripadvisor changes elements of webpage in a period of time so scrapers that are copied does not work any more ,
So there is a dictionary in the python file which you can change anytime tripadvisor changes it's elements ( you can find class of html elements with inspect element option in web browsers).

### Prerequisites

Selenium and Beautifulsoup libraries needed to run this code

### Installing

```
pip install Selenium
```
```
pip install 
```

End with an example of getting some data out of the system or using it for a little demo

## Built With

* [Selenium](https://selenium-python.readthedocs.io) -  automated testing suite for web applications
* [Beautifulsoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) - HTML and XML files data extract

## Output

Output of this script will be a csv file which has 20 features (columns):
"Hotel Name", "Hotel Class", "Hotel Rating", "Hotel Quality", 3 of hotel aspects, "User Name", "Review Title", "Review Text",
"Date of Stay", "User Rating", "Review Likes", "Trip Type", 6 of hotel aspects that users would mention in their review

## Authors

* **Alireza Nazari** - *Initial work* - [AlirezaNazari](https://github.com/alirezaznz)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

