import requests, json, time, sys
from operator import itemgetter, attrgetter, methodcaller


	
def processGames(api_key, urladd, gameListFile, whatServer, outputFile, incorrectFile):
	inputFile = open(gameListFile, 'r')
	gameList = json.load(inputFile)
	gamesProcessed = 0
	gamesCounter = 0
	terminate = 0
	for game in gameList:
		currently_processed = int(game)
		gamesCounter += 1
		terminate += 1
		if terminate < 10:
			req = urladd + str(game)
			print req + '\n'
			processGame(req, outputFile, api_key)
			if gamesCounter > 9:
				print terminate
				gamesCounter = 0
				time.sleep(10)
		else:
			with open(outputFile, 'w') as outfile:
				json.dump(outputDictionary, outfile)
			with open(incorrectFile, 'w') as outfile:
				json.dump(processed_uncorrectly, outfile)
			sys.exit(str(terminate))
			
def getItemInfo(akey):
	parameters = {'itemListData': 'all', 'api_key': akey}
	req = 'https://global.api.pvp.net/api/lol/static-data/euw/v1.2/item'
	r = requests.get(req, params=parameters)
	if r.status_code == 200:
		smallDict = {}
		itemDict = {}
		itemData = r.json()
		for i in itemData['data']:
			if 'FlatMagicDamageMod' in itemData['data'][i]['stats'] and itemData['data'][i].has_key('from') and itemData['data'][i].has_key('into') == False:
				itemDict.update({itemData['data'][i]['id'] : itemData['data'][i]['name']})
		itemDict.update({3003 : 'Archangel\'s Staff'})
		smallDict.update({1058 : 'Needlessly Large Rod'})
		smallDict.update({3108 : 'Fiendish Codex'})
		smallDict.update({1026 : 'Blasting Wand'})
		smallDict.update({3113 : 'Aether Wisp'})
		smallDict.update({3145 : 'Hextech Revolver'})
		smallDict.update({3191 : 'Seeker\'s Armguard'})
		smallDict.update({3057 : 'Sheen'})
		smallDict.update({3136 : 'Haunting Guise'})
		
		del itemDict[3040]
		del itemDict[3048]
		del itemDict[3090]
		del itemDict[3170]
		del itemDict[3430]
		del itemDict[3431]
		del itemDict[3434]
		del itemDict[3744]
		del itemDict[3829]
		itemList = set(itemDict.keys())	
		smallList = set(smallDict.keys())
	else:
		print "ERROR Item info"
		sys.exit(str(terminate))
	return itemDict, itemList, smallDict, smallList	
	
def getChampionInfo(akey):
	parameters = {'api_key': akey}
	req = 'https://global.api.pvp.net/api/lol/static-data/euw/v1.2/champion'
	r = requests.get(req, params=parameters)
	if r.status_code == 200:
		championData = r.json()
	else:
		print "ERROR Champ info"
		sys.exit(str(terminate))	
	return championData	
	
