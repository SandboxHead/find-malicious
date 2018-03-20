import requests
from bs4 import BeautifulSoup 
from gglsbl import SafeBrowsingList
import yaml, sys


def find_links(link):
	page = requests.get(link)
	try:
		page.raise_for_status()
	except:
		return []
	soup = BeautifulSoup(page.text, "lxml")
	elements = soup.findAll('a')
	links = []
	for a in elements:
		my_link = a.get('href')
		if (my_link==None or len(my_link)==0 or my_link=='#'):
			continue
		elif (my_link[0]=='/'):
			links.append(link + my_link)
		elif (my_link[0]!='h'):
			links.append(link + '/' + my_link)
		else:
			links.append(my_link)
	return links



def find_threats(link, api_key):
	sbl = SafeBrowsingList(api_key)
	threat_list = sbl.lookup_url(link)
	if threat_list == None:
		return ('No threat')
	else:
		return ('threats: '+ str(threat_list))


def main():
	threats = {}
	with open('keys.yaml') as f:
		keys = yaml.load(f)
		key = keys['API_KEY']

	filename = sys.argv[1]
	file_object = open(filename, "r")
	for line in file_object:
		# print (line)
		link = "https://www.cse.iitd.ac.in/~"+line[:-1]
		print (link)
		for web_link in find_links(link):
			print (web_link)
			threats[web_link] = find_threats(web_link, key)

	print (threats)


if __name__=='__main__':
    main()