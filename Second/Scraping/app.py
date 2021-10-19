import requests
from bs4 import BeautifulSoup
import re


# La función get_main_news retornará un diccionario con todas las urls y títulos de noticias encontrados en la sección principal.
def get_main_news():
	url = 'https://www.eltiempo.com/'

	respuesta = requests.get(
		url,
		headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
		}
	)
	contenido_web = BeautifulSoup(respuesta.text, 'lxml')
	box = contenido_web.find('div', attrs={'class':'secondary-b1 containt'})
	seccion = box.findChildren('article', attrs={"class":"image-left"})
	for x in seccion:
		urlsec = x.find('a',attrs={'class':'epigraph page-link'})
		title = x.find('a',attrs={'class':'title page-link'})
		print(title)
		print(urlsec,end="\n\n")

if __name__ == '__main__':
    noticias = get_main_news()

#r = requests.get('https://www.eltiempo.com/')
#g = list(filter(lambda x: 'class="article-details"' in x, r))