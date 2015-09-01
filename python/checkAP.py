import requests, json, time, sys
from operator import itemgetter, attrgetter, methodcaller

toProcess = ['EUNE', 'EUW', 'NA', 'KR' 'LAN', 'LAS', 'OCE', 'BR', 'RU', 'TR']

def convertToTime(val):
	minutes = str(val // 60000)
	seconds = str((val % 60000) / 1000).zfill(2)
	return minutes + ':' + seconds
	
def processFiles(sufix):
	for prefix in toProcess:
		filename = prefix + sufix + '.json'
		processFile(filename)

def processFile(name):
	with open(inputFile, 'r') as file:
		statsData = json.load(file)
	analysedFiles += statsData['processedGames']	

def getItemInfo(akey):
	parameters = {'itemListData': 'all', 'api_key': akey}
	req = 'https://global.api.pvp.net/api/lol/static-data/euw/v1.2/item'
	r = requests.get(req, params=parameters)
	if r.status_code == 200:
		itemDictionary = {}
		itemData = r.json()
		for i in itemData['data']:
			itemDictionary.update({itemData['data'][i]['id'] : itemData['data'][i]['name']})
		itemIDList = set(itemDictionary.keys())	
		return itemDictionary, itemIDList	
	else:
		print "ERROR Item info"
		sys.exit(str("Failed to obtain item data"))
		
analysedMatches = 0	
processFiles('before')
print analysedFiles	
		
	
	
		
		