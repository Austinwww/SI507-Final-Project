#################################
##### Name: Yuchen Wu    ########
##### Uniqname: yuchenwu ########
#################################

from bs4 import BeautifulSoup
import requests
import json
import re
API_KEY = 'sQvJBRIZQ5QgHD34XviXXbXt6Dn1OJFSBHh39w9Jdl6zQgnqY0NLd_56YhVZT46Zdn1YZB' \
          'XXorD5EAuIUw9wZ5N-1WjfUVzEsJo6LfJu1rQl89qe0_632EF9vmFmZXYx'
CLIENT_ID = 'Bl9X4isxqq5Yf-LYu9LMIg'

CACHE_FILENAME = 'cache.json'
CACHE_DICT = {}
HEADERS = {'Authorization': 'Bearer ' + API_KEY}


def saveCache(cache):
    '''
    Save cache data

    Parameters
    cache: dict

    Reture:  None
    '''

    jsonCashe = json.dumps(cache)
    fw = open(CACHE_FILENAME, "w")
    fw.write(jsonCashe)
    fw.close()

def loadCache():
    '''
    Open cache file. If the file is empty, create a empty dict

    Parameters
    None

    Return: dict
    '''
    try:
        cacheFile = open(CACHE_FILE_NAME, 'r')
        content = cacheFile.read()
        cache = json.loads(content)
        cacheFile.close()
    except:
        cache = {}
    return cache



def cityAPI(url, cache):
    '''
    1. Check whether url of the city information is in cache. 
    2. If it is in the cache, reutrn it. If not, make a new request

    Parameters
    url: string
    cache: dict

    Return: str

    '''

    if url in (cache.keys()):
        print("Using cache")
    else:
        print("Fetching")
        response = requests.get(url)
        cache[url] = response.text
        saveCache(cache)
    
    return cache[url]

class City(object):
    def __init__(self, rank, name, visitation):
        '''
        Initialize the city

        Parameters
        rank: string
        name: string
        visitation: string
        '''

        self.rank = int(rank)
        self.name = name
        self.visitation = visitation
    

    
    def getPrint(self):
        '''
        get a info of city in string

        return: None
        '''
        return_str = f'{self.rank}. {self.name}, {self.visitation}'
        print(return_str)



def cityList():
    '''
    build a list to store the city object information

    return: str
    '''
    cityList = []
    cityURL = 'https://www.worldatlas.com/cities/america-s-10-most-visited-cities.html'
    responseText = cityAPI(cityURL, CACHE_DICT)
    soup = BeautifulSoup(responseText, 'html.parser')    
    split1 = str(soup.find_all("h2")).split('">')
    split2 = split1[1:11]
    for item in split2:
        split3 = item.split("-")
        split4 = split3[1].split("</h2>")
        rank = split3[0][:2].strip(".")
        city = split3[0][3:].strip("")
        visitation = split4[0].strip()
        '''
        debug
        print(type(split3))
        print(split3)
        print(split4)
        print(rank)
        print(city)
        print(invitation)
        '''
        city = City(rank, city, visitation)
        cityList.append(city)
    return cityList

    
def showCityList(list):
    '''
    Show city informatino from city list
    
    Parameters
    list: list
    
    return: None
    '''
    
    for city in list:
        city.getPrint()





def yelpAPI(baseurl, params):
    '''
    1. Check the restaurants' information of the chosen city is in cache content. 
    2. If it is in the cache, reutrn it. If not, request a new API

    Parameters
    baseurl: string
    params: a dictionary of params

    Return: dict
    '''

    connector = "_"
    paramsList = []
    for item in params:
        paramsList.append(f'{item}_{params[item]}')
    paramsList.sort()
    key = baseurl + connector + connector.join(paramsList)
    if key in CACHE_DICT.keys():
        print("Using Cache")
    else:
        print("Fetching")
        CACHE_DICT[key] = requests.get(baseurl, params, headers=HEADERS).json()
        saveCache(CACHE_DICT)

    return CACHE_DICT[key]



class CityRes(object):
    def __init__(self, name=None, city=None, address=None, categories=None,
                 rating=None, price=None, phone=None):
        '''
        Intialize a place with restaurant

        Parameters
        name: str
        city: str
        address: str
        categories: str
        rating: str
        price: str
        phone: str
        '''
        self.name = name
        self.city = city
        self.address = address
        self.categories = categories
        self.rating = rating
        self.price = price
        self.phone = phone
    
    
    def getPrint(self):
        '''
        Print the informatino of a city restaurant

        Reture: None
        '''
        print(f'{self.name} | Rating: {self.rating} | Price: {self.price} | Address: {self.address}')


def YelpCity(city):
    '''
    Use Yelp API to obtain information of a city

    Parameters
    city: str

    return: dict
    '''
    yelpURL = "https://api.yelp.com/v3/businesses/search"
    yelpDict = yelpAPI(yelpURL, {
        "location": city,
        "term": "food",
        "limit": 50
    })
    return yelpDict





def CityResList(yelpDict, chosenCity, cat):
    '''
    build a list to store the list of the city restaurants
    
    Parameters
    yelpDict: dict
    city: str
    cat: str

    return: list
    '''
    cityResList = []
    for cityR in yelpDict["businesses"]:
        if cityR["categories"][0]["alias"] == cat:
            name = cityR["name"]
            city = chosenCity
            if "rating" not in cityR:
                rating = "No Rating"
            else:
                rating = cityR["rating"]
            if "price" not in cityR:
                price = "No Price"
            else:
                price = cityR["price"]
            phone = cityR["phone"]
            address = cityR["location"]["address1"]
            cityResList.append(CityRes(name, city, address, cat, rating, price, phone))
    return cityResList
             

def showResList(list):
    for item in list:
        item.getPrint()




if __name__ == "__main__":
    
    #get the city information
    CACHE_DICT = loadCache()
    cityList = cityList()
    showCityList(cityList)

    #get the restaurant information for cities
    #city = input("Please choose the city you want to go:")
    cityRestaurant = YelpCity("Miami")
    b = CityResList(cityRestaurant,"Miami", "bars")
    print(type(b))
    showResList(b)