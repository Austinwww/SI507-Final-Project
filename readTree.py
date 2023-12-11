#################################
##### Name: Yuchen Wu    ########
##### Uniqname: yuchenwu ########
#################################

#This file is used to read the Tree in the json file
import requests
import json
import re

CACHE_FILENAME = 'cache.json'
CACHE_DICT = {}

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

def dictToTree(treeDict):
    root = TreeNode(treeDict["data"])
    for child in treeDict.get("children", []):
        childNode = dictToTree(child)
        childNode.parent = root
        root.addChild(childNode)
        
    return root

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
        return cache[tree]
    else:
        print("Fail to load")
    

if __name__ == "__main__":
    
    CACHE_DICT = loadCache()
    tree = loadTree(CACHE_DICT)
    root = dictToTree(tree)
    root.printTree()