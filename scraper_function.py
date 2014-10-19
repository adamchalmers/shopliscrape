from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from recipe_scraper.spiders.taste_spider import RecipeSpider
from scrapy.utils.project import get_project_settings
import string
import json
import re
import sys
re.DOTALL

def scraper(url):   #function that scrapes recipe name and ingridients from given url
    open('results.log', 'w').close()
    spider = RecipeSpider(start_url=url)               #starts the RecipeSpider that crawls recipes
    settings = get_project_settings()
    crawler = Crawler(settings)
    crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()                                 #start crawl

    log.start(logfile="results.log", loglevel=log.DEBUG, crawler=crawler, logstdout=False)  #make stemporary file dump of log and scraped contens

    reactor.run()
    re_items = re.compile("u'.+")
    re_clean = re.compile("([^\s\w]|_)+[u']")
    items = []
    with open("results.log", "r") as f:
        #f.readline()
        #f.readline()
        #ingredients = f.readline()  #get results of scrape from log
        #name = f.readline()
        for line in f:
            search_items = re.findall(re_items,line)
            if search_items != []:
                items.append(search_items)
    raw_ingredients = items[0:-1]
    if len(raw_ingredients) == 1:
        raw_ingredients = str(raw_ingredients).split(', u')
    ingredients = []
    name = str(items[-1])
    name = name.split('["u')[1]
    name = name.strip(']}"]\n')              #create string of name
    name = name.strip("'")
    for item in raw_ingredients:
        item = str(item)
        item = re_clean.sub('',item)
        #item = item.split('"u')[1]            #format results nicely and strip random chars
        item = item.strip('],"]]')
        item = item.strip("'")
        ingredients.append(item)

    recipe = []                             #create list structure to hold recipe name and ingredient dicts
    recipe.append(name)                     #add name to structure
    re_amount = re.compile('[0-9]+')        #regex to find amount
    re_unit = re.compile('[a-zA-Z]+')      #regex to find units
    for ingredient in ingredients:          #for each ingredient in the list
        no_amount = True
        amount_check = re.findall(re_amount,ingredient)    #check if ingredient has an amount
        for instance in amount_check:
            if instance != '':
                no_amount = False
        if no_amount == False:                              #if ingredient has amount, process it
            ingredient = ingredient.split(',')      #split the ingredient into parts if it is split by a comma
            if re.match(re_amount,ingredient[-1]) == None:
                fusion = ','.join(ingredient)
                ingredient = [fusion]
            for part in ingredient:                 #for each ingredient part
                part = part.split(' ')
                name_ext = []
                amount = None
                unit = None
                name = None
                if re.findall(re_unit,part[0]) == []:   #check if there are space between amount and unit, if so then split accordingly
                    amount = part[0]
                    if len(part) ==2:
                        name = part[1]
                        unit = ''
                    else:
                        unit = part[1]
                        name =  ' '.join(part[2:])
                elif re.match(re_amount,part[0]) == None:
                    name_ext = name_ext.append(part[0])
                else:                                   #if no space between amount and unit, split accordingly
                    name = ' '.join(part[1:])
                    amount = re.findall(re_amount, part[0])[0]
                    '''
                    amounts =  re.findall(re_amount, part[0])[0]
                    total_amount = 0
                    for amount in amounts:
                        if amount != None:
                            total_amount = total_amount + amount
                    '''
                    units = re.findall(re_unit, part[0])
                    for i in range(0,len(units)):
                        if units[i] != '':
                            unit = units[i]
                            break
                        else:
                            unit = ''

                if type(name_ext) == list:
                    name_ext = ' '.join(name_ext)
                if name == None:
                    break
                name = str(name)+' '+str(name_ext)
            if name == None:
                ingredient == None
            else:
                ingredient = {'name': name, 'amount': amount, 'unit': unit} #create ingredient dictionary
        recipe.append(ingredient)           #append ingredient to recipe list structure

    print recipe
    return recipe      #return list of recipe name and ingredients

def json_scraper(url):
    results = scraper(url)
    recipe_name = results[0]
    ingredients = results[1:]
    d = {"name": recipe_name, "ingredients": ingredients}
    return json.dumps(d)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        print "Doing actual scrape"
        url = sys.argv[1]
    else:
        url = 'http://www.taste.com.au/recipes/37970/chorizo+and+crisp+smashed+potato+salad?ref=zone,salad-recipes'
    #scraper('http://www.taste.com.au/recipes/18338/basic+omelette')
    #scraper('http://www.taste.com.au/recipes/13783/salsa')
    #scraper('http://www.taste.com.au/recipes/37876/strawberry+coconut+ice?ref=zone,feed-your-family')
    #scraper('http://www.taste.com.au/recipes/37969/pulled+pork+rolls+with+apple+and+radish+coleslaw?ref=zone,salad-recipes')
    #scraper('http://www.taste.com.au/recipes/37822/chilli+mint+chicken+with+avocado+and+snow+pea+sprouts?ref=zone,lunch-and-snacks')
    scraper(url)



