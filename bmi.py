import requests

def get_bmi(age,weight,height,male):
	url1 = "https://fitness-calculator.p.rapidapi.com/bmi"

	querystring1 = {"age":age,"weight":weight,"height":height}
	headers= {
	    'x-rapidapi-key': "426b4d96cemshd973fe08c584871p189d8ajsnfd7cf6c191bf",
	    'x-rapidapi-host': "fitness-calculator.p.rapidapi.com"
	    }

	response1 = requests.request("GET", url1, headers=headers, params=querystring1)
	url2 = "https://fitness-calculator.p.rapidapi.com/idealweight"

	querystring2 = {"gender":'male' if male else 'female',"weight":weight,"height":"178"}


	response2 = requests.request("GET", url2, headers=headers, params=querystring2)

	return [response1.json(),response2.json()]
