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
    total_result = 50
    API_ID = '278937dd'
    API_KEY = 'd3c394fe3da45b85e2c2dc534748b4b8'
    PATH = f'https://api.edamam.com/search?q={query}&app_id={API_ID}&app_key={API_KEY}&from=0&to={total_result}'



    response = requests.get(PATH)
##    jprint(response.json())


    for number_of_result in range(total_result):

        

        try:
            calories = response.json()["hits"][number_of_result]["recipe"]["calories"]
            ingredient_list = response.json()["hits"][number_of_result]["recipe"]["ingredientLines"]
            food_label = response.json()["hits"][number_of_result]["recipe"]["label"]
            image_link = response.json()["hits"][number_of_result]["recipe"]["image"]
            source = response.json()["hits"][number_of_result]["recipe"]["url"]
            health_labels = response.json()["hits"][number_of_result]["recipe"]["healthLabels"]
            diet_labels = response.json()["hits"][number_of_result]["recipe"]["dietLabels"]

            try:
                meal_type = response.json()["hits"][number_of_result]["recipe"]["mealType"][0]
            except KeyError as ke:
                meal_type = None
                print(food_label + ' is missing '+str(ke))

            try:
                dish_type = response.json()["hits"][number_of_result]["recipe"]["dishType"][0]
            except KeyError as ke:
                dish_type = None
                print(food_label + ' is missing '+str(ke))
            fat_content = response.json()["hits"][number_of_result]["recipe"]["totalNutrients"]["FAT"]
            carb_content = response.json()["hits"][number_of_result]["recipe"]["totalNutrients"]["CHOCDF"]
            sugar_content = response.json()["hits"][number_of_result]["recipe"]["totalNutrients"]["SUGAR"]
            salt_content = response.json()["hits"][number_of_result]["recipe"]["totalNutrients"]["NA"]

            result_dict['search_query'] = query
            result_dict['recipe_name'] = food_label
            result_dict['calories'] = "{:.0f}".format(calories)
            result_dict['ingredient'] = ingredient_list
            result_dict['image_link'] = image_link
            result_dict['source_url'] = source
            result_dict['tags'] = health_labels
            result_dict['diet'] = diet_labels
            result_dict['meal_type'] = meal_type
            result_dict['dish_type'] = dish_type
            result_dict['fat_content'] = fat_content
            result_dict['carb_content'] = carb_content
            result_dict['sugar_content'] = sugar_content
            result_dict['salt_content'] = salt_content


            result_list.append(result_dict)
            result_dict = {}

        except IndexError:
            print(f'Only {number_of_result} results')
            break
        except KeyError as ke:
            print(food_label + ' is missing '+str(ke))
##            print(f'5 Queries/Minute REACHED, please wait...')
            continue
        
##        print()
##        
##        print("Recipe Name: " + food_label)
##        #print(response.json())
##
##        
##        print("Calories: "+ "{:.0f}".format(calories))
##        
##        
##        ingredient_list = response.json()["hits"][number_of_result]["recipe"]["ingredientLines"]
##        count = 1
##        print("Ingredients: ",end='')
##        for i in ingredient_list:
##            if count<len(ingredient_list):
##                i = i+', '
##                print(i,end='')
##            else:
##                print(i)
##            count+=1
##        
##        print("Image Link: " + image_link)
##        print()
        

        
    return result_list
        
