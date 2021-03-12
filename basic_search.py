import requests
import json



def search(query,allergy,num = 10):
    result_list = []
    result_dict = {}

    
    def jprint(obj):
        # create a formatted string of the Python JSON object
        text = json.dumps(obj, sort_keys=True, indent=4)
        print(text)



##    query = input('Please enter your food for recipe: ')
    # query = "chicken"
    total_result = num
    API_ID = '278937dd'
    API_KEY = 'd3c394fe3da45b85e2c2dc534748b4b8'
    PATH = f'https://api.edamam.com/search?q={query}&app_id={API_ID}&app_key={API_KEY}&hits=recipe[ingredients]&from=0&to={total_result}'
    for i in allergy:
        PATH+= ('&health='+i)



    response = requests.get(PATH)
    # jprint(response.json())

    print(len(response.json()["hits"]))
    for number_of_result in range(len(response.json()["hits"])):

        calories = response.json()["hits"][number_of_result]["recipe"]["calories"]
        ingredient_list = response.json()["hits"][number_of_result]["recipe"]["ingredientLines"]
        food_label = response.json()["hits"][number_of_result]["recipe"]["label"]
        image_link = response.json()["hits"][number_of_result]["recipe"]["image"]
        url= response.json()["hits"][number_of_result]["recipe"]["url"]


        result_dict['search_query'] = query
        result_dict['recipe_name'] = food_label
        result_dict['calories'] = "{:.0f}".format(calories)
        result_dict['ingredient'] = ingredient_list
        result_dict['image_link'] = image_link
        result_dict['url'] = url
        result_list.append(result_dict)
        result_dict = {}

        
        
        ingredient_list = response.json()["hits"][number_of_result]["recipe"]["ingredientLines"]
        count = 1

        for i in ingredient_list:
            if count<len(ingredient_list):
                i = i+', '
            else:

                count+=1
        

        

        
    return result_list
