import requests
from bs4 import BeautifulSoup
from mdutils.tools.Table import Table
from mdutils import MdUtils
from mdutils.tools.Image import Image
from googlesearch import search
import re
from mdutils.mdutils import MdUtils
import os



def remove_square_brackets(text):
    # Use regular expression to remove square brackets and their contents
    clean_text = re.sub(r'\[.*?\]', '', text)
    return clean_text

def scrape_wikipedia_article(url):
    # Send a GET request to the Wikipedia URL
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content using Beautiful Soup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the main content of the article (usually contained within <p> tags)
        paragraphs = soup.find_all('p')[:6]
        
        paragraphs = [x for x in paragraphs if x.text.replace('\n', '').replace(' ', '') != '']
                
        return paragraphs
    else:
        print(f"Failed to retrieve the article. Status code: {response.status_code}")
        return None


def cut_string_after_phrase(input_string, phrase):
    # Find the position of the phrase
    position = input_string.find(phrase)
    
    # If the phrase is found, return the portion of the string before the phrase
    if position != -1:
        return input_string[:position + len(phrase)]
    else:
        # If the phrase is not found, return the original string
        return input_string


base_page = 'https://www.tiobe.com'
script_dir = os.path.dirname(os.path.abspath(__file__))

'''
file = open("strona.txt", "r")
language_html = '\n'.join(file.readlines())
'''
r = requests.get(base_page + '/tiobe-index/')
language_html = r.content


soup = BeautifulSoup(language_html, 'html.parser')


####### Main page#########
article = soup.find_all(class_='tiobe-index container')[0]

link = base_page + article.find_all('a', href=True)[1]['href']
general_description = article.find_all('p')[1].text
general_description = cut_string_after_phrase(general_description, "index can be found ").replace('\n', ' ')




md = MdUtils(file_name = script_dir + '/content/_index', title='TIOBE Index for February 2024')

md.write(general_description)
md.write(f"[here.]({link})")
md.new_line("[See the list of the top 20 programming languages in February 2024](/strona/language_list)")
md.create_md_file()




######List########
tabelka = soup.find("table", {"id": "top20"})
jezyki = tabelka.find_all("tr")[1:]
lista_jezykow = []
for j in jezyki:
    t = j.find_all("td")
    nr = t[0].get_text()
    name = t[4].get_text()
    share = t[5].get_text()
    src = base_page + t[3].find("img")['src']
    zdj = f'![Image]({src})'
    filename = '/' + name.replace(" ", "").replace('/', '').lower()
    filelink = '/strona' + filename

    article_text = "loren ipsum"
    url = 'www.wikipedia.org'

    url = list(search(name + " site:wikipedia.org", stop=1))[0]

    paragraphs = scrape_wikipedia_article(url)
    article_summary = remove_square_brackets(paragraphs[0].text)
    article_text = remove_square_brackets(' '.join([p.text for p in paragraphs]))



    md = MdUtils(file_name= script_dir + '/content' + filename, title=name)
    md.new_line(f"![{name}]({src})")
    md.new_line(article_text)
    md.new_line(f"[Wikipedia]({url})")
    md.create_md_file()

    
    lista_jezykow.append({"nr": nr, "image": src, "name": name, "share": share, "description": article_summary, "url": url, "link": filelink})




md = MdUtils(file_name= script_dir + '/content/language_list', title='Top 20 programming languages in February 2024')

for item_info in lista_jezykow:
    # Add item name as a heading
    md.new_paragraph(f"# [{item_info['name']}]({item_info['link']}) ![{item_info['name']}]({item_info['image']})")

    md.new_paragraph(f"**Number:** {item_info['nr']}")
    md.new_paragraph(f"**Share:** {item_info['share']}")

    # Add image using Markdown syntax
    
    
    # Add description of the item
    md.new_paragraph(item_info['description'])

# Write the markdown file
md.create_md_file()




# Jely Hugo
