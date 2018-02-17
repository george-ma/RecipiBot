from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage

import random
import praw
import re
import webbrowser

reddit = praw.Reddit(user_agent='RecipiBot',
                         client_id='mieR1fbOj7yQAQ',
                         client_secret='odxIUlRELzho1gjBq9Q8j7OiL7U')

    # assume you have a Reddit instance bound to variable `reddit`
subreddit = reddit.subreddit('recipes')

def extract_ingrediants(body):
    ingredients_index = [i for i, item in enumerate(body) if re.search('.*Ingredients.*', item)]
    instructions_index = [i for i, item in enumerate(body) if re.search('.*Instructions.*|.*Directions.*|.*Method.*|.*Preparation.*', item, re.IGNORECASE)]
    return (ingredients_index[0] if len(ingredients_index) > 0 else 0, instructions_index[0] if len(instructions_index) > 0 else 0)


def get_recipe(ingredients_list):


    recipe_submission = list(set(subreddit.search('flair:"Recipe"')))
    not_found = True
    number = len(ingredients_list)
    while not_found:
        id = random.choice(recipe_submission)
        body = reddit.submission(id=id)
        index = extract_ingrediants(body.comments[0].body.splitlines())
        found = 0
        for i in range(index[0], index[1]):
            body_split = body.comments[0].body.splitlines()[i]
            # for ingredient in ingredients_list:
            if re.search('.*' + ingredients_list[found] + '.*', body_split, re.IGNORECASE):
                found += 1
                if found == number:
                    not_found = False
                    break
            if not not_found:
                break
        recipe_submission.remove(id)

    return (0, 0, 0) if not_found else ("http://www.reddit.com" + body.permalink, body.title, id)








def output_prediction(word):
    app = ClarifaiApp(api_key='b93c9746c9cc4a79baec13d0a83739cb')
    model = app.models.get('food-items-v1.0')
    image = ClImage(url=word)
    data = model.predict([image])
    food_list = [data['outputs'][0]['data']['concepts'][0]['name']]
    webbrowser.open(get_recipe(food_list)[0])
