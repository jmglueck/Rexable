from bs4 import BeautifulSoup
from urllib.request import urlopen
import re

def webscrape_recipe(the_url):
    answer_str = ''
    try:
        html = urlopen(the_url)
        soup = BeautifulSoup(html.read(), "html.parser")
        #matches with tags with the classes that contain any of 'preparation', 'direction', or 'instruction'
        regex = re.compile(".*(preparation|direction|instruction).*")
        results = soup.find_all('div', attrs = {'class': regex})
        regex2 = re.compile(r"<[^>]*>", re.IGNORECASE)
        for j in results:
            temp_str = str(j)
            #replaces matches with the newline
            newtext = re.sub(regex2, '\n', temp_str) 
            answer_str = answer_str + newtext
    except Exception as e:
        print(e)
        answer_str = 'No recipe text found.'
    return answer_str