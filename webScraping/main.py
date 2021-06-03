import string
from urllib import request
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq

def movie_names():
    movie_list = []
    for tags in containers:
        a = tags
        names = a.find("a")
        movie_list.append(names.text)
    return movie_list

def write_movies(movies, file_name):
    writes = open(file_name, 'w')
    writes.write("Top 10 imdb rated movies\n")
    for movie in movies:
        in_newline = movie + "\n" 
        writes.write(in_newline)
    writes.close()

if __name__ == '__main__':
    myUrl = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'
    uClient = uReq(myUrl)
    pageHtml= uClient.read()
    uClient.close()
    page_soup = soup(pageHtml, "html.parser")
    containers = page_soup.findAll("td", {"class": "titleColumn"})
    write_movies(movie_names(), "movies.txt")



