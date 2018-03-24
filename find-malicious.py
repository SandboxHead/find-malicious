import requests
from bs4 import BeautifulSoup 
from gglsbl import SafeBrowsingList
import yaml, sys



formats = []
def check_format(link):
	for form in formats:
		if (link.endswith(form)):
			return True
	return False

def find(domain):
	links = set()
	find_links(domain, domain, links)
	return links

def find_links(link, domain, links):
	page = requests.get(link)
	links.add(link)
	try:
		page.raise_for_status()
	except:
		return links
	soup = BeautifulSoup(page.text, "lxml")
	elements = soup.findAll('a')
	
	for a in elements:
		my_link = a.get('href')
		
		if (my_link==None or len(my_link)==0 or my_link[0]=='#' or my_link[0:6]=='mailto'):
			continue
		if (check_format(my_link)):
			continue
		
		elif (my_link[0]=='/'):
			link_forward = domain + my_link
			if (link_forward not in links):
				find_links(link_forward, domain, links)
			
		elif (my_link[0:4]!='http'):
			link_forward = domain + '/' + my_link
			if (link_forward not in links):
				find_links(link_forward, domain, links)

		elif (my_link.startswith(domain)):
			if (my_link not in links):
				find_links(my_link, domain, links)

		else :
			links.add(my_link)



def find_threats(link, api_key):
	sbl = SafeBrowsingList(api_key)
	try:
		threat_list = sbl.lookup_url(link)
	except :
		threat_list = None
		pass

	if threat_list == None:
		return ('No threat')
	else:
		return ('Threats: '+ str(threat_list))


def main():
	threats = {}
	with open('keys.yaml') as f:
		keys = yaml.load(f)
		key = keys['API_KEY']
		formats = keys['FORMATS']
	filename = sys.argv[1]
	file_object = open(filename, "r")
	file_write  = open(sys.argv[2], 'w')
	for line in file_object:
		link = "https://www.cse.iitd.ac.in/~"+line[:-1]
		for web_link in find(link):
			print ("[@] "+web_link)
			threat = find_threats(web_link, key)
			if (threat!= "No threat"):
				file_write.write('[*] {} : {} : {}'.format(link, web_link, threat))
	file_object.close()
	file_write.close()
	

if __name__=='__main__':
    main()