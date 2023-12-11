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
        cacheFile = open(CACHE_FILENAME, 'r')
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
        print("Using cache (City)")
    else:
        print("Fetching (City)")
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
        print("Using Cache (Restaurant)")
    else:
        print("Fetching (Restaurant)")
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
        if cityR["categories"][0]["title"] == cat:
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
    if list:
        for item in list:
            item.getPrint()
    else:
        print("Sorry, no restaurants found.")
    

class TreeNode():
    '''
    define a tree node to store the inofmration of the kind of restaurant
    
    Parameters
    data = str
    parent = None
    children = list

    '''
    def __init__(self, data, parent = None):
        self.data = data
        self.parent = parent
        self.children = []
    
    def addChild(self, child):
        child.parent = self
        self.children.append(child)
    
    def getData(self):
        return self.data
    
    def getParent(self):
        return self.parent
    
    def getChildren(self):
        return self.children

    def getLevel(self):
        level = 0
        p = self.parent
        while p:
            level = level + 1
            p = p.parent
        return level

    def printTree(self):
        space = "   " * self.getLevel()
        print(space + self.data)
        if self.children:
            for child in self.children:
                child.printTree()

    def toDict(self):
        result = {
            "data" : self.data,
            "children" : [child.toDict() for child in self.children]
        }
        return result



def buildTree():
    '''
    Build a tree to store the inofmration of the kind of restaurant.
    
    Parameters
    root = treeNode class
    
    return treeNode class

    '''
    
    root = TreeNode("Restaurant Categories")
    

    asian = TreeNode("Asian food")
    asian.addChild(TreeNode("Chinese"))
    asian.addChild(TreeNode("Korean"))
    asian.addChild(TreeNode("Cambodian"))
    asian.addChild(TreeNode("Asian Fusion"))
    asian.addChild(TreeNode("Indian"))
    asian.addChild(TreeNode("Thai"))
    asian.addChild(TreeNode("Japanese"))

    euro = TreeNode("European food")
    euro.addChild(TreeNode("Greek"))
    euro.addChild(TreeNode("Itatilan"))
    euro.addChild(TreeNode("Portuguese"))

    american = TreeNode("American food")
    american.addChild(TreeNode("New American"))
    american.addChild(TreeNode("Sandwiches"))
    american.addChild(TreeNode("Southern"))

    african = TreeNode("African food")

    arabian = TreeNode("Arabian food")

    other = TreeNode("Other food")
    other.addChild(TreeNode("Pubs"))
    other.addChild(TreeNode("Bars"))
    other.addChild(TreeNode("Comfort Food"))
    
    root.addChild(asian)
    root.addChild(euro)
    root.addChild(american)
    root.addChild(african)
    root.addChild(arabian)
    root.addChild(other)
    
    
    return root


def loadTree(cache):
    '''
    Check whether tree is in the cache. If so, load the tree. If not build a tree.

    Parameters
    tree: str
    cache: dict

    return: str
    '''
    tree = "tree"
    if tree in (cache.keys()):
        print("Using cache (Tree)")
        #return cache(tree)
    else:
        print("Build the tree")
        treeRes = buildTree().toDict()
        cache[tree] = treeRes
        print(cache)
        with open(CACHE_FILENAME, 'w') as json_file:
            json.dump(cache, json_file, default=lambda o: o.toDict(), indent=4)
       
    return cache[tree]

def dictToTree(treeDict):
    '''
    convert tree dictionary to treeNode
    
    Parameters
    treeDict: dict
    root: TreeNode
    
    return TreeNode
    '''
    root = TreeNode(treeDict["data"])
    for child in treeDict.get("children", []):
        childNode = dictToTree(child)
        childNode.parent = root
        root.addChild(childNode)
        
    return root



def chooseCity(num):
    '''
    After the user choose a city number, return the city name
    
    Parameters
    num = int
    
    return str
    
    '''
    if num == 1:
        return "New York City"
    if num == 2:
        return "Miami"
    if num == 3:
        return "Orlando"
    if num == 4:
        return "Los Angeles"
    if num == 5:
        return "San Francisco"
    if num == 6:
        return "Las Vegas"
    if num == 7:
        return "Washington D.C."
    if num == 8:
        return "Chicago"
    if num == 9:
        return "Boston"
    if num == 10:
        return "Honolulu"



if __name__ == "__main__":
    
    print("Welcome to the city restaurants program!")
    print("The cities shown below are the most visited citties in US.")
    print("------------------------------------------------------------")
    inner = True
    inner2 = True
    outter = True
    #get the city information
    CACHE_DICT = loadCache()
    cityList = cityList()
    tree = loadTree(CACHE_DICT)
    root = dictToTree(tree)
    
    while outter is True:
        inner = True
        showCityList(cityList)
        try:
            print("------------------------------------------------------------")
            cityNum = float(input("Please choose a city you would like to go: (Please input the integer between 1 and 10.)"))
            if cityNum.is_integer() and cityNum > 0 and cityNum < 11:         
                #list the categories and ask user to choose
                city = chooseCity(cityNum)
                print("Please choose a category!")
                print("***********************************")
                root.printTree()
                print("***********************************")
                cate = input("Please choose a category you are interested: (e.g. Chinese)")
                print(f"restaurant of {cate} category in {city}")
                print("------------------------------------------------------------")
                #get the restaurant information for the choosen city
                cityResL = CityResList(YelpCity(city),city, cate)
                showResList(cityResL)
                print("------------------------------------------------------------")
                choose = input("Please make your choose: 1. Choose another city. 2. Choose another category. 3. The category is not listed. 4. Exit")
                if choose == "1":
                    continue
                elif choose == "2":
                    inner = True
                    while inner == True:
                        cateAgain = input("Please choose a category you are interested: (e.g. Chinese)")
                        print(f"restaurant of {cateAgain} category in {city}")
                        print("------------------------------------------------------------")
                        #get the restaurant information for the choosen city
                        cityResL = CityResList(YelpCity(city),city, cateAgain)
                        showResList(cityResL)
                        print("------------------------------------------------------------")
                        play = input("Please make your choose: 1. Choose another city. 2. Choose another category. 3. Exit")
                        if play == "1":
                            inner = False
                        elif play == "2":
                            pass
                        elif play == "3":
                            inner = False
                            outter = False
                        else:
                            print("Wrong input. Back to beginning")
                            break
                    #continue
                elif choose == "3":
                    inner2 = True
                    while inner2 == True:
                        otherCate = input("Please input a category you are interested: (e.g. Chinese)")
                        print(f"restaurant of {otherCate} category in {city}")
                        print("------------------------------------------------------------")
                        #get the restaurant information for the choosen city
                        cityResL = CityResList(YelpCity(city),city, otherCate)
                        showResList(cityResL)
                        print("------------------------------------------------------------")
                        play = input("Please make your choose: 1. Choose another city. 2. Choose another category. 3. Exit")
                        if play == "1":
                            inner2 = False
                        elif play == "2":
                            pass
                        elif play == "3":
                            inner2 = False
                            outter = False
                        else:
                            print("Wrong input!")
                            pass
                elif choose == "4":
                    break
                else:
                    print("Wrong input. Back to beginning")
                    continue
            else:
                print("*****Wrong input! Please enter a integer between 1 - 10!*****")
                continue
        except: 
            print("*****Wrong input! Please enter agian!*****")
            pass
    

    