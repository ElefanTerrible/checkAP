# checkAP
Riot API challenge entry

The main goal of this project is to provide useful data on how changes to AP items made in patch 5.13 influenced the game. 

Most services providing match data analysis do not focus enough on the order of item purchases during the match. Information on whether item was bought in the game is not enough to get to proper conclusions about item power, its situational usefulness or synergy with a champion. CheckAP provides useful data about item purchase order and how this order influences the outcome of the match, while also showing the differences between item purchase order in patches 5.11 and 5.14.

Since contestants were provided with fixed amount of match data, author decided to not store match data in database but simply process data with created python scripts. First of them "getterScript.py" was responsible for downloading data, preprocess it in search for meaningful information and storing it for further aggregation and processing. Since analysis involved roughly 200000 matches (author decided that unranked games are too unpredictable in item builds and outcomes and focused only on ranked matches) basic api key allowed to get all data in short amount of time. Data processed by first script was agregated and further analysed with script "checkAP.py".

Aggregated data was then finally processed and displayed in web app resembling a chalkboard (sentiment - author spends a lot of time in front of one).

Data shown 
Interface of the app consists of icons of champions and items. Icon, when clicked, displays analysed data for champion/item. For champions - most common purchases of items are provided with specific information of which major AP item purchase it was and how often that purchase order resulted in a success. It shows information for both 5.11 and 5.14 patches what allows to arrive at conclusions about changes in item power or synergy with a specific champion (if for example an item was bought more often as 1st item instead of 3rd in former patch). For items - popularity of each item as 1st, 2nd, 3rd item is provided in form of a graph. That allows to see at what phase of the game item is most purchased. For every item, data about win ratio for 3 first buy positions is also included which provides some information about power of the item in every stage of the game. Author decided not to include data about 4th 5th and 6th buys because there was not enough information (games not long enough, non AP items purchased, limited number of matches) also, only champions that played solo lane in their games were included (to avoid data where for ex. support buys first ap item in 50 minute which influences avg. item buy time). 

Conclusions
- programing canvas without using external libraries is difficult
- Author regrets that he discovered contest too late (21 of August) and could not polish everything given very limited amount of time he had.
- For this type of analysis 100000 games for every patch is not enough