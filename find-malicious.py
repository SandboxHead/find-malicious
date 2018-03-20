import requests
from bs4 import BeautifulSoup 
from gglsbl import SafeBrowsingList
import yaml

def find_link(link):
	page = requests.get(link)
	page.raise_for_status()
	soup = BeautifulSoup(page.text, "lxml")
	links = soup.findAll('a')
	return links



def find_threats(link, api_key):
	sbl = SafeBrowsingList(api_key)
	threat_list = sbl.lookup_url(link)
	if threat_list == None:
		return ('No threat')
	else:
		return ('threats: '+ str(threat_list))


def main():
	with open('keys.yaml') as f:
		keys = yaml.load(f)
		key = keys['API_KEY']
	print (find_threats("http://www.doubletree3hilton.com", key))

if __name__=='__main__':
    main()