def processGame(gameURL, outFile, akey):
	global processed_uncorrectly
	parameters = {'includeTimeline': 'true', 'api_key': akey}
	r = requests.get(gameURL, params=parameters)
	if r.status_code == 200:
		outputDictionary['processedGames'] += 1
		championInfo = {}
		temp = {'itemsPurchased':{}}
		matchdata = r.json()
		purchases = []
		smallPurchases = []
		for i in matchdata['participants']:
			championInfo[i['participantId']] = {'championID': i['championId'], 'role': i['timeline']['role'], 'win':(i['stats']['winner'] * 1)}
		for i in matchdata['timeline']['frames']:
			if i.has_key('events'):
				for j in i['events']:
					if j['eventType'] == 'ITEM_PURCHASED' and championInfo[j['participantId']]['role'] == 'SOLO':
						if j['itemId'] in APitems:
							purchases.append(j)
						elif j['itemId'] in smallAPitems:
							smallPurchases.append(j)
					elif j['eventType'] == 'ITEM_UNDO' and championInfo[j['participantId']]['role'] == 'SOLO':
						if j['itemBefore'] in APitems:
							for x in purchases:
								if x['participantId'] == j['participantId'] and x['itemId'] == j['itemBefore']:
									purchases.remove(x)
						elif j['itemBefore'] in smallAPitems:
							for x in smallPurchases:
								if x['participantId'] == j['participantId'] and x['itemId'] == j['itemBefore']:
									smallPurchases.remove(x)
			
		purchases = sorted(purchases, key=itemgetter('participantId'))
		smallPurchases = sorted(smallPurchases, key=itemgetter('participantId'))
		player = 0
		whichItem = 0
		for a in purchases:
			currentChampion = championInfo[a['participantId']]['championID']
			if outputDictionary['championID'].has_key(currentChampion) == False:
				outputDictionary['championID'][currentChampion] = {}
			if 	outputDictionary['championID'][currentChampion].has_key(itemId_Name[a['itemId']]) == False:
				outputDictionary['championID'][currentChampion][itemId_Name[a['itemId']]] = {}
			if 	outputDictionary['championID'][currentChampion].has_key('smallPurchases') == False:
				outputDictionary['championID'][currentChampion]['smallPurchases'] = {}		
			if a['participantId'] != player:
				player = a['participantId']
				whichItem = 1  
			else:
				whichItem += 1
				
			if outputDictionary['championID'][currentChampion][itemId_Name[a['itemId']]].has_key(whichItem) == False:
				outputDictionary['championID'][currentChampion][itemId_Name[a['itemId']]][whichItem] = {'numbuys' : 1, 'win':championInfo[a['participantId']]['win']}
			else:
				outputDictionary['championID'][currentChampion][itemId_Name[a['itemId']]][whichItem]['numbuys'] += 1
				outputDictionary['championID'][currentChampion][itemId_Name[a['itemId']]][whichItem]['win'] += championInfo[a['participantId']]['win']
				
			if outputDictionary['championID'][currentChampion][itemId_Name[a['itemId']]].has_key('purchasesum') == False:
				outputDictionary['championID'][currentChampion][itemId_Name[a['itemId']]]['purchasesum'] = a['timestamp']
			else:
				outputDictionary['championID'][currentChampion][itemId_Name[a['itemId']]]['purchasesum'] += a['timestamp']
				
			if outputDictionary['championID'][currentChampion][itemId_Name[a['itemId']]].has_key('numbuys') == False:
				outputDictionary['championID'][currentChampion][itemId_Name[a['itemId']]]['numbuys'] = 1
			else:
				outputDictionary['championID'][currentChampion][itemId_Name[a['itemId']]]['numbuys'] += 1
			sml = set()
			sml.clear()
			if whichItem == 1:
				if 	outputDictionary['championID'][currentChampion].has_key('appearanceNumber') == False:
					outputDictionary['championID'][currentChampion]['appearanceNumber'] = 1	
				else:
					outputDictionary['championID'][currentChampion]['appearanceNumber'] += 1	
				pur = []
				for x in smallPurchases:
					if x['timestamp'] < a['timestamp'] and x['participantId'] == a['participantId']:
						sml.add(x['itemId'])
				pur = []
				for p in smallPurchases:
						if p['itemId'] in sml and p['participantId'] == a['participantId']:
							pur.append(p)	
				if pur:		
						
					pur = sorted(pur, key=itemgetter('timestamp'))	
					if pur[0]['itemId'] == 1058:
						if outputDictionary['championID'][currentChampion]['smallPurchases'].has_key('Needlessly Large Rod') == False:
							outputDictionary['championID'][currentChampion]['smallPurchases']['Needlessly Large Rod'] = 1				
						else:
							outputDictionary['championID'][currentChampion]['smallPurchases']['Needlessly Large Rod'] += 1
							
					elif pur[0]['itemId'] == 3108:
						if outputDictionary['championID'][currentChampion]['smallPurchases'].has_key('Fiendish Codex') == False:
							outputDictionary['championID'][currentChampion]['smallPurchases']['Fiendish Codex'] = 1		
						else:
							outputDictionary['championID'][currentChampion]['smallPurchases']['Fiendish Codex'] += 1	
														
					elif pur[0]['itemId'] == 1026:
						if outputDictionary['championID'][currentChampion]['smallPurchases'].has_key('Blasting Wand') == False:
							outputDictionary['championID'][currentChampion]['smallPurchases']['Blasting Wand'] = 1	
						else:
							outputDictionary['championID'][currentChampion]['smallPurchases']['Blasting Wand'] += 1
							
					elif pur[0]['itemId'] == 3113:
						if outputDictionary['championID'][currentChampion]['smallPurchases'].has_key('Aether Wisp') == False:
							outputDictionary['championID'][currentChampion]['smallPurchases']['Aether Wisp'] = 1	
						else:
							outputDictionary['championID'][currentChampion]['smallPurchases']['Aether Wisp'] += 1
							
					elif pur[0]['itemId'] == 3145:
						if outputDictionary['championID'][currentChampion]['smallPurchases'].has_key('Hextech Revolver') == False:
							outputDictionary['championID'][currentChampion]['smallPurchases']['Hextech Revolver'] = 1
						else:
							outputDictionary['championID'][currentChampion]['smallPurchases']['Hextech Revolver'] += 1
							
					elif pur[0]['itemId'] == 3191:
						if outputDictionary['championID'][currentChampion]['smallPurchases'].has_key('Seeker\'s Armguard') == False:
							outputDictionary['championID'][currentChampion]['smallPurchases']['Seeker\'s Armguard'] = 1	
						else:
							outputDictionary['championID'][currentChampion]['smallPurchases']['Seeker\'s Armguard'] += 1
							
					elif pur[0]['itemId'] == 3057:
						if outputDictionary['championID'][currentChampion]['smallPurchases'].has_key('Sheen') == False:
							outputDictionary['championID'][currentChampion]['smallPurchases']['Sheen'] = 1	
						else:
							outputDictionary['championID'][currentChampion]['smallPurchases']['Sheen'] += 1	
							
					elif pur[0]['itemId'] == 3057:
						if outputDictionary['championID'][currentChampion]['smallPurchases'].has_key('Haunting Guise') == False:
							outputDictionary['championID'][currentChampion]['smallPurchases']['Haunting Guise'] = 1	
						else:
							outputDictionary['championID'][currentChampion]['smallPurchases']['Haunting Guise'] += 1	
									
	else:
		processed_uncorrectly.append(int(gameURL[-10:]))

def checkAverage(item):
	globalsum = 0
	globalbuys = 0
	for a in outputDictionary['championID']:
		if outputDictionary['championID'][a].has_key(item):
			globalsum += outputDictionary['championID'][a][item]['purchasesum']
			globalbuys += outputDictionary['championID'][a][item]['numbuys']
	result = convertToTime(globalsum / globalbuys)	
	
processed_uncorrectly = []
itemId_Name, APitems, smallAPIdName, smallAPitems = getItemInfo('KEY')
print itemId_Name, "\n"
print smallAPIdName, "-------------\n\n\n"
champions = getChampionInfo('KEY')
outputDictionary = {'processedGames' : 0, 'championID':{}, 'server':'EUW'}	

processGames('KEY', 'https://euw.api.pvp.net/api/lol/euw/v2.2/match/', 'AP_ITEM_DATASET/5.11/RANKED_SOLO/EUW.json', 'EUW', 'euw_ranked_solo_before.txt', 'euw_ranked_solo_before_error.txt')
