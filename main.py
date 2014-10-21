
from flask import Flask
import json
import os
import subprocess
app = Flask(__name__)

@app.route('/recipe/<url>')
def crawl(url):
    url = url.replace('~', '/')
    result = subprocess.check_output(['python', 'scraper_function.py', url])
    return str(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
