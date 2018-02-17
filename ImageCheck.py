from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
from recipe_test import *

def output_prediction(word):
    app = ClarifaiApp(api_key='b93c9746c9cc4a79baec13d0a83739cb')
    model = app.models.get('food-items-v1.0')
    image = ClImage(url=word)
    data = model.predict([image])
    food_list = [data['outputs'][0]['data']['concepts'][0]['name']]
    return (food_list[0], get_recipe(food_list, [])[0])
