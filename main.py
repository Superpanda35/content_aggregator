import requests
from bs4 import BeautifulSoup
from Scraper import Scraper
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import csv

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////content_db.db'
db = SQLAlchemy(app)

class Aggregated_Content(db.Model):
    name = db.Column(db.String(1000), nullable=False, primary_key=True)

    def __repr__(self):
        return '< Content: %>' %self.name


# @app.route('/')
# @app.route('/home')
# def home():
#     return render_template('home_page.html')

all_content = []

URL = 'https://www.allrecipes.com/recipes/'
#recipe = Scraper(URL)
r = requests.get(URL)
soup = BeautifulSoup(r.content, 'html5lib')

recipes = soup.find_all('a', class_="fixed-recipe-card__title-link", limit=10)
img = soup.find('div',class_='ar-logo').img
width = img.width
height =img.height
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



URL = "http://www.reddit.com"
r = requests.get(URL)

soup = BeautifulSoup(r.content, 'html5lib')
table = soup.find('div',class_="rpBJOHq2PR60pnwJlUyP0")
#table = soup.find_all(attrs={'class': "_1poyrkZ7g36PawDueRza-J _2uazWzYzM0Qndpz5tFu3EX "})
#print(table)
links = []
for title in table.find_all('a', class_="SQnoC3ObvgnGjWt90zD9Z _2INHSNB8V5eaWp4P0rY_mE"):
    t = dict()
    try:
        t['title']=title.h3.text
        t['link'] = URL+title.get('href')
        links.append(t)
    except:
        pass
all_content.append(links)

@app.route('/')
def recipes():
    for site in all_content:
        right = 100
        margin = f'50px {str(right)}px'
        for link in site:
            new_column = Aggregated_Content(name = link['title'])
        #db.create_all()
        #db.session.add(new_column)
        #db.session.commit()
        right+=200
    return render_template('content_page.html', links=all_content, img=img['src'], width=width, height=height, margin=margin)


if __name__ == '__main__':
    app.run(debug=True)


