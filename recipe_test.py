import random

import praw
import re

reddit = praw.Reddit(user_agent='RecipiBot',
                         client_id='mieR1fbOj7yQAQ',
                         client_secret='odxIUlRELzho1gjBq9Q8j7OiL7U')

    # assume you have a Reddit instance bound to variable `reddit`
subreddit = reddit.subreddit('recipes')

def extract_ingrediants(body):
    ingredients_index = [i for i, item in enumerate(body) if re.search('.*Ingredients.*', item)]
    instructions_index = [i for i, item in enumerate(body) if re.search('.*Instructions.*|.*Directions.*|.*Method.*|.*Preparation.*', item, re.IGNORECASE)]
    return (ingredients_index[0] if len(ingredients_index) > 0 else 0, instructions_index[0] if len(instructions_index) > 0 else 0)

# for i in range(10000):
#     print("\n DIVIDE \n")
#     body = reddit.submission(id=random.choice(recipe_submission)).comments[0].body
#     # print(body)
#     a = extract_ingrediants(body.splitlines())
#     if len(a) < 2:
#         continue
#     for i in range(a[0], a[1]):
#         print(body.splitlines()[i])

def get_recipe(ingredients_list, used_recipe):


    recipe_submission = list(set(subreddit.search('flair:"Recipe"')) - set(used_recipe))
    not_found = True
    count = 0
    number = len(ingredients_list)
    while count < 20 and not_found and (len(recipe_submission) > 0):
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
        count += 1
        recipe_submission.remove(id)

    return (0, 0, 0) if not_found else ("http://www.reddit.com" + body.permalink, body.title, id)





