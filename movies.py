from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import re
import time
from imdb import Cinemagoer



#function to get user input
def getMovie():

    movieTitle = input("What is the movie name?")
    movieYear = input("What year did the movie come out?")
    movieSeen = input("Have you seen this movie or not?")

    return movieTitle, movieYear, movieSeen



#function to get movie code
def getCode(movieTitle, movieYear):

    ia = Cinemagoer()

    movie_data = ia.search_movie(movieTitle)
    for x in movie_data:
        if x['title'] == movieTitle and x['year'] == int(movieYear):
            return x.movieID



# function to get the user and critics ratings
def getRatings():

    main_page_html = requests.get(base_url).text
    soup = BeautifulSoup(main_page_html,'lxml')

    user_rating = soup.find('span', class_ = 'sc-7ab21ed2-1 jGRxWM').text
    metascore_rating = soup.find('span', class_ = 'score-meta').text
    print("The user rating is %s, and the metascore rating is %s" % (user_rating, metascore_rating))


# function to get user reviews
def getReviews(seen_film):

    # hides spoilers depending if you have seen the film or not
    if seen_film.casefold() == 'no':
        url2 = base_url + 'reviews?spoiler=hide'
    elif seen_film.casefold() == 'yes':
        url2 = base_url + 'reviews'
    
    reviews_html = requests.get(url2).text
    soup = BeautifulSoup(reviews_html,'lxml')

    reviews = soup.find_all('div', class_ = 'review-container')
    
    # gets the first 3 reviews for film
    for x in reviews[0:3]:
        title = x.select_one('a[class="title"]').text
        review = x.find_all('div',class_='content')

        for i in review:
            review_text = i.find('div',class_='text show-more__control').text
        print(title)
        print(review_text)


#get trivia from IMDB (again, check for spoilers)
def getTrivia():

    url_trivia = base_url + 'trivia'
    trivia_html = requests.get(url_trivia).text

    soup = BeautifulSoup(trivia_html, 'lxml')

    trivia = soup.find_all('div',class_= 'soda even sodavote')

    # initialize dictionary to rank trivia based on how many people find it interesting
    trivia_ranked = {}

    for x in trivia:
        
        trivia_text = x.find('div',class_ = 'sodatext')
        trivia_count = x.find('a',class_ = 'interesting-count-text')

        commaless = trivia_count.text.replace(',','')
        how_many_found_interesting = int(re.findall('\d+',commaless)[0])
        
        trivia_ranked[trivia_text.text] = how_many_found_interesting
    
    # sort trivia by bits people find most interesting
    trivia_ranked_sort = sorted(trivia_ranked.items(), key= lambda x: x[1], reverse=True)
    
    #print off 6 most interesting bits of trivia
    for i in trivia_ranked_sort[0:6]:
        print(i[0].strip())


#function to determine if TV or Movie > Scrape r/television or r/movies for OFFICIAL DISCUSSION comments
def getReddit(name):
   
    driver = webdriver.Chrome('C:\\Users\\SatchinMistry\\Downloads\\chromedriver_win32\\chromedriver.exe')
    #name of movie but underscored so it can be searched
    name_underscored = name.replace(' ','_')
    
    movie_url = 'https://www.reddit.com/r/movies/search/?q='
    driver.get(movie_url+name_underscored)
    driver.find_element(By.CLASS_NAME,'_2i5O0KNpb9tDq0bsNOZB_Q').click()
    
    time.sleep(10)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    
    top_comments = soup.select('div[class*="P8SGAKMtRxNwlmLz1zdJu HZ-cv9q391bm8s7qT54B3 _1z5rdmX8TDr6mqwNv7A70U"]')
    
    #prints off top 6 comments
    for x in top_comments[0:6]:
        comment = x.select('p')
        for i in comment:
            print(i.text)



movieTitle, movieYear, movieSeen = getMovie()
movieID = getCode(movieTitle, movieYear)

base_url = 'https://www.imdb.com/title/tt' + str(movieID) + '/'


getRatings()
getReviews(movieSeen)
getTrivia()
getReddit(movieTitle)
#TO-DO

#function to package everything up (maybe send as email)

