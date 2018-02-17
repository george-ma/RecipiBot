from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage

def output_prediction(word):
    app = ClarifaiApp(api_key='b93c9746c9cc4a79baec13d0a83739cb')
    model = app.models.get('food-items-v1.0')
    image = ClImage(url=word)
    food_list = []
    data = model.predict([image])
    if len(data['outputs'][0]['data']['concepts']) == 1:
        food_list = [data['outputs'][0]['data']['concepts'][0]['name']]
    elif len(data['outputs'][0]['data']['concepts']) == 2:
        food_list = [data['outputs'][0]['data']['concepts'][0]['name'],data['outputs'][0]['data']['concepts'][1]['name']]
    elif len(data['outputs'][0]['data']['concepts']) == 3:
        food_list = [data['outputs'][0]['data']['concepts'][0]['name'], data['outputs'][0]['data']['concepts'][1]['name'], data['outputs'][0]['data']['concepts'][2]['name']]
    return food_list
