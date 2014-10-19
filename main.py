from flask import Flask
from scraper_function import scraper, json_scraper
import json
app = Flask(__name__)

@app.route('/recipe/<url>')
def crawl(url):
    url = url.replace('~', '/')
    url = 'http://www.taste.com.au/recipes/25859/oven+baked+chicken+and+chorizo+paella'
    result = json_scraper(url)

    return result

if __name__ == '__main__':
    app.run(debug=True)
