from bs4 import BeautifulSoup
import requests
import re

base_url = 'https://www.imdb.com/title/tt9419884/'


# function to get the user and critics ratings
def getRatings():

    main_page_html = requests.get(base_url).text
    soup = BeautifulSoup(main_page_html,'lxml')

    user_rating = soup.find('span', class_ = 'sc-7ab21ed2-1 jGRxWM').text
    metascore_rating = soup.find('span', class_ = 'score-meta').text
    print("The user rating is %s, and the metascore rating is %s" % (user_rating, metascore_rating))


# function to get user reviews
def getReviews():

    # hides spoilers depending if you have seen the film or not
    seen_film = False
    if seen_film == False:
        url2 = base_url + 'reviews?spoiler=hide'
    elif seen_film == True:
        url2 = base_url + 'reviews'
    
    reviews_html = requests.get(url2).text
    soup = BeautifulSoup(reviews_html,'lxml')

    reviews = soup.find_all('div', class_ = 'review-container')
    
    # gets the first 3 reviews for film
    for x in reviews[0:3]:
        print(x.text)


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



#TO-DO

#maybe use IMDB APIs to get the movie code based on title

#function to determine if TV or Movie > Scrape r/television or r/movies for OFFICIAL DISCUSSION comments

#function to package everything up (maybe send as email)