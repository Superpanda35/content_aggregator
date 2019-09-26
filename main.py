import requests
from bs4 import BeautifulSoup
from Scraper import Scraper
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import csv

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////content_db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Aggregated_Content(db.Model):
    name = db.Column(db.String(1000), nullable=False, primary_key=True)

    def __repr__(self):
        return '< Content: %>' %self.name

all_content = []
all_images = []
length = 0

URL = 'https://www.allrecipes.com/recipes/'
#recipe = Scraper(URL)
r = requests.get(URL)
soup = BeautifulSoup(r.content, 'html5lib')

recipes = soup.find_all('a', class_="fixed-recipe-card__title-link",limit=15)
img = soup.find('div',class_='ar-logo').img
width = img.width
height =img.height
all_images.append(img['src'])
links = []

if recipes != -1:
    for title in recipes:
        t = dict()
        t['title'] = title.find('span').text
        t['link'] = title['href']
        links.append(t)
else:
    print('error')
all_content.append(links)
length+=1

URL = "https://medicalnewstoday.com"
r = requests.get(URL)
soup = BeautifulSoup(r.content, 'html5lib')
news = soup.find_all('li', class_="featured", limit=15)
img = soup.find('div',class_='logo').img['src']
all_images.append(img)
links = []
for post in news:
    t = dict()
    t['title'] = post.a['title']
    t['link'] = post.a['href']
    links.append(t)
all_content.append(links)
length+=1

URL = 'https://www.imdb.com'
r = requests.get(URL)
soup = BeautifulSoup(r.content,'html5lib')
img = soup.find('span', id="home_img_holder").
all_images.append("img":img,"width":width,"height",height)
links = []
posts = soup.find('div', id="main")

for post in posts.find_all('span', class_="oneline"):
    t=dict()
    try:
        t['title'] = post.h3.text
        t['link'] = URL+post.a['href']
        links.append(t)
    except:
        pass
all_content.append(links)


URL = "http://www.reddit.com"
r = requests.get(URL)

soup = BeautifulSoup(r.content, 'html5lib')
table = soup.find('div',class_="rpBJOHq2PR60pnwJlUyP0")
#table = soup.find_all(attrs={'class': "_1poyrkZ7g36PawDueRza-J _2uazWzYzM0Qndpz5tFu3EX "})
#print(table)
links = []
for title in table.find_all('a', class_="SQnoC3ObvgnGjWt90zD9Z _2INHSNB8V5eaWp4P0rY_mE", limit = 10):
    t = dict()
    try:
        t['title'] = title.h3.text
        t['link'] = URL+title.get('href')
        links.append(t)
    except:
        pass
all_content.append(links)

@app.route('/')
def content():
    for site in all_content:
        right = 25
        #margin = f'25px {str(right)}px'
        for link in site:
            new_column = Aggregated_Content(name=link['title'])
            #db.session.add(new_column)
            #db.session.commit()
        right += 25
    #print(Aggregated_Content.query.all())
    return render_template('content_page.html', links=all_content, all_images=all_images, length=length, width= width, height= height)


if __name__ == '__main__':
    app.run(debug=True)


