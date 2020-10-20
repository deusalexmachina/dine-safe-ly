import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','dinesafelysite.settings')

import django
django.setup()

import requests
import json
import pandas as pd
from sodapy import Socrata

from restaurant.models import Restaurant, InspectionRecords

def match_on_yelp(restaurant_name, restaurant_location):
    location_list = restaurant_location.split(", ")
    address1 = location_list[0]
    city = location_list[1]
    state = location_list[2]
    country = 'US'

    api_key = 'JaekzvTTKsWGtQ96HUiwAXOUwRt6Ndbqzch4zc2XFnOEBxwTmwr-esm1uWo2QFvFJtXS8nY2dXx51cfAnMqVHpHRcp8N7QtP7LNVCcoxJWV_9NJrmZWSMiq-R_mEX3Yx'
    YELP_ACCESS_TOKE = 'A_V_V4rxelsvDsI2uFW1kT2mP2lUjd75GTEEsEcLnnvVOK5ssemrbw-R49czpANtS2ZtAeCl6FaapQrp1_30cRt9YKao3pFL1I6304sAtwKwKJkF1JBgF88FZl1_X3Yx'
    headers = {'Authorization': 'Bearer %s' % YELP_ACCESS_TOKE}
    url = 'https://api.yelp.com/v3/businesses/matches'
    params = {'name': restaurant_name, 'address1': address1, 'city': city, 'state': state, 'country': country}

    response = requests.get(url, params=params, headers=headers)
    return response.text.encode("utf8")

if __name__ == '__main__':
    r = Restaurant.objects.all()[5000:]

    for rest in r:
        response = json.loads(match_on_yelp(rest.restaurant_name, rest.business_address))
        if next(iter(response)) == 'error':
            print("match failed")
            # print(response)
            continue
        elif not response['businesses']:
            print("not success")
            continue
        else:
            rest.business_id = response['businesses'][0]['id']
            rest.save()
            print("success")
        # print(rest)
        # print()