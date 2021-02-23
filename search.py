import urllib.parse
import urllib.request

def search(text):
	result = []
	url = 'https://api.edamam.com/search'
	query = {
	    'q':text,
	    'app_id':'ae963fd3',
	    'app_key':'157b37ca0ebe63d6a29058cc75b3052d',
	    'from':0,
	    'to':5,
	    'count':10,
	    'more':'false',
	    'calories':'200'
	}
	url = url + '?' + urllib.parse.urlencode(query)
	response = urllib.request.urlopen(url)
	data = eval(response.read().decode('utf-8').replace("true", "True").replace("false","False").replace('null','None'))
	for i in range(5):
		result.append((data['hits'][i]['recipe']['label']))
	return result
