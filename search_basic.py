import requests
import json



def search(query):
    result_list = []
    result_dict = {}

    
    def jprint(obj):
        # create a formatted string of the Python JSON object
        text = json.dumps(obj, sort_keys=True, indent=4)
        print(text)



##    query = input('Please enter your food for recipe: ')
    # query = "chicken"
    total_result = 2
    API_ID = '278937dd'
    API_KEY = 'd3c394fe3da45b85e2c2dc534748b4b8'
    PATH = f'https://api.edamam.com/search?q={query}&app_id={API_ID}&app_key={API_KEY}&hits=recipe[ingredients]&from=0&to={total_result}'



    response = requests.get(PATH)
    # jprint(response.json())


    for number_of_result in range(total_result):

        calories = response.json()["hits"][number_of_result]["recipe"]["calories"]
        ingredient_list = response.json()["hits"][number_of_result]["recipe"]["ingredientLines"]
        food_label = response.json()["hits"][number_of_result]["recipe"]["label"]
        image_link = response.json()["hits"][number_of_result]["recipe"]["image"]


        result_dict['search_query'] = query
        result_dict['recipe_name'] = food_label
        result_dict['calories'] = "{:.0f}".format(calories)
        result_dict['ingredient'] = ingredient_list
        result_dict['image_link'] = image_link
        result_list.append(result_dict)
        result_dict = {}
        print()
        
        print("Recipe Name: " + food_label)
        #print(response.json())

        
        print("Calories: "+ "{:.0f}".format(calories))
        
        
        ingredient_list = response.json()["hits"][number_of_result]["recipe"]["ingredientLines"]
        count = 1
        print("Ingredients: ",end='')
        for i in ingredient_list:
            if count<len(ingredient_list):
                i = i+', '
                print(i,end='')
            else:
                print(i)
            count+=1
        
        print("Image Link: " + image_link)
        print()
        

        
    return result_list
        
