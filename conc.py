import requests
from bs4 import BeautifulSoup
import json

url='https://www.pepite-pdl.fr/wp-json/wp/v2/pages/3386'

headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
blog_json = requests.get(url, headers=headers).json()

bs= BeautifulSoup(blog_json['content']['rendered'],"html.parser")

blocks=[]
for section in bs.find_all('section', class_='layoutContentImage gutenbergContent --hasBackground --backgroundWhite'):
    block=section.select("h3,h2,p,ul,li")
    blocks.append(block)

def parselink(nbr):
    res=""
    for row in blocks[nbr]:
        link=row.find_all('a',href=True)
        if link!=[]:
            res=link[0]['href']
    return res

def parseblock(row,h,title):
    conc={}

    try:
        while True:
            element=next(row)
            if element.name==h and element.text==title:
                conc['Titre']=element.text
                element=next(row)
                conc['description']=element.text
    except StopIteration:
        pass
    return conc



result=[]

for i in range(len(blocks)):
    crawl={}
    row=iter(blocks[i])
    crawl=parseblock(row,"h2",blocks[i][0].text)
    row=iter(blocks[i])
    crawl['calendrier']=parseblock(row,"h3","Calendrier :")['description']
    row=iter(blocks[i])
    try:
        crawl['prix']=parseblock(row,"h3","Prix à gagner :")['description']
    except:
        crawl['prix']="Non défini"
    result.append(crawl)
    crawl['link']=parselink(i)

with open('concours.json','w') as f:
    json.dump(result,f)

            
                          