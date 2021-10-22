import boto3
from bs4 import BeautifulSoup
import ntpath
import csv

def handler(event, context):
	try:
		bucketName = event['Records'][0]['s3']['bucket']['name']
		fileName = event['Records'][0]['s3']['object']['key']
		fileName = fileName.replace('%3D', '=')
		s3 = boto3.resource('s3')
		justFileName = ntpath.basename(fileName)
		s3.meta.client.download_file(bucketName, fileName, '/tmp/' + justFileName)
		f = open('/tmp/' + justFileName, 'r', encoding='utf-8')
		txt = f.read()
		soup = BeautifulSoup(txt, 'html.parser')
		if ("El_Tiempo" in fileName):
			webscraping(fileName, justFileName, "El_Tiempo", soup, s3)
		elif ("El_Espectador" in fileName):
			webscraping(fileName, justFileName, "El_Espectador", soup, s3)

		return {"statusCode": 200, "Body": "Successful WebScraping"}
	except Exception as e:
		return {"statusCode": 400, "Body": f"Failed WebScraping, error {e}"}

def webscraping(fullPath,fileName,newspaper,soup,s3):
	bucket = "news-big-data2021-2"
	csvFile = open('/tmp/' + fileName + '.csv', 'w', encoding='utf-8')
	writer = csv.writer(csvFile, dialect='unix')
	row = ['title', 'section', 'url']
	writer.writerow(row)

	if newspaper == "El_Tiempo":
		articles = soup.find_all('article')
		for article in articles:
			category_anchor = article.find("a", {'class': 'category'})
			title_anchor = article.find("a", {'class': 'title'})
			if category_anchor and title_anchor:
				category = category_anchor.getText()
				title = title_anchor.getText()
				url = 'https://www.eltiempo.com' + title_anchor.get('href')
				row = [title, category, url]
				writer.writerow(row)
	elif newspaper == "El_Espectador":
		articles = soup.findAll('div', {'class': 'Card-Container'})
		for article in articles:
			category_div = article.find("h4", {'class': 'Card-Section'})
			title_div = article.find("h2", {'class': 'Card-Title'})
			if category_div and title_div:
				category_anchor = category_div.find("a")
				category = category_anchor.getText()
				title_anchor = title_div.find("a")
				title = title_anchor.getText()
				url = 'https://www.elespectador.com' + title_anchor.get('href')
				row = [title, category, url]
				writer.writerow(row)
	csvFile.close()
	underFolders = fullPath.replace('headlines/raw', '')
	s3.meta.client.upload_file('/tmp/' + fileName + '.csv', bucket, 'news/final' + underFolders + '.csv')