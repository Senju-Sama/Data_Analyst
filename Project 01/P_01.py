from bs4 import BeautifulSoup
import urllib.request, urllib.error, urllib.parse
import re
import pandas as pd
from urllib.parse import urljoin






global all_books
all_books = []

def parse_book(url):
    #url = 'https://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html'

    str = urllib.request.urlopen(url).read().decode()
    str = str.strip()
    soup = BeautifulSoup(str, 'html.parser')

    #name = soup.find('body').find('div',class_ = 'container-fluid page').find('div',class_ = 'page_inner').find('div',class_ = 'content').find('h1').text.strip()
    name = soup.find('div',class_ = 'content').find('h1').text.strip()

    stock = soup.find('p',class_ = 'instock availability').text.strip()
    stock = re.search(r'[0-9]+',stock).group()

    rating = soup.find('p',class_='star-rating')['class'][1]
    rnum = {
        "One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5
    }
    rating = rnum.get(rating,0)

    genre = soup.find('ul',class_='breadcrumb').find('a',href = re.compile(r'category/books/')).text

    p_items = dict()
    p_items['Name']=name
    p_items['Stock']=stock
    p_items['Rating']=rating
    p_items['Genre']=genre
    t_items = ['UPC','Product Type','Price (incl. tax)','Price (excl. tax)','Tax','Number of reviews']
    def tags(tag):
        th_tag =soup.find('th',string=tag)
        
        if (th_tag):
            td =th_tag.find_next_sibling('td').text.strip()
        else :
            td = None
        return td

    for item in t_items:
        p_items[item] = tags(item)
    print(p_items)
    all_books.append(p_items)
    print(len(all_books))

def home_page(url):
    
    #url = 'https://books.toscrape.com/catalogue/category/books/travel_2/index.html'

    str = urllib.request.urlopen(url).read().decode()
    str = str.strip()
    soup = BeautifulSoup(str, 'html.parser')

    genres = soup.find('ul',class_="nav nav-list").find_all('a')
    
    links = list()
    for genre in genres:
        link = 'https://books.toscrape.com/' + genre['href']
        links.append(link)

    links = links[1:] # Removing the home link

    for link in links:
        book_link(link)



def book_link(url):
    while True:
        str_ = urllib.request.urlopen(url).read().decode().strip()
        soup = BeautifulSoup(str_, 'html.parser')

        # Find all book links on the current page
        book_tags = soup.select('h3 a')
        for tag in book_tags:
            book_url = urljoin(url, tag['href'])
            try:
                parse_book(book_url)
            except:
                print(book_url, 'Not found')

        # Check for next page
        next_btn = soup.find('li', class_='next')
        if next_btn:
            next_link = next_btn.find('a')['href']
            url = urljoin(url, next_link)
        else:
            break



url = input('Enter homepage link :')
home_page(url)

print(all_books)

df = pd.DataFrame(all_books)
df.to_csv("books_data.csv", index=False)
