import requests
import json


def getPokemon(pokemon):
    
    url = "https://pokeapi.co/api/v2/pokemon/%s" % (pokemon)

    try:
        response = requests.get(url).json()
        print(json.dumps(response, indent=4))
    except requests.exceptions.RequestException as e:
        print("Error: %s" % (e))



def getSpecies(pokemon):

    url = "https://pokeapi.co/api/v2/pokemon-species/%s" % (pokemon)

    try:
        response = requests.get(url).json()
        print(json.dumps(response, indent=4))
    except requests.exceptions.RequestException as e:
        print("Error: %s" % (e))



def getType(number):

    url = "https://pokeapi.co/api/v2/type/%s" % (number)

    try:
        response = requests.get(url).json()
        print(json.dumps(response, indent=4))
    except requests.exceptions.RequestException as e:
        print("Error: %s" % (e))



def getAbility(ability):

    url = "https://pokeapi.co/api/v2/ability/%s" % (ability)

    try:
        response = requests.get(url).json()
        print(json.dumps(response, indent=4))
    except requests.exceptions.RequestException as e:
        print("Error: %s" % (e))



def getListOfPokemon(number):

    url = "https://pokeapi.co/api/v2/pokemon?limit=%s&offset=0" % (number)

    try:
        response = requests.get(url).json()
        print(json.dumps(response, indent=4))
    except requests.exceptions.RequestException as e:
        print("Error: %s" % (e))