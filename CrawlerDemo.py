from googlesearch import search
import sys
import requests
from bs4 import BeautifulSoup
from gensim.summarization import keywords
import gensim
import networkx
import matplotlib.pyplot as plt

from gensim.summarization import keywords
import spacy
spacy_nlp = spacy.load('en_core_web_sm')


months = ["January","February","March","April","May","June","July","August","September","October","November","December"]

def any(list1,list2):
	"""

	:param list1:
	:param list2:
	:return:
	"""
	for each in list1 :
		if each in list2:
			return True
	return False

def smartSearch(query):
	"""

	:param query:
	:return:
	"""
	query  = "awesome github " + query
	urlList = [url for url in search(query, tld="co.in", num=10, stop=6, pause = 1)]
	request_url = requests.get(urlList[0])
	return request_url


def getTitle(webPage):
	"""

	:param webPage:
	:return:
	"""
	soup = BeautifulSoup(webPage.text,"html.parser")
	text = ' '.join(map(lambda var : var.text,soup.find_all("title")))
	return text


def summarizedPage(url):
	"""
	Takes input url
	:param :url
	:return: returns Summary in list format
	"""
	soup = BeautifulSoup(requests.get(url).text,"html.parser")
	hs = ["h1","h2","h3"]
	words = set()
	for hi in hs:
		textList = list(map(lambda var: var.text, soup.find_all(hi)))
		for text in textList:
			if not any(text.split(" "),months) and text != "":
				words.add(text)
	paras = list(map(lambda var : var.text,soup.find_all("p")))
	for para in paras:
		words.add(keywords(para, ratio=1.0,split=False,lemmatize=True,pos_filter=("NN")))

	return words

def parseMenu():
	"""
	:return:
	"""
	webPage = smartSearch("awesome github " + sys.argv[1])
	print(getTitle(webPage = webPage))
	soup = BeautifulSoup(webPage.text,"html.parser")
	unorderedlists = soup.find_all("ul")
	urls = []
	for u in unorderedlists:
		children = u.findChildren("a",href=True)
		for child in children :
			if child['href']:
				if 'github' not in child['href'] and child['href'][0] != '/' and 'opensource.guide' not in child['href'] and child['href'][0] != '#' :
					print((child.text, child['href']))
					urls.append((child.text,child['href']))

	return urls

def summarizeList(urls):
	"""
	:param urls:
	:return:
	"""
	tupleList = []
	for url in urls :
		summary = summarizedPage(url[1])
		tupleList.append((url[0],url[1],summary))
	return tupleList
plt.savefig("simple_path.png")
def main(keyword):
	webPage = smartSearch(keyword)
	print(getTitle(webPage = webPage))
	soup = BeautifulSoup(webPage.text,"html.parser")
	unorderedlists = soup.find_all("ul")
	#print(unorderedlists.find("a"))
	web_objects = [];
	for  u in  unorderedlists:
		children = u.findChildren("a",href=True)
		for child in children :
			if child['href']:
				if 'github' not in child['href'] and child['href'][0] != '/' and 'opensource.guide' not in child['href'] and child['href'][0] != '#' :
					title = [i for i in child.text if i.isalnum() or i == ' ']
					doc = spacy_nlp(''.join(title))
					tokens = [token.text for token in doc if not token.is_stop]
					title = ' '.join(tokens)
					web_objects.append((title,child['href']))
					#print((child.text,",",child["href"]))
	# for o in web_objects:
		# title = [i for i in o[0] if i.isalnum() or i == ' ']
		# #print(''.join(title))
		# doc = spacy_nlp(''.join(title))
		# tokens = [token.text for token in doc if not token.is_stop]
		# title = ' '.join(tokens)
		# print(o[0])	
		# o[0] = title
	return web_objects

def buildDAG(webObjects):
	"""

	:param webObjects:
	:return:
	"""
	directed_graph = networkx.DiGraph()
	for webObject1 in webObjects:
		for webObject2 in webObjects:
			if webObject1 == webObject2:
				continue
			for para in webObject2[2]:
				# title = gensim.summarization.keywords(webObject1[0].lower(), ratio=1.0, pos_filter=('NN'),lemmatize=True)
				# title2 = gensim.summarization.keywords(webObject2[0].lower(), ratio=1.0, pos_filter=('NN'),lemmatize=True)
				title,title2 = webObject1[0].lower(),webObject2[0].lower()
				for word in title.split(' '):
					if word in para:
						node1 = (title, webObject1[1])
						node2 = (title2, webObject2[1])
						#node1 = title
						#node2 = title2
						print(title,para)
						directed_graph.add_edge(node1,node2)
	return directed_graph


if __name__ == "__main__":

	# print(summarizedList("https://www.coursera.org/learn/systems-biology"))
	sList = summarizeList([("Python", "https://realpython.com/python-idle/"),
				   ("Numpy", "https://www.edureka.co/blog/python-numpy-tutorial/"),
				   ("Scikit-Learn","https://towardsdatascience.com/hands-on-introduction-to-scikit-learn-sklearn-f3df652ff8f2")
				   ])
	#sList = summarizeList(main("biology")[:5])

	#print(List)
	# for each in sList:
	# 	print(each)
	#print(sList)
	dag = buildDAG(sList)
	print(dag.nodes())

	networkx.draw_networkx(dag, with_labels=True)
	#networkx.draw(dag, pos=networkx.spring_layout(dag))
	plt.savefig("directedGraph.png")
	plt.show()






