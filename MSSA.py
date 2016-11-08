from __future__ import division
__author__ = 'Kuan Jia Qing'
#done by: Kuan Jia Qing
#UOG ID: 2228126k

import csv  #import the csv module
import math #import the math module
import os #imports the os module
import numpy as np
from collections import Counter #imports to process dictionary for top 5 tags in a word
from collections import defaultdict #special dict that returns default values whenever a key is selected from the dict
from collections import defaultdict


# open csv file
tags = open('tags.csv', "rt")
photos_tag = open('photos_tags.csv', "rt")
photos = open('photos.csv', "rt")

# file location to write to csv file
currentPath = os.getcwd()
csv_file = currentPath + "/Matrix.csv"

# declaration
coor_map = {}

data = defaultdict(list)
tags_dict = defaultdict(int)
temp_list = [] #tempoary list
w, h = 101, 101 #width and height of matrix
Matrix = [[0 for x in range(w)] for y in range(h)] #co-occurrence matrix
tag_list =[] #to store list of tags
totalCountOfPhotos = None
photo_list = []

def readCSV():
    #Reads from CSV file and add to a list
    with photos_tag as f: #reads photo tags from photo tags table
        reader = csv.reader(f)
        for val in reader:

           temp_list.append(val)

    for k, v in temp_list:
        data[k].append(v)

    with tags as f: #gets the list of tags from tag table
        reader = csv.reader(f)
        for val in reader:
            tag_list.append(val[0])

    tags2 = open('tags.csv', "rt")

    with tags2 as f: #reads photo tags from photo tags table
        reader = csv.reader(f)
        for val in reader:

           temp_list.append(val)

    for k, v in temp_list:
        tags_dict[k] = v

    with photos as f: #gets the list of tags from tag table
        reader = csv.reader(f)

        for val in reader:
            photo_list.append(val[0])


def fillMatrixHeaders():

    for num in range(1, (len(tag_list) + 1)):
        Matrix[num][0] = tag_list[(num - 1)]
    for num in range(1, (len(tag_list) + 1)):
        Matrix[0][num] = tag_list[(num - 1)]


def modifyMatrix(tag1, tag2):


    #print('Modifying coordinate X:',  tag_list.index(tag1) + 1, ' Y:', tag_list.index(tag2) + 1)
    tempnum = Matrix[tag_list.index(tag1) + 1][tag_list.index(tag2) + 1]
   #print('Current Occurences: ', tempnum)
    tempnum += 1
    #print('New Occurences: ', tempnum)
    Matrix[tag_list.index(tag1) + 1][tag_list.index(tag2) + 1] = tempnum
    Matrix[tag_list.index(tag2) + 1][tag_list.index(tag1) + 1] = tempnum



def buildCoor():
    for key in data:
        #print data[key]
        for num in range(0, len(data[key])):
            for num2 in range (num+1, len(data[key])):
                #print(data[key][num] + " and " + data[key][num2] + " found together")
                modifyMatrix(data[key][num], data[key][num2])



def gen_matrix_csv():#generates the format for a blank matrix
    a = np.array(Matrix)
    np.savetxt("coor.csv", a, delimiter=",", fmt="%s")

def getPopularTag(tag):
    indexnumber = tag_list.index(tag)

    popwordlist = defaultdict(int)
    for num in range(0, (len(tag_list))):
        #print(Matrix[(num)][indexnumber + 1])
        popwordlist[tag_list[num]] = (Matrix[(num+1)][indexnumber + 1])


    c = Counter(popwordlist)
    print "[Occurrences] Top 5 tags for %s according to occurrences are %s" % (tag, c.most_common(5))

    return popwordlist


    #print(heapq.nlargest(5, poptemplist))

def getPopularIDFTag(tag):
    tfidfdict = defaultdict(float)

    popwordlist = getPopularTag(tag)
    popwordsval0 = popwordlist.keys()

    for word in popwordsval0:
        IDF = math.log((float(len(photo_list)) / float(tags_dict[word])))
        TFIDF = (popwordlist[word] * IDF)
        tfidfdict[word] = TFIDF

    c = Counter(tfidfdict)
    print "[TF-IDF]      Top 5 tags for %s are %s" % (tag, c.most_common(5))





readCSV()
fillMatrixHeaders()
buildCoor()
gen_matrix_csv()
#getPopularTag("water")
#getPopularTag("people")
#getPopularTag("london")

getPopularIDFTag("water")
getPopularIDFTag("people")
getPopularIDFTag("london")